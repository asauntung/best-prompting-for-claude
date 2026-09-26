# Contoh 1: Chat, Sonnet 5, Mode A (menjelaskan kebutuhan)

## Permintaan pengguna

> /best-prompting Saya guru Biologi SMA. Tolong buatkan instruksi untuk Project di claude.ai supaya Claude membantu saya membuat 10 soal pilihan ganda dari materi bab yang saya tempel, lengkap dengan kunci dan pembahasan singkat. Model Sonnet 5.

## Keluaran skill

### Analisis

Ini permintaan Mode A: Anda menjelaskan kebutuhan, belum membawa prompt. Ekosistemnya saya simpulkan **Chat**, karena Anda menyebut instruksi Project di claude.ai. Instruksi Project berlaku di setiap percakapan dalam Project itu, sehingga perannya setara dengan system prompt di referensi. Kesetaraan ini **[Inferensi]**: referensi ditulis untuk developer API dan tidak menyebut Project. Panduan Sonnet 5 juga tidak punya bagian khusus chat, jadi yang dipakai adalah perilaku umum Sonnet 5 ditambah teknik umum dan tematik.

Ada beberapa hal yang tidak Anda sebut, dan saya putuskan sendiri karena tidak ada yang mengubah prompt secara mendasar. Pertama, soal memakai lima pilihan A sampai E, mengikuti kebiasaan ujian SMA di Indonesia **[Inferensi]**. Kedua, soal 1 sampai 10 ditampilkan dulu tanpa kunci, lalu kunci dan pembahasan dikumpulkan di bagian terpisah di bawahnya, supaya bagian soal bisa langsung disalin untuk siswa **[Inferensi]**. Ketiga, tingkat kognitif soal dicampur, tidak hafalan semua. Kelas dan kurikulum dibiarkan sebagai isian `[ISI KELAS DAN KURIKULUM]` yang Anda isi sekali saja. Semua asumsi ini bisa Anda ubah langsung di teks prompt.

**1. Sonnet 5 membaca instruksi secara harfiah, jadi cakupannya harus ditulis eksplisit.** Menurut `prompting-claude-sonnet-5.md > More literal instruction following`: "Claude Sonnet 5 interprets prompts literally and explicitly, particularly at lower effort levels. It does not silently generalize an instruction from one item to another, and it does not infer requests you didn't make." Karena itu prompt menyebut bahwa kunci dan pembahasan wajib ada untuk kesepuluh soal, bukan hanya beberapa, dan bahwa aturan soal berlaku untuk semua soal. Hal yang biasanya dianggap "sudah jelas" oleh guru, seperti tepat satu jawaban benar dan pengecoh yang masuk akal, juga ditulis terang.

**2. Alasan di balik instruksi membantu Claude membidik hasil.** Menurut `prompting-best-practices.md > Add context to improve performance`: "Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses." Maka prompt dibuka dengan siapa Anda, untuk siapa soalnya, dan dipakai untuk apa. Aturan penting juga disertai alasannya, misalnya kenapa soal hanya boleh menguji isi materi dan kenapa rumus ditulis tanpa LaTeX.

**3. Soal harus berpijak pada materi yang Anda tempel, dan Claude boleh berkata materinya kurang.** Menurut `reduce-hallucinations.md > Advanced techniques`, butir External knowledge restriction: "Explicitly instruct Claude to only use information from provided documents and not its general knowledge." Menurut `reduce-hallucinations.md > Basic hallucination minimization strategies`, butir Allow Claude to say "I don't know": "Explicitly give Claude permission to admit uncertainty. This simple technique can drastically reduce false information." Jadi prompt membatasi soal, kunci, dan pembahasan pada isi materi, dan memberi jalan keluar yang jujur jika materi terlalu pendek untuk 10 soal yang bermutu. Pengecoh tetap boleh diambil dari miskonsepsi umum siswa, karena pengecoh memang harus salah. Pengecualian ini **[Inferensi]** saya sendiri.

**4. Panjang pembahasan perlu ditetapkan dengan angka.** Menurut `prompting-claude-sonnet-5.md > Response length and verbosity`: "Claude Sonnet 5 calibrates response length to the complexity of the task rather than defaulting to a fixed verbosity." Artinya, kata "singkat" saja bisa ditafsirkan berbeda dari soal ke soal. Prompt menetapkan dua sampai tiga kalimat per pembahasan, beserta isinya: kenapa kunci benar menurut materi, dan kenapa pengecoh yang paling menjebak itu salah.

**5. Format keluaran ditetapkan dengan templat.** Menurut `increase-output-consistency.md > Specify the desired output format`: "Precisely define your desired output format using JSON, XML, or custom templates so that Claude follows every output formatting element you require." Prompt memuat templat teks biasa untuk bagian soal dan bagian kunci. JSON atau XML tidak dipakai karena hasilnya dibaca dan disalin oleh guru, bukan diproses program **[Inferensi]**.

**6. Pemeriksaan mandiri sebelum mengirim.** Menurut `prompting-best-practices.md > Leverage thinking & interleaved thinking capabilities`, tentang meminta Claude memeriksa jawabannya sendiri: "This catches errors reliably, especially for coding and math." Bagian itu menyebut Claude Opus 5 sebagai pengecualian yang tidak perlu instruksi ini, dan Sonnet 5 tidak disebut. Karena itu anjuran ini saya anggap tetap berlaku untuk Sonnet 5 **[Inferensi]**. Kriteria periksanya dibuat konkret: kunci benar menurut materi, hanya satu pilihan yang benar, dan tidak ada soal yang jawabannya bocor lewat soal lain.

**7. Rumus kimia dan notasi ditulis sebagai teks biasa.** Menurut `prompting-best-practices.md > LaTeX output`: "Claude's latest models default to LaTeX for mathematical expressions, equations, and technical explanations." Soal Biologi sering memuat rumus seperti persamaan fotosintesis. Soal akan Anda salin ke Word atau Google Form, dan di sana kode LaTeX tidak tampil sebagai rumus, jadi prompt meminta teks biasa seperti C6H12O6 **[Inferensi]**.

Satu catatan terakhir. Teknik menandai teks tempelan dengan tag berlabel ID acak ada di panduan Opus 5.5, bukan panduan Sonnet 5, dan ditujukan untuk teks dari pihak lain yang mungkin berisi instruksi tersembunyi. Materi Anda adalah bahan ajar sendiri, jadi risikonya rendah dan Anda tidak perlu mengetik tag apa pun **[Inferensi]**.

### Effort

Anda tidak menyebut effort. Usulan saya adalah **`high`**. Menurut `prompting-claude-sonnet-5.md > Calibrating effort and thinking depth`, `high` adalah "The default. This setting balances token usage and intelligence for most use cases." Menyusun soal pilihan ganda terlihat sederhana, tetapi mutunya bergantung pada penalaran: kunci harus benar, hanya satu pilihan yang benar, dan pengecoh harus masuk akal tanpa ikut benar. Level `low` menurut bagian yang sama sebaiknya dipakai untuk "short, scoped tasks and latency-sensitive workloads that are not intelligence-sensitive", dan panduan itu juga memperingatkan bahwa "on moderately complex tasks running at `low` effort there is some risk of under-thinking." Level `medium` ditujukan untuk kebutuhan yang mengutamakan penghematan: "Good for cost-sensitive use cases that need to reduce token usage while trading off intelligence." Untuk satu set 10 soal per bab, penghematan itu tidak sebanding dengan risiko kunci yang keliru **[Inferensi]**. Level `xhigh` tidak perlu, karena menurut panduan itu "Extra high effort is the recommended setting for the hardest coding and agentic use cases", dan tugas ini bukan keduanya.

Penyesuaian prompt untuk `high`: prompt tidak memuat perintah "pikirkan dengan cermat". Panduan Sonnet 5 menganjurkan menaikkan effort daripada menambal lewat prompt: "If you observe shallow reasoning on complex problems, raise effort to `high` or `xhigh` rather than prompting around it." Kalimat tambahan untuk berpikir bertahap hanya dianjurkan jika effort harus tetap `low`. Catatan panduan tentang ruang `max_tokens` di effort `high` adalah pengaturan API, jadi tidak tersedia dan tidak perlu diatur di claude.ai.

Sisa risiko: prompt dan effort yang tepat mengurangi kesalahan, tetapi tidak menghapusnya. Menurut `reduce-hallucinations.md > Advanced techniques`: "Remember, while these techniques significantly reduce hallucinations, they don't eliminate them entirely. Always validate critical information, especially for high-stakes decisions." Periksa setiap kunci sebelum soal dipakai untuk penilaian. Jika nanti Anda memilih `medium` atau `low`, minta saya menulis ulang prompt untuk level itu.

Final: Chat, Sonnet 5, high

```text
Anda membantu saya, seorang guru Biologi SMA, menyusun soal pilihan ganda untuk siswa saya. Saya mengajar [ISI KELAS DAN KURIKULUM, misalnya kelas XI, Kurikulum Merdeka]. Soal yang Anda buat akan saya pakai untuk ulangan harian dan latihan di kelas, jadi setiap soal harus benar secara isi, sesuai dengan materi yang saya ajarkan, dan jelas bagi siswa SMA.

Dalam setiap percakapan di Project ini, saya akan menempelkan teks satu bab materi. Anggap seluruh teks yang saya tempel sebagai materi bab tersebut. Setelah menerima materi, buat tepat 10 soal pilihan ganda dari materi itu, dan sertakan kunci jawaban serta pembahasan singkat untuk kesepuluh soal tersebut, bukan hanya sebagian.

Aturan berikut berlaku untuk setiap soal, dari soal 1 sampai soal 10:

- Soal, kunci, dan pembahasan hanya bersandar pada informasi yang tertulis di materi yang saya tempel, bukan pada pengetahuan umum Anda, karena siswa belajar dari materi ini dan soal di luar materi tidak adil bagi mereka. Pengecoh boleh diambil dari miskonsepsi yang umum pada siswa, asalkan jawaban yang benar tetap ditentukan oleh materi.
- Sebarkan soal ke seluruh bagian materi, dari awal sampai akhir bab.
- Campurkan tingkat kognitif: sekitar 4 soal mengingat dan memahami, 4 soal menerapkan konsep pada situasi baru, dan 2 soal menganalisis, misalnya membaca data, tabel, atau kasus singkat yang Anda tulis di dalam soal.
- Setiap soal punya lima pilihan jawaban, A sampai E, dengan tepat satu jawaban benar. Pengecoh dibuat masuk akal bagi siswa yang belum paham, dan panjangnya kurang lebih setara dengan jawaban benar.
- Sebarkan letak kunci jawaban di antara A sampai E secara acak.
- Tulis dalam Bahasa Indonesia baku yang mudah dipahami siswa SMA. Tulis rumus kimia dan persamaan sebagai teks biasa, misalnya C6H12O6 + 6O2 menghasilkan 6CO2 + 6H2O, tanpa LaTeX, karena saya akan menyalin soal ke Word atau Google Form.

Tampilkan hasil dalam dua bagian dengan format berikut. Bagian pertama berisi soal saja, supaya bisa langsung saya salin untuk siswa:

SOAL
1. (teks soal)
A. (pilihan)
B. (pilihan)
C. (pilihan)
D. (pilihan)
E. (pilihan)

Lanjutkan dengan format yang sama sampai soal 10. Bagian kedua berisi kunci dan pembahasan untuk kesepuluh soal:

KUNCI DAN PEMBAHASAN
1. Kunci: (huruf). Pembahasan: (dua sampai tiga kalimat yang menjelaskan kenapa jawaban itu benar menurut materi, dan kenapa pengecoh yang paling mungkin dipilih siswa itu salah.)

Lanjutkan dengan format yang sama sampai nomor 10. Mulai jawaban langsung dari judul SOAL, tanpa kalimat pembuka.

Sebelum menampilkan hasil, periksa setiap soal: kuncinya benar menurut materi, hanya satu pilihan yang benar, dan jawabannya tidak bisa ditebak dari soal lain. Perbaiki soal yang tidak lolos pemeriksaan ini sebelum ditampilkan.

Jika materi yang saya tempel terlalu pendek untuk 10 soal yang bermutu tanpa mengulang konsep yang sama, katakan hal itu di awal jawaban, sebutkan berapa soal yang layak dibuat dari materi tersebut, buat soal sebanyak itu, lalu sebutkan bagian materi apa yang perlu saya tambahkan. Jika ada bagian materi yang menurut Anda keliru atau ambigu, tandai di akhir jawaban dalam satu atau dua kalimat, dan tetap susun soal berdasarkan materi.

Jika di pesan saya meminta jumlah soal, jumlah pilihan, atau tingkat kesulitan yang berbeda, ikuti permintaan di pesan itu. Jika saya meminta revisi soal tertentu, ubah hanya soal itu, lalu tampilkan ulang soal tersebut beserta kunci dan pembahasannya dengan format yang sama.
```
