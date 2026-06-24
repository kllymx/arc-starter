#!/usr/bin/env python3
"""Lane F self-check: context-hygiene guide and templates exist and stay under 200 lines."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_LINES = 200

REQUIRED = [
    ROOT / "guides" / "context-hygiene.md",
    ROOT / "guides" / "templates" / "CLAUDE.md.example",
    ROOT / "guides" / "templates" / "memory.md.example",
    ROOT / "guides" / "templates" / "agents-fragment.example.md",
]

HYGIENE = ROOT / "guides" / "context-hygiene.md"
LANE_MARKERS = [
    "Lean SessionStart injection",
    "On-demand retrieval",
    "Garden pass",
]


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED:
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(ROOT)}")
            continue
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count >= MAX_LINES:
            errors.append(
                f"{path.relative_to(ROOT)}: {line_count} lines (max {MAX_LINES - 1})"
            )

    if HYGIENE.is_file():
        text = HYGIENE.read_text(encoding="utf-8")
        for marker in LANE_MARKERS:
            if marker not in text:
                errors.append(f"context-hygiene.md missing lane reference: {marker!r}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1

    print("OK: all Lane F docs present and within line budget")
    for path in REQUIRED:
        n = len(path.read_text(encoding="utf-8").splitlines())
        print(f"  {path.relative_to(ROOT)}: {n} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())