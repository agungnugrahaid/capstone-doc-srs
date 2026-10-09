# DRAFT: Laporan Capstone Project Kelompok 1

> Gambar final diagram (Visual Paradigm CE 18) ada di `doc-srs/diagram/png/` dan proyeknya di `doc-srs/diagram/SAPA.vpp`.
>
> Draft untuk direviu sebelum dibuat menjadi `.docx` final. Bagian bertanda **[ISI: …]** wajib dilengkapi tim (data yang tidak tersedia di dokumen/chat). Semua diagram di draft ini berupa **spesifikasi**; gambar finalnya dibuat di Visual Paradigm dengan gaya contoh mata kuliah ANSI.

---

## SAMPUL

**LAPORAN CAPSTONE PROJECT**
**SAPA: Sistem Asisten Pelanggan dan Akuisisi**
Chatbot WhatsApp Omnichannel Berbasis Kecerdasan Artifisial dan CRM pada Bimbingan Belajar Asentra

Disusun Oleh Kelompok 1:

| Nama | NIM | Peran |
|---|---|---|
| Rifqi Adhi Saputra | 231210019 | System Designer |
| Isnaini Anggista Damayanti | 241220006 | System Developer |
| Enrico Yuda Dwinata | 241220073 | System Analyst |
| Yordan Gabriell | 241220049 | Project Manager |
| Agung Nugraha Eka Saputra | 241220055 | System Developer |

PROGRAM STUDI SISTEM INFORMASI, FAKULTAS TEKNOLOGI INFORMASI, UNIVERSITAS MERCU BUANA YOGYAKARTA, TAHUN 2026

*(Daftar Isi, Daftar Tabel, Daftar Gambar dibuat otomatis di Word.)*

---

## BAB I PENDAHULUAN

### 1.1 Latar Belakang

Perkembangan teknologi informasi telah mengubah cara organisasi melayani pelanggannya. Aplikasi pesan instan seperti WhatsApp kini bukan sekadar alat komunikasi pribadi, melainkan pintu masuk utama pertanyaan dan transaksi pelanggan, khususnya pada usaha kecil dan menengah. Pelanggan memilih kanal berdasarkan kemudahan dan kecepatan, sehingga mutu kanal yang sudah dipakai lebih menentukan daripada menambah kanal baru (Wolf & Steul-Fischer, 2023). Bersamaan dengan itu, kecerdasan artifisial generatif yang dipadukan dengan teknik *retrieval-augmented generation* (RAG) memungkinkan chatbot menjawab berdasarkan dokumen resmi organisasi sehingga jawabannya dapat ditelusuri sumbernya (Fan dkk., 2024). Kombinasi kanal pesan instan, data pelanggan terpusat, dan pengukuran kinerja inilah yang mendorong lahirnya sistem informasi layanan pelanggan berbasis AI seperti yang dibangun dalam proyek ini.

Mitra proyek ini adalah Bimbingan Belajar Asentra, penyedia jasa pendidikan nonformal yang menyelenggarakan kelas eksklusif, program reguler, dan kelas persiapan tes kemampuan akademik. Asentra melayani calon siswa melalui lebih dari satu nomor WhatsApp, yaitu nomor admin dan nomor sales, tetapi tidak ada sistem yang menaungi keduanya. Akibatnya tidak ada pihak yang mengetahui berapa percakapan masuk pada tiap nomor, siapa yang menanganinya, dan percakapan mana yang belum dibalas. Semua pertanyaan mengenai jadwal, biaya, fasilitas, dan cara pendaftaran dijawab manual dari ponsel masing-masing sehingga kecepatan balasan bergantung pada siapa yang sedang memegang nomor. Informasi program dan jadwal hanya beredar sebagai kartu gambar di percakapan, sehingga admin menjawab pertanyaan yang sama berulang kali. Percakapan tersimpan terpisah di beberapa perangkat tanpa riwayat terpusat maupun hak akses per nomor, data calon siswa tidak pernah tercatat, tindak lanjut bergantung pada ingatan, dan peluang pendaftaran hilang tanpa terdeteksi.

Untuk menjawab permasalahan tersebut dibangun SAPA (Sistem Asisten Pelanggan dan Akuisisi), aplikasi web yang menautkan beberapa nomor WhatsApp milik Asentra melalui pemindaian kode QR dan menyatukan seluruh percakapan dalam satu kotak masuk omnichannel. SAPA menjawab pertanyaan berulang dari basis pengetahuan resmi mitra dengan menyertakan sumber kutipan, mengenali maksud pesan, menarik data calon siswa (jenjang, kelas, mata pelajaran), dan menghitung skor prioritas tindak lanjut yang komponennya dapat dilihat. Percakapan dialihkan kepada admin ketika keyakinan AI rendah atau pelanggan memintanya. Hak akses per nomor ditegakkan di sisi server, setiap tindakan penting tercatat dalam log audit, mesin anti-ban menjaga ritme pengiriman untuk menekan risiko pembatasan nomor, dan dasbor menampilkan volume percakapan, waktu balas pertama, percakapan belum dibalas, serta konversi pendaftaran per nomor.

### 1.2 Perumusan Masalah

Rumusan masalah yang dapat didefinisikan dalam *software project* ini adalah sebagai berikut.

1. Bagaimana merancang sistem informasi yang menyatukan beberapa nomor WhatsApp milik Bimbingan Belajar Asentra ke dalam satu kotak masuk omnichannel sehingga seluruh percakapan dan data calon siswa terpusat?
2. Bagaimana membangun pemantauan per nomor WhatsApp yang menampilkan volume percakapan, waktu balas pertama, percakapan belum dibalas, dan konversi menjadi pendaftaran?
3. Bagaimana menerapkan kecerdasan artifisial yang menjawab pertanyaan berdasarkan basis pengetahuan resmi, mengenali maksud pesan, menarik data calon siswa, dan menentukan prioritas tindak lanjut secara dapat dipertanggungjawabkan?
4. Bagaimana menerapkan kontrol akses berbasis peran sehingga setiap pengguna hanya dapat melihat dan membalas percakapan pada nomor WhatsApp yang menjadi tanggung jawabnya?
5. Bagaimana menjaga kelayakan operasional pengiriman pesan pada kanal WhatsApp tidak resmi, termasuk pengelolaan risiko pembatasan nomor dan pelindungan data pribadi calon siswa?

### 1.3 Manfaat Aplikasi

Manfaat aplikasi ini secara umum adalah memberi Bimbingan Belajar Asentra satu sumber kebenaran untuk seluruh percakapan calon siswa, sekaligus bukti terukur bahwa kualitas layanan dapat dievaluasi, bukan sekadar diingat.

Adapun manfaat secara khusus di antaranya adalah sebagai berikut.

1. Pertanyaan berulang dijawab otomatis dari basis pengetahuan resmi sehingga admin dan sales dapat berfokus pada percakapan yang membutuhkan manusia.
2. Setiap calon siswa otomatis tercatat sebagai kontak dan prospek lengkap dengan tahap tindak lanjut dan skor prioritas yang dapat dijelaskan, sehingga peluang pendaftaran tidak hilang.
3. Pengelola memperoleh pemantauan per nomor: volume percakapan, waktu balas pertama, percakapan belum dibalas, dan konversi pendaftaran.
4. Hak akses per nomor menegakkan pembagian kerja admin dan sales, sementara log audit memungkinkan penelusuran setiap perubahan pengaturan dan tindakan penting.
5. Risiko pembatasan nomor WhatsApp ditekan melalui penilaian pesan sebelum dikirim, batas laju bertingkat, pemanasan nomor, dan rencana pemulihan insiden.
6. Data pribadi calon siswa dikelola seperlunya dengan akses terbatas, sejalan dengan UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi.

---

## BAB II TINJAUAN PUSTAKA DAN LANDASAN TEORI

### 2.1 Tinjauan Pustaka

Tinjauan sistematis terhadap 40 publikasi empiris menelaah pengalaman pelanggan saat berinteraksi dengan chatbot layanan pelanggan (Nicolescu & Tudorache, 2022). Faktor pengalaman pelanggan dikelompokkan menjadi faktor yang melekat pada chatbot (fitur fungsional, fitur sistem, dan fitur antropomorfik), pada pelanggan, dan pada konteks pemakaian. Kombinasi faktor tersebut membentuk persepsi positif atau negatif yang kemudian menentukan niat dan perilaku pelanggan terhadap teknologi maupun perusahaan.

Chatbot AI yang terhubung dengan WhatsApp telah dibangun untuk konsultasi dan penjualan rakitan komputer di Toko Micro Batam; jawaban yang bersumber dari data produk membuat layanan lebih cepat, menurunkan beban staf, dan membuat pertanyaan tetap terjawab di luar jam operasional (Prasetyo dkk., 2025). Chatbot WhatsApp juga dirancang sebagai solusi layanan informasi karena pelanggan menilai informasi yang diterima tidak memadai dan jawaban petugas lambat; hasil uji *black box* dan kuesioner kepuasan menunjukkan rata-rata akurasi 98,6 persen (Puspitasari, 2025).

Pada sisi teknik penjawaban, metode RAG diterapkan untuk meningkatkan akurasi jawaban chatbot layanan pelanggan (Dhaman dkk., 2025), dan chatbot WhatsApp berbasis RAG dan OpenAI dikembangkan untuk menjawab pertanyaan dari dokumen aturan organisasi (Imaduddin dkk., 2026). Keduanya menunjukkan bahwa menambatkan jawaban pada dokumen resmi merupakan cara utama menekan jawaban yang tidak berdasar. Dari sisi kanal, tinjauan atas 128 makalah mengurai 66 faktor pemilihan kanal ke dalam lima kategori; karakteristik kanal yang dipersepsikan, kebutuhan pelanggan, dan faktor situasional memengaruhi pilihan kanal secara langsung (Wolf & Steul-Fischer, 2023).

Penelitian ini fokus pada celah yang belum dibahas penelitian di atas, yaitu menyatukan beberapa nomor WhatsApp dalam satu basis data, menegakkan kontrol akses per nomor, menyediakan pemantauan per kanal, dan mengendalikan risiko pembatasan nomor, tanpa mengganti nomor yang sudah dipakai mitra dan tanpa biaya per percakapan.

### 2.2 Landasan Teori

> Semua sumber Landasan Teori terbit 2021–2026 (≤ 5 tahun), ber-ISBN/ISSN, dan DOI-nya sudah diverifikasi lewat Crossref.

#### 2.2.1 Kanal Pesan Instan dan Layanan Omnichannel
Omnichannel adalah pendekatan layanan yang menyatukan berbagai titik kontak sehingga pelanggan mendapat pengalaman yang konsisten di kanal mana pun. Pemilihan kanal dipengaruhi karakteristik kanal yang dipersepsikan, kebutuhan pelanggan, dan faktor situasional, sehingga organisasi sebaiknya memperbaiki mutu kanal yang sudah dipakai pelanggannya (Wolf & Steul-Fischer, 2023). Pada SAPA, seluruh nomor WhatsApp mitra diperlakukan sebagai satu kanal layanan dengan satu kotak masuk dan satu riwayat percakapan.

#### 2.2.2 Chatbot dan Retrieval-Augmented Generation (RAG)
Chatbot adalah program yang melayani percakapan dengan manusia menggunakan bahasa alami. RAG menggabungkan model bahasa besar dengan pengambilan dokumen dari sumber pengetahuan eksternal sehingga jawaban dapat diperbarui tanpa melatih ulang model dan dapat dilacak asalnya, sekaligus mengurangi halusinasi (Fan dkk., 2024). Penerapan RAG pada layanan informasi sekolah terbukti membantu menjawab pertanyaan berulang berdasarkan dokumen resmi institusi (Elysia & Herianto, 2024).

#### 2.2.3 Klasifikasi Maksud dan Skor Prioritas Prospek (Lead Scoring)
Lead scoring adalah pemberian nilai pada setiap calon pelanggan untuk menentukan siapa yang ditindaklanjuti lebih dahulu. Pendekatan berbasis kecerdasan artifisial membedakan prospek "dingin" dan "panas" berdasarkan data perilaku, bukan tebakan pemasar (Jadli dkk., 2023). Model skor yang transparan membantu tim penjualan memprioritaskan prospek dengan peluang konversi tertinggi (González-Flores dkk., 2025). SAPA menghitung skor dari lima komponen berbobot yang ditampilkan agar dapat diperiksa admin.

#### 2.2.4 Customer Relationship Management (CRM)
CRM adalah strategi inti bisnis yang memadukan proses dan fungsi internal dengan jaringan eksternal untuk menciptakan dan memberikan nilai kepada pelanggan sasaran secara menguntungkan, ditopang data pelanggan yang berkualitas dan teknologi informasi (Prior dkk., 2024). CRM operasional pada SAPA berwujud kartu prospek, tahapan tindak lanjut, dan catatan aktivitas.

#### 2.2.5 Role-Based Access Control (RBAC)
RBAC adalah model kendali akses yang memberikan izin kepada peran, bukan langsung kepada pengguna, sehingga pengelolaan hak akses cukup dilakukan dengan menetapkan peran (Sahyudi & Susanto, 2025). Analisis empiris sistem kendali akses menunjukkan bahwa kesalahan konfigurasi izin merupakan sumber utama celah keamanan sehingga izin perlu ditegakkan dan diaudit secara konsisten (Parkinson & Khan, 2022). SAPA menerapkan RBAC berlapis: peran pengguna dan level akses per nomor WhatsApp.

#### 2.2.6 Unified Modeling Language (UML)
UML adalah bahasa pemodelan visual standar untuk menspesifikasikan, menggambarkan, dan mendokumentasikan sistem berorientasi objek. Diagram yang lazim dipakai dalam perancangan sistem informasi adalah use case diagram, activity diagram, sequence diagram, dan class diagram (Purnasari dkk., 2022; Narulita dkk., 2024).

#### 2.2.7 Extreme Programming (XP)
XP adalah metode pengembangan perangkat lunak dalam keluarga Agile yang menekankan iterasi pendek, rilis kecil, keterlibatan pengguna, dan pengujian berkelanjutan melalui tahapan *planning*, *design*, *coding*, dan *testing* (Tjahyanti, 2023). XP cocok untuk proyek dengan kebutuhan yang dapat berubah dan tim kecil (Irawan & Fahmi, 2025).

#### 2.2.8 Pelindungan Data Pribadi
Nomor telepon, isi percakapan, dan keterangan pribadi termasuk data pribadi yang pemrosesannya wajib memiliki dasar yang sah, terbatas pada tujuan, dan dilindungi dari akses tidak sah (Undang-Undang Republik Indonesia Nomor 27 Tahun 2022).

---

## BAB III METODOLOGI

### 3.1 Bahan

Bahan pembangunan aplikasi adalah data operasional Bimbingan Belajar Asentra yang dikumpulkan pada tahap elisitasi kebutuhan. Basis data aplikasi dimulai kosong tanpa data contoh, dan seluruh contoh percakapan dalam laporan ini dianonimkan.

**Tabel 3.1 Profil Mitra**

| Aspek | Keterangan |
|---|---|
| Nama mitra | Bimbingan Belajar Asentra |
| Bidang usaha | Jasa pendidikan nonformal (bimbingan belajar) |
| Layanan | Kelas eksklusif, program reguler, dan kelas persiapan tes kemampuan akademik |
| Alamat | Grasak, Gondang, Kec. Gondang, Kabupaten Sragen, Jawa Tengah 57254 |
| Tahun berdiri | 2024 |
| Jumlah siswa aktif | 128 siswa |
| Jumlah pengajar / staf | 24 pengajar, 1 admin, 2 sales |
| Jenjang yang dilayani | Pra-sekolah (preschool), SD, SMP, dan SMA |
| Kanal layanan saat ini | Lebih dari satu nomor WhatsApp: nomor admin dan nomor sales sebagai jalur konversi |
| Pengelola / narasumber | Greta (Owner) |
| Kondisi sebelum sistem | Pertanyaan dijawab manual dari ponsel masing-masing; percakapan terpisah per perangkat; data calon siswa tidak tercatat; tidak ada pemantauan per nomor |
| Kebutuhan utama | Kotak masuk terpadu, jawaban otomatis dari katalog resmi, pencatatan calon siswa, hak akses per nomor, pemantauan kinerja |

**Tabel 3.2 Data yang Diolah Sistem**

| No | Data | Rincian | Sumber | Kegunaan dalam sistem |
|---|---|---|---|---|
| 1 | Katalog program | Jenjang, mata pelajaran, durasi pertemuan, kapasitas kelas, jadwal, biaya | Wawancara mitra | Sumber jawaban AI (FTS5) |
| 2 | Basis pengetahuan (FAQ) | Jam operasional, fasilitas, cara pendaftaran, program persiapan tes | Wawancara mitra | Sumber jawaban AI beserta kutipan |
| 3 | Percakapan WhatsApp | Nomor pengirim, nomor tujuan, isi pesan, waktu, status penanganan | Gerbang WhatsApp Web | Kotak masuk, riwayat, pengukuran |
| 4 | Data calon siswa | Nama, nomor WhatsApp, jenjang, kelas, mata pelajaran, sumber, tahap tindak lanjut | Ekstraksi otomatis + input agen | Kontak, kartu prospek, skor prioritas |
| 5 | Pengguna & nomor WhatsApp | Akun, peran, akses per nomor, status nomor | Pengaturan Administrator | RBAC dan pemantauan |
| 6 | Metrik harian per nomor | Volume, balasan AI/manusia, belum dibalas, waktu balas pertama, konversi | Perhitungan sistem | Dasbor |
| 7 | Log audit | Pelaku, aksi, entitas, waktu, detail | Setiap tindakan penting | Penelusuran perubahan |

**Tabel 3.3 Komponen Kecerdasan Artifisial dan Cara Pengujiannya**

| No | Komponen | Bentuk teknis | Target uji |
|---|---|---|---|
| 1 | Jawab otomatis dari basis pengetahuan | Pencarian FTS5 (bm25) + penyusun jawaban; setiap jawaban menyertakan sumber | 50 pertanyaan uji, laju halusinasi < 5% |
| 2 | Klasifikasi maksud & ekstraksi data | Pengenalan maksud pesan dan entitas (nama, jenjang, kelas, mapel) | F1 per kelas maksud |
| 3 | Skor prioritas prospek | Lima komponen berbobot, rincian tampil di panel pelanggan | Presisi 20 prospek teratas |
| 4 | Ringkasan & draf balasan | Ringkasan percakapan untuk agen | Penilaian agen |
| 5 | Eskalasi ke manusia | Ambang keyakinan, kata kunci eskalasi, nada pesan | Percakapan dialihkan & AI berhenti membalas |

*Seluruh angka uji adalah target pengukuran, bukan klaim hasil.*

### 3.2 Alat

**Tabel 3.4 Perangkat Keras**

| No | Perangkat | Spesifikasi | Fungsi |
|---|---|---|---|
| 1 | Laptop pengembang 1 (Agung) | Apple MacBook Air (M1, 2020); prosesor Apple M1 8-core CPU (4 performance + 4 efficiency), GPU 7/8-core; RAM 8 GB unified memory; SSD 256 GB; layar 13,3" 2560×1600; macOS 27 | Pengembangan backend, gerbang WhatsApp, pengujian |
| 2 | PC pengembang 2 (Rifqi) | PC Windows; prosesor AMD Ryzen 5 5600G; RAM 16 GB; penyimpanan NVMe 512 GB | Pemodelan sistem (Visual Paradigm) |
| 3 | Laptop pengembang 3 (Enrico) | HP-NI97MBHI; prosesor AMD Ryzen 5 2500U; RAM 8 GB; GPU AMD Radeon Vega 8; SSD 128 GB; Windows 11 | Rancangan antarmuka (Figma) |
| 4 | Laptop pengembang 4 (Yordan) | Apple MacBook Air M4; prosesor Apple M4 10-core CPU (4 performance + 6 efficiency); RAM 16 GB; SSD 256 GB; macOS 15.6.1 | Manajemen proyek, integrasi AI |
| 5 | Laptop pengembang 5 (Isnaini) | Acer Aspire A514-51KG; prosesor Intel Core i3-7020U @ 2,30 GHz; RAM 12 GB; SSD 237 GB + HDD ±929 GB; Windows 10 64-bit | Pengembangan & dokumentasi |
| 6 | Ponsel Android uji | TECNO Pova 7 4G (RAM 8 GB, penyimpanan 256 GB); Android 15; WhatsApp versi terbaru; kamera untuk pindai QR | Menautkan nomor WhatsApp melalui pemindaian QR |
| 7 | Nomor WhatsApp uji | 1 nomor cadangan (bukan nomor operasional mitra) | Pengujian kirim/terima tanpa risiko pada nomor mitra |
| 8 | Server / VPS | 2 vCPU (AMD EPYC 9754 128-Core); RAM 2 GB (+ swap 2 GB); penyimpanan SSD 40 GB; Ubuntu 24.04.4 LTS (x86_64) | Menjalankan aplikasi dan gerbang WhatsApp 24 jam |
| 9 | Koneksi internet | Kecepatan lebih dari 10 Mbps | Sesi WhatsApp Web dan pemanggilan API AI |

**Tabel 3.5 Perangkat Lunak**

| No | Perangkat lunak | Versi | Fungsi |
|---|---|---|---|
| 1 | Node.js | 22 LTS atau lebih baru | Runtime server |
| 2 | Express | 5 | Kerangka REST API |
| 3 | SQLite (modul `node:sqlite`) + FTS5 | bawaan Node.js 22 | Basis data dan pencarian teks penuh |
| 4 | React | 19 | Antarmuka pengguna |
| 5 | Vite | 8.3 | Build tool antarmuka |
| 6 | Tailwind CSS | 4 | Gaya antarmuka |
| 7 | @whiskeysockets/baileys | 6.17.16 | Gerbang WhatsApp Web multi-nomor (QR) |
| 8 | Penyedia AI | Mode aturan bawaan / OpenAI / kompatibel OpenAI / Gemini | Klasifikasi maksud & penyusunan jawaban; kunci API terenkripsi AES-256-GCM |
| 9 | Visual Studio Code | 1.140.0 | Editor kode |
| 10 | Git & GitHub | - | Kontrol versi, branch, dan peninjauan kode |
| 11 | Visual Paradigm Community Edition | 18.0 | Pemodelan UML |
| 12 | Figma | - | Mockup *high-fidelity* dan prototipe |
| 13 | Microsoft Word + Mendeley Reference Manager | - | Penyusunan laporan dan sitasi |
| 14 | Google Chrome | versi terbaru | Pengujian antarmuka |

### 3.3 Analisis Kebutuhan

**Tabel 3.6 Aktor Sistem**

| Aktor | Keterangan | Hak akses |
|---|---|---|
| Pelanggan | Calon siswa / orang tua yang menghubungi nomor WhatsApp Asentra | Tidak login; berinteraksi lewat WhatsApp |
| Agen/CS | Admin dan sales Asentra yang membalas percakapan | Hanya nomor yang ditugaskan |
| Supervisor | Pengelola Asentra yang memantau kinerja layanan | Semua nomor (baca), basis pengetahuan, log audit |
| Administrator | Pengelola sistem | Seluruh fitur, termasuk nomor WhatsApp, pengaturan AI, tim & akses |
| WhatsApp Web (sekunder) | Layanan WhatsApp yang dihubungkan melalui Baileys | Menerima/mengirim pesan |
| Penyedia AI (sekunder) | Layanan model bahasa (opsional) | Dipanggil untuk menyusun jawaban |

**Tabel 3.7 Kebutuhan Fungsional**

| Kode | Kebutuhan | UC |
|---|---|---|
| FR-01 | Sistem menyediakan login dengan email dan kata sandi serta mengarahkan pengguna sesuai peran | UC-01 |
| FR-02 | Sistem menerima pesan dari semua nomor WhatsApp yang tertaut dan menyimpannya dalam satu basis data | UC-02 |
| FR-03 | Sistem otomatis membuat kontak dan prospek untuk nomor pengirim baru | UC-02 |
| FR-04 | Sistem menjawab otomatis dari basis pengetahuan disertai sumber dan nilai keyakinan | UC-03 |
| FR-05 | Sistem mengalihkan percakapan ke agen bila keyakinan rendah, ada kata kunci eskalasi, atau nada marah | UC-03 |
| FR-06 | Sistem menilai setiap pesan keluar dengan mesin anti-ban (kirim/tunda/tahan) | UC-03, UC-04 |
| FR-07 | Agen dapat membaca, membalas, mengambil alih, dan menyelesaikan percakapan pada nomor yang diizinkan | UC-04 |
| FR-08 | Agen dapat mengelola tahap prospek, catatan aktivitas, dan tindak lanjut; skor prioritas tampil beserta rinciannya | UC-05 |
| FR-09 | Agen dapat mencari dan memperbarui data kontak | UC-06 |
| FR-10 | Sistem menampilkan dasbor per nomor: volume, waktu balas pertama, belum dibalas, konversi | UC-07 |
| FR-11 | Administrator dapat menautkan, memantau, dan memutus nomor WhatsApp melalui kode QR | UC-08 |
| FR-12 | Supervisor/Administrator dapat mengelola artikel basis pengetahuan | UC-09 |
| FR-13 | Administrator dapat mengatur penyedia AI, ambang keyakinan, kata kunci eskalasi, batas anti-ban, dan menguji keputusan AI | UC-10 |
| FR-14 | Administrator dapat mengelola pengguna, peran, dan akses per nomor | UC-11 |
| FR-15 | Sistem mencatat log audit setiap tindakan penting dan menampilkannya dengan filter | UC-12 |

**Tabel 3.8 Kebutuhan Non-Fungsional**

| Kode | Kebutuhan |
|---|---|
| NFR-01 | Hak akses per nomor ditegakkan di sisi server pada setiap permintaan API |
| NFR-02 | Kunci API penyedia AI disimpan terenkripsi AES-256-GCM; kata sandi disimpan sebagai hash |
| NFR-03 | Satu nomor terputus tidak menghentikan nomor lain; antrean pesan keluar tetap tersimpan |
| NFR-04 | Balasan bot < 5 detik untuk 90% pesan (di luar waktu pemanggilan model) |
| NFR-05 | Tidak ada pesan promosi massal; bot hanya membalas percakapan yang dimulai pelanggan |
| NFR-06 | Antarmuka berbahasa Indonesia dan responsif |
| NFR-07 | Data pribadi diproses sesuai UU No. 27 Tahun 2022 |

### 3.4 Pemodelan

#### 3.4.1 Use Case Diagram

![Use Case Diagram SAPA](../diagram/png/Use%20Case%20Diagram%20SAPA.png)

**Spesifikasi gambar (Gambar 3.1 Use Case Diagram SAPA)**: gaya ANSI: aktor di kiri, aktor sekunder di kanan, kotak sistem "Sistem Asisten Pelanggan dan Akuisisi (SAPA): Bimbingan Belajar Asentra", use case elips biru muda, Login di kanan, panah putus-putus `<<Include>>` dari use case **menuju** Login.

| Aktor | Use case yang terhubung |
|---|---|
| Pelanggan | UC-02 Mengirim Pesan WhatsApp |
| Agen/CS | UC-04 Mengelola Percakapan, UC-05 Mengelola Prospek, UC-06 Mengelola Kontak Pelanggan |
| Supervisor | UC-07 Melihat Dasbor Pemantauan, UC-09 Mengelola Basis Pengetahuan, UC-12 Melihat Log Audit |
| Administrator | UC-07, UC-08 Mengelola Nomor WhatsApp, UC-09, UC-10 Mengatur AI & Anti-ban, UC-11 Mengelola Tim & Hak Akses, UC-12 |
| WhatsApp Web (kanan) | UC-03 Menjawab Pesan Otomatis dengan AI |
| Penyedia AI (kanan) | UC-03 |

Relasi: UC-04 s.d. UC-12 `<<Include>>` → UC-01 Login. UC-02 `<<Include>>` → UC-03. UC-02 dan UC-03 **tidak** meng-include Login (pelanggan tidak login; UC-03 dijalankan sistem).

#### 3.4.2 Use Case Description

Format setiap tabel mengikuti contoh ANSI: Nama Use Case, Nomor Use Case, Aktor, Deskripsi Singkat, Pre Condition, Basic Flow of Event (kolom Aktor | Sistem), Post Condition, Alternative Flow, Error Condition.

---

**UC-01: Login**

| Elemen | Isi |
|---|---|
| Nama Use Case | Login |
| Nomor Use Case | UC-01 |
| Aktor | Agen/CS, Supervisor, Administrator |
| Deskripsi Singkat | Pengguna memasukkan email dan kata sandi untuk masuk ke SAPA sesuai peran dan nomor WhatsApp yang menjadi aksesnya. |
| Pre Condition | Pengguna memiliki akun berstatus aktif yang dibuat Administrator dan berada di halaman Login. |
| Post Condition | Pengguna masuk, sesi aktif, dan menu yang tampil sesuai peran. |
| Alternative Flow | A-1. Pada langkah 4, jika akun berstatus nonaktif, sistem menampilkan "Akun Anda dinonaktifkan, hubungi Administrator". |
| Error Condition | Email atau kata sandi salah: sistem menampilkan "Email atau kata sandi salah" dan meminta pengguna mengisi ulang; setelah 5 kali gagal, login ditahan 5 menit. |

| Aktor | Sistem |
|---|---|
| 1. Membuka halaman Login. | |
| | 2. Menampilkan form email dan kata sandi. |
| 3. Mengisi email dan kata sandi, lalu menekan tombol "Masuk". | |
| | 4. Memvalidasi kredensial ke data pengguna. |
| | 5. Mengambil peran dan daftar nomor WhatsApp yang boleh diakses. |
| | 6. Mencatat log audit login dan menampilkan halaman awal sesuai peran (Dasbor untuk Supervisor/Administrator, Kotak Masuk untuk Agen/CS). |

---

**UC-02: Mengirim Pesan WhatsApp**

| Elemen | Isi |
|---|---|
| Nama Use Case | Mengirim Pesan WhatsApp |
| Nomor Use Case | UC-02 |
| Aktor | Pelanggan |
| Deskripsi Singkat | Pelanggan mengirim pertanyaan ke salah satu nomor WhatsApp Asentra; pesan diterima gerbang, dicatat, lalu dibalas melalui UC-03. |
| Pre Condition | Nomor WhatsApp Asentra yang dituju berstatus tersambung di SAPA. |
| Post Condition | Pesan tersimpan, kontak dan prospek tercatat, percakapan tampil di Kotak Masuk, dan pelanggan menerima balasan. |
| Alternative Flow | A-1. Pada langkah 5, jika percakapan sedang ditangani manusia, sistem tidak memanggil AI, menandai percakapan "belum dibalas", dan memberi tanda pada Kotak Masuk agen. |
| Error Condition | Nomor tujuan terputus: pesan tidak diterima sistem dan status nomor tampil "terputus" pada halaman Nomor WhatsApp. |

| Aktor | Sistem |
|---|---|
| 1. Mengirim pesan ke nomor WhatsApp Asentra. | |
| | 2. Menerima pesan masuk melalui gerbang WhatsApp Web. |
| | 3. Mencari kontak berdasarkan nomor pengirim; bila belum ada, membuat kontak baru dan prospek bertahap "baru". |
| | 4. Membuka atau memperbarui percakapan dan menyimpan pesan. |
| | 5. Menjalankan UC-03 Menjawab Pesan Otomatis dengan AI. |
| 6. Menerima balasan di aplikasi WhatsApp. | |

---

**UC-03: Menjawab Pesan Otomatis dengan AI**

| Elemen | Isi |
|---|---|
| Nama Use Case | Menjawab Pesan Otomatis dengan AI |
| Nomor Use Case | UC-03 |
| Aktor | Pelanggan (penerima), WhatsApp Web, Penyedia AI |
| Deskripsi Singkat | Sistem mengenali maksud pesan, menarik data calon siswa, mencari jawaban di basis pengetahuan, menghitung keyakinan, menilai risiko anti-ban, lalu mengirim jawaban atau mengalihkan ke agen. |
| Pre Condition | Pesan masuk telah tersimpan (UC-02) dan AI aktif untuk nomor tersebut. |
| Post Condition | Balasan bersumber terkirim atau percakapan dialihkan ke agen; jejak keputusan AI tersimpan. |
| Alternative Flow | A-1. Pada langkah 5, jika keyakinan di bawah ambang, terdapat kata kunci eskalasi ("admin", "komplain"), atau nada marah, sistem mengalihkan percakapan ke agen, AI berhenti membalas, dan mengirim pesan "Pertanyaan Anda kami teruskan ke admin". A-2. Pada langkah 6, jika keputusan anti-ban "tunda" atau "tahan", pesan disimpan di antrean keluar dan dicatat di Pusat Risiko. |
| Error Condition | Penyedia AI gagal/timeout: sistem beralih ke mode aturan bawaan. Tidak ada artikel yang relevan: percakapan dialihkan ke agen. |

| Aktor | Sistem |
|---|---|
| | 1. Mengklasifikasi maksud pesan dan mengekstrak entitas (nama, jenjang, kelas, mata pelajaran). |
| | 2. Memperbarui data kontak dan menghitung ulang skor prioritas prospek. |
| | 3. Mencari artikel basis pengetahuan yang relevan (FTS5). |
| Penyedia AI: 4. Menyusun jawaban dari artikel terpilih. | |
| | 5. Menghitung nilai keyakinan dan membandingkannya dengan ambang serta kata kunci eskalasi. |
| | 6. Menilai pesan keluar dengan mesin anti-ban dan memasukkannya ke antrean keluar. |
| WhatsApp Web: 7. Mengirim balasan beserta sumber ke pelanggan. | |
| | 8. Mencatat jejak keputusan AI dan metrik harian. |

---

**UC-04: Mengelola Percakapan**

| Elemen | Isi |
|---|---|
| Nama Use Case | Mengelola Percakapan |
| Nomor Use Case | UC-04 |
| Aktor | Agen/CS |
| Deskripsi Singkat | Agen melihat percakapan dari nomor yang menjadi tanggung jawabnya, membaca jawaban AI beserta sumbernya, membalas, mengambil alih, atau menyelesaikan percakapan. |
| Pre Condition | Agen telah login (include UC-01) dan memiliki akses minimal satu nomor WhatsApp. |
| Post Condition | Balasan terkirim, status percakapan dan metrik waktu balas diperbarui, log audit tercatat. |
| Alternative Flow | A-1. Pada langkah 5, agen menekan "Selesaikan"; sistem mengubah status percakapan menjadi selesai. A-2. Agen menekan "Kembalikan ke AI"; sistem mengaktifkan kembali balasan AI untuk percakapan tersebut. |
| Error Condition | Agen membuka percakapan nomor yang tidak diizinkan: sistem menolak dengan "Anda tidak memiliki akses ke nomor ini". Pesan ditahan anti-ban: sistem menampilkan "Pesan ditunda oleh pengaman pengiriman". |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Kotak Masuk. | |
| | 2. Menampilkan daftar percakapan dari nomor yang diizinkan, diurutkan dari yang belum dibalas. |
| 3. Memilih satu percakapan. | |
| | 4. Menampilkan riwayat pesan, jawaban AI dan sumbernya, panel data pelanggan, serta jejak keputusan AI. |
| 5. Menekan "Ambil alih", mengetik balasan, lalu menekan "Kirim". | |
| | 6. Menghentikan AI untuk percakapan ini, menilai pesan dengan anti-ban, dan mengirim balasan melalui antrean keluar. |
| | 7. Memperbarui status percakapan, metrik waktu balas pertama, dan mencatat log audit. |

---

**UC-05: Mengelola Prospek**

| Elemen | Isi |
|---|---|
| Nama Use Case | Mengelola Prospek |
| Nomor Use Case | UC-05 |
| Aktor | Agen/CS |
| Deskripsi Singkat | Agen memantau calon siswa per tahap (baru, dihubungi, tertarik, penawaran, daftar, batal), melihat skor prioritas beserta rinciannya, memindahkan tahap, dan mencatat aktivitas tindak lanjut. |
| Pre Condition | Agen telah login (include UC-01); terdapat prospek pada nomor yang diizinkan. |
| Post Condition | Tahap prospek, catatan aktivitas, dan jadwal tindak lanjut tersimpan. |
| Alternative Flow | A-1. Pada langkah 5, jika prospek dipindah ke "daftar", sistem menambah hitungan konversi pada metrik harian. |
| Error Condition | Catatan aktivitas kosong: sistem menampilkan "Catatan wajib diisi". |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Prospek. | |
| | 2. Menampilkan papan prospek per tahap, diurutkan berdasarkan skor prioritas. |
| 3. Memilih kartu prospek. | |
| | 4. Menampilkan detail prospek, rincian lima komponen skor, riwayat aktivitas, dan tautan ke percakapan. |
| 5. Mengubah tahap, menambah catatan aktivitas, dan menetapkan tanggal tindak lanjut, lalu menekan "Simpan". | |
| | 6. Memvalidasi dan menyimpan perubahan, menghitung ulang skor, dan mencatat log audit. |

---

**UC-06: Mengelola Kontak Pelanggan**

| Elemen | Isi |
|---|---|
| Nama Use Case | Mengelola Kontak Pelanggan |
| Nomor Use Case | UC-06 |
| Aktor | Agen/CS |
| Deskripsi Singkat | Agen mencari dan memperbarui data kontak calon siswa (nama, jenjang, kelas, mata pelajaran, kota, sumber, label). |
| Pre Condition | Agen telah login (include UC-01). |
| Post Condition | Data kontak terbaru tersimpan dan dipakai oleh AI serta skor prospek. |
| Alternative Flow | A-1. Pada langkah 3, jika kontak tidak ditemukan, sistem menampilkan "Kontak tidak ditemukan". |
| Error Condition | Format nomor WhatsApp tidak valid atau nomor sudah terdaftar: sistem menolak penyimpanan dan menandai kolom yang salah. |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Kontak dan mengetik kata kunci pencarian. | |
| | 2. Menampilkan daftar kontak yang sesuai. |
| 3. Memilih kontak, lalu menekan "Ubah". | |
| | 4. Menampilkan form data kontak beserta riwayat percakapannya. |
| 5. Memperbarui data dan menekan "Simpan". | |
| | 6. Memvalidasi data, menyimpan perubahan, dan mencatat log audit. |

---

**UC-07: Melihat Dasbor Pemantauan**

| Elemen | Isi |
|---|---|
| Nama Use Case | Melihat Dasbor Pemantauan |
| Nomor Use Case | UC-07 |
| Aktor | Supervisor, Administrator |
| Deskripsi Singkat | Pengguna memantau kinerja layanan per nomor WhatsApp: volume percakapan, waktu balas pertama, percakapan belum dibalas, balasan AI vs manusia, dan konversi pendaftaran. |
| Pre Condition | Pengguna telah login (include UC-01). |
| Post Condition | Pengguna memperoleh ringkasan kinerja layanan sesuai filter. |
| Alternative Flow | A-1. Pada langkah 3, pengguna memilih nomor tertentu atau rentang waktu (hari ini, 7 hari, 30 hari); sistem memperbarui grafik. |
| Error Condition | Tidak ada data pada periode terpilih: sistem menampilkan "Belum ada data pada periode ini". |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Dasbor. | |
| | 2. Mengambil metrik harian seluruh nomor yang diizinkan dan menampilkan kartu ringkasan, grafik volume, serta status tiap nomor. |
| 3. Memilih filter nomor dan periode. | |
| | 4. Menghitung ulang metrik sesuai filter dan menampilkan hasilnya. |

---

**UC-08: Mengelola Nomor WhatsApp**

| Elemen | Isi |
|---|---|
| Nama Use Case | Mengelola Nomor WhatsApp |
| Nomor Use Case | UC-08 |
| Aktor | Administrator |
| Deskripsi Singkat | Administrator menambah nomor WhatsApp (label, nomor, tujuan admin/sales), menautkannya dengan memindai kode QR, memantau status sesi, dan memutus nomor. |
| Pre Condition | Administrator telah login (include UC-01) dan memegang ponsel dengan nomor yang akan ditautkan. |
| Post Condition | Nomor berstatus tersambung dan pesannya masuk ke Kotak Masuk. |
| Alternative Flow | A-1. Administrator menekan "Putuskan"; sistem mengakhiri sesi dan mengubah status menjadi terputus. |
| Error Condition | Kode QR kedaluwarsa (± 60 detik): sistem menampilkan "QR kedaluwarsa" dan tombol "Buat ulang QR". Penautan gagal: status "gagal tertaut" dan dicatat di Pusat Risiko. |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Nomor WhatsApp dan menekan "Tambah Nomor". | |
| | 2. Menampilkan form label, nomor, dan tujuan nomor. |
| 3. Mengisi form dan menekan "Tautkan". | |
| | 4. Membuat sesi WhatsApp Web dan menampilkan kode QR. |
| 5. Memindai kode QR dari aplikasi WhatsApp di ponsel. | |
| | 6. Menerima konfirmasi tertaut dari WhatsApp Web, menyimpan sesi, mengubah status menjadi tersambung, dan mencatat log audit. |

---

**UC-09: Mengelola Basis Pengetahuan**

| Elemen | Isi |
|---|---|
| Nama Use Case | Mengelola Basis Pengetahuan |
| Nomor Use Case | UC-09 |
| Aktor | Supervisor, Administrator |
| Deskripsi Singkat | Pengguna menambah, mengubah, menonaktifkan, dan menguji artikel basis pengetahuan (program, jadwal, biaya, fasilitas, pendaftaran) yang menjadi sumber jawaban AI. |
| Pre Condition | Pengguna telah login (include UC-01). |
| Post Condition | Artikel tersimpan dan terindeks ulang sehingga langsung dipakai AI. |
| Alternative Flow | A-1. Pada langkah 5, pengguna menekan "Uji Pencarian" dan mengetik pertanyaan; sistem menampilkan artikel yang paling relevan beserta skornya. |
| Error Condition | Judul atau isi kosong: sistem menolak penyimpanan dan menampilkan "Judul dan isi wajib diisi". |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Basis Pengetahuan. | |
| | 2. Menampilkan daftar artikel per kategori. |
| 3. Menekan "Tambah Artikel" atau memilih artikel untuk diubah. | |
| | 4. Menampilkan form judul, kategori, isi, label, dan status aktif. |
| 5. Mengisi form dan menekan "Simpan". | |
| | 6. Memvalidasi, menyimpan artikel, mengindeks ulang FTS5, dan mencatat log audit. |

---

**UC-10: Mengatur AI dan Anti-ban**

| Elemen | Isi |
|---|---|
| Nama Use Case | Mengatur AI dan Anti-ban |
| Nomor Use Case | UC-10 |
| Aktor | Administrator |
| Deskripsi Singkat | Administrator mengatur penyedia AI, kunci API, persona, ambang keyakinan, kata kunci eskalasi, serta batas pengiriman anti-ban; menguji keputusan AI di konsol uji; dan memantau antrean keluar serta Pusat Risiko. |
| Pre Condition | Administrator telah login (include UC-01). |
| Post Condition | Pengaturan baru tersimpan dan berlaku untuk pesan berikutnya. |
| Alternative Flow | A-1. Pada langkah 5, Administrator menekan "Uji Keputusan" dan memasukkan contoh pesan; sistem menampilkan jejak keputusan (maksud, entitas, artikel, keyakinan, keputusan kirim/eskalasi). |
| Error Condition | Kunci API tidak valid: sistem menampilkan "Kunci API ditolak penyedia" dan tetap memakai pengaturan lama. Nilai batas tidak wajar (mis. negatif): ditolak dengan pesan kolom yang salah. |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Pengaturan AI. | |
| | 2. Menampilkan pengaturan AI, anti-ban, antrean keluar, dan Pusat Risiko saat ini. |
| 3. Mengubah penyedia AI, kunci API, ambang keyakinan, kata kunci eskalasi, dan batas pengiriman. | |
| 4. Menekan "Simpan". | |
| | 5. Memvalidasi nilai dan menguji koneksi penyedia AI. |
| | 6. Mengenkripsi kunci API (AES-256-GCM), menyimpan pengaturan, dan mencatat log audit. |

---

**UC-11: Mengelola Tim dan Hak Akses**

| Elemen | Isi |
|---|---|
| Nama Use Case | Mengelola Tim dan Hak Akses |
| Nomor Use Case | UC-11 |
| Aktor | Administrator |
| Deskripsi Singkat | Administrator menambah pengguna, menetapkan peran, mengatur level akses per nomor WhatsApp, dan menonaktifkan pengguna. |
| Pre Condition | Administrator telah login (include UC-01). |
| Post Condition | Akun dan hak akses tersimpan; perubahan langsung berlaku pada permintaan berikutnya. |
| Alternative Flow | A-1. Administrator menekan "Nonaktifkan"; sistem mengubah status pengguna dan mengakhiri sesinya. |
| Error Condition | Email sudah terdaftar: sistem menampilkan "Email sudah digunakan". Administrator mencoba menonaktifkan dirinya sendiri: ditolak. |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Tim & Akses. | |
| | 2. Menampilkan daftar pengguna, peran, dan akses nomor. |
| 3. Menekan "Tambah Pengguna" atau memilih pengguna. | |
| | 4. Menampilkan form nama, email, peran, dan matriks akses per nomor. |
| 5. Mengisi form, memilih level akses tiap nomor, dan menekan "Simpan". | |
| | 6. Memvalidasi, menyimpan pengguna dan akses nomor, serta mencatat log audit. |

---

**UC-12: Melihat Log Audit**

| Elemen | Isi |
|---|---|
| Nama Use Case | Melihat Log Audit |
| Nomor Use Case | UC-12 |
| Aktor | Supervisor, Administrator |
| Deskripsi Singkat | Pengguna menelusuri riwayat tindakan penting (login, perubahan pengaturan, ambil alih, perubahan akses) berdasarkan pelaku, jenis aksi, dan rentang tanggal. |
| Pre Condition | Pengguna telah login (include UC-01). |
| Post Condition | Pengguna memperoleh daftar log yang sesuai filter. |
| Alternative Flow | A-1. Pada langkah 5, pengguna memilih satu baris log; sistem menampilkan detail perubahan. |
| Error Condition | Tidak ada log sesuai filter: sistem menampilkan "Tidak ada aktivitas pada filter ini". |

| Aktor | Sistem |
|---|---|
| 1. Memilih menu Log Audit. | |
| | 2. Menampilkan log terbaru. |
| 3. Mengisi filter pelaku, jenis aksi, dan rentang tanggal. | |
| | 4. Mengambil dan menampilkan log sesuai filter. |

---

#### 3.4.3 Sequence Diagram

Notasi mengikuti contoh ANSI: bingkai `sd [SD-xx - Nama]`; lifeline Aktor → `View : …` (boundary) → `Cont : …` (control) → `Ent : …` (entity); pesan bernomor bertingkat; balasan garis putus-putus.

| SD | Lifeline | Urutan pesan |
|---|---|---|
| SD-01 Login | Pengguna, View : Login, Cont : Login, Ent : Pengguna, Ent : AksesNomor, Ent : LogAudit | 1: Isi email & kata sandi, klik Masuk → View; 1.1: login(email, kataSandi) → Cont; 1.1.1: cariPengguna(email) → Ent:Pengguna; 1.1.2: dataPengguna ⇠; 1.1.3: verifikasiKataSandi() (self); 1.1.4: ambilAksesNomor(idPengguna) → Ent:AksesNomor; 1.1.5: daftarNomor ⇠; 1.1.6: catatLog("login") → Ent:LogAudit; 1.2: tampilkanHalamanSesuaiPeran ⇠ View |
| SD-02 Mengirim Pesan WhatsApp | Pelanggan, View : WhatsAppGateway, Cont : Percakapan, Ent : Kontak, Ent : Prospek, Ent : Percakapan, Ent : Pesan, Cont : AIEngine | 1: Kirim pesan → View; 1.1: terimaPesan(nomor, isi) → Cont:Percakapan; 1.1.1: cariAtauBuatKontak(nomor) → Ent:Kontak; 1.1.2: dataKontak ⇠; 1.1.3: buatProspek("baru") → Ent:Prospek [kontak baru]; 1.1.4: bukaPercakapan(idKontak, idNomor) → Ent:Percakapan; 1.1.5: simpanPesan(masuk) → Ent:Pesan; 1.1.6: prosesBalasan(pesan) → Cont:AIEngine (UC-03); 1.1.7: balasan ⇠; 1.2: kirimBalasan(balasan) → View; 1.3: balasan diterima ⇠ Pelanggan |
| SD-03 Menjawab Pesan Otomatis dengan AI | Cont : AIEngine, Ent : Kontak, Ent : Prospek, Ent : ArtikelPengetahuan, Penyedia AI, Ent : PengaturanAI, Cont : AntiBan, Ent : AntreanKeluar, WhatsApp Web | 1: prosesBalasan(pesan) (dari Cont:Percakapan); 1.1: klasifikasiMaksud() & ekstrakEntitas() (self); 1.2: perbaruiKontak(entitas) → Ent:Kontak; 1.3: hitungSkor() → Ent:Prospek; 1.4: cariArtikel(kueri) → Ent:ArtikelPengetahuan; 1.5: artikelRelevan ⇠; 1.6: susunJawaban(artikel) → Penyedia AI; 1.7: jawaban ⇠; 1.8: ambilAmbang() → Ent:PengaturanAI; 1.9: ambang ⇠; 1.10: hitungKeyakinan() (self); 1.11: nilaiPesan(jawaban) → Cont:AntiBan; 1.11.1: simpanAntrean(keputusan) → Ent:AntreanKeluar; 1.11.2: kirimPesan() → WhatsApp Web; 1.11.3: terkirim ⇠ |
| SD-04 Mengelola Percakapan | Agen/CS, View : KotakMasuk, Cont : Percakapan, Ent : AksesNomor, Ent : Percakapan, Ent : Pesan, Cont : AntiBan, Ent : LogAudit | 1: Klik menu Kotak Masuk; 1.1: muatPercakapan(idPengguna) → Cont; 1.1.1: ambilAksesNomor() → Ent:AksesNomor; 1.1.2: ambilPercakapan(daftarNomor) → Ent:Percakapan; 1.1.3: daftarPercakapan ⇠; 1.2: tampilkanDaftar ⇠ View; 2: Pilih percakapan; 2.1: muatPesan(idPercakapan) → Cont; 2.1.1: ambilPesan() → Ent:Pesan; 2.1.2: riwayat & jejak AI ⇠; 2.2: tampilkanRiwayat ⇠; 3: Ambil alih & kirim balasan; 3.1: kirimBalasan(isi) → Cont; 3.1.1: setPenangan("manusia") → Ent:Percakapan; 3.1.2: nilaiPesan() → Cont:AntiBan; 3.1.3: keputusan ⇠; 3.1.4: simpanPesan(keluar) → Ent:Pesan; 3.1.5: catatLog("ambil alih") → Ent:LogAudit; 3.2: balasanTerkirim ⇠ View |
| SD-05 Mengelola Prospek | Agen/CS, View : Prospek, Cont : Prospek, Ent : Prospek, Ent : AktivitasProspek, Ent : LogAudit | 1: Klik menu Prospek; 1.1: muatProspek() → Cont; 1.1.1: ambilProspek() → Ent:Prospek; 1.1.2: daftarProspek ⇠; 1.2: tampilkanPapan ⇠; 2: Ubah tahap & isi catatan; 2.1: simpanPerubahan(tahap, catatan, tglTindakLanjut) → Cont; 2.1.1: validasi() (self); 2.1.2: ubahTahap() → Ent:Prospek; 2.1.3: tambahAktivitas() → Ent:AktivitasProspek; 2.1.4: hitungUlangSkor() → Ent:Prospek; 2.1.5: catatLog() → Ent:LogAudit; 2.2: tampilkanProspekTersimpan ⇠ |
| SD-06 Mengelola Kontak | Agen/CS, View : Kontak, Cont : Kontak, Ent : Kontak, Ent : LogAudit | 1: Cari kontak; 1.1: cariKontak(kataKunci) → Cont; 1.1.1: cari() → Ent:Kontak; 1.1.2: hasil ⇠; 1.2: tampilkanDaftar ⇠; 2: Ubah data & simpan; 2.1: simpanKontak(data) → Cont; 2.1.1: validasiData() (self); 2.1.2: perbarui() → Ent:Kontak; 2.1.3: catatLog() → Ent:LogAudit; 2.2: tampilkanTersimpan ⇠ |
| SD-07 Melihat Dasbor | Supervisor/Administrator, View : Dasbor, Cont : Dasbor, Ent : AksesNomor, Ent : MetrikHarian, Ent : NomorWhatsApp | 1: Klik menu Dasbor; 1.1: muatDasbor() → Cont; 1.1.1: ambilAksesNomor() → Ent:AksesNomor; 1.1.2: ambilMetrik(nomor, periode) → Ent:MetrikHarian; 1.1.3: metrik ⇠; 1.1.4: ambilStatusNomor() → Ent:NomorWhatsApp; 1.1.5: status ⇠; 1.2: tampilkanDasbor ⇠; 2: Pilih filter; 2.1: filterPeriode(nomor, periode) → Cont; 2.1.1: hitungMetrik() (self); 2.2: tampilkanHasilFilter ⇠ |
| SD-08 Mengelola Nomor WhatsApp | Administrator, View : NomorWhatsApp, Cont : NomorWA, Ent : NomorWhatsApp, WhatsApp Web, Ent : LogAudit | 1: Isi form & klik Tautkan; 1.1: tambahNomor(label, nomor, tujuan) → Cont; 1.1.1: simpanNomor("menunggu") → Ent; 1.1.2: buatSesi() → WhatsApp Web; 1.1.3: kodeQR ⇠; 1.2: tampilkanQR ⇠; 2: Pindai QR dari ponsel → WhatsApp Web; 2.1: konfirmasiTertaut → Cont; 2.1.1: ubahStatus("tersambung") → Ent; 2.1.2: catatLog() → Ent:LogAudit; 2.2: tampilkanStatusTersambung ⇠ |
| SD-09 Mengelola Basis Pengetahuan | Supervisor/Administrator, View : BasisPengetahuan, Cont : BasisPengetahuan, Ent : ArtikelPengetahuan, Ent : LogAudit | 1: Klik menu; 1.1: muatArtikel() → Cont; 1.1.1: ambilArtikel() → Ent; 1.1.2: daftarArtikel ⇠; 1.2: tampilkanDaftar ⇠; 2: Isi form & Simpan; 2.1: simpanArtikel(data) → Cont; 2.1.1: validasi() (self); 2.1.2: simpan() → Ent; 2.1.3: indeksUlangFTS() → Ent; 2.1.4: catatLog() → Ent:LogAudit; 2.2: tampilkanTersimpan ⇠ |
| SD-10 Mengatur AI & Anti-ban | Administrator, View : PengaturanAI, Cont : PengaturanAI, Penyedia AI, Ent : PengaturanAI, Ent : PengaturanAntiBan, Ent : LogAudit | 1: Klik menu; 1.1: muatPengaturan() → Cont; 1.1.1: ambil() → Ent:PengaturanAI & Ent:PengaturanAntiBan; 1.1.2: pengaturan ⇠; 1.2: tampilkanPengaturan ⇠; 2: Ubah nilai & Simpan; 2.1: simpanPengaturan(data) → Cont; 2.1.1: validasiNilai() (self); 2.1.2: ujiKoneksi(kunciAPI) → Penyedia AI; 2.1.3: koneksiOK ⇠; 2.1.4: enkripsiKunci() (self); 2.1.5: simpan() → Ent:PengaturanAI; 2.1.6: simpan() → Ent:PengaturanAntiBan; 2.1.7: catatLog() → Ent:LogAudit; 2.2: tampilkanTersimpan ⇠ |
| SD-11 Mengelola Tim & Hak Akses | Administrator, View : TimAkses, Cont : TimAkses, Ent : Pengguna, Ent : AksesNomor, Ent : LogAudit | 1: Klik menu; 1.1: muatPengguna() → Cont; 1.1.1: ambil() → Ent:Pengguna; 1.1.2: daftar ⇠; 1.2: tampilkan ⇠; 2: Isi form & Simpan; 2.1: simpanPengguna(data, akses) → Cont; 2.1.1: cekEmailUnik() → Ent:Pengguna; 2.1.2: simpan() → Ent:Pengguna; 2.1.3: simpanAkses() → Ent:AksesNomor; 2.1.4: catatLog() → Ent:LogAudit; 2.2: tampilkanTersimpan ⇠ |
| SD-12 Melihat Log Audit | Supervisor/Administrator, View : LogAudit, Cont : LogAudit, Ent : LogAudit | 1: Klik menu; 1.1: muatLog() → Cont; 1.1.1: ambilTerbaru() → Ent; 1.1.2: daftarLog ⇠; 1.2: tampilkan ⇠; 2: Isi filter; 2.1: filterLog(pelaku, aksi, tanggal) → Cont; 2.1.1: cari() → Ent; 2.1.2: hasil ⇠; 2.2: tampilkanHasil ⇠ |

#### 3.4.4 Class Diagram

Tata letak **M-V-C** seperti contoh ANSI: kolom kiri `UI:` (View, atribut + get/set), kolom tengah `Cont:` (Controller, operasi), kolom kanan `Ent:` (Model, atribut). Garis asosiasi UI→Cont→Ent.

![Class Diagram SAPA](../diagram/png/Class%20Diagram%20SAPA%20(MVC).png)

| UI (View) | Atribut |
|---|---|
| UI:Login | email, kataSandi |
| UI:Dasbor | nomorTerpilih, periode |
| UI:KotakMasuk | percakapanTerpilih, isiBalasan |
| UI:Prospek | tahapFilter, prospekTerpilih, catatan |
| UI:Kontak | kataKunci, dataKontak |
| UI:NomorWhatsApp | label, nomor, tujuan |
| UI:BasisPengetahuan | judul, kategori, isi, label |
| UI:PengaturanAI | penyedia, kunciAPI, ambangKeyakinan, kataKunciEskalasi, batasPerJam |
| UI:TimAkses | nama, email, peran, aksesNomor |
| UI:LogAudit | filterPelaku, filterAksi, rentangTanggal |
| UI:WhatsAppGateway | nomorPengirim, isiPesan |

(Setiap atribut UI memiliki `+getX()` dan `+setX(X) : void`.)

| Cont (Controller) | Operasi | Terhubung ke Ent |
|---|---|---|
| Cont:Login | +validasiLogin(), +ambilAksesNomor(), +catatLogin() | Pengguna, AksesNomor, LogAudit |
| Cont:Percakapan | +terimaPesan(), +muatPercakapan(), +kirimBalasan(), +ambilAlih(), +selesaikan() | Kontak, Percakapan, Pesan, Prospek |
| Cont:AIEngine | +klasifikasiMaksud(), +ekstrakEntitas(), +cariArtikel(), +susunJawaban(), +hitungKeyakinan(), +eskalasi() | ArtikelPengetahuan, PengaturanAI, Prospek |
| Cont:AntiBan | +nilaiPesan(), +antrekan(), +kirimAntrean(), +catatInsiden() | AntreanKeluar, PengaturanAntiBan, Insiden |
| Cont:Prospek | +muatProspek(), +ubahTahap(), +tambahAktivitas(), +hitungSkor() | Prospek, AktivitasProspek |
| Cont:Kontak | +cariKontak(), +simpanKontak() | Kontak |
| Cont:Dasbor | +muatDasbor(), +filterPeriode(), +hitungMetrik() | MetrikHarian, NomorWhatsApp |
| Cont:NomorWA | +tambahNomor(), +buatQR(), +cekStatus(), +putuskan() | NomorWhatsApp |
| Cont:BasisPengetahuan | +simpanArtikel(), +indeksUlang(), +ujiPencarian() | ArtikelPengetahuan |
| Cont:PengaturanAI | +simpanPengaturan(), +enkripsiKunci(), +ujiKeputusan() | PengaturanAI, PengaturanAntiBan |
| Cont:TimAkses | +simpanPengguna(), +aturAksesNomor(), +nonaktifkan() | Pengguna, AksesNomor |
| Cont:LogAudit | +muatLog(), +filterLog() | LogAudit |

| Ent (Model) | Atribut |
|---|---|
| Ent:Pengguna | idPengguna, nama, email, kataSandiHash, peran, status |
| Ent:AksesNomor | idPengguna, idNomor, level |
| Ent:NomorWhatsApp | idNomor, label, nomor, tujuan, status, modeAI, skorKesehatan |
| Ent:Kontak | idKontak, nomor, nama, jenjang, kelas, mapel, kota, sumber, label |
| Ent:Percakapan | idPercakapan, idKontak, idNomor, status, penangan, idAgen, belumDibaca, waktuBalasPertama |
| Ent:Pesan | idPesan, idPercakapan, arah, jenisPengirim, isi, status, metaAI |
| Ent:Prospek | idProspek, idKontak, tahap, skor, rincianSkor, idPemilik, tindakLanjutBerikut |
| Ent:AktivitasProspek | idAktivitas, idProspek, idPengguna, jenis, catatan, waktu |
| Ent:ArtikelPengetahuan | idArtikel, judul, kategori, isi, label, aktif |
| Ent:PengaturanAI | idNomor, penyedia, kunciAPITerenkripsi, persona, ambangKeyakinan, kataKunciEskalasi |
| Ent:PengaturanAntiBan | batasPerMenit, batasPerJam, batasPerHari, jedaMin, jedaMaks, jamAktif |
| Ent:AntreanKeluar | idAntrean, idPesan, prioritas, status, skorRisiko, keputusan, jadwalKirim |
| Ent:Insiden | idInsiden, idNomor, jenis, tingkat, rencanaPemulihan, status |
| Ent:MetrikHarian | idNomor, tanggal, pesanMasuk, pesanKeluar, balasanAI, balasanManusia, belumDibalas, rataWaktuBalas, prospekBaru, konversi |
| Ent:LogAudit | idLog, idPengguna, aksi, entitas, idEntitas, detail, waktu |

#### 3.4.5 Activity Diagram

Setiap activity diagram diturunkan dari Use Case Description: dua swimlane (**Aktor** | **Sistem**), initial node, aksi sesuai Basic Flow, decision node untuk Alternative/Error Flow, final node.

| AD | Alur (swimlane Aktor ⇄ Sistem) | Decision |
|---|---|---|
| AD-01 Login | A: buka Login → S: tampil form → A: isi email & kata sandi → S: validasi | ◇ valid? Tidak → S: tampil "Email atau kata sandi salah" → kembali ke isi. ◇ akun aktif? Tidak → S: tampil "Akun dinonaktifkan" → selesai. Ya → S: ambil peran & akses nomor → S: catat log → S: tampil halaman sesuai peran → selesai |
| AD-02 Mengirim Pesan WA | A(Pelanggan): kirim pesan → S: terima pesan → S: cari kontak | ◇ kontak ada? Tidak → S: buat kontak & prospek "baru". → S: simpan pesan ◇ ditangani manusia? Ya → S: tandai belum dibalas → selesai. Tidak → S: jalankan UC-03 → A: terima balasan → selesai |
| AD-03 Jawab Otomatis AI | S: klasifikasi maksud & ekstrak entitas → S: perbarui kontak & skor → S: cari artikel | ◇ artikel ditemukan? Tidak → eskalasi. → S: susun jawaban (◇ penyedia AI berhasil? Tidak → mode aturan) → S: hitung keyakinan ◇ keyakinan ≥ ambang & tanpa kata kunci eskalasi? Tidak → S: alihkan ke agen & kirim pemberitahuan. Ya → S: nilai anti-ban ◇ keputusan? kirim → S: kirim via WhatsApp Web; tunda/tahan → S: simpan antrean & catat risiko → S: catat jejak keputusan → selesai |
| AD-04 Mengelola Percakapan | A: buka Kotak Masuk → S: tampil daftar (nomor diizinkan) → A: pilih percakapan | ◇ akses nomor? Tidak → S: tolak. Ya → S: tampil riwayat & jejak AI → A: ambil alih & tulis balasan → S: hentikan AI → S: nilai anti-ban ◇ kirim? Tidak → S: tampil "Pesan ditunda". Ya → S: kirim → S: perbarui status & metrik, catat log → selesai |
| AD-05 Mengelola Prospek | A: buka Prospek → S: tampil papan → A: pilih kartu → S: tampil detail & rincian skor → A: ubah tahap, isi catatan, simpan | ◇ catatan terisi? Tidak → S: tampil "Catatan wajib diisi". Ya → S: simpan, hitung ulang skor ◇ tahap = daftar? Ya → S: tambah konversi. → S: catat log → selesai |
| AD-06 Mengelola Kontak | A: cari kontak → S: tampil hasil | ◇ ditemukan? Tidak → S: tampil "Kontak tidak ditemukan". Ya → A: ubah data & simpan → S: validasi ◇ valid? Tidak → S: tandai kolom salah. Ya → S: simpan & catat log → selesai |
| AD-07 Dasbor | A: buka Dasbor → S: ambil metrik & status nomor → S: tampil dasbor → A: pilih filter → S: hitung ulang | ◇ ada data? Tidak → S: tampil "Belum ada data". Ya → S: tampil grafik → selesai |
| AD-08 Nomor WA | A: tambah nomor & isi form → S: buat sesi & tampil QR → A: pindai QR | ◇ QR masih berlaku? Tidak → S: tampil "QR kedaluwarsa" → A: buat ulang QR. ◇ tertaut? Tidak → S: status gagal & catat risiko. Ya → S: status tersambung, catat log → selesai |
| AD-09 Basis Pengetahuan | A: buka menu → S: tampil artikel → A: tambah/ubah, isi form, simpan → S: validasi | ◇ judul & isi terisi? Tidak → S: tampil pesan wajib. Ya → S: simpan, indeks ulang FTS5, catat log → selesai |
| AD-10 Pengaturan AI | A: buka menu → S: tampil pengaturan → A: ubah nilai & simpan → S: validasi nilai | ◇ nilai wajar? Tidak → S: tolak. ◇ kunci API diterima? Tidak → S: tampil "Kunci API ditolak". Ya → S: enkripsi kunci, simpan, catat log → selesai |
| AD-11 Tim & Akses | A: buka menu → S: tampil pengguna → A: isi form & akses nomor, simpan | ◇ email unik? Tidak → S: tampil "Email sudah digunakan". Ya → S: simpan pengguna & akses, catat log → selesai |
| AD-12 Log Audit | A: buka menu → S: tampil log terbaru → A: isi filter → S: cari log | ◇ ada hasil? Tidak → S: tampil "Tidak ada aktivitas". Ya → S: tampil hasil → selesai |

### 3.5 Mockup Aplikasi

Mockup *high-fidelity* dibuat di Figma (spesifikasi per halaman: `draft/mockup-spec-untuk-figma.md`). Setiap halaman memiliki satu gambar dan deskripsi komponennya.

| No | Halaman | Use case | Gambar |
|---|---|---|---|
| MK-01 | Login | UC-01 | Gambar 3.x Mockup Halaman Login |
| MK-02 | Dasbor Pemantauan | UC-07 | Gambar 3.x Mockup Dasbor |
| MK-03 | Kotak Masuk | UC-04 (UC-02, UC-03) | Gambar 3.x Mockup Kotak Masuk |
| MK-04 | Prospek | UC-05 | Gambar 3.x Mockup Prospek |
| MK-05 | Kontak | UC-06 | Gambar 3.x Mockup Kontak |
| MK-06 | Nomor WhatsApp | UC-08 | Gambar 3.x Mockup Nomor WhatsApp |
| MK-07 | Basis Pengetahuan | UC-09 | Gambar 3.x Mockup Basis Pengetahuan |
| MK-08 | Pengaturan AI & Konsol Uji | UC-10 | Gambar 3.x Mockup Pengaturan AI |
| MK-09 | Antrean Keluar & Pusat Risiko | UC-10 | Gambar 3.x Mockup Antrean & Pusat Risiko |
| MK-10 | Tim & Akses | UC-11 | Gambar 3.x Mockup Tim & Akses |
| MK-11 | Log Audit | UC-12 | Gambar 3.x Mockup Log Audit |

*(Deskripsi per halaman di laporan final diambil dari ringkasan setiap halaman pada file spesifikasi mockup.)*

### 3.6 System Development Life Cycle

System Development Life Cycle (SDLC) yang digunakan adalah metode eXtreme Programming (XP) yang termasuk dalam model Agile. Secara garis besar tahap-tahap dalam metode eXtreme Programming (Ambler, 2002) dapat dilihat pada Gambar 3.x berikut ini. *(kalimat & sitasi bawaan template)*

---

## DAFTAR PUSTAKA (APA 7: dibuat otomatis oleh Word dari sumber terverifikasi)

Ambler, S. (2002). *Agile modeling: Effective practices for eXtreme Programming and the Unified Process*. John Wiley & Sons. *(bawaan template)*

Dhaman, D., Anggai, S., & Waskita, A. A. (2025). Optimasi akurasi jawaban aplikasi chatbot layanan pelanggan dengan metode RAG (Retrieval-Augmented Generation). *Journal of Information System Research (JOSH), 6*(4), 2120–2128. https://doi.org/10.47065/josh.v6i4.8048

Elysia, S., & Herianto. (2024). Chatbot berbasis Retrieval Augmented Generation (RAG) untuk peningkatan layanan informasi sekolah. *Journal TIFDA (Technology Information and Data Analytic), 1*(2), 52–58. https://doi.org/10.70491/tifda.v1i2.52

Fan, W., Ding, Y., Ning, L., Wang, S., Li, H., Yin, D., Chua, T.-S., & Li, Q. (2024). A survey on RAG meeting LLMs: Towards retrieval-augmented large language models. In *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining* (pp. 6491–6501). ACM. https://doi.org/10.1145/3637528.3671470

González-Flores, L., Rubiano-Moreno, J., & Sosa-Gómez, G. (2025). The relevance of lead prioritization: A B2B lead scoring model based on machine learning. *Frontiers in Artificial Intelligence, 8*, 1554325. https://doi.org/10.3389/frai.2025.1554325

Imaduddin, M., Susanto, R., & Pradana, A. I. (2026). Pengembangan chatbot WhatsApp berbasis Retrieval-Augmented Generation (RAG) dan OpenAI untuk penyediaan jawaban akurat dari dokumen aturan organisasi. *Adopsi Teknologi dan Sistem Informasi (ATASI), 5*(1), 23–31. https://doi.org/10.30872/atasi.v5i1.3472

Irawan, R., & Fahmi. (2025). Implementasi metode Extreme Programming (XP) pada sistem manajemen data layanan bimbingan dan konseling di Madrasah Aliyah. *JSiI (Jurnal Sistem Informasi), 12*(1), 49–55. https://doi.org/10.30656/jsii.v12i1.10023

Jadli, A., Hain, M., & Hasbaoui, A. (2023). Artificial intelligence-based lead propensity prediction. *IAES International Journal of Artificial Intelligence (IJ-AI), 12*(3), 1281–1290. https://doi.org/10.11591/ijai.v12.i3.pp1281-1290

Narulita, S., Nugroho, A., & Abdillah, M. Z. (2024). Diagram Unified Modelling Language (UML) untuk perancangan sistem informasi manajemen penelitian dan pengabdian masyarakat (SIMLITABMAS). *Bridge: Jurnal Publikasi Sistem Informasi dan Telekomunikasi, 2*(3), 244–256. https://doi.org/10.62951/bridge.v2i3.174

Nicolescu, L., & Tudorache, M. T. (2022). Human-computer interaction in customer service: The experience with AI chatbots: A systematic literature review. *Electronics, 11*(10), 1579. https://doi.org/10.3390/electronics11101579

Parkinson, S., & Khan, S. (2022). A survey on empirical security analysis of access-control systems: A real-world perspective. *ACM Computing Surveys, 55*(6), 1–28. https://doi.org/10.1145/3533703

Prasetyo, S. E., Puteri, V. A., & Sabariman. (2025). Implementasi chatbot AI dan WhatsApp untuk mendukung penjualan dan konsultasi rakitan komputer di Toko Micro Batam. *Journal of Information System Management (JOISM), 7*(1), 120–126. https://doi.org/10.24076/joism.2025v7i1.2098

Prior, D. D., Buttle, F., & Maklan, S. (2024). *Customer relationship management: Concepts, applications and technologies* (5th ed.). Routledge. ISBN 9781032247441.

Purnasari, M., Hartiwi, Y., & Nurhayati. (2022). Perancangan sistem informasi pengelolaan dana masjid berbasis web menggunakan Unified Modeling Language (UML). *Resolusi: Rekayasa Teknik Informatika dan Informasi, 2*(6), 258–264. https://doi.org/10.30865/resolusi.v2i6.416

Puspitasari, N. B. (2025). Bot innovation realizing service excellence: Designing WhatsApp chatbot as a customer service solution. *Jurnal Sistem Informasi Bisnis, 15*(2), 221–229. https://doi.org/10.14710/vol15iss2pp221-229

Sahyudi, M., & Susanto, E. R. (2025). Analisis implementasi sistem keamanan basis data berbasis Role-Based Access Control (RBAC) pada aplikasi Enterprise Resource Planning. *SATESI: Jurnal Sains Teknologi dan Sistem Informasi, 5*(1), 105–116. https://doi.org/10.54259/satesi.v5i1.3997

Tjahyanti, L. P. A. S. (2023). Pengembangan sistem informasi pendaftaran PKL di Universitas Panji Sakti. *Jurnal Minfo Polgan, 12*(1), 997–1004. https://doi.org/10.33395/jmp.v12i1.12545

Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi. (2022). https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022

Wolf, L., & Steul-Fischer, M. (2023). Factors of customers' channel choice in an omnichannel environment: A systematic literature review. *Management Review Quarterly, 73*(4), 1579–1630. https://doi.org/10.1007/s11301-022-00281-w
