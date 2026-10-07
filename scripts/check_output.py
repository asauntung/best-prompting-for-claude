#!/usr/bin/env python3
"""Automatically check the output format rules of the /best-prompting skill.

Usage:
    python3 scripts/check_output.py FILE [FILE ...]

FILE contains the skill output as is. If FILE contains the heading
"## Skill output" (the format of the examples/ folder), only the part after
that heading is checked.

Only rules a machine can judge are checked. The quality of the analysis and
the accuracy of quotes still need human review (see evals/README.md).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "best-prompting" / "SKILL.md"
REFS = ROOT / "best-prompting" / "references"

ECOSYSTEMS = ["Chat", "Cowork", "Claude Code"]
EFFORTS = ["low", "medium", "high", "xhigh", "max"]
API_TERMS = ["max_tokens", "budget_tokens", "clear_at", "stop_reason", "tool_result", "prefill", "role: \"system\""]


def supported_models():
    """Read the model list from the table in SKILL.md section 1, its only source."""
    text = SKILL.read_text(encoding="utf-8")
    section = text.split("## 1.", 1)[1].split("\n## ", 1)[0]
    return re.findall(r"^\| `([^`]+)` \|", section, flags=re.M)


def check(text: str):
    errors, warnings = [], []
    if "## Skill output" in text:
        text = text.split("## Skill output", 1)[1]

    if "—" in text:
        errors.append("contains an em-dash (—)")

    blocks = list(re.finditer(r"^```text[^\n]*\n(.*?)^```[ \t]*$", text, flags=re.M | re.S))
    if len(blocks) != 1:
        errors.append(f"expected exactly one codeblock of type text, found {len(blocks)}")
        return errors, warnings
    block = blocks[0]
    prompt = block.group(1)

    if text[block.end():].strip():
        errors.append("there is text after the prompt codeblock")

    before = [l for l in text[:block.start()].splitlines() if l.strip()]
    final = before[-1].strip().strip("`*").strip() if before else ""
    models = supported_models()
    pattern = r"Final: (%s), (%s), (%s)" % ("|".join(map(re.escape, ECOSYSTEMS)), "|".join(map(re.escape, models)), "|".join(EFFORTS))
    if not re.fullmatch(pattern, final):
        errors.append(f"the line right before the codeblock is not a valid Final line: {final!r}")

    for term in API_TERMS:
        if term.lower() in prompt.lower():
            errors.append(f"prompt contains API mechanics or an outdated technique: {term!r}")

    lines = prompt.splitlines()
    for a, b in zip(lines, lines[1:]):
        if a.strip() and b.strip() and not re.search(r"[.:;!?)\]>\"'`]$", a.strip()) and re.match(r"[a-z]", b.strip()):
            warnings.append(f"possible hard wrap: {a.strip()[-40:]!r} / {b.strip()[:40]!r}")

    analysis = text[:block.start()]
    refs = {p.name for p in REFS.glob("*.md")}
    cited = set(re.findall(r"`?([\w.-]+\.md) >", analysis))
    if not cited:
        errors.append("analysis has no reference in the form `file-name > section heading`")
    for name in sorted(cited - refs):
        errors.append(f"analysis cites a file that is not in references/: {name}")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    failed = False
    for arg in sys.argv[1:]:
        errors, warnings = check(Path(arg).read_text(encoding="utf-8"))
        status = "FAIL" if errors else "PASS"
        print(f"{status}  {arg}")
        for e in errors:
            print(f"   x {e}")
        for w in warnings:
            print(f"   ! {w}")
        failed |= bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
