#!/usr/bin/env python3
"""
Create the local-only `private/` tier scaffold, idempotently.

The private tier is gitignored, so it never ships in git — it is created on each
machine by `setup.sh` (every bootstrap) and by `/upgrade-to-company`. Existing
files are never overwritten, so running this repeatedly is safe.

The boundary exists from day one even in personal mode: it gives the founder a
place to stash personal notes, and makes the eventual personal→company upgrade a
move-into-an-existing-folder rather than a retrofit.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import (  # noqa: E402
    PRIVATE_CONCEPTS_DIR,
    PRIVATE_CONNECTIONS_DIR,
    PRIVATE_CONTEXT_DIR,
    PRIVATE_DIR,
    PRIVATE_QA_DIR,
    PRIVATE_WIKI_DIR,
    PRIVATE_WIKI_INDEX,
)

README = """# Private tier (local only)

This folder is your **personal** layer of the ARC brain. It is gitignored, so
nothing here is ever pushed to a shared/company remote — it stays on this machine.

Use it for anything that should not be team-visible: personal finances, comp and
equity, health, candid notes about people, career thoughts, draft thinking. In
company mode, new auto-captured knowledge lands in `private/wiki/` first and only
reaches the shared `wiki/` when you run `/promote`.

Layout mirrors the shared wiki: `wiki/concepts/`, `wiki/connections/`, `wiki/qa/`,
plus `context/` for private snapshot notes, and `imports/` for documents you want
ARC to read but NOT sync to the team (drop a file there and ask ARC to ingest it).

Never put real secrets (API keys, passwords) even here — use `.env`.
"""

INDEX = """# Private Wiki Index

> Local-only. Articles here are never shared until you `/promote` them.

_No private articles yet._
"""

LOG = """# Private Wiki Log

Chronological log of private-tier wiki operations.
"""


def _write_if_absent(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def scaffold_private() -> list[str]:
    """Create the private scaffold. Returns the list of paths newly created."""
    created: list[str] = []

    private_imports_dir = PRIVATE_DIR / "imports"
    for directory in (
        PRIVATE_DIR,
        PRIVATE_WIKI_DIR,
        PRIVATE_CONCEPTS_DIR,
        PRIVATE_CONNECTIONS_DIR,
        PRIVATE_QA_DIR,
        PRIVATE_CONTEXT_DIR,
        private_imports_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    files = {
        PRIVATE_DIR / "README.md": README,
        PRIVATE_WIKI_INDEX: INDEX,
        PRIVATE_WIKI_DIR / "log.md": LOG,
        PRIVATE_CONCEPTS_DIR / ".gitkeep": "",
        PRIVATE_CONNECTIONS_DIR / ".gitkeep": "",
        PRIVATE_QA_DIR / ".gitkeep": "",
        PRIVATE_CONTEXT_DIR / ".gitkeep": "",
        private_imports_dir / ".gitkeep": "",
    }
    for path, content in files.items():
        if _write_if_absent(path, content):
            created.append(str(path.relative_to(PROJECT_ROOT)))

    return created


def main() -> int:
    created = scaffold_private()
    if created:
        print(f"Created private tier scaffold ({len(created)} file(s)).")
    else:
        print("Private tier scaffold already present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
