"""Build the tab-separated diagram spec consumed by the sapa.gen Visual Paradigm plugin.

Usage: python3 build_specs.py out.tsv
Diagrams follow the ANSI course style: use case with <<Include>> to Login, sequence with
Actor -> View (boundary) -> Cont (control) -> Ent (entity), class diagram in M-V-C columns,
activity diagrams with Aktor | Sistem swimlanes derived from the use case descriptions.
"""
import math
import sys

CH = 6.4  # approx. pixel width of one character in VP's default font
OUT = []


def emit(*cols):
    OUT.append("\t".join(str(c) for c in cols))


def tw(text):
    return int(len(text) * CH) + 14


# --------------------------------------------------------------------------- use case
def use_case_diagram():
    emit("DIAGRAM", "usecase", "Use Case Diagram SAPA")
    sx, sy, sw = 200, 20, 680
    left = [  # (id, name)
        ("uc02", "Mengirim Pesan WhatsApp"),
        ("uc04", "Mengelola Percakapan"),
        ("uc05", "Mengelola Prospek"),
        ("uc06", "Mengelola Kontak Pelanggan"),
        ("uc07", "Melihat Dasbor Pemantauan"),
        ("uc09", "Mengelola Basis Pengetahuan"),
        ("uc12", "Melihat Log Audit"),
        ("uc08", "Mengelola Nomor WhatsApp"),
        ("uc10", "Mengatur AI dan Anti-ban"),
        ("uc11", "Mengelola Tim dan Hak Akses"),
    ]
    row_h, top = 78, sy + 70
    sh = top + row_h * len(left) + 10 - sy
    emit("SHAPE", "sys", "system", sx, sy, sw, sh, "Sistem Asisten Pelanggan dan Akuisisi (SAPA)\\nBimbingan Belajar Asentra")
    ucw, uch = 250, 52
    pos = {}
    for i, (uid, name) in enumerate(left):
        x, y = sx + 50, top + i * row_h
        emit("SHAPE", uid, "usecase", x, y, ucw, uch, name)
        emit("PARENT", uid, "sys")
        pos[uid] = (x, y)
    emit("SHAPE", "uc03", "usecase", sx + 420, top, 230, uch, "Menjawab Pesan Otomatis dengan AI")
    emit("PARENT", "uc03", "sys")
    ly = top + row_h * 4 + 10
    emit("SHAPE", "uc01", "usecase", sx + 500, ly, 150, uch, "Login")
    emit("PARENT", "uc01", "sys")

    def ycenter(uid):
        return pos[uid][1] + uch // 2

    actors = [  # id, name, y (centred near its use cases)
        ("pel", "Pelanggan", ycenter("uc02") - 40),
        ("agen", "Agen/CS", ycenter("uc05") - 40),
        ("sup", "Supervisor", ycenter("uc09") - 40),
        ("adm", "Administrator", ycenter("uc10") - 40),
    ]
    for aid, name, y in actors:
        emit("SHAPE", aid, "actor", 40, y, 40, 80, name)
    emit("SHAPE", "wa", "actor", sx + sw + 70, top - 10, 40, 80, "WhatsApp Web")
    emit("SHAPE", "ai", "actor", sx + sw + 70, top + 150, 40, 80, "Penyedia AI")

    links = {
        "pel": ["uc02"],
        "agen": ["uc04", "uc05", "uc06"],
        "sup": ["uc07", "uc09", "uc12"],
        "adm": ["uc07", "uc09", "uc12", "uc08", "uc10", "uc11"],
    }
    for aid, ucs in links.items():
        for u in ucs:
            emit("CONN", "assoc", aid, u)
    for u in ("uc03",):
        emit("CONN", "assoc", "wa", u)
    emit("CONN", "assoc", "ai", "uc03")
    emit("CONN", "include", "uc02", "uc03")
    lx, lyc = sx + 500 + 75, ly + uch // 2
    for uid in ("uc04", "uc05", "uc06", "uc07", "uc09", "uc12", "uc08", "uc10", "uc11"):
        x0, y0 = pos[uid][0] + ucw, pos[uid][1] + uch // 2
        # caption 30% along the line so the labels do not pile up near Login
        cx = int(x0 + (lx - 75 - x0) * 0.35) - 10
        cy = int(y0 + (lyc - y0) * 0.35) - 16
        emit("CONN", "include", uid, "uc01", "", "", "", "", f"{cx},{cy}")


# --------------------------------------------------------------------------- sequence
STEREO = {"V": "boundary", "C": "control", "E": "entity"}


def sequence(name, lifelines, msgs):
    """lifelines: [(id, label, kind)] kind in A (actor), V, C, E.
    msgs: [(kind, from, to, label, seq)] kind in msg/ret/self."""
    emit("DIAGRAM", "sequence", name)
    xs, x = {}, 30
    widths = {}
    for i, (lid, label, kind) in enumerate(lifelines):
        w = max(110, tw(label))
        widths[lid] = w
    # spacing driven by the longest label of messages between neighbouring lifelines
    order = [l[0] for l in lifelines]
    gap = {}
    for kind, a, b, label, seq in msgs:
        if kind == "self":
            continue
        i, j = sorted((order.index(a), order.index(b)))
        need = tw(f"{seq}: {label}") // (j - i) + 30
        for k in range(i, j):
            gap[k] = max(gap.get(k, 0), need)
    y_top, step = 40, 32
    n = len(msgs)
    height = 120 + n * step + 60
    for i, (lid, label, kind) in enumerate(lifelines):
        w = widths[lid]
        if i > 0:
            prev = lifelines[i - 1][0]
            x = xs[prev] + widths[prev] // 2 + max(170, gap.get(i - 1, 0)) - w // 2
        xs[lid] = x
        if kind == "A":
            emit("SHAPE", lid, "iactor", x + w // 2 - 20, y_top, 40, height, label)
            xs[lid] = x + w // 2 - 20
            widths[lid] = 40
        else:
            emit("SHAPE", lid, "lifeline", x, y_top, w, height, label, STEREO[kind])
    # message y positions
    ys = []
    y = 130
    for kind, a, b, label, seq in msgs:
        ys.append(y)
        y += step + (20 if kind == "self" else 0)
    # activations per top-level step for every non-actor lifeline involved
    kinds = {l[0]: l[2] for l in lifelines}
    groups = {}
    for (kind, a, b, label, seq), yy in zip(msgs, ys):
        g = seq.split(".")[0]
        for lid in (a, b):
            if kinds[lid] == "A":
                continue
            lo, hi = groups.get((g, lid), (yy, yy))
            hi2 = yy + (24 if kind == "self" else 0)
            groups[(g, lid)] = (min(lo, yy), max(hi, hi2))
    k = 0
    for (g, lid), (lo, hi) in sorted(groups.items(), key=lambda t: t[1][0]):
        k += 1
        emit("ACT", f"act{k}", lid, lo - 6, hi + 10)
    for (kind, a, b, label, seq), yy in zip(msgs, ys):
        emit("CONN", kind, a, b, label, seq, yy)


def sequences():
    S = sequence
    S("SD-01 - Login",
      [("U", "Pengguna", "A"), ("V", "View : Login", "V"), ("C", "Cont : Login", "C"),
       ("E1", "Ent : Pengguna", "E"), ("E2", "Ent : AksesNomor", "E"), ("E3", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Isi email & kata sandi, klik Masuk", "1"),
       ("msg", "V", "C", "login(email, kataSandi)", "1.1"),
       ("msg", "C", "E1", "cariPengguna(email)", "1.1.1"),
       ("ret", "E1", "C", "dataPengguna", "1.1.2"),
       ("self", "C", "C", "verifikasiKataSandi()", "1.1.3"),
       ("msg", "C", "E2", "ambilAksesNomor(idPengguna)", "1.1.4"),
       ("ret", "E2", "C", "daftarNomor", "1.1.5"),
       ("msg", "C", "E3", "catatLog(\"login\")", "1.1.6"),
       ("ret", "C", "V", "tampilkanHalamanSesuaiPeran", "1.2")])
    S("SD-02 - Mengirim Pesan WhatsApp",
      [("P", "Pelanggan", "A"), ("V", "View : WhatsAppGateway", "V"), ("C", "Cont : Percakapan", "C"),
       ("E1", "Ent : Kontak", "E"), ("E2", "Ent : Prospek", "E"), ("E3", "Ent : Percakapan", "E"),
       ("E4", "Ent : Pesan", "E"), ("AI", "Cont : AIEngine", "C")],
      [("msg", "P", "V", "Kirim pesan", "1"),
       ("msg", "V", "C", "terimaPesan(nomor, isi)", "1.1"),
       ("msg", "C", "E1", "cariAtauBuatKontak(nomor)", "1.1.1"),
       ("ret", "E1", "C", "dataKontak", "1.1.2"),
       ("msg", "C", "E2", "buatProspek(\"baru\")", "1.1.3"),
       ("msg", "C", "E3", "bukaPercakapan(idKontak, idNomor)", "1.1.4"),
       ("msg", "C", "E4", "simpanPesan(masuk)", "1.1.5"),
       ("msg", "C", "AI", "prosesBalasan(pesan)", "1.1.6"),
       ("ret", "AI", "C", "balasan", "1.1.7"),
       ("msg", "C", "V", "kirimBalasan(balasan)", "1.2"),
       ("ret", "V", "P", "Balasan diterima", "1.3")])
    S("SD-03 - Menjawab Pesan Otomatis dengan AI",
      [("C", "Cont : AIEngine", "C"), ("E1", "Ent : Kontak", "E"), ("E2", "Ent : Prospek", "E"),
       ("E3", "Ent : ArtikelPengetahuan", "E"), ("AI", "Penyedia AI", "A"), ("E4", "Ent : PengaturanAI", "E"),
       ("AB", "Cont : AntiBan", "C"), ("E5", "Ent : AntreanKeluar", "E"), ("WA", "WhatsApp Web", "A")],
      [("self", "C", "C", "klasifikasiMaksud() & ekstrakEntitas()", "1"),
       ("msg", "C", "E1", "perbaruiKontak(entitas)", "1.1"),
       ("msg", "C", "E2", "hitungSkor()", "1.2"),
       ("msg", "C", "E3", "cariArtikel(kueri)", "1.3"),
       ("ret", "E3", "C", "artikelRelevan", "1.4"),
       ("msg", "C", "AI", "susunJawaban(artikel)", "1.5"),
       ("ret", "AI", "C", "jawaban", "1.6"),
       ("msg", "C", "E4", "ambilAmbang()", "1.7"),
       ("ret", "E4", "C", "ambang", "1.8"),
       ("self", "C", "C", "hitungKeyakinan()", "1.9"),
       ("msg", "C", "AB", "nilaiPesan(jawaban)", "1.10"),
       ("msg", "AB", "E5", "simpanAntrean(keputusan)", "1.10.1"),
       ("msg", "AB", "WA", "kirimPesan()", "1.10.2"),
       ("ret", "WA", "AB", "terkirim", "1.10.3"),
       ("ret", "AB", "C", "statusKirim", "1.11")])
    S("SD-04 - Mengelola Percakapan",
      [("U", "Agen/CS", "A"), ("V", "View : KotakMasuk", "V"), ("C", "Cont : Percakapan", "C"),
       ("E1", "Ent : AksesNomor", "E"), ("E2", "Ent : Percakapan", "E"), ("E3", "Ent : Pesan", "E"),
       ("AB", "Cont : AntiBan", "C"), ("E4", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Kotak Masuk", "1"),
       ("msg", "V", "C", "muatPercakapan(idPengguna)", "1.1"),
       ("msg", "C", "E1", "ambilAksesNomor()", "1.1.1"),
       ("msg", "C", "E2", "ambilPercakapan(daftarNomor)", "1.1.2"),
       ("ret", "E2", "C", "daftarPercakapan", "1.1.3"),
       ("ret", "C", "V", "tampilkanDaftar", "1.2"),
       ("msg", "U", "V", "Pilih percakapan", "2"),
       ("msg", "V", "C", "muatPesan(idPercakapan)", "2.1"),
       ("msg", "C", "E3", "ambilPesan()", "2.1.1"),
       ("ret", "E3", "C", "riwayat & jejak AI", "2.1.2"),
       ("ret", "C", "V", "tampilkanRiwayat", "2.2"),
       ("msg", "U", "V", "Ambil alih & kirim balasan", "3"),
       ("msg", "V", "C", "kirimBalasan(isi)", "3.1"),
       ("msg", "C", "E2", "setPenangan(\"manusia\")", "3.1.1"),
       ("msg", "C", "AB", "nilaiPesan()", "3.1.2"),
       ("ret", "AB", "C", "keputusan", "3.1.3"),
       ("msg", "C", "E3", "simpanPesan(keluar)", "3.1.4"),
       ("msg", "C", "E4", "catatLog(\"ambil alih\")", "3.1.5"),
       ("ret", "C", "V", "balasanTerkirim", "3.2")])
    S("SD-05 - Mengelola Prospek",
      [("U", "Agen/CS", "A"), ("V", "View : Prospek", "V"), ("C", "Cont : Prospek", "C"),
       ("E1", "Ent : Prospek", "E"), ("E2", "Ent : AktivitasProspek", "E"), ("E3", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Prospek", "1"),
       ("msg", "V", "C", "muatProspek()", "1.1"),
       ("msg", "C", "E1", "ambilProspek()", "1.1.1"),
       ("ret", "E1", "C", "daftarProspek", "1.1.2"),
       ("ret", "C", "V", "tampilkanPapan", "1.2"),
       ("msg", "U", "V", "Ubah tahap & isi catatan, klik Simpan", "2"),
       ("msg", "V", "C", "simpanPerubahan(tahap, catatan, tgl)", "2.1"),
       ("self", "C", "C", "validasi()", "2.1.1"),
       ("msg", "C", "E1", "ubahTahap()", "2.1.2"),
       ("msg", "C", "E2", "tambahAktivitas()", "2.1.3"),
       ("msg", "C", "E1", "hitungUlangSkor()", "2.1.4"),
       ("msg", "C", "E3", "catatLog()", "2.1.5"),
       ("ret", "C", "V", "tampilkanProspekTersimpan", "2.2")])
    S("SD-06 - Mengelola Kontak Pelanggan",
      [("U", "Agen/CS", "A"), ("V", "View : Kontak", "V"), ("C", "Cont : Kontak", "C"),
       ("E1", "Ent : Kontak", "E"), ("E2", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Ketik kata kunci pencarian", "1"),
       ("msg", "V", "C", "cariKontak(kataKunci)", "1.1"),
       ("msg", "C", "E1", "cari()", "1.1.1"),
       ("ret", "E1", "C", "hasil", "1.1.2"),
       ("ret", "C", "V", "tampilkanDaftar", "1.2"),
       ("msg", "U", "V", "Ubah data & klik Simpan", "2"),
       ("msg", "V", "C", "simpanKontak(data)", "2.1"),
       ("self", "C", "C", "validasiData()", "2.1.1"),
       ("msg", "C", "E1", "perbarui()", "2.1.2"),
       ("msg", "C", "E2", "catatLog()", "2.1.3"),
       ("ret", "C", "V", "tampilkanTersimpan", "2.2")])
    S("SD-07 - Melihat Dasbor Pemantauan",
      [("U", "Supervisor/Administrator", "A"), ("V", "View : Dasbor", "V"), ("C", "Cont : Dasbor", "C"),
       ("E1", "Ent : AksesNomor", "E"), ("E2", "Ent : MetrikHarian", "E"), ("E3", "Ent : NomorWhatsApp", "E")],
      [("msg", "U", "V", "Klik menu Dasbor", "1"),
       ("msg", "V", "C", "muatDasbor()", "1.1"),
       ("msg", "C", "E1", "ambilAksesNomor()", "1.1.1"),
       ("msg", "C", "E2", "ambilMetrik(nomor, periode)", "1.1.2"),
       ("ret", "E2", "C", "metrik", "1.1.3"),
       ("msg", "C", "E3", "ambilStatusNomor()", "1.1.4"),
       ("ret", "E3", "C", "status", "1.1.5"),
       ("ret", "C", "V", "tampilkanDasbor", "1.2"),
       ("msg", "U", "V", "Pilih filter nomor & periode", "2"),
       ("msg", "V", "C", "filterPeriode(nomor, periode)", "2.1"),
       ("self", "C", "C", "hitungMetrik()", "2.1.1"),
       ("ret", "C", "V", "tampilkanHasilFilter", "2.2")])
    S("SD-08 - Mengelola Nomor WhatsApp",
      [("U", "Administrator", "A"), ("V", "View : NomorWhatsApp", "V"), ("C", "Cont : NomorWA", "C"),
       ("E1", "Ent : NomorWhatsApp", "E"), ("WA", "WhatsApp Web", "A"), ("E2", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Isi form & klik Tautkan", "1"),
       ("msg", "V", "C", "tambahNomor(label, nomor, tujuan)", "1.1"),
       ("msg", "C", "E1", "simpanNomor(\"menunggu\")", "1.1.1"),
       ("msg", "C", "WA", "buatSesi()", "1.1.2"),
       ("ret", "WA", "C", "kodeQR", "1.1.3"),
       ("ret", "C", "V", "tampilkanQR", "1.2"),
       ("msg", "U", "WA", "Pindai kode QR dari ponsel", "2"),
       ("msg", "WA", "C", "konfirmasiTertaut()", "2.1"),
       ("msg", "C", "E1", "ubahStatus(\"tersambung\")", "2.1.1"),
       ("msg", "C", "E2", "catatLog()", "2.1.2"),
       ("ret", "C", "V", "tampilkanStatusTersambung", "2.2")])
    S("SD-09 - Mengelola Basis Pengetahuan",
      [("U", "Supervisor/Administrator", "A"), ("V", "View : BasisPengetahuan", "V"),
       ("C", "Cont : BasisPengetahuan", "C"), ("E1", "Ent : ArtikelPengetahuan", "E"), ("E2", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Basis Pengetahuan", "1"),
       ("msg", "V", "C", "muatArtikel()", "1.1"),
       ("msg", "C", "E1", "ambilArtikel()", "1.1.1"),
       ("ret", "E1", "C", "daftarArtikel", "1.1.2"),
       ("ret", "C", "V", "tampilkanDaftar", "1.2"),
       ("msg", "U", "V", "Isi form artikel & klik Simpan", "2"),
       ("msg", "V", "C", "simpanArtikel(data)", "2.1"),
       ("self", "C", "C", "validasi()", "2.1.1"),
       ("msg", "C", "E1", "simpan()", "2.1.2"),
       ("msg", "C", "E1", "indeksUlangFTS()", "2.1.3"),
       ("msg", "C", "E2", "catatLog()", "2.1.4"),
       ("ret", "C", "V", "tampilkanTersimpan", "2.2")])
    S("SD-10 - Mengatur AI dan Anti-ban",
      [("U", "Administrator", "A"), ("V", "View : PengaturanAI", "V"), ("C", "Cont : PengaturanAI", "C"),
       ("AI", "Penyedia AI", "A"), ("E1", "Ent : PengaturanAI", "E"), ("E2", "Ent : PengaturanAntiBan", "E"),
       ("E3", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Pengaturan AI", "1"),
       ("msg", "V", "C", "muatPengaturan()", "1.1"),
       ("msg", "C", "E1", "ambilPengaturanAI()", "1.1.1"),
       ("msg", "C", "E2", "ambilPengaturanAntiBan()", "1.1.2"),
       ("ret", "E2", "C", "pengaturan", "1.1.3"),
       ("ret", "C", "V", "tampilkanPengaturan", "1.2"),
       ("msg", "U", "V", "Ubah nilai & klik Simpan", "2"),
       ("msg", "V", "C", "simpanPengaturan(data)", "2.1"),
       ("self", "C", "C", "validasiNilai()", "2.1.1"),
       ("msg", "C", "AI", "ujiKoneksi(kunciAPI)", "2.1.2"),
       ("ret", "AI", "C", "koneksiOK", "2.1.3"),
       ("self", "C", "C", "enkripsiKunci()", "2.1.4"),
       ("msg", "C", "E1", "simpan()", "2.1.5"),
       ("msg", "C", "E2", "simpan()", "2.1.6"),
       ("msg", "C", "E3", "catatLog()", "2.1.7"),
       ("ret", "C", "V", "tampilkanTersimpan", "2.2")])
    S("SD-11 - Mengelola Tim dan Hak Akses",
      [("U", "Administrator", "A"), ("V", "View : TimAkses", "V"), ("C", "Cont : TimAkses", "C"),
       ("E1", "Ent : Pengguna", "E"), ("E2", "Ent : AksesNomor", "E"), ("E3", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Tim & Akses", "1"),
       ("msg", "V", "C", "muatPengguna()", "1.1"),
       ("msg", "C", "E1", "ambilPengguna()", "1.1.1"),
       ("ret", "E1", "C", "daftarPengguna", "1.1.2"),
       ("ret", "C", "V", "tampilkanDaftar", "1.2"),
       ("msg", "U", "V", "Isi form & akses nomor, klik Simpan", "2"),
       ("msg", "V", "C", "simpanPengguna(data, akses)", "2.1"),
       ("msg", "C", "E1", "cekEmailUnik(email)", "2.1.1"),
       ("ret", "E1", "C", "unik", "2.1.2"),
       ("msg", "C", "E1", "simpan()", "2.1.3"),
       ("msg", "C", "E2", "simpanAkses()", "2.1.4"),
       ("msg", "C", "E3", "catatLog()", "2.1.5"),
       ("ret", "C", "V", "tampilkanTersimpan", "2.2")])
    S("SD-12 - Melihat Log Audit",
      [("U", "Supervisor/Administrator", "A"), ("V", "View : LogAudit", "V"), ("C", "Cont : LogAudit", "C"),
       ("E1", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Log Audit", "1"),
       ("msg", "V", "C", "muatLog()", "1.1"),
       ("msg", "C", "E1", "ambilTerbaru()", "1.1.1"),
       ("ret", "E1", "C", "daftarLog", "1.1.2"),
       ("ret", "C", "V", "tampilkanLog", "1.2"),
       ("msg", "U", "V", "Isi filter pelaku, aksi & tanggal", "2"),
       ("msg", "V", "C", "filterLog(pelaku, aksi, tanggal)", "2.1"),
       ("msg", "C", "E1", "cari()", "2.1.1"),
       ("ret", "E1", "C", "hasil", "2.1.2"),
       ("ret", "C", "V", "tampilkanHasil", "2.2")])


# --------------------------------------------------------------------------- class (MVC)
UI = [
    ("UI:Login", ["Email", "KataSandi"]),
    ("UI:Dasbor", ["NomorTerpilih", "Periode"]),
    ("UI:KotakMasuk", ["PercakapanTerpilih", "IsiBalasan"]),
    ("UI:Prospek", ["TahapFilter", "ProspekTerpilih", "Catatan"]),
    ("UI:Kontak", ["KataKunci", "DataKontak"]),
    ("UI:NomorWhatsApp", ["Label", "Nomor", "Tujuan"]),
    ("UI:BasisPengetahuan", ["Judul", "Kategori", "Isi", "Label"]),
    ("UI:PengaturanAI", ["Penyedia", "KunciAPI", "AmbangKeyakinan", "KataKunciEskalasi", "BatasPerJam"]),
    ("UI:TimAkses", ["Nama", "Email", "Peran", "AksesNomor"]),
    ("UI:LogAudit", ["FilterPelaku", "FilterAksi", "RentangTanggal"]),
    ("UI:WhatsAppGateway", ["NomorPengirim", "IsiPesan"]),
]
CONT = [
    ("Cont:Login", ["validasiLogin", "ambilAksesNomor", "catatLogin"]),
    ("Cont:Dasbor", ["muatDasbor", "filterPeriode", "hitungMetrik"]),
    ("Cont:Percakapan", ["terimaPesan", "muatPercakapan", "kirimBalasan", "ambilAlih", "selesaikan"]),
    ("Cont:Prospek", ["muatProspek", "ubahTahap", "tambahAktivitas", "hitungSkor"]),
    ("Cont:Kontak", ["cariKontak", "simpanKontak"]),
    ("Cont:NomorWA", ["tambahNomor", "buatQR", "cekStatus", "putuskan"]),
    ("Cont:BasisPengetahuan", ["simpanArtikel", "indeksUlang", "ujiPencarian"]),
    ("Cont:PengaturanAI", ["simpanPengaturan", "enkripsiKunci", "ujiKeputusan"]),
    ("Cont:TimAkses", ["simpanPengguna", "aturAksesNomor", "nonaktifkan"]),
    ("Cont:LogAudit", ["muatLog", "filterLog"]),
    ("Cont:AIEngine", ["klasifikasiMaksud", "ekstrakEntitas", "cariArtikel", "susunJawaban", "hitungKeyakinan", "eskalasi"]),
    ("Cont:AntiBan", ["nilaiPesan", "antrekan", "kirimAntrean", "catatInsiden"]),
]
ENT = [
    ("Ent:Pengguna", ["idPengguna", "nama", "email", "kataSandiHash", "peran", "status"]),
    ("Ent:AksesNomor", ["idPengguna", "idNomor", "level"]),
    ("Ent:MetrikHarian", ["idNomor", "tanggal", "pesanMasuk", "pesanKeluar", "balasanAI", "balasanManusia", "belumDibalas", "rataWaktuBalas", "prospekBaru", "konversi"]),
    ("Ent:Percakapan", ["idPercakapan", "idKontak", "idNomor", "status", "penangan", "idAgen", "belumDibaca", "waktuBalasPertama"]),
    ("Ent:Pesan", ["idPesan", "idPercakapan", "arah", "jenisPengirim", "isi", "status", "metaAI"]),
    ("Ent:Prospek", ["idProspek", "idKontak", "tahap", "skor", "rincianSkor", "idPemilik", "tindakLanjutBerikut"]),
    ("Ent:AktivitasProspek", ["idAktivitas", "idProspek", "idPengguna", "jenis", "catatan", "waktu"]),
    ("Ent:Kontak", ["idKontak", "nomor", "nama", "jenjang", "kelas", "mapel", "kota", "sumber", "label"]),
    ("Ent:NomorWhatsApp", ["idNomor", "label", "nomor", "tujuan", "status", "modeAI", "skorKesehatan"]),
    ("Ent:ArtikelPengetahuan", ["idArtikel", "judul", "kategori", "isi", "label", "aktif"]),
    ("Ent:PengaturanAI", ["idNomor", "penyedia", "kunciAPITerenkripsi", "persona", "ambangKeyakinan", "kataKunciEskalasi"]),
    ("Ent:LogAudit", ["idLog", "idPengguna", "aksi", "entitas", "idEntitas", "detail", "waktu"]),
    ("Ent:PengaturanAntiBan", ["batasPerMenit", "batasPerJam", "batasPerHari", "jedaMin", "jedaMaks", "jamAktif"]),
    ("Ent:AntreanKeluar", ["idAntrean", "idPesan", "prioritas", "status", "skorRisiko", "keputusan", "jadwalKirim"]),
    ("Ent:Insiden", ["idInsiden", "idNomor", "jenis", "tingkat", "rencanaPemulihan", "status"]),
]
UI_CONT = {
    "UI:Login": ["Cont:Login"], "UI:Dasbor": ["Cont:Dasbor"], "UI:KotakMasuk": ["Cont:Percakapan"],
    "UI:Prospek": ["Cont:Prospek"], "UI:Kontak": ["Cont:Kontak"], "UI:NomorWhatsApp": ["Cont:NomorWA"],
    "UI:BasisPengetahuan": ["Cont:BasisPengetahuan"], "UI:PengaturanAI": ["Cont:PengaturanAI"],
    "UI:TimAkses": ["Cont:TimAkses"], "UI:LogAudit": ["Cont:LogAudit"], "UI:WhatsAppGateway": ["Cont:Percakapan"],
}
CONT_ENT = {
    "Cont:Login": ["Ent:Pengguna", "Ent:AksesNomor", "Ent:LogAudit"],
    "Cont:Dasbor": ["Ent:MetrikHarian", "Ent:NomorWhatsApp"],
    "Cont:Percakapan": ["Ent:Kontak", "Ent:Percakapan", "Ent:Pesan", "Ent:Prospek"],
    "Cont:Prospek": ["Ent:Prospek", "Ent:AktivitasProspek"],
    "Cont:Kontak": ["Ent:Kontak"],
    "Cont:NomorWA": ["Ent:NomorWhatsApp"],
    "Cont:BasisPengetahuan": ["Ent:ArtikelPengetahuan"],
    "Cont:PengaturanAI": ["Ent:PengaturanAI", "Ent:PengaturanAntiBan"],
    "Cont:TimAkses": ["Ent:Pengguna", "Ent:AksesNomor"],
    "Cont:LogAudit": ["Ent:LogAudit"],
    "Cont:AIEngine": ["Ent:ArtikelPengetahuan", "Ent:PengaturanAI", "Ent:Prospek"],
    "Cont:AntiBan": ["Ent:AntreanKeluar", "Ent:PengaturanAntiBan", "Ent:Insiden"],
}
ROW = 15  # VP row height for attributes/operations
HEAD = 24


def class_diagram():
    emit("DIAGRAM", "class", "Class Diagram SAPA (MVC)")
    ids = {}

    def column(items, x, kind, gap):
        y = 20
        for name, members in items:
            cid = "c" + str(len(ids))
            ids[name] = cid
            if kind == "UI":
                lines = [m for m in members] + [f"getX" for m in members] * 2
                w = max(tw(name) + 20, max(tw(f"+set{m}({m}) : void") for m in members) + 10)
                h = HEAD + ROW * 3 * len(members) + 6
            elif kind == "Cont":
                w = max(tw(name) + 20, max(tw(f"+{m}()") for m in members) + 10)
                h = HEAD + ROW * len(members) + 10
            else:
                w = max(tw(name) + 20, max(tw(f"-{m}") for m in members) + 10)
                h = HEAD + ROW * len(members) + 10
            emit("SHAPE", cid, "class", x, y, w, h, name)
            for m in members:
                if kind == "UI":
                    emit("ATTR", cid, m)
                elif kind == "Ent":
                    emit("ATTR", cid, m)
            if kind == "UI":
                for m in members:
                    emit("OP", cid, f"get{m}", "", "")
                    emit("OP", cid, f"set{m}", m, "void")
            elif kind == "Cont":
                for m in members:
                    emit("OP", cid, m, "", "")
            y += h + gap

    column(UI, 20, "UI", 22)
    column(CONT, 520, "Cont", 48)
    column(ENT, 920, "Ent", 20)
    for ui, conts in UI_CONT.items():
        for c in conts:
            emit("CONN", "assoc", ids[ui], ids[c])
    for c, ents in CONT_ENT.items():
        for e in ents:
            emit("CONN", "assoc", ids[c], ids[e])


# --------------------------------------------------------------------------- activity
LANE_A_W, LANE_S_W = 320, 560
ACT_W = 190


class Node:
    def __init__(self, nid, lane, row, col, kind, text):
        self.id, self.lane, self.row, self.col, self.kind, self.text = nid, lane, row, col, kind, text
        if kind == "action":
            lines = max(1, math.ceil(tw(text) / (ACT_W - 16)))
            self.w, self.h = ACT_W, max(40, lines * 15 + 16)
        elif kind == "decision":
            self.w = self.h = 34
        else:
            self.w = self.h = 24
        if lane == "A":
            cx = 20 + LANE_A_W // 2 + col * 200
        else:
            cx = 20 + LANE_A_W + (170 if col == 0 else 420)
        cy = 90 + row * 82
        self.cx, self.cy = cx, cy
        self.x, self.y = cx - self.w // 2, cy - self.h // 2

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h


def activity(name, lane_a, nodes, edges):
    emit("DIAGRAM", "activity", name)
    N = {}
    for nid, lane, row, col, kind, text in nodes:
        N[nid] = Node(nid, lane, row, col, kind, text)
    height = max(n.bottom for n in N.values()) + 50
    emit("SHAPE", "pa", "partition", 20, 20, LANE_A_W, height, lane_a)
    emit("SHAPE", "ps", "partition", 20 + LANE_A_W, 20, LANE_S_W, height, "Sistem SAPA")
    for n in N.values():
        emit("SHAPE", n.id, n.kind, n.x, n.y, n.w, n.h, n.text)
    for a, b, guard in edges:
        s, t = N[a], N[b]
        pts, cap = route(s, t)
        emit("CONN", "flow", a, b, guard, "", "", ";".join(f"{x},{y}" for x, y in pts),
             f"{cap[0]},{cap[1]}" if guard else "")


def route(s, t):
    if t.row == s.row:  # side branch on the same row
        if t.cx > s.cx:
            pts = [(s.right, s.cy), (t.x, t.cy)]
            cap = (s.right + 6, s.cy - 18)
        else:
            pts = [(s.x, s.cy), (t.right, t.cy)]
            cap = (t.right + 6, s.cy - 18)
    elif t.row > s.row:
        if abs(s.cx - t.cx) < 4:
            pts = [(s.cx, s.bottom), (t.cx, t.y)]
            cap = (s.cx + 6, s.bottom + 2)
        elif t.row > s.row + 1 and (s.col == 1 or (s.kind == "decision" and t.col == 1)):
            # long drop: run down the outer edge of the Sistem lane so no box is crossed
            dec = s.kind == "decision"
            xr = 20 + LANE_A_W + LANE_S_W - (12 if dec else 30)
            sy, ty = s.cy + (0 if dec else 8), t.cy - (8 if dec else 0)
            pts = [(s.right, sy), (xr, sy), (xr, ty), (t.right, ty)]
            cap = (s.right + 6, s.cy - 18)
        elif s.kind == "decision" and t.cx > s.cx:
            # branch: leave the decision sideways, then drop into the target top
            pts = [(s.right, s.cy), (t.cx, s.cy), (t.cx, t.y)]
            cap = (s.right + 6, s.cy - 18)
        else:
            # leave the source downward, then run horizontally into the target side
            tx = t.x if t.cx > s.cx else t.right
            pts = [(s.cx, s.bottom), (s.cx, t.cy), (tx, t.cy)]
            cap = (s.cx + 6, s.bottom + 2)
    else:  # loop back upward along the right of both nodes
        # loop back upward and enter the target from above so it never merges with another arrow
        xr = max(s.right, t.right) + 22
        ty = t.y - 14
        pts = [(s.right, s.cy), (xr, s.cy), (xr, ty), (t.cx + 40, ty), (t.cx + 40, t.y)]
        cap = (s.right + 6, s.cy - 18)
    return pts, cap


def activities():
    A = activity
    A("AD-01 - Login", "Pengguna", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Membuka halaman Login"),
        ("s1", "S", 2, 0, "action", "Menampilkan form email dan kata sandi"),
        ("a2", "A", 3, 0, "action", "Mengisi email dan kata sandi, klik Masuk"),
        ("s2", "S", 4, 0, "action", "Memvalidasi kredensial"),
        ("d1", "S", 5, 0, "decision", ""),
        ("e1", "S", 5, 1, "action", "Menampilkan \"Email atau kata sandi salah\""),
        ("d2", "S", 6, 0, "decision", ""),
        ("e2", "S", 6, 1, "action", "Menampilkan \"Akun Anda dinonaktifkan\""),
        ("f2", "S", 7, 1, "final", ""),
        ("s3", "S", 7, 0, "action", "Mengambil peran dan akses nomor"),
        ("s4", "S", 8, 0, "action", "Mencatat log audit login"),
        ("s5", "S", 9, 0, "action", "Menampilkan halaman sesuai peran"),
        ("f", "S", 10, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "d1", ""),
        ("d1", "d2", "kredensial valid"), ("d1", "e1", "kredensial salah"), ("e1", "a2", ""),
        ("d2", "s3", "akun aktif"), ("d2", "e2", "akun nonaktif"), ("e2", "f2", ""),
        ("s3", "s4", ""), ("s4", "s5", ""), ("s5", "f", "")])
    A("AD-02 - Mengirim Pesan WhatsApp", "Pelanggan", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Mengirim pesan ke nomor WhatsApp Asentra"),
        ("s1", "S", 2, 0, "action", "Menerima pesan melalui gerbang WhatsApp Web"),
        ("s2", "S", 3, 0, "action", "Mencari kontak berdasarkan nomor pengirim"),
        ("d1", "S", 4, 0, "decision", ""),
        ("s3", "S", 4, 1, "action", "Membuat kontak dan prospek tahap \"baru\""),
        ("s4", "S", 5, 0, "action", "Membuka percakapan dan menyimpan pesan"),
        ("d2", "S", 6, 0, "decision", ""),
        ("s5", "S", 6, 1, "action", "Menandai percakapan \"belum dibalas\" untuk agen"),
        ("f2", "S", 7, 1, "final", ""),
        ("s6", "S", 7, 0, "action", "Menjalankan UC-03 Menjawab Pesan Otomatis dengan AI"),
        ("a2", "A", 8, 0, "action", "Menerima balasan di WhatsApp"),
        ("f", "A", 9, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "s2", ""), ("s2", "d1", ""),
        ("d1", "s4", "kontak sudah ada"), ("d1", "s3", "kontak baru"), ("s3", "s4", ""),
        ("s4", "d2", ""), ("d2", "s6", "ditangani AI"), ("d2", "s5", "ditangani manusia"), ("s5", "f2", ""),
        ("s6", "a2", ""), ("a2", "f", "")])
    A("AD-03 - Menjawab Pesan Otomatis dengan AI", "Penyedia AI / WhatsApp Web", [
        ("i", "S", 0, 0, "initial", ""),
        ("s1", "S", 1, 0, "action", "Mengklasifikasi maksud dan mengekstrak entitas"),
        ("s2", "S", 2, 0, "action", "Memperbarui kontak dan skor prioritas"),
        ("s3", "S", 3, 0, "action", "Mencari artikel basis pengetahuan (FTS5)"),
        ("d1", "S", 4, 0, "decision", ""),
        ("x1", "A", 5, 0, "action", "Penyedia AI menyusun jawaban dari artikel"),
        ("d2", "S", 6, 0, "decision", ""),
        ("s4", "S", 6, 1, "action", "Menyusun jawaban dengan mode aturan bawaan"),
        ("s5", "S", 7, 0, "action", "Menghitung nilai keyakinan"),
        ("d3", "S", 8, 0, "decision", ""),
        ("esc", "S", 8, 1, "action", "Mengalihkan percakapan ke agen dan mengirim pemberitahuan"),
        ("s6", "S", 9, 0, "action", "Menilai pesan dengan mesin anti-ban"),
        ("d4", "S", 10, 0, "decision", ""),
        ("s7", "S", 10, 1, "action", "Menyimpan di antrean dan mencatat di Pusat Risiko"),
        ("x2", "A", 11, 0, "action", "WhatsApp Web mengirim balasan beserta sumber"),
        ("s8", "S", 12, 0, "action", "Mencatat jejak keputusan AI dan metrik harian"),
        ("f", "S", 13, 0, "final", ""),
    ], [("i", "s1", ""), ("s1", "s2", ""), ("s2", "s3", ""), ("s3", "d1", ""),
        ("d1", "x1", "artikel ditemukan"), ("d1", "esc", "tidak ada artikel"), ("x1", "d2", ""),
        ("d2", "s5", "berhasil"), ("d2", "s4", "gagal/timeout"), ("s4", "s5", ""),
        ("s5", "d3", ""), ("d3", "s6", "yakin"), ("d3", "esc", "di bawah ambang"),
        ("esc", "s8", ""), ("s6", "d4", ""), ("d4", "x2", "kirim"), ("d4", "s7", "tunda/tahan"),
        ("s7", "s8", ""), ("x2", "s8", ""), ("s8", "f", "")])
    A("AD-04 - Mengelola Percakapan", "Agen/CS", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Kotak Masuk"),
        ("s1", "S", 2, 0, "action", "Menampilkan daftar percakapan dari nomor yang diizinkan"),
        ("a2", "A", 3, 0, "action", "Memilih percakapan"),
        ("d1", "S", 4, 0, "decision", ""),
        ("s2", "S", 4, 1, "action", "Menolak: \"Anda tidak memiliki akses ke nomor ini\""),
        ("f2", "S", 5, 1, "final", ""),
        ("s3", "S", 5, 0, "action", "Menampilkan riwayat, jawaban AI, dan jejak keputusan"),
        ("a3", "A", 6, 0, "action", "Mengambil alih, menulis balasan, klik Kirim"),
        ("s4", "S", 7, 0, "action", "Menghentikan AI untuk percakapan ini"),
        ("s5", "S", 8, 0, "action", "Menilai pesan dengan mesin anti-ban"),
        ("d2", "S", 9, 0, "decision", ""),
        ("s6", "S", 9, 1, "action", "Menampilkan \"Pesan ditunda oleh pengaman pengiriman\""),
        ("s7", "S", 10, 0, "action", "Mengirim balasan melalui antrean keluar"),
        ("s8", "S", 11, 0, "action", "Memperbarui status, metrik, dan log audit"),
        ("f", "S", 12, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "d1", ""),
        ("d1", "s3", "akses diizinkan"), ("d1", "s2", "tidak diizinkan"), ("s2", "f2", ""),
        ("s3", "a3", ""), ("a3", "s4", ""), ("s4", "s5", ""), ("s5", "d2", ""),
        ("d2", "s7", "kirim"), ("d2", "s6", "tunda/tahan"), ("s6", "s8", ""), ("s7", "s8", ""), ("s8", "f", "")])
    A("AD-05 - Mengelola Prospek", "Agen/CS", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Prospek"),
        ("s1", "S", 2, 0, "action", "Menampilkan papan prospek per tahap urut skor"),
        ("a2", "A", 3, 0, "action", "Memilih kartu prospek"),
        ("s2", "S", 4, 0, "action", "Menampilkan detail, rincian skor, dan riwayat aktivitas"),
        ("a3", "A", 5, 0, "action", "Mengubah tahap, mengisi catatan dan tanggal tindak lanjut, klik Simpan"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s3", "S", 6, 1, "action", "Menampilkan \"Catatan wajib diisi\""),
        ("s4", "S", 7, 0, "action", "Menyimpan perubahan dan menghitung ulang skor"),
        ("d2", "S", 8, 0, "decision", ""),
        ("s5", "S", 8, 1, "action", "Menambah hitungan konversi"),
        ("s6", "S", 9, 0, "action", "Mencatat log audit"),
        ("f", "S", 10, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "a3", ""),
        ("a3", "d1", ""), ("d1", "s4", "catatan terisi"), ("d1", "s3", "catatan kosong"), ("s3", "a3", ""),
        ("s4", "d2", ""), ("d2", "s6", "tahap lain"), ("d2", "s5", "tahap = daftar"), ("s5", "s6", ""),
        ("s6", "f", "")])
    A("AD-06 - Mengelola Kontak Pelanggan", "Agen/CS", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Kontak dan mengetik kata kunci"),
        ("s1", "S", 2, 0, "action", "Mencari kontak"),
        ("d1", "S", 3, 0, "decision", ""),
        ("s2", "S", 3, 1, "action", "Menampilkan \"Kontak tidak ditemukan\""),
        ("f2", "S", 4, 1, "final", ""),
        ("s3", "S", 4, 0, "action", "Menampilkan daftar kontak"),
        ("a2", "A", 5, 0, "action", "Memilih kontak, klik Ubah"),
        ("s4", "S", 6, 0, "action", "Menampilkan form data dan riwayat percakapan"),
        ("a3", "A", 7, 0, "action", "Memperbarui data, klik Simpan"),
        ("d2", "S", 8, 0, "decision", ""),
        ("s5", "S", 8, 1, "action", "Menandai kolom yang salah"),
        ("s6", "S", 9, 0, "action", "Menyimpan perubahan dan mencatat log audit"),
        ("f", "S", 10, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "d1", ""), ("d1", "s3", "ditemukan"),
        ("d1", "s2", "tidak ditemukan"), ("s2", "f2", ""), ("s3", "a2", ""), ("a2", "s4", ""),
        ("s4", "a3", ""), ("a3", "d2", ""), ("d2", "s6", "data valid"), ("d2", "s5", "tidak valid"),
        ("s5", "a3", ""), ("s6", "f", "")])
    A("AD-07 - Melihat Dasbor Pemantauan", "Supervisor / Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Dasbor"),
        ("s1", "S", 2, 0, "action", "Mengambil metrik harian dan status nomor yang diizinkan"),
        ("s2", "S", 3, 0, "action", "Menampilkan kartu ringkasan, grafik, dan status nomor"),
        ("a2", "A", 4, 0, "action", "Memilih filter nomor dan periode"),
        ("s3", "S", 5, 0, "action", "Menghitung ulang metrik sesuai filter"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s4", "S", 6, 1, "action", "Menampilkan \"Belum ada data pada periode ini\""),
        ("s5", "S", 7, 0, "action", "Menampilkan hasil filter"),
        ("f", "S", 8, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "s2", ""), ("s2", "a2", ""), ("a2", "s3", ""),
        ("s3", "d1", ""), ("d1", "s5", "ada data"), ("d1", "s4", "tidak ada data"), ("s4", "f", ""),
        ("s5", "f", "")])
    A("AD-08 - Mengelola Nomor WhatsApp", "Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Nomor WhatsApp, klik Tambah Nomor"),
        ("s1", "S", 2, 0, "action", "Menampilkan form label, nomor, dan tujuan"),
        ("a2", "A", 3, 0, "action", "Mengisi form, klik Tautkan"),
        ("s2", "S", 4, 0, "action", "Membuat sesi WhatsApp Web dan menampilkan kode QR"),
        ("a3", "A", 5, 0, "action", "Memindai kode QR dari ponsel"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s3", "S", 6, 1, "action", "Menampilkan \"QR kedaluwarsa\" dan tombol Buat ulang"),
        ("d2", "S", 7, 0, "decision", ""),
        ("s4", "S", 7, 1, "action", "Status \"gagal tertaut\" dan dicatat di Pusat Risiko"),
        ("f2", "S", 8, 1, "final", ""),
        ("s5", "S", 8, 0, "action", "Menyimpan sesi, status \"tersambung\", dan log audit"),
        ("f", "S", 9, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "a3", ""),
        ("a3", "d1", ""), ("d1", "d2", "QR berlaku"), ("d1", "s3", "kedaluwarsa"), ("s3", "s2", ""),
        ("d2", "s5", "tertaut"), ("d2", "s4", "gagal"), ("s4", "f2", ""), ("s5", "f", "")])
    A("AD-09 - Mengelola Basis Pengetahuan", "Supervisor / Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Basis Pengetahuan"),
        ("s1", "S", 2, 0, "action", "Menampilkan daftar artikel per kategori"),
        ("a2", "A", 3, 0, "action", "Klik Tambah Artikel atau memilih artikel"),
        ("s2", "S", 4, 0, "action", "Menampilkan form artikel"),
        ("a3", "A", 5, 0, "action", "Mengisi judul, kategori, isi, label, klik Simpan"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s3", "S", 6, 1, "action", "Menampilkan \"Judul dan isi wajib diisi\""),
        ("s4", "S", 7, 0, "action", "Menyimpan artikel dan mengindeks ulang FTS5"),
        ("s5", "S", 8, 0, "action", "Mencatat log audit"),
        ("f", "S", 9, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "a3", ""),
        ("a3", "d1", ""), ("d1", "s4", "lengkap"), ("d1", "s3", "kosong"), ("s3", "a3", ""),
        ("s4", "s5", ""), ("s5", "f", "")])
    A("AD-10 - Mengatur AI dan Anti-ban", "Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Pengaturan AI"),
        ("s1", "S", 2, 0, "action", "Menampilkan pengaturan AI, anti-ban, antrean, dan Pusat Risiko"),
        ("a2", "A", 3, 0, "action", "Mengubah penyedia, kunci API, ambang, kata kunci, dan batas kirim"),
        ("a3", "A", 4, 0, "action", "Klik Simpan"),
        ("d1", "S", 5, 0, "decision", ""),
        ("s2", "S", 5, 1, "action", "Menolak dan menandai kolom yang salah"),
        ("s3", "S", 6, 0, "action", "Menguji koneksi penyedia AI"),
        ("d2", "S", 7, 0, "decision", ""),
        ("s4", "S", 7, 1, "action", "Menampilkan \"Kunci API ditolak penyedia\""),
        ("s5", "S", 8, 0, "action", "Mengenkripsi kunci API (AES-256-GCM)"),
        ("s6", "S", 9, 0, "action", "Menyimpan pengaturan dan mencatat log audit"),
        ("f", "S", 10, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "a3", ""), ("a3", "d1", ""),
        ("d1", "s3", "nilai wajar"), ("d1", "s2", "tidak wajar"), ("s2", "a2", ""),
        ("s3", "d2", ""), ("d2", "s5", "diterima"), ("d2", "s4", "ditolak"), ("s4", "a2", ""),
        ("s5", "s6", ""), ("s6", "f", "")])
    A("AD-11 - Mengelola Tim dan Hak Akses", "Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Tim & Akses"),
        ("s1", "S", 2, 0, "action", "Menampilkan daftar pengguna, peran, dan akses nomor"),
        ("a2", "A", 3, 0, "action", "Klik Tambah Pengguna atau memilih pengguna"),
        ("s2", "S", 4, 0, "action", "Menampilkan form dan matriks akses per nomor"),
        ("a3", "A", 5, 0, "action", "Mengisi data, memilih level akses, klik Simpan"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s3", "S", 6, 1, "action", "Menampilkan \"Email sudah digunakan\""),
        ("s4", "S", 7, 0, "action", "Menyimpan pengguna dan akses nomor"),
        ("s5", "S", 8, 0, "action", "Mencatat log audit"),
        ("f", "S", 9, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "a3", ""),
        ("a3", "d1", ""), ("d1", "s4", "email unik"), ("d1", "s3", "sudah terdaftar"), ("s3", "a3", ""),
        ("s4", "s5", ""), ("s5", "f", "")])
    A("AD-12 - Melihat Log Audit", "Supervisor / Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Log Audit"),
        ("s1", "S", 2, 0, "action", "Menampilkan log terbaru"),
        ("a2", "A", 3, 0, "action", "Mengisi filter pelaku, aksi, dan tanggal"),
        ("s2", "S", 4, 0, "action", "Mencari log sesuai filter"),
        ("d1", "S", 5, 0, "decision", ""),
        ("s3", "S", 5, 1, "action", "Menampilkan \"Tidak ada aktivitas pada filter ini\""),
        ("s4", "S", 6, 0, "action", "Menampilkan daftar log"),
        ("f", "S", 7, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "d1", ""),
        ("d1", "s4", "ada hasil"), ("d1", "s3", "tidak ada"), ("s3", "f", ""), ("s4", "f", "")])


if __name__ == "__main__":
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    if which in ("all", "uc"):
        use_case_diagram()
    if which in ("all", "cd"):
        class_diagram()
    if which in ("all", "sd"):
        sequences()
    if which in ("all", "ad"):
        activities()
    with open(sys.argv[1], "w", encoding="utf-8") as fh:
        fh.write("\n".join(OUT) + "\n")
    print(f"{len(OUT)} spec lines -> {sys.argv[1]}")
