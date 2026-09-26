# Changelog

## v1.1.1 (2026-09-26)

- Skill diganti nama dari `prompting-claude` menjadi `best-prompting`, dipanggil dengan `/best-prompting`. Nama lama ditolak saat diunggah ke claude.ai karena kolom `name` tidak boleh memuat kata "claude" atau "anthropic".
- Folder skill kini `best-prompting/` dan zip siap unggah kini `dist/best-prompting.zip`.

## v1.1.0 (2026-09-26)

- `SKILL.md`: bagian baru 7 tentang prompt yang ringkas. Potongan referensi dipakai hanya bila gejalanya ada, satu instruksi singkat menggantikan daftar kasus, alasan diberikan sekali, tiap aturan ditulis sekali, dan memadatkan tidak boleh merumuskan ulang kalimat kriteria. Bagian sesudahnya bergeser nomor.
- Mode B kini juga mendiagnosis kelebihan, dan membuang dihitung sebagai perbaikan.
- Analisis ditutup dengan jumlah kata prompt, dan di Mode B dibandingkan dengan prompt lama.
- Ditambahkan contoh 4: memadatkan prompt yang gemuk (Claude Code, Fable 5.1).

## v1.0.0 (2026-09-26)

Rilis publik pertama.

- Skill diberi nama `prompting-claude` dan dipanggil dengan `/prompting-claude`.
- Model yang didukung: Claude Sonnet 5, Claude Opus 5.5, Claude Fable 5.1. Daftar model kini ditulis di satu tabel di `SKILL.md`.
- Referensi diambil ulang dari dokumentasi Anthropic per 2026-09-26. `prompting-best-practices.md` versi baru sudah mencakup Fable 5.1 dan Opus 5.5.
- Referensi dikonversi ke format GitHub (link absolut, tanpa komponen MDX) dan diberi header sumber seragam.
- Sisipan `[CATATAN LOKAL]` diperbarui untuk struktur dokumen baru dan disimpan di `scripts/local_notes.json`.
- Halaman "Define success criteria and build evaluations" kini bernama `develop-tests` dan dipindah ke `evals/references/`, tidak lagi dibaca skill di setiap pemanggilan.
- `SKILL.md`: ekosistem boleh disimpulkan dari konteks, kutipan dibatasi satu per klaim, bahasa mengikuti pengguna, asumsi pengguna non-programmer dijadikan default yang bisa disesuaikan, dan prompt gambar dikecualikan dari pemicu.
- Ditambahkan: studi kasus, kasus uji, pemeriksa keluaran otomatis, pembuat zip, dan prosedur pemeliharaan.
