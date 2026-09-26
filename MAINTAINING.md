# Memelihara skill ini

Dokumentasi Anthropic berubah beberapa kali dalam setahun, dan model baru terus dirilis. Prosedur di bawah menjaga skill tetap mutakhir. Semua skrip hanya butuh Python 3.9 ke atas, tanpa pustaka tambahan.

## A. Anthropic memperbarui dokumen yang sudah ada

1. Unduh ulang dan konversi semua referensi:

   ```bash
   python3 scripts/update_references.py
   ```

   Skrip mengambil versi Markdown tiap halaman (URL halaman + `.md`), mengubah komponen situs ke format GitHub, memasang ulang semua `[CATATAN LOKAL]`, dan menulis header dengan tanggal hari ini.

2. Jika skrip berhenti dengan pesan "judul ... ditemukan 0 kali", berarti Anthropic mengganti judul bagian yang diberi catatan. Buka `scripts/local_notes.json`, sesuaikan `heading` dengan judul baru, lalu jalankan lagi. Periksa juga apakah isi catatan itu masih benar.

3. Baca perubahannya dengan `git diff`. Perhatikan terutama:
   - bagian baru yang menyebut model lama dan perlu diberi `[CATATAN LOKAL]`;
   - bagian lama yang diberi catatan tapi kini sudah diperbarui Anthropic, sehingga catatannya perlu dihapus;
   - perubahan anjuran effort di panduan model.

4. Uji ulang (lihat bagian D), bangun ulang zip, perbarui `CHANGELOG.md`.

## B. Anthropic merilis model baru

1. Tambahkan halaman panduan model baru ke daftar `PAGES` di `scripts/update_references.py`, lalu jalankan skripnya.
2. Perbarui tabel di bagian 1 `SKILL.md` (nama model, panduan, induk). Tabel itu satu-satunya tempat daftar model ditulis. Pemeriksa keluaran juga membaca daftar model dari tabel itu.
3. Perbarui tabel isi `references/` di bagian 2 `SKILL.md`, `description` di frontmatter, dan README.
4. Jika model lama tidak lagi didukung, hapus dari tabel dan dari `PAGES`, lalu hapus file referensinya.
5. Tinjau ulang semua `[CATATAN LOKAL]`: rujukan silang ke panduan model mungkin perlu ditambah.

## C. Mengubah atau menambah `[CATATAN LOKAL]`

Jangan mengedit file di `references/` dengan tangan, karena perubahan akan hilang saat skrip dijalankan lagi. Edit `scripts/local_notes.json`, lalu jalankan `python3 scripts/update_references.py`. Setiap catatan terdiri dari nama file, judul bagian yang persis sama dengan dokumen, dan paragraf catatan.

## D. Menguji dan merilis

1. Jalankan kasus uji di `evals/README.md` dengan skill versi baru, minimal kasus bertanda wajib.
2. Periksa keluaran dan contoh:

   ```bash
   python3 scripts/check_output.py examples/*.md
   ```

3. Bila perilaku skill berubah, perbarui contoh di `examples/` dengan menjalankan ulang skill.
4. Bangun zip, lalu commit:

   ```bash
   python3 scripts/build_zip.py
   ```

5. Catat perubahan di `CHANGELOG.md` dan naikkan versi.
