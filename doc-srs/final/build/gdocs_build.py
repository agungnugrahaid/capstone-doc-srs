"""Turn the markdown draft into Google Docs batchUpdate requests for one (empty) tab.

Usage: python gdocs_build.py <tabId> <outdir>
Writes outdir/batch_NN.json (requests only) and outdir/plan.json (expected end index after each batch).
Content is appended at the end of the tab; indexes are tracked locally (UTF-16 units).
Images can't be uploaded through the Docs API without a public URL, so each figure gets a
placeholder line naming the PNG to insert, followed by its caption.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DRAFT = os.path.join(ROOT, "draft", "Laporan-Capstone-SAPA-draft.md")
MOCKSPEC = os.path.join(ROOT, "draft", "mockup-spec-untuk-figma.md")
TAB = sys.argv[1]
OUTDIR = sys.argv[2]
os.makedirs(OUTDIR, exist_ok=True)

FONT = {"weightedFontFamily": {"fontFamily": "Times New Roman"}}
USABLE_PT = 481.0


def u16(s):
    return len(s.encode("utf-16-le")) // 2


# ------------------------------------------------------------------ blocks
blocks = []  # (kind, payload)


def H(level, text, pagebreak=False):
    blocks.append(("h", (level, text, pagebreak)))


def P(text, style="body"):
    blocks.append(("p", (text, style)))


def L(items, numbered):
    blocks.append(("list", (items, numbered)))


def CAP(kind, text):
    SEQ[kind] += 1
    label = f"{kind} 3.{SEQ[kind]} {text}"
    CAPS[kind].append(label)
    blocks.append(("p", (label, "caption")))


def T(rows, widths=None):
    blocks.append(("table", (rows, widths)))


def UC(elem, flow):
    blocks.append(("uc", (elem, flow)))


def IMG(fname, desc):
    blocks.append(("p", (f"[Sisipkan gambar: {fname}]", "imgph")))
    CAP("Gambar", desc)


SEQ = {"Tabel": 0, "Gambar": 0}
CAPS = {"Tabel": [], "Gambar": []}

UC_NAMES = ["Login", "Mengirim Pesan WhatsApp", "Menjawab Pesan Otomatis dengan AI", "Mengelola Percakapan",
            "Mengelola Prospek", "Mengelola Kontak Pelanggan", "Melihat Dasbor Pemantauan",
            "Mengelola Nomor WhatsApp", "Mengelola Basis Pengetahuan", "Mengatur AI dan Anti-ban",
            "Mengelola Tim dan Hak Akses", "Melihat Log Audit"]
MOCKS = [("MK-01", "Login"), ("MK-02", "Dasbor Pemantauan"), ("MK-03", "Kotak Masuk"), ("MK-04", "Prospek"),
         ("MK-05", "Kontak"), ("MK-06", "Nomor WhatsApp"), ("MK-07", "Basis Pengetahuan"),
         ("MK-08", "Pengaturan AI dan Konsol Uji"), ("MK-09", "Antrean Keluar dan Pusat Risiko"),
         ("MK-10", "Tim dan Akses"), ("MK-11", "Log Audit")]
MOCKFILES = ["MK-01-login.png", "MK-02-dasbor.png", "MK-03-kotak-masuk.png", "MK-04-prospek.png",
             "MK-05-kontak.png", "MK-06-nomor-whatsapp.png", "MK-07-basis-pengetahuan.png",
             "MK-08-pengaturan-ai.png", "MK-09-antrean-risiko.png", "MK-10-tim-akses.png", "MK-11-log-audit.png"]
mock_desc = dict(re.findall(r"- \*\*(MK-\d+)\*\*: (.+)", open(MOCKSPEC, encoding="utf-8").read()))


def gen_341():
    P("Use case diagram SAPA menggambarkan interaksi empat aktor utama (Pelanggan, Agen/CS, Supervisor, dan "
      "Administrator) serta dua aktor sekunder (WhatsApp Web dan Penyedia AI) dengan dua belas use case. Setiap use "
      "case yang memerlukan autentikasi memiliki relasi <<Include>> ke use case Login, sedangkan Mengirim Pesan "
      "WhatsApp tidak memerlukan login karena dilakukan pelanggan melalui aplikasi WhatsApp dan meng-include "
      "Menjawab Pesan Otomatis dengan AI yang dijalankan sistem.")
    IMG("diagram/png/Use Case Diagram SAPA.png", "Use Case Diagram SAPA")


def gen_343():
    P("Sequence diagram disusun untuk setiap use case pada use case diagram. Setiap diagram memuat aktor, objek "
      "antarmuka (View/boundary), pengendali (Cont/control), dan entitas (Ent/entity) beserta urutan pesan bernomor "
      "sesuai Basic Flow of Event pada use case description.")
    for i, n in enumerate(UC_NAMES, 1):
        IMG(f"diagram/png/SD-{i:02d} - {n}.png", f"Sequence Diagram SD-{i:02d} {n}")


def gen_344():
    P("Class diagram disusun dengan tata letak Model-View-Controller (MVC). Kolom kiri berisi kelas antarmuka (UI) "
      "beserta atribut dan operasi get/set, kolom tengah berisi kelas pengendali (Cont) yang memuat logika proses "
      "setiap use case, dan kolom kanan berisi kelas entitas (Ent) yang merepresentasikan data tersimpan.")
    IMG("diagram/png/Class Diagram SAPA (MVC).png", "Class Diagram SAPA dengan Layout MVC")


def gen_345():
    P("Activity diagram diturunkan dari setiap use case description. Swimlane kiri memuat aktivitas aktor dan "
      "swimlane kanan memuat aktivitas sistem; percabangan (decision) menggambarkan Alternative Flow dan Error "
      "Condition.")
    for i, n in enumerate(UC_NAMES, 1):
        IMG(f"diagram/png/AD-{i:02d} - {n}.png", f"Activity Diagram AD-{i:02d} {n}")


def gen_35():
    P("Mockup aplikasi dibuat dalam bentuk high-fidelity menggunakan Figma untuk setiap halaman yang akan dibangun. "
      "Setiap halaman dipetakan ke use case yang dilayaninya.")
    for (code, title), fname in zip(MOCKS, MOCKFILES):
        P(f"**{code}, Halaman {title}.** {mock_desc.get(code, '')}")
        IMG(f"final/mockup/{fname} (ekspor Figma)", f"Mockup Halaman {title}")


GENERATED = {"3.4.1": gen_341, "3.4.3": gen_343, "3.4.4": gen_344, "3.4.5": gen_345, "3.5": gen_35}

# ------------------------------------------------------------------ cover + front matter
cover = [("LAPORAN CAPSTONE PROJECT", "covertitle"),
         ("SAPA: Sistem Asisten Pelanggan dan Akuisisi", "covertitle"),
         ("Chatbot WhatsApp Omnichannel Berbasis Kecerdasan Artifisial dan CRM pada Bimbingan Belajar Asentra", "center"),
         ("Disusun untuk memenuhi Tugas Mata Kuliah Capstone Project (SIF26062P)", "center"),
         ("Dosen Pengampu: Albert Yakobus Chandra, S.Kom., M.Eng.", "center"),
         ("Disusun Oleh Kelompok 1:", "center")]
for t, s in cover:
    P(t, s)
T([["Nama", "NIM"], ["Rifqi Adhi Saputra", "231210019"], ["Isnaini Anggista Damayanti", "241220006"],
   ["Yordan Gabriell", "241220049"], ["Agung Nugraha Eka Saputra", "241220055"],
   ["Enrico Yuda Dwinata", "241220073"]], [300, 150])
for t in ["PROGRAM STUDI SISTEM INFORMASI", "FAKULTAS TEKNOLOGI INFORMASI",
          "UNIVERSITAS MERCU BUANA YOGYAKARTA", "TAHUN 2026"]:
    P(t, "coverbold")
H(1, "DAFTAR ISI", pagebreak=True)
P("[ISI: sisipkan daftar isi otomatis lewat menu Sisipkan > Daftar isi]", "imgph")
FRONT_TABEL = len(blocks)
H(1, "DAFTAR TABEL", pagebreak=True)
FRONT_GAMBAR_PLACE = None

# ------------------------------------------------------------------ parse draft
md = open(DRAFT, encoding="utf-8").read()
lines = md[md.index("## BAB I PENDAHULUAN"):].split("\n")
i, skip, in_bib = 0, False, False
pending_cap, pending_elem = None, None
body_blocks_start = None


def parse_table(start):
    rows, j = [], start
    while j < len(lines) and lines[j].startswith("|"):
        rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
        j += 1
    return [r for r in rows if not all(re.fullmatch(r":?-{3,}:?", c) for c in r)], j


def widths_for(rows):
    n = len(rows[0])
    need = []
    for j in range(n):
        col = [r[j] if j < len(r) else "" for r in rows]
        longest = max(len(c) for c in col)
        avg = sum(len(c) for c in col[1:]) / max(1, len(col) - 1)
        need.append(max(1.1, longest * 0.22) if longest <= 6 else 2.2 + avg * 0.06)
    tot = sum(need)
    return [round(USABLE_PT * x / tot, 1) for x in need]


list_buf, list_num = [], None


def flush_list():
    global list_buf, list_num
    if list_buf:
        L(list_buf, list_num)
    list_buf, list_num = [], None


bib = []
while i < len(lines):
    s = lines[i].strip()
    if s.startswith("#"):
        flush_list()
        level = len(s) - len(s.lstrip("#"))
        title = s.lstrip("#").strip()
        skip = False
        if title.startswith("DAFTAR PUSTAKA"):
            H(1, "DAFTAR PUSTAKA", pagebreak=True)
            in_bib = True
            i += 1
            continue
        if body_blocks_start is None:
            body_blocks_start = len(blocks)
        if level == 2:
            H(1, title, pagebreak=True)
        else:
            H(2 if level == 3 else 3, title)
        num = title.split()[0]
        if num in GENERATED:
            GENERATED[num]()
            skip = True
        if num == "3.4.2":
            P("Use case description disusun berdasarkan use case diagram pada Gambar 3.1. Setiap tabel memuat nama, "
              "nomor, aktor, deskripsi singkat, kondisi awal, alur utama (aktor dan sistem), kondisi akhir, alur "
              "alternatif, dan kondisi galat.")
        i += 1
        continue
    if skip:
        i += 1
        continue
    if in_bib:
        if s and not s.startswith("*("):
            bib.append(re.sub(r"\s*\*\(bawaan template\)\*", "", s))
        i += 1
        continue
    if not s or s == "---" or s.startswith(">") or s.startswith("*(") or s.startswith("![") \
            or s.startswith("Format setiap tabel mengikuti contoh ANSI"):
        if not s:
            flush_list()
        i += 1
        continue
    m = re.fullmatch(r"\*\*Tabel 3\.\S* (.+)\*\*", s)
    if m:
        pending_cap = m.group(1)
        i += 1
        continue
    m = re.fullmatch(r"\*\*(UC-\d+): (.+)\*\*", s)
    if m:
        pending_cap = f"Use Case Description {m.group(1)} {m.group(2)}"
        i += 1
        continue
    if s.startswith("|"):
        flush_list()
        rows, i = parse_table(i)
        if rows[0][:2] == ["Elemen", "Isi"]:
            pending_elem = {r[0]: r[1] for r in rows[1:]}
            continue
        if rows[0] == ["Aktor", "Sistem"] and pending_elem is not None:
            CAP("Tabel", pending_cap or pending_elem.get("Nama Use Case", ""))
            UC(pending_elem, rows[1:])
            pending_elem = pending_cap = None
            continue
        if pending_cap:
            CAP("Tabel", pending_cap)
            pending_cap = None
        T(rows, widths_for(rows))
        continue
    m = re.match(r"(\d+)\. (.+)", s)
    if m:
        if list_num is False:
            flush_list()
        list_num = True
        list_buf.append(m.group(2))
        i += 1
        continue
    if s.startswith("- "):
        if list_num is True:
            flush_list()
        list_num = False
        list_buf.append(s[2:])
        i += 1
        continue
    flush_list()
    text = s.replace(" *(kalimat & sitasi bawaan template)*", "")
    if "Gambar 3.x berikut ini" in text:
        P(text.replace("Gambar 3.x", f"Gambar 3.{SEQ['Gambar'] + 1}"))
        IMG("Siklus Hidup XP (gambar template, Ambler 2002)",
            "Siklus Hidup Metode Pengembangan eXtreme Programming (Ambler, 2002)")
    elif s.startswith("*") and s.endswith("*") and not s.startswith("**"):
        P(s.strip("*"), "note")
    else:
        P(text)
    i += 1
flush_list()
for b in bib:
    P(b, "bib")

# static lists of tables and figures (Google Docs has no automatic list of figures)
front = [("p", (c, "toclist")) for c in CAPS["Tabel"]]
front += [("h", (1, "DAFTAR GAMBAR", True))]
front += [("p", (c, "toclist")) for c in CAPS["Gambar"]]
blocks[FRONT_TABEL + 1:FRONT_TABEL + 1] = front

# ------------------------------------------------------------------ requests
E = 1  # index of the trailing empty paragraph's newline
batches, cur = [], []
plan = []


def loc(i):
    return {"index": i, "tabId": TAB}


def rng(a, b):
    return {"startIndex": a, "endIndex": b, "tabId": TAB}


def strip_marks(text):
    """Remove **bold** / *italic* markers; return clean text and (start,end,kind) spans."""
    out, spans, pos = "", [], 0
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*)", text):
        if not tok:
            continue
        kind = None
        if tok.startswith("**") and tok.endswith("**"):
            tok, kind = tok[2:-2], "bold"
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            tok, kind = tok[1:-1], "italic"
        if kind:
            spans.append((u16(out), u16(out) + u16(tok), kind))
        out += tok
    return out, spans


PSTYLE = {
    "body": ({"namedStyleType": "NORMAL_TEXT", "alignment": "JUSTIFIED", "lineSpacing": 150,
              "indentFirstLine": {"magnitude": 36, "unit": "PT"}, "spaceBelow": {"magnitude": 6, "unit": "PT"}},
             {"fontSize": {"magnitude": 12, "unit": "PT"}}),
    "note": ({"namedStyleType": "NORMAL_TEXT", "alignment": "JUSTIFIED", "lineSpacing": 150},
             {"fontSize": {"magnitude": 12, "unit": "PT"}, "italic": True}),
    "list": ({"namedStyleType": "NORMAL_TEXT", "alignment": "JUSTIFIED", "lineSpacing": 150},
             {"fontSize": {"magnitude": 12, "unit": "PT"}}),
    "caption": ({"namedStyleType": "NORMAL_TEXT", "alignment": "CENTER", "lineSpacing": 100,
                 "spaceAbove": {"magnitude": 6, "unit": "PT"}, "spaceBelow": {"magnitude": 10, "unit": "PT"},
                 "keepWithNext": True},
                {"fontSize": {"magnitude": 11, "unit": "PT"}, "bold": True}),
    "imgph": ({"namedStyleType": "NORMAL_TEXT", "alignment": "CENTER", "lineSpacing": 100, "keepWithNext": True},
              {"fontSize": {"magnitude": 11, "unit": "PT"}, "italic": True,
               "backgroundColor": {"color": {"rgbColor": {"red": 1, "green": 1, "blue": 0}}}}),
    "bib": ({"namedStyleType": "NORMAL_TEXT", "alignment": "JUSTIFIED", "lineSpacing": 115,
             "indentStart": {"magnitude": 36, "unit": "PT"}, "indentFirstLine": {"magnitude": 0, "unit": "PT"},
             "spaceBelow": {"magnitude": 6, "unit": "PT"}},
            {"fontSize": {"magnitude": 12, "unit": "PT"}}),
    "toclist": ({"namedStyleType": "NORMAL_TEXT", "alignment": "START", "lineSpacing": 115},
                {"fontSize": {"magnitude": 11, "unit": "PT"}}),
    "center": ({"namedStyleType": "NORMAL_TEXT", "alignment": "CENTER", "lineSpacing": 115},
               {"fontSize": {"magnitude": 12, "unit": "PT"}}),
    "covertitle": ({"namedStyleType": "NORMAL_TEXT", "alignment": "CENTER", "lineSpacing": 115,
                    "spaceAbove": {"magnitude": 12, "unit": "PT"}},
                   {"fontSize": {"magnitude": 16, "unit": "PT"}, "bold": True}),
    "coverbold": ({"namedStyleType": "NORMAL_TEXT", "alignment": "CENTER", "lineSpacing": 115},
                  {"fontSize": {"magnitude": 13, "unit": "PT"}, "bold": True}),
}
HSTYLE = {1: ({"namedStyleType": "HEADING_1", "alignment": "CENTER", "keepWithNext": True,
               "spaceAbove": {"magnitude": 0, "unit": "PT"}, "spaceBelow": {"magnitude": 12, "unit": "PT"}},
              {"fontSize": {"magnitude": 14, "unit": "PT"}, "bold": True}),
          2: ({"namedStyleType": "HEADING_2", "alignment": "START", "keepWithNext": True,
               "spaceAbove": {"magnitude": 12, "unit": "PT"}, "spaceBelow": {"magnitude": 6, "unit": "PT"}},
              {"fontSize": {"magnitude": 13, "unit": "PT"}, "bold": True}),
          3: ({"namedStyleType": "HEADING_3", "alignment": "START", "keepWithNext": True,
               "spaceAbove": {"magnitude": 10, "unit": "PT"}, "spaceBelow": {"magnitude": 6, "unit": "PT"}},
              {"fontSize": {"magnitude": 12, "unit": "PT"}, "bold": True})}


pending = []  # paragraphs waiting to be inserted: (text, style, extra_pstyle, bullet_group)


def flush():
    """Insert all pending paragraphs in one insertText, then style them in grouped ranges."""
    global E, pending
    if not pending:
        return []
    s0 = E
    texts, meta = [], []
    pos = s0
    for text, style, extra, bgroup in pending:
        clean, spans = strip_marks(text)
        n = u16(clean)
        meta.append((pos, pos + n + 1, style, extra, spans, bgroup))
        texts.append(clean)
        pos += n + 1
    reqs = [{"insertText": {"location": loc(s0), "text": "\n".join(texts) + "\n"}}]
    # paragraph styles: merge consecutive paragraphs with identical style
    groups = []
    for a, b, style, extra, spans, bg in meta:
        key = (style, json.dumps(extra, sort_keys=True))
        if groups and groups[-1][0] == key and groups[-1][2] == a:
            groups[-1][2] = b
        else:
            groups.append([key, a, b, style, extra])
    for key, a, b, style, extra in groups:
        ps, ts = (HSTYLE[int(style[1])] if style.startswith("h") else PSTYLE[style])
        ps = dict(ps)
        if extra:
            ps.update(extra)
        reqs.append({"updateParagraphStyle": {"range": rng(a, b), "paragraphStyle": ps, "fields": ",".join(ps)}})
        if ts and b - 1 > a:
            reqs.append({"updateTextStyle": {"range": rng(a, b - 1), "textStyle": ts, "fields": ",".join(ts)}})
    for a, b, style, extra, spans, bg in meta:
        for x, y, kind in spans:
            reqs.append({"updateTextStyle": {"range": rng(a + x, a + y), "textStyle": {kind: True}, "fields": kind}})
    # bullets
    bl = {}
    for a, b, style, extra, spans, bg in meta:
        if bg is not None:
            bl.setdefault(bg[0], [a, b, bg[1]])[1] = b
    for gid, (a, b, numbered) in bl.items():
        reqs.append({"createParagraphBullets": {"range": rng(a, b - 1), "bulletPreset":
                     "NUMBERED_DECIMAL_ALPHA_ROMAN" if numbered else "BULLET_DISC_CIRCLE_SQUARE"}})
    E = pos
    pending = []
    return reqs


def table_requests(rows, widths, label_cells=None):
    """Insert a table after the paragraph that ends at E (index E-1 is its newline)."""
    global E
    R, C = len(rows), max(len(r) for r in rows)
    i = E - 1
    reqs = [{"insertTable": {"rows": R, "columns": C, "location": loc(i)}}]
    pos = lambda r, c: i + 4 + r * (2 * C + 1) + 2 * c
    cells = [(r, c, (rows[r][c] if c < len(rows[r]) else "").replace("**", "")) for r in range(R) for c in range(C)]
    for r, c, t in reversed(cells):
        if t:
            reqs.append({"insertText": {"location": loc(pos(r, c)), "text": t}})
    shift, final = 0, {}
    for r, c, t in cells:
        final[(r, c)] = (pos(r, c) + shift, pos(r, c) + shift + u16(t))
        shift += u16(t)
    tstart, tend = i + 1, i + 3 + R * (2 * C + 1) + shift - 1
    reqs.append({"updateParagraphStyle": {"range": rng(tstart, tend), "paragraphStyle": {
        "namedStyleType": "NORMAL_TEXT", "alignment": "START", "lineSpacing": 100,
        "indentFirstLine": {"magnitude": 0, "unit": "PT"}, "spaceBelow": {"magnitude": 0, "unit": "PT"},
        "keepWithNext": False}, "fields": "namedStyleType,alignment,lineSpacing,indentFirstLine,spaceBelow,keepWithNext"}})
    reqs.append({"updateTextStyle": {"range": rng(tstart, tend), "textStyle": {"fontSize": {"magnitude": 10, "unit": "PT"}},
                                     "fields": "fontSize,bold,italic"}})
    tloc = {"index": tstart, "tabId": TAB}
    gray = {"backgroundColor": {"color": {"rgbColor": {"red": 0.85, "green": 0.85, "blue": 0.85}}}}

    def shade(r, c, rs, cs):
        reqs.append({"updateTableCellStyle": {"tableRange": {"tableCellLocation": {
            "tableStartLocation": tloc, "rowIndex": r, "columnIndex": c}, "rowSpan": rs, "columnSpan": cs},
            "tableCellStyle": gray, "fields": "backgroundColor"}})

    def bold(a, b):
        if b > a:
            reqs.append({"updateTextStyle": {"range": rng(a, b), "textStyle": {"bold": True}, "fields": "bold"}})
    if label_cells is None:
        shade(0, 0, 1, C)
        bold(final[(0, 0)][0], final[(0, C - 1)][1])
    else:
        shade(0, 0, R, 1)
        for (r, c) in label_cells:
            bold(*final[(r, c)])
            if c:
                shade(r, c, 1, 1)
    if widths:
        for c, w in enumerate(widths):
            reqs.append({"updateTableColumnProperties": {"tableStartLocation": tloc, "columnIndices": [c],
                         "tableColumnProperties": {"widthType": "FIXED_WIDTH", "width": {"magnitude": w, "unit": "PT"}},
                         "fields": "widthType,width"}})
    E = i + 4 + R * (2 * C + 1) + shift
    return reqs, tstart


uc_tables = []  # (block index) merges done in a later pass after a fresh read

bgid = 0
for kind, payload in blocks:
    reqs = []
    if kind == "h":
        level, text, pb = payload
        pending.append((text, f"h{level}", {"pageBreakBefore": True} if pb else None, None))
    elif kind == "p":
        text, style = payload
        pending.append((text, style, None, None))
    elif kind == "list":
        items, numbered = payload
        bgid += 1
        for it in items:
            pending.append((it, "list", None, (bgid, numbered)))
    elif kind in ("table", "uc"):
        reqs = flush()
        if kind == "table":
            rows, widths = payload
            r2, _ = table_requests(rows, widths)
        else:
            elem, flow = payload
            rows = [[k, elem.get(k, "-"), ""] for k in ["Nama Use Case", "Nomor Use Case", "Aktor",
                                                        "Deskripsi Singkat", "Pre Condition"]]
            first = len(rows)
            rows.append(["Basic Flow of Event", "Aktor", "Sistem"])
            rows += [["", a, s_] for a, s_ in flow]
            last = len(rows) - 1
            rows += [[k, elem.get(k, "-"), ""] for k in ["Post Condition", "Alternative Flow", "Error Condition"]]
            labels = [(r, 0) for r in range(len(rows)) if rows[r][0]] + [(first, 1), (first, 2)]
            r2, tstart = table_requests(rows, [110, 185, 186], labels)
            uc_tables.append({"merge_rows": [r for r in range(len(rows)) if r < first or r > last],
                              "flow": [first, last]})
        reqs += r2
    if kind in ("h", "p", "list") and len(pending) >= 35:
        reqs = flush()
    cur += reqs
    if len(json.dumps(cur, ensure_ascii=False)) > 45000:
        batches.append(cur)
        plan.append(E)
        cur = []
cur += flush()
cur.append({"updateTextStyle": {"range": rng(1, E), "textStyle": {"weightedFontFamily": {"fontFamily": "Times New Roman"}},
                                "fields": "weightedFontFamily"}})
if cur:
    batches.append(cur)
    plan.append(E)

for n, b in enumerate(batches):
    json.dump(b, open(os.path.join(OUTDIR, f"batch_{n:02d}.json"), "w"), ensure_ascii=False)
json.dump({"expected_end": plan, "uc_tables": uc_tables, "tables": SEQ["Tabel"], "figures": SEQ["Gambar"]},
          open(os.path.join(OUTDIR, "plan.json"), "w"))
print(len(batches), "batches", [len(b) for b in batches], "sizes",
      [len(json.dumps(b, ensure_ascii=False)) for b in batches], "end", E)
