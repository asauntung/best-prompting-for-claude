# Contoh 2: Claude Code, Opus 5.5, Mode B (memperbaiki prompt)

## Permintaan pengguna

/best-prompting Perbaiki prompt saya ini untuk Claude Code, model Opus 5.5, effort max:

```text
PENTING!!! Kamu adalah editor profesional. Rapikan SEMUA file markdown di folder catatan/, perbaiki typo dan ejaan, samakan format judul. JANGAN ADA YANG TERLEWAT. Kerjakan secepatnya.
```

## Keluaran skill

### Analisis

Parameter lengkap: ekosistem Claude Code, model Opus 5.5, effort `max`. Ini Mode B, jadi maksud asli dipertahankan (merapikan semua file Markdown di `catatan/`, memperbaiki salah ketik dan ejaan, menyeragamkan format judul, tanpa ada yang terlewat) dan yang diperbaiki adalah cara menyampaikannya. Tugas ini jenis kerja agentik berbasis file dan folder, jadi bagian referensi yang relevan adalah kerja agentik di panduan Opus 5.5, panduan induknya, dan `prompting-best-practices.md`. Panduan induk Opus 5 ikut dipakai karena panduan Opus 5.5 sendiri menyatakan: "Existing Claude Opus 5 prompts should perform well without changes" (`prompting-claude-opus-5-5.md > Prompting Claude Opus 5.5`).

Diagnosis prompt lama, satu per satu:

**1. Penekanan dengan huruf kapital dan tanda seru, tanpa alasan.** "PENTING!!!" dan "JANGAN ADA YANG TERLEWAT" memberi tekanan tetapi tidak memberi tahu Claude kenapa tugas ini penting atau untuk apa catatan itu dipakai. Referensi menganjurkan alasan, bukan volume: "Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses." (`prompting-best-practices.md > Add context to improve performance`). Karena itu, di prompt baru huruf kapital diganti kalimat biasa, dan ada satu tempat (placeholder) untuk menjelaskan kegunaan catatan. Anjuran referensi untuk mengendurkan bahasa agresif seperti "CRITICAL: You MUST" ada di bagian yang oleh `[CATATAN LOKAL]` dinyatakan khusus Claude Opus 4.5 dan 4.6 (`prompting-best-practices.md > Tool usage`), jadi tidak dijadikan dasar di sini.

**2. Instruksi yang ambigu.** "Rapikan" bisa berarti apa saja, dari membetulkan ejaan sampai menulis ulang paragraf. "Samakan format judul" tidak menyebut format yang mana. "Folder catatan/" tidak menjelaskan apakah subfolder ikut. Uji dari referensi: "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too." (`prompting-best-practices.md > Be clear and direct`). Rekan kerja yang membaca prompt lama pasti bertanya format judul mana yang dipakai. Prompt baru mendefinisikan "rapikan" sebagai dua hal saja (ejaan dan format judul), meminta Claude menentukan konvensi judul dari pola yang dominan di folder lalu menyatakannya sebelum mengedit, dan memasukkan subfolder. Asumsi bahwa subfolder ikut dihitung adalah pembacaan saya atas kata "SEMUA"; jika tidak, hapus frasa itu di langkah 1.

**3. Batas cakupan yang hilang.** Opus 5, induk Opus 5.5, cenderung memperluas tugas: "Claude Opus 5 can also expand the scope of a task, adding steps that weren't requested or applying its own judgment about what the task should be. For narrow tasks, constrain scope explicitly" (`prompting-claude-opus-5.md > Task scope and over-verification`). Menyunting catatan pribadi adalah tugas sempit, dan kata "Rapikan" dengan peran "editor profesional" mengundang penulisan ulang gaya. Prompt baru menyebut dengan tegas apa yang tidak boleh disentuh (isi, struktur, blok kode, tautan, front matter, nama diri) dan memuat terjemahan dua kalimat dari contoh prompt referensi yang sama. Teks aslinya: "Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work."

**4. "Jangan ada yang terlewat" tanpa cara memastikannya.** Kelengkapan lebih terjamin oleh urutan kerja yang jelas daripada oleh huruf kapital: "Provide instructions as sequential steps using numbered lists or bullet points when the order or completeness of steps matters." (`prompting-best-practices.md > Be clear and direct`). Prompt baru memakai langkah bernomor yang dimulai dengan mendata semua file ke daftar tugas, lalu mencentangnya satu per satu. **[Inferensi]** Daftar tugas ini dipilih karena kelengkapan di tugas banyak file adalah soal pencatatan, bukan soal berpikir lebih keras; Claude Code punya daftar to-do bawaan, jadi instruksi ini tidak menuntut pengguna menyiapkan apa pun.

**5. Tidak perlu instruksi "periksa ulang".** Godaan wajar untuk "JANGAN ADA YANG TERLEWAT" adalah menambahkan "periksa lagi semua file sebelum selesai". Referensi induk menyarankan sebaliknya: "Claude Opus 5 verifies its own work without being told to." (`prompting-claude-opus-5.md > Task scope and over-verification`). Karena itu prompt baru tidak memuat langkah verifikasi ulang; syarat berhentinya cukup "semua file di daftar sudah ditandai selesai".

**6. Salah ketik yang meragukan.** Catatan pribadi biasanya berisi nama orang, singkatan sendiri, istilah daerah, atau istilah asing yang tampak seperti salah ketik padahal disengaja. Referensi menganjurkan memberi izin untuk ragu: "Explicitly give Claude permission to admit uncertainty. This simple technique can drastically reduce false information." (`reduce-hallucinations.md > Basic hallucination minimization strategies`). Prompt baru meminta Claude membiarkan kasus yang meragukan apa adanya dan mencatatnya di laporan, alih-alih menebak.

**7. Laporan akhir yang tidak diminta.** Prompt lama tidak menyebut apa yang harus dilaporkan, padahal pengguna perlu tahu file mana yang berubah dan apa yang dibiarkan. Referensi induk memberi bentuk laporan yang langsung ke hasil: "When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it." (`prompting-claude-opus-5.md > User-facing progress updates`). Kalimat ini diterjemahkan ke paragraf terakhir prompt, lalu ditambah isi laporan yang spesifik untuk tugas ini.

Peran "editor profesional" dipertahankan karena itu bagian dari maksud asli. **[Inferensi]** Referensi membahas peran di system prompt, sedangkan di Claude Code prompt ini dikirim sebagai pesan pengguna; di sana peran tetap berguna sebagai penanda standar kerja, asalkan cakupannya dibatasi seperti di butir 3. Instruksi "Kerjakan secepatnya" dihapus dari prompt; alasannya dibahas di bagian Effort.

### Effort

Effort usulan: `medium`. Effort pilihan pengguna, `max`, menurut referensi kurang tepat untuk tugas ini, dengan tiga alasan.

Pertama, titik awal yang dianjurkan untuk Opus 5.5 adalah default-nya: "Start at `medium`, the default on Claude Opus 5.5 (Claude Opus 5 defaults to `high`), set it explicitly, and test several levels against your own evals rather than carrying over the setting you used on Claude Opus 5." (`prompting-claude-opus-5-5.md > Calibrate effort`). Level tertinggi disimpan untuk kasus yang sudah terbukti butuh: "Reserve `xhigh` and `max` for work where you've measured a quality gain." (bagian yang sama). Memperbaiki ejaan dan menyeragamkan judul adalah pekerjaan rutin, dan di level `medium` model ini sudah kuat untuk jenis kerja semacam itu: "in Anthropic's testing, Claude Opus 5.5 at `medium` matches or exceeds Claude Opus 5 at `high` on coding and knowledge-work evaluations" (bagian yang sama).

Kedua, `max` bertentangan dengan permintaan "Kerjakan secepatnya" di prompt Anda sendiri: "At a given level, Claude Opus 5.5 tends to think more per turn than Claude Opus 5, especially at `xhigh` and `max`." (bagian yang sama). Artinya `max` membuat setiap langkah lebih lama dan lebih mahal.

Ketiga, kecepatan dikendalikan lewat effort, bukan lewat kalimat di prompt: "To get less thinking, lower the effort level first. Lowering effort reduces thinking, and with it cost and latency, more reliably than prompt instructions do." (bagian yang sama). Karena itu "Kerjakan secepatnya" dihapus dari prompt dan maksudnya dipindahkan ke pilihan effort `medium`.

Penyesuaian prompt untuk `medium`: referensi tidak menyediakan tambahan prompt khusus effort `medium` untuk Opus 5.5, jadi tidak ada yang ditambahkan. **[Inferensi]** Pengaman kelengkapan di prompt ini (daftar tugas dan syarat berhenti) tidak bergantung pada banyaknya berpikir, sehingga tetap bekerja di effort yang lebih rendah.

Jika Anda tetap memilih `max`, prompt di bawah bisa dipakai tanpa perubahan isi; cukup ganti baris Final menjadi `Final: Claude Code, Opus 5.5, max`. Terimalah bahwa gilirannya akan lebih panjang dan lebih mahal, dan keinginan "secepatnya" tidak akan tercapai. Anjuran referensi untuk level tinggi, "Set `max_tokens` high enough to leave room for the model's thinking tokens and the reply." (bagian yang sama), adalah mekanik API dan tidak tersedia di Claude Code. Jika hasil di `medium` ternyata melewatkan salah ketik yang seharusnya tertangkap, naikkan ke `high` lebih dulu sebelum `xhigh` atau `max`.

Sisa risiko: di effort mana pun, prompt tidak bisa menjamin nol salah ketik terlewat, dan referensi berulang kali menyebut effort sebagai tuas utama, bukan kalimat prompt. **[Inferensi]** Salah ketik yang sah secara ejaan tetapi salah konteks (misalnya "makam" yang seharusnya "makan") paling mungkin lolos. Periksa daftar keraguan di laporan akhir, dan jika folder ini ada di repositori git, tinjau perubahannya dengan diff sebelum disimpan permanen.

Final: Claude Code, Opus 5.5, medium

```text
Bertindaklah sebagai editor profesional. Tugasmu adalah merapikan semua file Markdown di folder catatan/, dan "merapikan" di sini berarti dua hal saja: memperbaiki salah ketik dan ejaan, serta menyeragamkan format judul. [TULIS DI SINI UNTUK APA CATATAN INI DIPAKAI, misalnya "Catatan ini akan dibagikan ke tim sebagai bahan rujukan, jadi harus bersih dan seragam." Hapus kalimat ini jika tidak perlu.]

Tidak boleh ada file yang terlewat, jadi kerjakan dengan urutan berikut:

1. Data semua file berekstensi .md di dalam catatan/, termasuk yang ada di subfolder. Catat semuanya di daftar tugas, sebutkan jumlahnya, dan perbarui daftar itu setiap kali satu file selesai. Jangan membuat file baru di dalam catatan/.
2. Baca judul di seluruh file dan tentukan konvensi judul yang paling dominan: jenis penanda judul, urutan jenjang judul, penulisan huruf kapital, dan baris kosong di sekitar judul. Sebelum mulai mengedit, tulis konvensi itu dalam satu paragraf singkat beserta alasannya. Jika tidak ada pola yang dominan, pilih konvensi yang paling sesuai dengan struktur isi catatan dan nyatakan pilihan itu sebagai asumsi.
3. Kerjakan file satu per satu sesuai daftar. Perbaiki salah ketik dan ejaan mengikuti kaidah baku bahasa yang dipakai catatan itu, lalu terapkan konvensi judul dari langkah 2. Tandai file sebagai selesai di daftar.
4. Berhenti hanya ketika semua file di daftar sudah ditandai selesai.

Kerjakan apa yang diminta, pada cakupan yang dimaksud. Jangan menulis ulang kalimat demi gaya, jangan mengubah urutan atau struktur isi, dan jangan menambah atau menghapus konten. Jangan ubah isi blok kode, kode sebaris, URL, tautan, path, front matter, dan nama file. Nama orang, nama tempat, istilah teknis, istilah asing, dan kutipan langsung hanya boleh diubah jika salah ketiknya tidak meragukan. Ambil sendiri keputusan rutin, dan tanyakan kepada saya hanya jika pembacaan yang berbeda atas permintaan ini akan menghasilkan pekerjaan yang berbeda secara material.

Jika kamu ragu apakah sesuatu itu salah ketik atau memang disengaja, misalnya ejaan sebuah nama, singkatan pribadi, istilah daerah, atau bahasa percakapan, biarkan apa adanya dan catat untuk laporan. Lebih baik mengakui ragu daripada menebak.

Setelah selesai, awali laporan dengan hasilnya: kalimat pertamamu menjawab "apa yang terjadi", yaitu berapa file yang diperiksa dan berapa yang diubah. Setelah itu sebutkan konvensi judul yang kamu pakai, lalu daftar hal yang kamu ragukan dan biarkan apa adanya, lengkap dengan nama file dan barisnya.
```
