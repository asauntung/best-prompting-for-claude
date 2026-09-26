#!/usr/bin/env python3
"""Periksa otomatis aturan format keluaran skill /prompting-claude.

Pemakaian:
    python3 scripts/check_output.py FILE [FILE ...]

FILE berisi keluaran skill apa adanya. Jika FILE memuat judul
"## Keluaran skill" (format folder examples/), hanya bagian setelah judul itu
yang diperiksa.

Yang diperiksa hanya aturan yang bisa dinilai mesin. Mutu analisis dan
ketepatan kutipan tetap perlu dinilai manusia (lihat evals/README.md).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "prompting-claude" / "SKILL.md"
REFS = ROOT / "prompting-claude" / "references"

ECOSYSTEMS = ["Chat", "Cowork", "Claude Code"]
EFFORTS = ["low", "medium", "high", "xhigh", "max"]
API_TERMS = ["max_tokens", "budget_tokens", "clear_at", "stop_reason", "tool_result", "prefill", "role: \"system\""]


def supported_models():
    """Ambil daftar model dari tabel di SKILL.md bagian 1, satu-satunya sumbernya."""
    text = SKILL.read_text(encoding="utf-8")
    section = text.split("## 1.", 1)[1].split("\n## ", 1)[0]
    return re.findall(r"^\| `([^`]+)` \|", section, flags=re.M)


def check(text: str):
    errors, warnings = [], []
    if "## Keluaran skill" in text:
        text = text.split("## Keluaran skill", 1)[1]

    if "—" in text:
        errors.append("ada em-dash (—)")

    blocks = list(re.finditer(r"^```text[^\n]*\n(.*?)^```[ \t]*$", text, flags=re.M | re.S))
    if len(blocks) != 1:
        errors.append(f"harus ada tepat satu codeblock bertipe text, ditemukan {len(blocks)}")
        return errors, warnings
    block = blocks[0]
    prompt = block.group(1)

    if text[block.end():].strip():
        errors.append("ada teks setelah codeblock prompt")

    before = [l for l in text[:block.start()].splitlines() if l.strip()]
    final = before[-1].strip().strip("`*").strip() if before else ""
    models = supported_models()
    pattern = r"Final: (%s), (%s), (%s)" % ("|".join(map(re.escape, ECOSYSTEMS)), "|".join(map(re.escape, models)), "|".join(EFFORTS))
    if not re.fullmatch(pattern, final):
        errors.append(f"baris tepat sebelum codeblock bukan baris Final yang sah: {final!r}")

    for term in API_TERMS:
        if term.lower() in prompt.lower():
            errors.append(f"prompt memuat mekanik API atau teknik usang: {term!r}")

    lines = prompt.splitlines()
    for a, b in zip(lines, lines[1:]):
        if a.strip() and b.strip() and not re.search(r"[.:;!?)\]>\"'`]$", a.strip()) and re.match(r"[a-z]", b.strip()):
            warnings.append(f"kemungkinan hard wrap: {a.strip()[-40:]!r} / {b.strip()[:40]!r}")

    analysis = text[:block.start()]
    refs = {p.name for p in REFS.glob("*.md")}
    cited = set(re.findall(r"`?([\w.-]+\.md) >", analysis))
    if not cited:
        errors.append("analisis tidak memuat rujukan dalam bentuk `nama-file > judul bagian`")
    for name in sorted(cited - refs):
        errors.append(f"analisis merujuk file yang tidak ada di references/: {name}")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    failed = False
    for arg in sys.argv[1:]:
        errors, warnings = check(Path(arg).read_text(encoding="utf-8"))
        status = "GAGAL" if errors else "LULUS"
        print(f"{status}  {arg}")
        for e in errors:
            print(f"   x {e}")
        for w in warnings:
            print(f"   ! {w}")
        failed |= bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
