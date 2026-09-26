# Kasus uji

Setiap kasus berisi input yang dikirim apa adanya, perilaku yang diharapkan, dan kriteria lulus.

## Parameter dan cakupan

### K01 [wajib] Model tidak disebut

Input:
```text
/prompting-claude Buatkan prompt untuk meringkas notulen rapat mingguan kantor saya.
```
Diharapkan: skill bertanya model mana (dan ekosistem, dalam pertanyaan yang sama) lalu berhenti.
Lulus jika: tidak ada analisis maupun prompt sebelum pengguna menjawab, dan pertanyaan diajukan dalam satu kali bertanya.

### K02 [wajib] Model di luar cakupan

Input:
```text
/prompting-claude Buatkan prompt untuk Claude Haiku 4.5 di chat, untuk menerjemahkan email ke bahasa Inggris.
```
Diharapkan: skill menyatakan hanya melayani Sonnet 5, Opus 5.5, dan Fable 5.1, lalu bertanya model mana yang dimaksud.
Lulus jika: tidak ada prompt yang dihasilkan untuk Haiku 4.5.

### K03 Ekosistem bisa disimpulkan

Input:
```text
/prompting-claude Tolong buatkan isi CLAUDE.md untuk repo skripsi saya supaya Claude selalu memakai gaya sitasi APA dan tidak mengubah folder data/. Model Sonnet 5.
```
Diharapkan: ekosistem disimpulkan sebagai Claude Code tanpa bertanya, dan kesimpulan itu dinyatakan di analisis.
Lulus jika: baris Final berbunyi `Final: Claude Code, Sonnet 5, <effort>` dan analisis menyebut dasar kesimpulannya.

### K04 Bukan untuk prompt gambar

Input:
```text
Buatkan prompt Nano Banana untuk ilustrasi secangkir kopi di meja kayu.
```
Diharapkan: skill /prompting-claude tidak terpicu (atau, jika dipanggil paksa, menyatakan bahwa skill ini bukan untuk prompt gambar).
Lulus jika: tidak ada keluaran berformat skill ini.

## Effort

### K05 [wajib] Effort tidak disebut

Input:
```text
/prompting-claude Buatkan prompt untuk Claude Code, model Fable 5.1, untuk mengubah 200 file CSV penjualan menjadi satu laporan ringkasan bulanan.
```
Diharapkan: skill mengusulkan effort dengan kutipan dari bagian effort `prompting-claude-fable-5-1.md`.
Lulus jika: bagian Effort memuat kutipan verbatim dari panduan Fable 5.1 dan baris Final memuat effort usulan itu.

### K06 Effort pengguna kurang tepat

Input:
```text
/prompting-claude Prompt untuk Cowork, Opus 5.5, effort low: riset mendalam 20 jurnal tentang pupuk organik lalu tulis tinjauan pustaka 10 halaman.
```
Diharapkan: skill menilai `low` untuk tugas riset panjang ini berdasarkan bagian effort panduan Opus 5.5 dan induknya, bukan dari ingatan. Referensi menyebut `medium` sebagai default Opus 5.5 dan `low` "comes close" pada sebagian evaluasi coding, jadi kesimpulannya harus dibangun dari kutipan, bukan dari anggapan bahwa effort rendah selalu buruk.
Lulus jika: penilaian effort disertai kutipan verbatim dari `prompting-claude-opus-5-5.md > Calibrate effort` atau panduan induknya; bila skill mengusulkan level lain, baris Final memakai level usulan itu dan skill menegaskan keputusan tetap di tangan pengguna.

### K07 [wajib] Pengguna menolak usulan effort (lanjutan K06)

Jalankan hanya jika di K06 skill mengusulkan level selain `low`.

Input (di percakapan yang sama setelah K06):
```text
Saya tetap mau low karena kuota terbatas.
```
Diharapkan: prompt ditulis ulang untuk `low`, dengan penyesuaian khusus effort rendah dari referensi dan sisa risikonya.
Lulus jika: baris Final berbunyi `Final: Cowork, Opus 5.5, low` dan analisis menyebut penyesuaian serta sisa risiko.

## Mode B dan teknik usang

### K08 [wajib] Prompt lama memakai prefill

Input:
```text
/prompting-claude Perbaiki prompt ini untuk chat, Sonnet 5:

Jawab dalam format JSON. Assistant: {"hasil": 
```
Diharapkan: skill mendiagnosis prefill sebagai teknik yang tidak berfungsi, merujuk `[CATATAN LOKAL]` dan `prompting-best-practices.md > Migrating away from prefilled responses`, lalu memakai pengganti yang bisa dipakai di chat.
Lulus jika: prompt final tidak memuat prefill, dan diagnosisnya disertai rujukan.

### K09 Prompt berhuruf kapital dan bernada mendesak

Input:
```text
/prompting-claude Perbaiki untuk Claude Code, Opus 5.5: KAMU HARUS SELALU MEMAKAI TOOL SEARCH. WAJIB!!! JANGAN PERNAH LUPA.
```
Diharapkan: skill mendiagnosis bahasa berintensitas tinggi dengan rujukan dari referensi, mempertahankan maksud (memakai pencarian), dan memberi alasan alih-alih perintah keras.
Lulus jika: maksud asli terjaga, dan diagnosis punya kutipan. Bila mengutip bagian yang diberi `[CATATAN LOKAL]` khusus model lama, analisis mencatat hal itu.

## Ekosistem dan inferensi

### K10 [wajib] Label [Inferensi] untuk Cowork

Input:
```text
/prompting-claude Prompt untuk Cowork, Fable 5.1, effort high: baca semua email klien minggu ini dan buat daftar tindak lanjut di spreadsheet.
```
Diharapkan: pemetaan Cowork ke kerja agentik lintas aplikasi diberi label **[Inferensi]**, dan risiko prompt injection dari isi email dibahas dengan rujukan ke `mitigate-jailbreaks-and-prompt-injections.md`.
Lulus jika: kedua hal itu ada.

### K11 Pengguna developer menanyakan mekanik API

Input:
```text
/prompting-claude Saya pakai Claude di chat, Opus 5.5. Berapa max_tokens yang harus saya taruh di prompt supaya jawabannya panjang?
```
Diharapkan: skill menjelaskan bahwa `max_tokens` adalah parameter API yang tidak bisa diatur dari prompt di chat, lalu menawarkan pendekatan yang bisa dikendalikan pengguna.
Lulus jika: prompt final tidak memuat `max_tokens`.

## Bahasa

### K12 Pengguna berbahasa Inggris

Input:
```text
/prompting-claude Write me a system prompt for a customer-support chat Project on claude.ai. Model: Sonnet 5.
```
Diharapkan: analisis dan prompt dalam bahasa Inggris, kutipan tetap verbatim.
Lulus jika: seluruh keluaran berbahasa Inggris dan format empat bagian tetap utuh.
