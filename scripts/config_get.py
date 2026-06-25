#!/usr/bin/env python3
"""
Expose resolved config values to the shell hooks so bash and Python share ONE
source of truth (env overrides + sharing.md/workspace.md precedence), instead of
the hooks re-implementing detection by grepping and drifting out of sync.

Stdlib only, so it runs under the system python3 before `setup.sh` has built the
uv environment.

Usage:
    python3 scripts/config_get.py mode      # personal | company
    python3 scripts/config_get.py sync      # pr | direct
    python3 scripts/config_get.py branch    # arc/<slug>
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.config import (  # noqa: E402
    get_mode,
    get_sync_strategy,
    get_user_branch,
)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    key = args[0] if args else ""
    if key == "mode":
        print(get_mode())
    elif key == "sync":
        print(get_sync_strategy())
    elif key == "branch":
        print(get_user_branch())
    else:
        print("usage: config_get.py mode|sync|branch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
