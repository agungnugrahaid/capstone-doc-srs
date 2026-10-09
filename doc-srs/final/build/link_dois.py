"""Make every DOI / URL in Daftar Pustaka a clickable hyperlink (run AFTER Word refreshed the BIBLIOGRAPHY field).

Word's APA style prints DOIs as plain 'doi:10.xxx'. This rewrites them as 'https://doi.org/10.xxx' and wraps them in a
w:hyperlink so the PDF export has real links. Usage: python link_dois.py <docx>
"""
import copy, re, sys
import docx
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

path = sys.argv[1]
doc = docx.Document(path)
body = doc.element.body
paras = list(body.iter(qn("w:p")))
start = None
for i, p in enumerate(paras):
    if "".join(t.text or "" for t in p.iter(qn("w:t"))).strip().upper() == "DAFTAR PUSTAKA":
        start = i  # last occurrence wins (the first is the table of contents entry)
n = 0
URL = re.compile(r"(?:doi:\s*|https?://doi\.org/|(?<![\w/])https?://)(\S+)")
for p in paras[start + 1:]:
    for r in list(p.iter(qn("w:r"))):
        ts = r.findall(qn("w:t"))
        if len(ts) != 1 or r.getparent().tag == qn("w:hyperlink"):
            continue
        txt = ts[0].text or ""
        m = URL.search(txt)
        if not m:
            continue
        raw = m.group(0)
        tail = m.group(1).rstrip(".,;")
        url = raw.strip() if raw.startswith("http") and "doi.org" not in raw and "doi:" not in raw else "https://doi.org/" + tail
        if raw.startswith("http") and "doi:" not in raw and "doi.org" not in raw:
            url = "https://" + raw.split("://", 1)[1].rstrip(".,;")
        shown = url
        before, after = txt[:m.start()], txt[m.start() + len(raw.rstrip(".,;")):]
        rid = doc.part.relate_to(url, RT.HYPERLINK, is_external=True)
        def clone(text):
            c = copy.deepcopy(r)
            for t in c.findall(qn("w:t")):
                t.text = text; t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            return c
        link = OxmlElement("w:hyperlink"); link.set(qn("r:id"), rid)
        lr = clone(shown)
        link.append(lr)
        idx = r.getparent().index(r)
        parent = r.getparent()
        parent.remove(r)
        pieces = []
        if before: pieces.append(clone(before))
        pieces.append(link)
        if after: pieces.append(clone(after))
        for k, el in enumerate(pieces):
            parent.insert(idx + k, el)
        n += 1
doc.save(path)
print("hyperlinks added:", n)
