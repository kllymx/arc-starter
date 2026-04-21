#!/usr/bin/env python3
"""Lightweight regression checks for ARC bootstrap and hook behavior."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import scripts.config as config


def assert_equal(actual, expected, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def run_python_with_clean_agent_env(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "python3",
            "-c",
            code,
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=True,
        env={
            key: value
            for key, value in os.environ.items()
            if key != "CLAUDE_CODE" and not key.startswith("CODEX_")
        },
    )


def test_detect_environment_placeholder_is_unknown() -> None:
    result = run_python_with_clean_agent_env(
        "from scripts.config import detect_environment; print(detect_environment())",
    )
    assert_equal(
        result.stdout.strip(),
        "unknown",
        "placeholder workspace should not force a backend",
    )


def test_get_llm_backend_unknown_falls_back_to_claude() -> None:
    result = run_python_with_clean_agent_env(
        "from scripts.config import get_llm_backend\n"
        "print(get_llm_backend()['type'])\n"
    )
    assert_equal(
        result.stdout.strip(),
        "claude",
        "unknown direct runs should fall back to Claude safely",
    )


def test_detect_environment_explicit_codex() -> None:
    original_workspace = config.WORKSPACE_FILE
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir) / "workspace.md"
            workspace.write_text(
                "# Workspace Context\n\n## Environment\n- Primary environment: Codex\n"
            )
            config.WORKSPACE_FILE = workspace
            assert_equal(
                config.detect_environment(),
                "codex",
                "explicit workspace setting should map to codex",
            )
    finally:
        config.WORKSPACE_FILE = original_workspace


def test_detect_environment_from_codex_env_var() -> None:
    result = run_command(
        "env",
        "CODEX_THREAD_ID=smoke-test-thread",
        "python3",
        "-c",
        "from scripts.config import detect_environment; print(detect_environment())",
    )
    assert_equal(
        result.stdout.strip(),
        "codex",
        "CODEX_* environment variables should map to codex",
    )


def test_detect_environment_from_arc_override() -> None:
    result = run_command(
        "env",
        "ARC_ENVIRONMENT=Codex",
        "python3",
        "-c",
        "from scripts.config import detect_environment; print(detect_environment())",
    )
    assert_equal(
        result.stdout.strip(),
        "codex",
        "ARC_ENVIRONMENT should provide an explicit override",
    )


def test_session_start_hook_skips_placeholder_context() -> None:
    result = run_command("python3", "hooks/session-start.py")
    assert_equal(
        result.stdout.strip(),
        "",
        "session-start.py should not inject placeholder files",
    )

    result = run_command("bash", "hooks/session-start.sh")
    assert_equal(
        result.stdout.strip(),
        "",
        "session-start.sh should not inject placeholder files",
    )


def test_structural_lint_blank_wiki() -> None:
    result = run_command("python3", "scripts/lint.py", "--structural-only")
    assert "No wiki articles found. Run /setup to build the wiki." in result.stdout


def test_hook_configs_export_runtime_env() -> None:
    """Hook wiring uses the right lifecycle events and exports the
    harness-identifying env var every hook downstream relies on.

    Expected shape after Session 2 (2026-04-25) framework update:
      .claude/settings.json → SessionStart, PreCompact, SessionEnd
        (NOT Stop — Stop fires per-turn, SessionEnd fires once at terminate)
      .codex/hooks.json → SessionStart only
        (Stop was removed; session-end.py short-circuits on CODEX_CLI and
         Codex has no SessionEnd event yet, tracked at openai/codex#17148)
    """
    claude_settings = json.loads((PROJECT_ROOT / ".claude" / "settings.json").read_text())
    codex_hooks = json.loads((PROJECT_ROOT / ".codex" / "hooks.json").read_text())

    # Claude Code: SessionStart, PreCompact, SessionEnd — all must carry CLAUDE_CODE=1
    claude_events = claude_settings["hooks"]
    assert "SessionStart" in claude_events, "Claude must have SessionStart hook"
    assert "PreCompact" in claude_events, "Claude must have PreCompact hook"
    assert "SessionEnd" in claude_events, "Claude must have SessionEnd hook (migrated from Stop)"
    assert "Stop" not in claude_events, (
        "Claude Stop hook was removed in favour of SessionEnd. "
        "Stop fires per-turn and was wasteful."
    )
    for event in ("SessionStart", "PreCompact", "SessionEnd"):
        cmd = claude_events[event][0]["hooks"][0]["command"]
        assert "CLAUDE_CODE=1" in cmd, f"Claude {event} missing CLAUDE_CODE=1"

    # Codex: SessionStart only — Stop was removed
    codex_events = codex_hooks["hooks"]
    assert "SessionStart" in codex_events, "Codex must have SessionStart hook"
    assert "Stop" not in codex_events, (
        "Codex Stop hook was removed: session-end.py short-circuits on "
        "CODEX_CLI anyway, and firing per-turn was wasted work."
    )
    codex_start = codex_events["SessionStart"][0]["hooks"][0]["command"]
    assert "CODEX_CLI=1" in codex_start, "Codex SessionStart missing CODEX_CLI=1"


def test_hook_timeouts_are_seconds_not_milliseconds() -> None:
    """Claude Code and Codex hook timeouts are in seconds, defaults ~60s.

    The old config used 15000/10000, which meant 15000 seconds (4+ hours)
    of potential hang on a stuck hook. Corrected to 15/10. This test
    enforces the correct unit by asserting every timeout is <= 300s.
    """
    claude_settings = json.loads((PROJECT_ROOT / ".claude" / "settings.json").read_text())
    codex_hooks = json.loads((PROJECT_ROOT / ".codex" / "hooks.json").read_text())

    def collect_timeouts(hooks_root: dict) -> list[tuple[str, int]]:
        timeouts = []
        for event, entries in hooks_root.get("hooks", {}).items():
            for entry in entries:
                for hook in entry.get("hooks", []):
                    if "timeout" in hook:
                        timeouts.append((event, int(hook["timeout"])))
        return timeouts

    for event, t in collect_timeouts(claude_settings) + collect_timeouts(codex_hooks):
        assert t <= 300, (
            f"{event} timeout is {t}s — suspiciously long, likely meant to be in "
            f"seconds not ms. Correct range is typically 10-60s."
        )


def main() -> None:
    tests = [
        test_detect_environment_placeholder_is_unknown,
        test_get_llm_backend_unknown_falls_back_to_claude,
        test_detect_environment_explicit_codex,
        test_detect_environment_from_codex_env_var,
        test_detect_environment_from_arc_override,
        test_session_start_hook_skips_placeholder_context,
        test_structural_lint_blank_wiki,
        test_hook_configs_export_runtime_env,
        test_hook_timeouts_are_seconds_not_milliseconds,
    ]

    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
