# Best Prompting for Claude

Skill `/best-prompting` untuk menyusun dan memperbaiki prompt **berdasarkan dokumentasi resmi Anthropic**, jadi ini bukan tebakan atau dari "tips viral". Setiap saran disertai kutipan langsung dari dokumen sumber, sehingga Anda bisa memeriksa sendiri dasarnya.

*English summary: a Claude skill that writes or fixes prompts for Claude Sonnet 5, Opus 5.5, and Fable 5.1 (chat, Cowork, Claude Code), grounded only in Anthropic's official prompting docs bundled in `references/`, with verbatim citations for every claim. Default output language is Indonesian; it follows the user's language otherwise.*

## Apa yang dilakukan skill ini

Panggil `/best-prompting`, lalu jelaskan kebutuhan Anda atau tempel prompt yang ingin diperbaiki. Lalu, skill akan:

1. Membaca seluruh dokumentasi Anthropic di `references/`.
2. Menganalisis kebutuhan Anda, atau mendiagnosis kelemahan prompt lama, dengan kutipan verbatim dan rujukan `nama-file > judul bagian`. Saran yang tidak berdasar dokumen diberi label **[Inferensi]**.
3. Menilai level effort yang tepat (`low` sampai `max`) untuk model dan tugas Anda.
4. Memberikan satu prompt final siap salin, diawali baris penanda seperti `Final: Claude Code, Opus 5.5, high`.

| | Didukung |
|---|---|
| Model | Claude Sonnet 5, Claude Opus 5.5, Claude Fable 5.1 |
| Ekosistem | Chat (claude.ai dan aplikasi), Cowork, Claude Code |
| Bahasa | Indonesia (default), mengikuti bahasa pengguna |

Lihat hasil studi kasusnya di folder [`examples/`](examples/).

## Cara memasang

**claude.ai dan Cowork.** Unduh [`dist/best-prompting.zip`](dist/best-prompting.zip) (klik file, lalu tombol unduh). Di claude.ai buka **Customize > Skills**, klik **+**, pilih **+ Create skill**, lalu **Upload a skill** dan pilih zip tadi. Jangan ganti nama zip maupun folder di dalamnya: nama folder harus sama dengan nama skill. Skill yang sudah diunggah juga tersedia di Cowork dan bisa dinyalakan atau dimatikan di sana. Rujukan resmi: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

**Claude Code.** Jika Anda masuk ke Claude Code dengan akun Claude yang sama, skill yang diunggah di claude.ai ikut termuat (menurut halaman bantuan di atas, perlu Claude Code v2.1.273 atau lebih baru). Cara manual: salin folder `best-prompting/` ke folder skill pribadi Anda.

```bash
git clone https://github.com/asauntung/best-prompting-for-claude.git
mkdir -p ~/.claude/skills
cp -r best-prompting-for-claude/best-prompting ~/.claude/skills/
```

Atau ke `.claude/skills/` di dalam sebuah proyek bila hanya ingin dipakai di proyek itu.

## Cara memakai

Contoh permintaan:

```text
/best-prompting Buatkan instruksi Project di claude.ai untuk membantu saya menulis caption Instagram dari catatan produk. Model Sonnet 5.
```

```text
/best-prompting Perbaiki prompt ini untuk Claude Code, Opus 5.5, effort high:
[tempel prompt Anda]
```

Sebutkan **model** (wajib) dan **ekosistem**. Effort boleh tidak disebut: skill akan mengusulkannya. Jika model atau ekosistem tidak jelas, skill akan bertanya dulu.

## Batasan yang perlu Anda tahu

- Skill ini sengaja hanya berpijak pada dokumen di `references/`. Kalau dokumen tidak membahas sesuatu, skill akan mengatakannya, bukan mengarang.
- Membaca seluruh referensi (sekitar 250 KB) memakan cukup banyak token di setiap pemanggilan. Itu harga dari analisis yang bisa dipertanggungjawabkan.
- Dokumentasi Anthropic terus berubah. Tanggal pengambilan tercantum di header setiap file referensi dan di [`CHANGELOG.md`](CHANGELOG.md).
- Prompt yang baik tidak menggantikan pilihan model dan effort yang tepat. Skill akan menyebut sisa risiko yang tidak bisa ditutup oleh prompt.

## Isi repo

| Path | Isi |
|---|---|
| `best-prompting/` | Skill itu sendiri: `SKILL.md` dan `references/` |
| `dist/best-prompting.zip` | Skill siap unggah |
| `examples/` | Studi kasus: contoh keluaran dan peragaan skill |
| `evals/` | Kasus uji dan cara menguji skill |
| `scripts/` | Pemutakhiran referensi, pemeriksa keluaran, pembuat zip |
| `MAINTAINING.md` | Prosedur saat Anthropic memperbarui dokumen atau merilis model baru |

## Lisensi dan atribusi

Tulisan asli di repo ini (SKILL.md, skrip, contoh, evals, dokumentasi) berlisensi [MIT](LICENSE). File di `best-prompting/references/` dan `evals/references/` adalah salinan dokumentasi Anthropic dan **tidak** termasuk lisensi MIT; lihat [`NOTICE.md`](NOTICE.md). Proyek ini tidak berafiliasi dengan, dan tidak didukung oleh, Anthropic.
