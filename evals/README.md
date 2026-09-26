# Menguji skill /best-prompting

Tujuan folder ini: memastikan skill tetap berperilaku benar setelah referensi diperbarui, model baru ditambahkan, atau `SKILL.md` diubah. Prinsipnya mengikuti dokumen Anthropic yang disertakan di [`references/develop-tests.md`](references/develop-tests.md): tetapkan kriteria keberhasilan yang spesifik dan terukur, lalu uji dengan kasus yang mencakup situasi normal dan tepi.

Dokumen `develop-tests.md` sengaja disimpan di sini, bukan di `best-prompting/references/`, supaya tidak ikut dibaca skill di setiap pemanggilan.

## Cara menjalankan

1. Buka percakapan baru dengan skill terpasang. Satu kasus, satu percakapan.
2. Kirim "Input" dari kasus di [`kasus-uji.md`](kasus-uji.md) apa adanya.
3. Simpan keluaran skill ke `evals/hasil/<ID>.md` (folder ini tidak perlu di-commit).
4. Untuk kasus yang menghasilkan prompt, jalankan pemeriksa otomatis:

   ```bash
   python3 scripts/check_output.py evals/hasil/*.md
   ```

5. Nilai kriteria manual di tiap kasus: lulus atau gagal, dengan catatan singkat.

## Dua lapis penilaian

**Otomatis** (`scripts/check_output.py`): baris Final sah dan tepat sebelum codeblock, tepat satu codeblock `text`, tidak ada teks sesudahnya, tidak ada em-dash, tidak ada mekanik API atau prefill di prompt, rujukan `nama-file > bagian` ada dan menunjuk file yang benar-benar ada, serta peringatan kemungkinan hard wrap.

**Manual** (rubrik per kasus): ketepatan kutipan, relevansi analisis, penilaian effort, dan kepatuhan pada perilaku yang diharapkan. Untuk ketepatan kutipan, ambil dua kutipan secara acak dan cari dengan fitur pencarian di file referensinya. Kutipan yang tidak ditemukan persis berarti gagal.

## Ambang rilis

Semua kasus bertanda **[wajib]** harus lulus sebelum versi baru dirilis. Kasus lain dicatat hasilnya di `CHANGELOG.md` bila gagal.
