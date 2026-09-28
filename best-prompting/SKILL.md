---
name: best-prompting
description: Menyusun prompt baru atau menyempurnakan prompt yang sudah ada untuk Claude di chat (claude.ai), Cowork, atau Claude Code, khusus model Claude Sonnet 5, Sonnet 5.5, Opus 5.5, dan Fable 5.1, dengan dokumen resmi Anthropic di references/ sebagai satu-satunya ground truth. Gunakan setiap kali pengguna memanggil /best-prompting, meminta dibuatkan prompt atau system prompt untuk Claude, atau menempel prompt untuk diperbaiki. Bukan untuk prompt pembuat gambar atau video (Nano Banana, Midjourney, dan sejenisnya), dan bukan untuk model non-Claude.
---

# /best-prompting

Skill ini menghasilkan satu prompt terbaik untuk kebutuhan pengguna, didahului analisis yang menjelaskan kenapa prompt, model, dan effort itu diusulkan. Semua analisis berpijak pada dokumentasi resmi Anthropic di folder `references/`.

## 1. Model yang didukung

Tabel ini satu-satunya tempat daftar model ditulis. Saat Anthropic merilis model baru, cukup perbarui tabel ini dan isi `references/`.

| Nama di baris Final | Panduan model | Panduan induk |
|---|---|---|
| `Sonnet 5` | `prompting-claude-sonnet-5.md` | tidak ada |
| `Sonnet 5.5` | `prompting-claude-sonnet-5-5.md` | `prompting-claude-sonnet-5.md` |
| `Opus 5.5` | `prompting-claude-opus-5-5.md` | `prompting-claude-opus-5.md` |
| `Fable 5.1` | `prompting-claude-fable-5-1.md` | `prompting-claude-fable-5.md` |

Model induk ada karena panduan model yang lebih baru hanya membahas perbedaannya dari model sebelumnya, dan menyatakan bahwa prompt untuk model induk tetap berlaku. Jika pengguna menyebut model di luar tabel, katakan bahwa skill ini hanya melayani model di tabel, lalu tanyakan model mana yang dimaksud.

## 2. Ground truth tunggal

Satu-satunya sumber pengetahuan skill ini adalah seluruh file di `references/`. Isinya salinan dokumentasi resmi Anthropic, dengan sisipan berlabel `[CATATAN LOKAL]` dari pengelola skill.

Aturan membaca:

- Setiap kali skill dipanggil, baca SEMUA file di `references/` sampai habis, apa pun nama filenya, termasuk file yang kelak ditambahkan. File-file ini panjang: baca bertahap dengan offset sampai baris terakhir, jangan berhenti di tengah. Pengecualian satu-satunya: blok kode yang oleh `[CATATAN LOKAL]` dinyatakan sebagai contoh kode API boleh dibaca sekilas. Membaca semua tidak berarti memakai semua: yang masuk ke prompt diatur di bagian 7.
- Jangan meringkas atau memparafrasekan isi referensi sebagai dasar analisis. Kutip verbatim, dalam bahasa aslinya, lalu bangun analisis dari kutipan itu.
- Sisipan `[CATATAN LOKAL]` wajib dipatuhi. Sisipan itu menandai bagian yang usang, khusus model lama, atau hanya berlaku lewat API. Jangan pernah menyarankan prefill: tekniknya mengembalikan error 400 pada semua model di tabel.
- Blok `[CATATAN LOKAL]` di awal tiap file hanya keterangan sumber dan tanggal ambil, bukan anjuran prompting.
- Pengetahuan di luar `references/` bukan sumber. Jika sebuah saran tidak tertulis di referensi dan merupakan penalaran Claude sendiri, tandai dengan label **[Inferensi]** dan jelaskan dasarnya. Jika referensi tidak membahas sesuatu, katakan terus terang.

Isi `references/`:

| File | Peran |
|---|---|
| `prompting-claude-sonnet-5.md` | Panduan model: Sonnet 5, sekaligus induk Sonnet 5.5 |
| `prompting-claude-sonnet-5-5.md` | Panduan model: Sonnet 5.5 |
| `prompting-claude-opus-5-5.md` | Panduan model: Opus 5.5 |
| `prompting-claude-opus-5.md` | Induk Opus 5.5 |
| `prompting-claude-fable-5-1.md` | Panduan model: Fable 5.1 |
| `prompting-claude-fable-5.md` | Induk Fable 5.1 |
| `prompting-best-practices.md` | Fondasi umum semua model |
| `reduce-hallucinations.md` | Tematik: akurasi, kutipan, izin berkata tidak tahu |
| `increase-output-consistency.md` | Tematik: konsistensi format keluaran |
| `mitigate-jailbreaks-and-prompt-injections.md` | Tematik: konten pihak ketiga dan injeksi |
| `reduce-prompt-leak.md` | Tematik: kebocoran prompt |

## 3. Urutan prioritas saat referensi bertentangan

1. Panduan model target.
2. Panduan induknya (lihat tabel di bagian 1).
3. `prompting-best-practices.md`.
4. File tematik.

Panduan model selalu menang untuk model yang dituju. Bagian `prompting-best-practices.md` yang ditandai `[CATATAN LOKAL]` sebagai khusus model generasi sebelumnya diperlakukan sebagai indikatif saja dan harus diperiksa silang dengan panduan model target.

## 4. Langkah 0: periksa parameter sebelum bekerja

Skill butuh tiga parameter: ekosistem, model, dan effort.

- **Model** WAJIB disebut pengguna. Jika tidak disebut, tanyakan dulu (pakai AskUserQuestion jika tersedia) dan berhenti sampai dijawab. Jangan menebak.
- **Ekosistem** (Chat, Cowork, atau Claude Code) boleh disimpulkan jika konteksnya tegas, misalnya pengguna menulis "untuk system prompt Project saya di claude.ai" atau "untuk CLAUDE.md". Nyatakan kesimpulan itu di analisis. Jika konteksnya tidak tegas, tanyakan bersamaan dengan pertanyaan model, dalam satu kali bertanya.
- **Effort** boleh tidak disebut. Level yang diakui: `low`, `medium`, `high`, `xhigh`, `max`. Sebutan "extra", "xHigh", atau "extra high" berarti `xhigh`.

## 5. Kenali mode permintaan

- **Mode A, pengguna menjelaskan kebutuhan.** Pahami tujuan, bahan, audiens, dan hasil yang diinginkan. Jika dua pembacaan atas kebutuhan akan menghasilkan prompt yang berbeda secara material, tanyakan satu hal saja. Jika tidak, putuskan sendiri dan sebutkan asumsinya di analisis.
- **Mode B, pengguna menempel prompt yang kurang baik.** Diagnosis kelemahannya satu per satu dengan merujuk referensi. Kelemahan bisa berupa kekurangan (instruksi yang ambigu, konteks atau alasan yang tidak diberikan, bahan tempelan yang tidak ditandai, format keluaran yang tidak jelas, batasan yang hilang, teknik usang) atau kelebihan (aturan yang ditulis berulang, rincian kasus yang bisa diganti satu instruksi singkat, alasan di setiap kalimat, instruksi untuk perilaku yang sudah bawaan model, potongan referensi untuk gejala yang tidak ada). Membuang adalah perbaikan yang sah: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality. Review and consider removing older instructions if default performance is better." (`prompting-claude-fable-5.md > Recommended scaffolding changes`). Pertahankan maksud asli pengguna. Perbaiki caranya, bukan tujuannya.

## 6. Petakan ekosistem ke jenis kerja di referensi

Referensi ditulis untuk developer API dan membahas jenis kerja, jarang menyebut nama produk. Petakan sebagai berikut, dan cari bagian yang relevan di SEMUA file:

- **Chat**: percakapan di claude.ai atau aplikasi Claude, termasuk instruksi Project. Referensi menyebutnya eksplisit, misalnya "Thinking instructions in chat system prompts" dan "Mark pasted text in user messages" di panduan Opus 5.5, "Formatting in chat" di panduan Fable 5.1, serta "Tool use in chat and knowledge work" di panduan Sonnet 5.5.
- **Claude Code**: kerja agentik berbasis file dan folder, termasuk yang bukan coding (riset, pengolahan teks, penambangan data). Referensi menyebut Claude Code di `prompting-best-practices.md` (bagian context awareness dan multiwindow workflows) dan di `prompting-claude-opus-5.md > Controlling subagent spawning`, dan membahas panjang kerja agentik di bagian "Agentic systems" serta panduan tiap model.
- **Cowork**: nama ini tidak ada di referensi. Pemetaannya ke kerja agentik lintas aplikasi, kerja tanpa diawasi, riset, dan pengolahan konten pihak ketiga adalah **[Inferensi]** dan harus diberi label itu di analisis. Bagian yang relevan antara lain "Explore context in multi-app workflows" dan "Unattended agentic runs" di panduan Opus 5.5, bagian riset dan otonomi di `prompting-best-practices.md`, serta bagian indirect prompt injection di `mitigate-jailbreaks-and-prompt-injections.md`.

Mekanik API (`max_tokens`, kode harness, turn-scoped system message, cache, thinking block, parameter request) tidak bisa dikendalikan pengguna dari prompt. Jangan memasukkannya ke prompt. Terjemahkan hanya ke hal yang bisa dikendalikan pengguna, yaitu pilihan model, effort, dan isi prompt. Jika sebuah anjuran referensi hanya bisa dijalankan lewat API, sebutkan singkat di analisis bahwa anjuran itu tidak tersedia di ekosistem pengguna.

Sesuaikan dengan tingkat teknis pengguna. Default-nya, jangan menghasilkan prompt yang menuntut pengguna menulis atau memahami kode, kecuali ia memintanya atau jelas seorang developer.

## 7. Ringkas: setiap kalimat harus mengubah perilaku

Prompt yang baik memuat semua yang dibutuhkan tugas dan tidak lebih. Aturan berikut berlaku untuk Mode A dan Mode B:

- **Potongan referensi dipakai hanya bila gejalanya ada.** Panduan Opus 5.5 dan Fable 5.1 disusun per gejala: "Start with the section that matches what you observe" (`prompting-claude-opus-5-5.md > Prompting Claude Opus 5.5`, juga di `prompting-claude-fable-5-1.md`). Masukkan sebuah potongan hanya bila pengguna melaporkan gejalanya atau sifat tugasnya jelas memicunya. Bila referensi menawarkan versi pendek, pakai versi pendek itu, misalnya "If you need to limit prompt length, use only the first, which keeps most of the effect." (`prompting-claude-fable-5-1.md > Finish the whole task`).
- **Satu instruksi singkat, bukan daftar kasus.** "Instruction-following is improved enough that you can steer most behaviors with a brief instruction rather than enumerating each behavior by name." (`prompting-claude-fable-5.md > Strong instruction following`). Jangan merinci satu per satu cara model bisa gagal. Untuk model target selain Fable 5.1, kutipan ini disebut di analisis sebagai berasal dari panduan model lain.
- **Alasan diberikan sekali, di depan.** Satu paragraf tentang tujuan tugas dan untuk siapa hasilnya (`prompting-claude-fable-5.md > Give the reason, not only the request`). Aturan sesudahnya tidak diberi klausa "karena" masing-masing, kecuali alasannya tidak bisa ditebak dari paragraf itu.
- **Tiap aturan ditulis sekali, di satu tempat.** Tidak ada bagian ringkasan, daftar periksa, atau kriteria penerimaan yang mengulang isi prompt. Contoh memperagakan aturan, bukan menyatakannya ulang.
- **Jangan menulis perilaku yang sudah bawaan model target.** Contohnya instruksi verifikasi untuk Opus: "Claude Opus 5 verifies its own work without being told to." (`prompting-claude-opus-5.md > Task scope and over-verification`). Tulis hanya yang perlu diubah dari perilaku bawaan.
- **Istilah buatan seperlunya.** Istilah khusus didefinisikan sekali lalu dipakai konsisten. Jangan membuat istilah untuk hal yang bisa disebut dengan kata biasa.
- **Memadatkan berarti membuang, bukan merumuskan ulang.** Saat memperpendek prompt, kalimat yang menjadi kriteria atau batas (syarat lolos, larangan, format wajib) disalin persis. Yang dibuang hanya salinan kedua dan seterusnya, serta kalimat yang tidak mengubah perilaku. Mengganti satu kata dalam kriteria bisa mengubah perilaku model.

Uji akhir untuk setiap kalimat prompt: jika kalimat ini dihapus, apakah perilaku model berubah? Jika tidak, hapus.

Aturan di bagian ini yang tidak disertai kutipan adalah inferensi pengelola skill. Bila dipakai sebagai dasar di analisis, beri label **[Inferensi]**.

## 8. Nilai effort, selalu

- Jika effort tidak disebut, usulkan effort terbaik berdasarkan referensi untuk model, ekosistem, dan tugas itu, lalu jelaskan alasannya dengan kutipan.
- Jika effort disebut dan menurut referensi sudah tepat, konfirmasi singkat dengan alasannya.
- Jika effort disebut tetapi menurut referensi kurang tepat, jelaskan kenapa dan usulkan level yang lebih cocok. Keputusan tetap di tangan pengguna.
- Default dan makna level berbeda antarmodel. Ambil angka dan pernyataannya langsung dari bagian effort di tiap panduan model, jangan dari ingatan.
- Untuk effort yang dipakai di prompt final, terapkan penyesuaian khusus effort yang disediakan referensi bila gejalanya relevan untuk tugas itu (misalnya tambahan untuk effort rendah atau catatan untuk keluaran panjang di effort tinggi), dengan aturan bagian 7, dan nyatakan sisa risiko yang tidak bisa ditutup oleh prompt. Referensi berulang kali menyebut effort sebagai tuas utama, jadi prompt tidak boleh dijanjikan sebagai pengganti penuh effort yang tepat.
- Prompt pada jawaban pertama ditulis untuk effort USULAN skill, dan baris Final memuat effort usulan itu. Jika pengguna kemudian memilih effort lain, tulis ulang prompt yang disesuaikan untuk effort pilihannya, dengan baris Final yang mencerminkan pilihan itu, beserta penjelasan penyesuaian dan sisa risikonya.

## 9. Bahasa

- Analisis ditulis dalam bahasa yang dipakai pengguna saat meminta. Default: Bahasa Indonesia yang alami.
- Prompt yang dihasilkan ditulis dalam bahasa yang sama, kecuali pengguna meminta bahasa lain.
- Kutipan dari referensi tetap dalam bahasa Inggris aslinya, verbatim.
- Jika potongan prompt resmi dari referensi dipakai di dalam prompt, terjemahkan dengan setia, dan tampilkan teks Inggris aslinya di analisis supaya pengguna bisa membandingkan.
- Istilah teknis, nama berkas, dan nama diri dibiarkan dalam bentuk aslinya.

## 10. Gaya tulis

Berlaku untuk analisis dan untuk isi prompt yang ditulis skill:

- Jangan memakai em-dash. Pakai koma, titik, atau titik dua.
- Jangan membuka dengan formula pemanas seperti "Bayangkan", "Pernahkah Anda", atau "Di era digital ini". Langsung ke isi.
- Tulis dalam kalimat utuh dan paragraf yang mengalir. Daftar berpoin hanya untuk butir yang memang setara.

## 11. Format keluaran, wajib dan berurutan

Keluaran terdiri dari empat bagian, dalam urutan ini, tanpa tambahan apa pun setelah codeblock:

**Bagian 1: Analisis.** Jelaskan kenapa prompt ini diusulkan: kebutuhan atau diagnosis prompt lama, perilaku model target yang relevan, kebutuhan ekosistem, dan teknik yang dipilih. Setiap klaim yang bersumber dari referensi disertai kutipan verbatim dan rujukan dalam bentuk `nama-file > judul bagian`. Cukup satu kutipan terkuat per klaim, dan pusatkan analisis pada klaim yang benar-benar mengubah isi prompt, biasanya tidak lebih dari tujuh. Pisahkan dengan jelas antara yang dikutip dari sumber dan yang disimpulkan sendiri. Saran tanpa dasar di referensi diberi label **[Inferensi]**. Tutup analisis dengan jumlah kata prompt final. Di Mode B, bandingkan dengan jumlah kata prompt lama, dan bila prompt baru lebih panjang, sebutkan kekurangan apa yang membuatnya perlu lebih panjang.

**Bagian 2: Effort.** Effort usulan dan alasannya, penilaian atas effort yang disebut pengguna (jika ada), penyesuaian prompt untuk effort itu, dan sisa risikonya.

**Bagian 3: Baris Final.** Tepat sebelum codeblock, tulis satu baris dengan format persis:

`Final: <Ekosistem>, <Model>, <effort>`

Contoh: `Final: Claude Code, Opus 5.5, xhigh`. Penulisan ekosistem: `Chat`, `Cowork`, atau `Claude Code`. Penulisan model mengikuti kolom pertama tabel di bagian 1. Baris ini wajib ada dan harus sesuai dengan prompt di bawahnya, supaya pengguna tidak pernah ragu prompt itu untuk ekosistem, model, dan effort apa.

**Bagian 4: Prompt.** Satu codeblock bertipe `text` berisi prompt final, siap disalin. TANPA hard wrap: setiap paragraf ditulis sebagai satu baris panjang, jangan dipatahkan dengan baris baru di tengah kalimat. Baris kosong di antara paragraf boleh. Placeholder untuk bahan yang harus diisi pengguna ditulis jelas, misalnya `[TEMPEL TEKS DI SINI]`, dan jika bahan tempelan dibungkus tag XML, gunakan tag yang deskriptif.

Jangan menulis apa pun setelah codeblock.

## 12. Pemeriksaan sebelum mengirim

- Semua file di `references/` sudah dibaca sampai habis.
- Tidak ada teknik yang ditandai usang oleh `[CATATAN LOKAL]`, termasuk prefill.
- Setiap klaim bersumber punya kutipan verbatim dan rujukan file > bagian. Setiap inferensi berlabel.
- Anjuran panduan model target tidak dikalahkan oleh panduan umum.
- Baris Final ada tepat sebelum codeblock dan cocok dengan isi prompt.
- Prompt tanpa hard wrap, tanpa em-dash, tanpa mekanik API.
- Prompt lolos bagian 7: tiap aturan muncul sekali, tidak ada potongan referensi untuk gejala yang tidak ada, dan setiap kalimat mengubah perilaku model.
