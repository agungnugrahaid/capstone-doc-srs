# Spesifikasi Mockup High-Fidelity SAPA (untuk Figma)

Untuk: Enrico (mockup hi-fi). Revisi dosen: *mockup high fidelity, detail untuk setiap halaman yang akan dibuat*. Setiap halaman = 1 frame Figma, lalu ekspor PNG 2x dan simpan sebagai `doc-srs/final/mockup/MK-xx-nama.png` (nama file di tabel bawah) agar langsung masuk ke laporan.

## Aturan umum
- **Frame**: Desktop 1440 × 900. Halaman Login boleh tanpa sidebar.
- **Warna** (berwarna, bukan hitam-putih):
  - Primer `#0F766E` (teal 700), hover `#115E59`, latar primer tipis `#CCFBF1`
  - Aksen WhatsApp `#25D366` (hanya untuk ikon/status tersambung)
  - Netral: latar `#F8FAFC`, kartu `#FFFFFF`, garis `#E2E8F0`, teks `#0F172A`, teks sekunder `#64748B`
  - Status: sukses `#16A34A`, peringatan `#F59E0B`, bahaya `#DC2626`, info `#2563EB`
- **Tipografi**: Inter. Judul halaman 24/32 semibold, subjudul 14/20 regular sekunder, isi 14/20, label 12/16 medium.
- **Komponen bersama**: sudut 8–12 px, bayangan halus kartu, ikon Lucide.
- **Layout aplikasi**: sidebar kiri 248 px (logo SAPA + nama pengguna & peran; menu: Dasbor, Kotak Masuk [badge belum dibalas], Prospek, Kontak, Nomor WhatsApp, Basis Pengetahuan, Pengaturan AI, Antrean & Risiko, Tim & Akses, Log Audit; menu yang tidak sesuai peran disembunyikan). Header atas: judul halaman, subjudul, kolom cari global, pemilih nomor ("Semua nomor"), avatar + tombol Keluar.
- **Data contoh** (anonim, konsisten di semua halaman): nomor "Admin Asentra" 0812-xxxx-1001 dan "Sales Asentra" 0812-xxxx-1002; agen Dewi (Admin), Raka (Sales); supervisor Pak Yordan; pelanggan Rina Kusuma (SMP kelas 8, Matematika), Bapak Hendra, Sinta, Agus Wibowo.

## Halaman

| Kode | File PNG | Halaman | Use case |
|---|---|---|---|
| MK-01 | MK-01-login.png | Login | UC-01 |
| MK-02 | MK-02-dasbor.png | Dasbor Pemantauan | UC-07 |
| MK-03 | MK-03-kotak-masuk.png | Kotak Masuk | UC-04 (UC-02, UC-03) |
| MK-04 | MK-04-prospek.png | Prospek | UC-05 |
| MK-05 | MK-05-kontak.png | Kontak | UC-06 |
| MK-06 | MK-06-nomor-whatsapp.png | Nomor WhatsApp | UC-08 |
| MK-07 | MK-07-basis-pengetahuan.png | Basis Pengetahuan | UC-09 |
| MK-08 | MK-08-pengaturan-ai.png | Pengaturan AI & Konsol Uji | UC-10 |
| MK-09 | MK-09-antrean-risiko.png | Antrean Keluar & Pusat Risiko | UC-10 |
| MK-10 | MK-10-tim-akses.png | Tim & Akses | UC-11 |
| MK-11 | MK-11-log-audit.png | Log Audit | UC-12 |

### MK-01 Login
- Layout dua kolom: kiri panel teal dengan logo SAPA, tagline "Satu kotak masuk untuk semua nomor WhatsApp Asentra", ilustrasi chat; kanan kartu login.
- Kartu: judul "Masuk ke SAPA", field Email, field Kata sandi (ikon mata), checkbox "Ingat saya", tombol primer penuh "Masuk".
- Tampilkan state error di bawah form: alert merah "Email atau kata sandi salah" (bisa sebagai varian frame kecil di samping).
- Footer: "Bimbingan Belajar Asentra · SIF26062P Capstone".

### MK-02 Dasbor Pemantauan
- Filter atas: pemilih nomor (Semua / Admin / Sales), segmented periode (Hari ini · 7 hari · 30 hari).
- Baris 4 kartu KPI: Percakapan masuk (mis. 128, ▲12%), Rata-rata waktu balas pertama (1 m 42 d), Belum dibalas (3, merah), Konversi pendaftaran (9 · 7,0%).
- Grafik garis volume per hari (2 seri: Admin vs Sales) + grafik batang "Dibalas AI vs Manusia".
- Tabel "Kinerja per nomor": label, status (titik hijau "Tersambung"), masuk, keluar, belum dibalas, waktu balas, konversi, skor kesehatan nomor (progress bar).
- Panel kanan kecil "Prospek prioritas hari ini" (5 nama dengan skor).

### MK-03 Kotak Masuk (halaman paling penting)
- Tiga kolom: daftar percakapan | percakapan aktif | panel pelanggan.
- Daftar: tab Semua / Belum dibalas / Ditangani AI / Ditangani saya; tiap item: avatar inisial, nama, cuplikan pesan, jam, chip nomor (Admin/Sales), badge jumlah belum dibaca; item aktif ter-highlight teal.
- Percakapan: header nama + nomor + chip "Dibalas AI"; gelembung pelanggan (putih, kiri) dan balasan (teal muda, kanan). Balasan AI berlabel "SAPA (AI) · keyakinan 0,88" dan baris kecil "Sumber: Basis Pengetahuan › Program SMP".
- Tampilkan satu pesan sistem "Percakapan dialihkan ke admin (keyakinan 0,41 < 0,62)" sebagai contoh eskalasi.
- Kotak ketik: textarea, tombol lampiran, tombol "Kirim"; di atasnya tombol "Ambil alih percakapan" (outline) dan "Selesaikan".
- Panel pelanggan: data (jenjang, kelas, mapel, kota, sumber, tahap prospek), skor prioritas 78 dengan rincian 5 komponen (bar kecil), "Jejak keputusan AI" (maksud, entitas, artikel + skor, keyakinan vs ambang), tombol "Ubah tahap prospek".

### MK-04 Prospek
- Papan kanban kolom: Baru · Dihubungi · Tertarik · Penawaran · Daftar · Batal (jumlah di header kolom).
- Kartu: nama, jenjang/kelas/mapel, chip nomor, skor (badge warna: ≥70 hijau, 40–69 kuning, <40 abu), tanggal tindak lanjut, avatar pemilik.
- Drawer kanan untuk kartu terpilih: rincian skor (5 komponen berbobot), riwayat aktivitas (timeline), form "Tambah catatan" + pilih tanggal tindak lanjut + tombol Simpan; validasi "Catatan wajib diisi".

### MK-05 Kontak
- Toolbar: cari, filter jenjang, filter sumber, tombol "Tambah Kontak".
- Tabel: nama, nomor WhatsApp, jenjang, kelas, mapel, kota, sumber, label (chip), tahap prospek, terakhir chat; paginasi.
- Modal "Ubah Kontak" (frame terpisah atau overlay): field data, riwayat percakapan singkat; contoh error kolom "Nomor sudah terdaftar".

### MK-06 Nomor WhatsApp
- Grid kartu nomor: label, nomor, tujuan (Admin/Sales), status (Tersambung hijau / Menunggu QR kuning / Terputus merah), mode AI (Otomatis/Draf/Mati), skor kesehatan, pesan hari ini vs batas, tombol "Putuskan".
- Tombol "Tambah Nomor" membuka modal: langkah 1 form (label, nomor, tujuan), langkah 2 kode QR besar 360 px + hitung mundur 60 detik + petunjuk "Buka WhatsApp › Perangkat tertaut › Tautkan perangkat", state "QR kedaluwarsa · Buat ulang QR".

### MK-07 Basis Pengetahuan
- Kiri: daftar kategori (Program, Jadwal, Biaya, Fasilitas, Pendaftaran, Persiapan Tes) dengan jumlah artikel.
- Tengah: tabel artikel (judul, kategori, label, status aktif toggle, diperbarui).
- Kanan: editor artikel (judul, kategori, isi rich text, label, aktif) + tombol Simpan.
- Panel "Uji Pencarian": input pertanyaan "jadwal kelas 8 SMP?" dan hasil 3 artikel teratas dengan skor bm25.

### MK-08 Pengaturan AI & Konsol Uji
- Tab: Model AI · Eskalasi · Anti-ban · Konsol Uji.
- Model AI: pilihan penyedia (Aturan bawaan / OpenAI / Kompatibel OpenAI + Base URL / Gemini), kunci API (tersamar ••••, label "Terenkripsi AES-256-GCM"), persona & nada, panjang balasan maks.
- Eskalasi: slider ambang keyakinan 0,62, chip kata kunci eskalasi ("admin", "komplain", "refund"), toggle "Alihkan bila pelanggan marah".
- Anti-ban: batas per menit/jam/hari, jeda min–maks (ms), jam aktif 07.00–21.00, hari pemanasan nomor.
- Konsol Uji: input pesan contoh → kartu hasil langkah demi langkah (maksud, entitas, artikel, keyakinan, keputusan anti-ban, keputusan akhir "Kirim" / "Eskalasi").

### MK-09 Antrean Keluar & Pusat Risiko
- Atas: kartu ringkas Antrean (antre, terkirim, ditunda, ditahan).
- Tabel antrean: waktu jadwal, nomor, penerima, cuplikan pesan, skor risiko (bar), keputusan (chip Kirim/Tunda/Tahan), percobaan, aksi (Kirim sekarang / Batalkan).
- Bawah: daftar Insiden Pusat Risiko: jenis (batas laju terlampaui, soft ban, terputus), tingkat (peringatan/tinggi/kritis), nomor, waktu, rencana pemulihan, status (aktif/selesai).

### MK-10 Tim & Akses
- Tabel pengguna: nama, email, peran (chip: Administrator, Supervisor, Agen), status (Aktif/Nonaktif), terakhir login, aksi.
- Modal/drawer "Tambah Pengguna": nama, email, peran, **matriks akses per nomor** (baris = nomor, kolom = Tidak ada / Lihat / Agen / Admin, radio), tombol Simpan; contoh error "Email sudah digunakan".

### MK-11 Log Audit
- Filter: pelaku, jenis aksi (login, ambil alih, ubah pengaturan, ubah akses, tautkan nomor), rentang tanggal.
- Tabel: waktu, pelaku, aksi, entitas, ringkasan, IP.
- Drawer detail baris terpilih: before/after perubahan (dua kolom).

## Deskripsi singkat untuk laporan (akan dipakai di bawah tiap gambar)
- **MK-01**: Halaman masuk dengan email dan kata sandi; menampilkan pesan galat ketika kredensial salah.
- **MK-02**: Ringkasan kinerja per nomor: percakapan masuk, waktu balas pertama, belum dibalas, konversi, grafik volume, serta kesehatan nomor.
- **MK-03**: Kotak masuk omnichannel tiga kolom; jawaban AI tampil dengan nilai keyakinan dan sumber, agen dapat mengambil alih dan menyelesaikan percakapan, panel kanan memuat data calon siswa, skor prioritas, dan jejak keputusan AI.
- **MK-04**: Papan prospek per tahap dengan skor prioritas berwarna; detail kartu memuat rincian skor, riwayat aktivitas, dan form tindak lanjut.
- **MK-05**: Daftar kontak calon siswa dengan pencarian, filter, dan form ubah data.
- **MK-06**: Pengelolaan nomor WhatsApp: status sesi, mode AI, kesehatan nomor, dan penautan melalui kode QR.
- **MK-07**: Pengelolaan artikel basis pengetahuan per kategori beserta uji pencarian.
- **MK-08**: Pengaturan penyedia AI, ambang keyakinan, kata kunci eskalasi, batas anti-ban, dan konsol uji keputusan.
- **MK-09**: Pemantauan antrean pesan keluar beserta keputusan anti-ban dan daftar insiden pada Pusat Risiko.
- **MK-10**: Pengelolaan pengguna, peran, dan matriks akses per nomor WhatsApp.
- **MK-11**: Penelusuran log audit dengan filter dan detail perubahan.
