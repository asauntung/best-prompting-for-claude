# Contoh 4: Claude Code, Fable 5.1, Mode B (memadatkan prompt yang gemuk)

## Permintaan pengguna

/prompting-claude Perbaiki prompt ini untuk Claude Code, Fable 5.1, effort high. Saya jalankan lalu saya tinggal.

```text
Kamu adalah asisten riset kualitatif yang sangat teliti. Tugasmu adalah membaca 30 transkrip wawancara petani di folder transkrip/ dan menyusun tabel temuan di hasil/temuan.md. Ini sangat penting karena tabel ini akan dipakai untuk laporan penelitian saya, dan kalau ada kesalahan, laporan saya bisa ditolak pembimbing.

ATURAN KUTIPAN: Setiap temuan WAJIB disertai kutipan langsung dari transkrip. Kutipan harus disalin persis, karena pembimbing saya akan mencocokkannya dengan transkrip asli. JANGAN PERNAH mengarang kutipan. Kalau tidak ada kutipan yang mendukung, jangan tulis temuannya, karena temuan tanpa kutipan tidak ada gunanya bagi saya.

ATURAN TEMA: Kelompokkan temuan ke dalam tema. Temanya harus muncul dari data, bukan dari kepalamu, karena ini penelitian induktif. Jangan memaksakan tema. Kalau satu temuan cocok untuk dua tema, pilih yang paling cocok, karena satu temuan hanya boleh muncul sekali.

ATURAN FORMAT: Tabel punya kolom Tema | Temuan | Kutipan | Kode responden | Baris. Nomor baris harus benar karena pembimbing akan mengecek.

CARA KERJA: Baca semua transkrip satu per satu. Jangan melewatkan satu transkrip pun, karena setiap responden penting. Panggil alat secara paralel supaya cepat. Jangan menulis ulang seluruh file untuk perubahan kecil. Jangan melapor apa pun kepada saya sampai semua selesai, simpan semua temuan untuk laporan akhir.

JANGAN BERHENTI SEBELUM SELESAI. Saya pernah melihat kamu berhenti dengan cara-cara ini: (1) menulis rangkuman lalu bilang "selanjutnya saya akan..." tanpa mengerjakannya, (2) bertanya "mau saya lanjutkan?", (3) memberi daftar pertanyaan padahal tidak perlu, (4) berhenti karena merasa percakapan sudah panjang. Keempatnya tidak saya inginkan. Kerjakan terus sampai selesai.

INGAT: kutipan harus persis dan jangan dikarang. Satu temuan hanya sekali. Nomor baris harus benar.

SYARAT SELESAI:
1. Semua 30 transkrip sudah dibaca.
2. Setiap temuan punya kutipan persis.
3. Tidak ada kutipan karangan.
4. Tidak ada temuan ganda.
5. Nomor baris benar.
6. Tabel tersimpan di hasil/temuan.md.
```

## Keluaran skill

### Analisis

Parameter lengkap: ekosistem Claude Code, model Fable 5.1, effort `high`. Ini Mode B. Maksud aslinya dipertahankan: tabel temuan dari 30 transkrip, kutipan persis dengan nomor baris, tema induktif, tanpa temuan ganda, dan kerja sampai selesai tanpa ditunggui. Masalah prompt lama bukan kekurangan, melainkan kelebihan, jadi perbaikannya sebagian besar berupa membuang. Referensi membenarkan langkah itu: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality. Review and consider removing older instructions if default performance is better." (`prompting-claude-fable-5.md > Recommended scaffolding changes`). Panduan induk Fable 5 dipakai karena panduan Fable 5.1 menyatakan: "Your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes" (`prompting-claude-fable-5-1.md > Prompting Claude Fable 5.1`).

Diagnosis prompt lama:

**1. Aturan yang sama ditulis tiga kali.** "Kutipan harus persis" muncul di ATURAN KUTIPAN, di INGAT, dan di SYARAT SELESAI. "Satu temuan hanya sekali" dan "nomor baris harus benar" juga masing-masing muncul tiga kali. SYARAT SELESAI seluruhnya mengulang isi prompt. **[Inferensi]** Pengulangan tidak menambah kepatuhan; ia hanya memperpanjang prompt. Di prompt baru tiap aturan ditulis sekali, dan kalimat kriterianya disalin dari prompt lama, bukan dirumuskan ulang. Yang diubah hanya huruf kapitalnya.

**2. Alasan ditempel di hampir setiap kalimat.** Ada tujuh klausa "karena", dan hampir semuanya bermuara pada satu hal: pembimbing akan mencocokkan tabel dengan transkrip. Referensi menganjurkan konteks tujuan, cukup sekali: "Claude Fable 5 tends to perform better when it understands the intent behind a request: context lets it connect the task to relevant information rather than inferring intent on its own." (`prompting-claude-fable-5.md > Give the reason, not only the request`). Prompt baru membuka dengan satu paragraf konteks. Satu-satunya "karena" yang dipertahankan adalah "karena ini penelitian induktif", sebab alasan itu tidak bisa ditebak dari paragraf pembuka.

**3. Empat cara berhenti dirinci satu per satu, dengan huruf kapital.** Referensi menyatakan instruksi singkat sudah cukup: "Instruction-following is improved enough that you can steer most behaviors with a brief instruction rather than enumerating each behavior by name." (`prompting-claude-fable-5.md > Strong instruction following`). Karena prompt ini dijalankan tanpa ditunggui, prompt baru memakai versi pendek dari blok resmi. Referensi sendiri menyediakan jalan pintas itu: "If you need to limit prompt length, use only the first, which keeps most of the effect." (`prompting-claude-fable-5-1.md > Finish the whole task`). Dari blok pertama itu dipakai kalimat pembuka dan paragraf pemeriksaan akhir. Kalimat pembukanya dipertahankan karena "The opening sentence, which tells the model the user isn't watching, carries much of the effect. Keep it as written." (bagian yang sama). Teks asli yang diterjemahkan: "You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work." dan "Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls." Paragraf ketiga dan keempat dari blok itu tidak dipakai. **[Inferensi]** Paragraf tentang konteks yang panjang tidak dipakai karena tugas ini tidak berisiko menghabiskan konteks, dan paragraf tentang perintah yang mengubah sistem tidak relevan untuk tugas yang hanya membaca dan menulis satu berkas.

**4. "Jangan melapor apa pun sampai semua selesai" harus dibuang.** Referensi menyebut baris seperti ini secara khusus: "Some earlier models were eager to give updates while working, which led to system prompt lines such as "hold all findings for the final response." Remove lines like that before adding anything." (`prompting-claude-fable-5-1.md > Ask for user-facing progress updates`). Kalimat itu dihapus, dan tidak ada instruksi kabar progres yang ditambahkan sebagai gantinya, karena pengguna tidak melaporkan masalah soal kabar progres.

**5. Instruksi untuk gejala yang tidak ada.** "Panggil alat secara paralel" dan "Jangan menulis ulang seluruh file" adalah obat untuk dua gejala dalam daftar panduan Fable 5.1, yaitu "One tool call per turn in agent loops" dan "Whole files rewritten for small changes". Panduan itu disusun per gejala: "Start with the section that matches what you observe" (`prompting-claude-fable-5-1.md > Prompting Claude Fable 5.1`). Pengguna tidak melaporkan kedua gejala itu, dan tugas ini hanya menulis satu berkas baru, jadi kedua kalimat dihapus.

**6. Satu pemeriksaan yang nyata menggantikan tiga pengingat.** Risiko terbesar tugas ini adalah kutipan atau nomor baris yang meleset. Tiga kali mengingatkan "harus persis" tidak menutup risiko itu, sedangkan pemeriksaan terpisah bisa: "Separate, fresh-context verifier subagents tend to outperform self-critique." (`prompting-claude-fable-5.md > Recommended scaffolding changes`). Prompt baru memuat satu kalimat yang meminta subagen berkonteks baru mencocokkan kutipan dengan transkrip.

**7. Laporan akhir diberi isi.** Prompt lama menyebut "laporan akhir" tanpa isinya. Satu kalimat mengikuti anjuran "Lead with the outcome." (`prompting-claude-fable-5.md > Strong instruction following`), dengan isi yang spesifik untuk tugas ini.

Peran "asisten riset kualitatif yang sangat teliti" dihapus. **[Inferensi]** Ketelitian yang dimaksud sudah dinyatakan lewat syarat kutipan dan pemeriksaan subagen, sehingga peran itu tidak mengubah perilaku.

Panjang prompt: prompt lama 295 kata, prompt baru 207 kata.

### Effort

Effort `high` yang Anda pilih sudah tepat. Ini default Fable 5.1 dan titik awal yang dianjurkan: "Start at the default effort level, `high`, then test the other levels (`low`, `medium`, `xhigh`, and `max`) against your own evals." (`prompting-claude-fable-5-1.md > Consider all effort levels`). Kecermatan kutipan dan nomor baris pada 30 transkrip adalah jenis kerja yang diuntungkan oleh effort tinggi. Referensi tidak menyediakan tambahan prompt khusus untuk `high`, jadi tidak ada yang ditambahkan.

Sisa risiko: "On routine work at higher effort, Claude Fable 5 can gather context and deliberate beyond what the task needs." (`prompting-claude-fable-5.md > Consider all effort levels`). Jika hasilnya rapi tetapi lama, coba `medium` pada beberapa transkrip dan bandingkan. Tidak ada prompt yang menjamin nol kutipan meleset, jadi tetap periksa daftar kutipan yang diperbaiki pemeriksa di laporan akhir.

Final: Claude Code, Fable 5.1, high

```text
Saya sedang menulis laporan penelitian kualitatif tentang pengalaman petani, dan pembimbing saya akan mencocokkan setiap kutipan di tabel ini dengan transkrip aslinya.

Baca ke-30 transkrip wawancara di folder transkrip/, lalu susun tabel temuan di hasil/temuan.md dengan kolom Tema | Temuan | Kutipan | Kode responden | Baris.

Setiap temuan wajib disertai kutipan langsung dari transkrip. Kutipan harus disalin persis, beserta nomor barisnya. Kalau tidak ada kutipan yang mendukung, jangan tulis temuannya. Temanya harus muncul dari data, bukan dari kepalamu, karena ini penelitian induktif. Kalau satu temuan cocok untuk dua tema, pilih yang paling cocok; satu temuan hanya boleh muncul sekali.

Sebelum selesai, minta satu subagen berkonteks baru mencocokkan setiap kutipan dan nomor baris dengan berkas transkripnya, lalu perbaiki yang tidak cocok.

Kamu bekerja tanpa diawasi. Saya tidak memantau dan tidak bisa menjawab di tengah tugas, jadi bertanya "Mau saya…?" atau "Perlu saya…?" akan menghentikan pekerjaan. Sebelum mengakhiri giliran, periksa paragraf terakhirmu: kalau isinya rencana, analisis, pertanyaan, daftar langkah berikutnya, atau janji atas pekerjaan yang belum dikerjakan, kerjakan sekarang dengan panggilan alat. Berhenti hanya bila tabel sudah mencakup ke-30 transkrip, atau bila ada hal yang hanya bisa saya putuskan.

Setelah selesai, awali laporan dengan hasilnya: jumlah transkrip yang dibaca, jumlah tema dan temuan, lalu kutipan yang diperbaiki pemeriksa.
```
