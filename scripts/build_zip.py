#!/usr/bin/env python3
"""Package the best-prompting/ folder into dist/best-prompting.zip.

This zip file is what gets uploaded to the Skills menu on claude.ai.
It contains a single best-prompting/ folder with SKILL.md and references/.

Usage:
    python3 scripts/build_zip.py
"""

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "best-prompting"
OUT = ROOT / "dist" / "best-prompting.zip"


def main():
    OUT.parent.mkdir(exist_ok=True)
    files = sorted(p for p in SKILL_DIR.rglob("*") if p.is_file() and not p.name.startswith("."))
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            info = zipfile.ZipInfo(str(path.relative_to(ROOT)), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    print(f"ok  {OUT.relative_to(ROOT)}  ({len(files)} files, {OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
