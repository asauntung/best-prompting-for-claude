#!/usr/bin/env python3
"""Unduh ulang dokumentasi resmi Anthropic ke best-prompting/references/.

Langkahnya:
1. Ambil versi Markdown tiap halaman (URL halaman + ".md").
2. Ubah komponen situs (Note, Tip, Accordion, Card, CodeGroup) ke format
   yang tampil rapi di GitHub, tanpa mengubah kata-kata dokumen.
3. Pasang ulang sisipan [CATATAN LOKAL] dari scripts/local_notes.json.
4. Tulis header sumber (URL, tanggal ambil, jumlah sisipan).

Pemakaian:
    python3 scripts/update_references.py            # unduh dari internet
    python3 scripts/update_references.py --offline DIR   # pakai file .md yang sudah diunduh

Hanya memakai pustaka standar Python 3.9+.
"""

import argparse
import datetime
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_REFS = ROOT / "best-prompting" / "references"
EVAL_REFS = ROOT / "evals" / "references"
NOTES_FILE = ROOT / "scripts" / "local_notes.json"
DOCS = "https://platform.claude.com/docs/en/"

# (nama file lokal, path halaman, folder tujuan)
PAGES = [
    ("prompting-claude-sonnet-5-5.md", "build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5", SKILL_REFS),
    ("prompting-claude-sonnet-5.md", "build-with-claude/prompt-engineering/prompting-claude-sonnet-5", SKILL_REFS),
    ("prompting-claude-opus-5-5.md", "build-with-claude/prompt-engineering/prompting-claude-opus-5-5", SKILL_REFS),
    ("prompting-claude-opus-5.md", "build-with-claude/prompt-engineering/prompting-claude-opus-5", SKILL_REFS),
    ("prompting-claude-fable-5-1.md", "build-with-claude/prompt-engineering/prompting-claude-fable-5-1", SKILL_REFS),
    ("prompting-claude-fable-5.md", "build-with-claude/prompt-engineering/prompting-claude-fable-5", SKILL_REFS),
    ("prompting-best-practices.md", "build-with-claude/prompt-engineering/claude-prompting-best-practices", SKILL_REFS),
    ("reduce-hallucinations.md", "test-and-evaluate/strengthen-guardrails/reduce-hallucinations", SKILL_REFS),
    ("increase-output-consistency.md", "test-and-evaluate/strengthen-guardrails/increase-consistency", SKILL_REFS),
    ("mitigate-jailbreaks-and-prompt-injections.md", "test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks", SKILL_REFS),
    ("reduce-prompt-leak.md", "test-and-evaluate/strengthen-guardrails/reduce-prompt-leak", SKILL_REFS),
    ("develop-tests.md", "test-and-evaluate/develop-tests", EVAL_REFS),
]

ALERTS = {"Note": "NOTE", "Tip": "TIP", "Info": "NOTE", "Warning": "WARNING", "Check": "TIP"}
FENCE = re.compile(r"^\s*(```|~~~)")
ATTR = re.compile(r'(\w+)="([^"]*)"')


def fetch(page_path: str) -> str:
    req = urllib.request.Request(DOCS + page_path + ".md", headers={"User-Agent": "best-prompting-updater/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def split_frontmatter(text: str):
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        meta = {}
        for line in text[4:end].splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        return meta, text[end + 5:]
    return {}, text


def convert_mdx(body: str) -> str:
    """Ubah komponen MDX ke Markdown GitHub. Isi di dalam blok kode tidak disentuh."""
    out = []
    stack = []  # tiap elemen: jenis komponen ("quote", "details", "wrap")
    in_fence = False
    card = None  # [judul, href, isi]

    def depth_indent():
        return "  " * len(stack)

    def quote_prefix():
        return "> " * sum(1 for kind in stack if kind == "quote")

    def emit(line):
        prefix = quote_prefix()
        out.append((prefix + line).rstrip() if prefix else line)

    for raw in body.splitlines():
        # buang indentasi yang berasal dari komponen pembungkus
        indent = depth_indent()
        line = raw[len(indent):] if raw.startswith(indent) else raw.lstrip()

        if in_fence:
            emit(line)
            if FENCE.match(line):
                in_fence = False
            continue

        if card is not None:
            if line.strip().startswith("</Card>"):
                title, href, parts = card
                desc = " ".join(p.strip().rstrip("\\").strip() for p in parts if p.strip().rstrip("\\").strip())
                emit(f"- **[{title}]({href})**: {desc}" if desc else f"- **[{title}]({href})**")
                card = None
            else:
                card[2].append(line)
            continue

        stripped = line.strip()
        if FENCE.match(line):
            in_fence = True
            emit(line)
            continue

        m = re.fullmatch(r"<(Note|Tip|Info|Warning|Check)>", stripped)
        if m:
            emit(f"> [!{ALERTS[m.group(1)]}]")
            stack.append("quote")
            continue
        if re.fullmatch(r"</(Note|Tip|Info|Warning|Check)>", stripped):
            stack.pop()
            emit("")
            continue
        m = re.fullmatch(r"<Accordion(\s[^>]*)?>", stripped)
        if m:
            attrs = dict(ATTR.findall(m.group(1) or ""))
            opened = " open" if "defaultOpen" in (m.group(1) or "") else ""
            emit(f"<details{opened}>")
            emit(f"<summary>{attrs.get('title', 'Detail')}</summary>")
            emit("")
            stack.append("details")
            continue
        if stripped == "</Accordion>":
            stack.pop()
            emit("")
            emit("</details>")
            emit("")
            continue
        if re.fullmatch(r"<(AccordionGroup|CardGroup|CodeGroup)(\s[^>]*)?>", stripped):
            stack.append("wrap")
            continue
        if re.fullmatch(r"</(AccordionGroup|CardGroup|CodeGroup)>", stripped):
            stack.pop()
            continue
        m = re.fullmatch(r"<Card(\s[^>]*)?>(.*?)(</Card>)?", stripped)
        if m:
            attrs = dict(ATTR.findall(m.group(1) or ""))
            card = [attrs.get("title", ""), attrs.get("href", ""), [m.group(2)]]
            if m.group(3):
                line = "</Card>"
                title, href, parts = card
                desc = " ".join(p.strip() for p in parts if p.strip())
                emit(f"- **[{title}]({href})**: {desc}" if desc else f"- **[{title}]({href})**")
                card = None
            continue

        emit(line)

    if stack or in_fence or card is not None:
        raise ValueError(f"komponen tidak tertutup: stack={stack}, fence={in_fence}, card={card is not None}")

    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def leftover_components(body: str):
    found, in_fence = [], False
    for line in body.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            found += re.findall(r"</?(?:Note|Tip|Info|Warning|Check|Accordion\w*|Card\w*|CodeGroup|Tabs?|Steps?|Frame)\b", line)
    return found


def insert_notes(body: str, notes):
    lines = body.splitlines()
    for note in notes:
        hits = [i for i, l in enumerate(lines) if l.strip() == note["heading"]]
        if len(hits) != 1:
            raise ValueError(f"judul '{note['heading']}' ditemukan {len(hits)} kali di {note['file']} (harus tepat 1)")
        block = [""] + ["> " + t if i == 0 else ">\n> " + t for i, t in enumerate(note["text"])] + [""]
        lines[hits[0] + 1:hits[0] + 1] = "\n".join(block).splitlines()
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def build(name, raw, notes, today):
    meta, body = split_frontmatter(raw)
    body = convert_mdx(body)
    left = leftover_components(body)
    if left:
        raise ValueError(f"{name}: masih ada komponen situs yang belum dikonversi: {sorted(set(left))}")
    mine = [n for n in notes if n["file"] == name]
    body = insert_notes(body, mine)
    title = meta.get("title", name)
    header = [
        "---",
        f"title: {title}",
        f"url: {meta.get('url', '')}",
        f"description: {meta.get('description', '')}",
        "publisher: Anthropic",
        f"retrieved: {today}",
        f"local_notes: {len(mine)}",
        "---",
        "",
        f"# {title}",
        "",
        "> [!IMPORTANT]",
        f"> **[CATATAN LOKAL]** Salinan dokumentasi resmi Anthropic dari URL di atas, diambil pada {today}. "
        "Kata-kata dokumen asli tidak diubah. Yang disesuaikan hanya tampilan: komponen situs (Note, Tip, Accordion, Card, CodeGroup) "
        "diubah ke format Markdown GitHub dan judul H1 ditambahkan. "
        + (f"Ada {len(mine)} sisipan berlabel `[CATATAN LOKAL]` dari pengelola repo ini; sisipan itu bukan bagian dokumen asli. " if mine else "Tidak ada sisipan lain di file ini. ")
        + "Hak cipta isi dokumen tetap milik Anthropic. Jangan edit file ini dengan tangan: jalankan `scripts/update_references.py`.",
        "",
    ]
    return "\n".join(header) + "\n" + body


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", type=Path, help="folder berisi file .md hasil unduhan (nama = bagian akhir path halaman)")
    ap.add_argument("--date", default=datetime.date.today().isoformat(), help="tanggal ambil (default: hari ini)")
    args = ap.parse_args()

    notes = json.loads(NOTES_FILE.read_text(encoding="utf-8"))["notes"]
    known = {name for name, _, _ in PAGES}
    for n in notes:
        if n["file"] not in known:
            sys.exit(f"local_notes.json menyebut file yang tidak dikenal: {n['file']}")

    for name, page, dest in PAGES:
        if args.offline:
            raw = (args.offline / (page.rsplit("/", 1)[1] + ".md")).read_text(encoding="utf-8")
        else:
            raw = fetch(page)
        try:
            text = build(name, raw, notes, args.date)
        except ValueError as e:
            sys.exit(f"GAGAL pada {name}: {e}")
        dest.mkdir(parents=True, exist_ok=True)
        (dest / name).write_text(text, encoding="utf-8")
        print(f"ok  {dest.relative_to(ROOT)}/{name}  ({len(text):,} byte)")


if __name__ == "__main__":
    main()
