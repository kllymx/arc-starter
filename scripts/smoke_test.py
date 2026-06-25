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

    Expected shape:
      .claude/settings.json → SessionStart, PreCompact, SessionEnd
        (NOT Stop — Stop fires per-turn, SessionEnd fires once at terminate)
      .codex/hooks.json → SessionStart, PreCompact
        (Codex shipped PreCompact since the original framework — openai/codex#17148.
         Still NO Stop: it fires per-turn and would be wasted work.
         Still NO SessionEnd: Codex has no such event yet, openai/codex#20603.)
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

    # Codex: SessionStart + PreCompact. Still NO Stop (fires per-turn),
    # still NO SessionEnd (no such event in Codex yet, openai/codex#20603).
    codex_events = codex_hooks["hooks"]
    assert "SessionStart" in codex_events, "Codex must have SessionStart hook"
    assert "PreCompact" in codex_events, (
        "Codex must have PreCompact hook — Codex shipped compaction hooks "
        "(openai/codex#17148) so long-session capture now matches Claude Code."
    )
    assert "Stop" not in codex_events, (
        "Codex must NOT have a Stop hook: Stop fires per-turn, so using it for "
        "capture is wasted work. Auto-capture rides PreCompact instead."
    )
    assert "SessionEnd" not in codex_events, (
        "Codex has no SessionEnd event yet (openai/codex#20603); don't wire one."
    )
    for event in ("SessionStart", "PreCompact"):
        cmd = codex_events[event][0]["hooks"][0]["command"]
        assert "CODEX_CLI=1" in cmd, f"Codex {event} missing CODEX_CLI=1"


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


def test_maintenance_commands_have_skill_parity() -> None:
    """New maintenance commands ship as BOTH a Claude command and a Codex skill,
    so capture/maintenance works on either harness (added 2026-06-24)."""
    for name in ("garden", "link"):
        assert (PROJECT_ROOT / ".claude" / "commands" / f"{name}.md").exists(), (
            f"/{name} missing its Claude command (.claude/commands/{name}.md)"
        )
        assert (PROJECT_ROOT / ".codex" / "skills" / name / "SKILL.md").exists(), (
            f"/{name} missing its Codex skill (.codex/skills/{name}/SKILL.md)"
        )


def test_company_mode_wiring() -> None:
    """Company mode (2026-06-25): mode resolver defaults to personal, the
    private tier is gitignored, and the new commands ship with Codex parity."""
    # Mode resolver exists and defaults to personal in a clean env.
    result = run_python_with_clean_agent_env(
        "import os; os.environ.pop('ARC_MODE', None)\n"
        "from scripts.config import get_mode; print(get_mode())\n"
    )
    assert_equal(
        result.stdout.strip(),
        "personal",
        "get_mode must default to personal",
    )

    # The private tier and research scrapes must be gitignored.
    gitignore = (PROJECT_ROOT / ".gitignore").read_text()
    assert "private/" in gitignore, "private/ must be gitignored (company-mode boundary)"
    assert ".firecrawl/" in gitignore, ".firecrawl/ must be gitignored"

    # New commands ship as BOTH a Claude command and a Codex skill.
    for name in ("upgrade-to-company", "promote", "reconcile", "join-company"):
        assert (PROJECT_ROOT / ".claude" / "commands" / f"{name}.md").exists(), (
            f"/{name} missing its Claude command (.claude/commands/{name}.md)"
        )
        assert (PROJECT_ROOT / ".codex" / "skills" / name / "SKILL.md").exists(), (
            f"/{name} missing its Codex skill (.codex/skills/{name}/SKILL.md)"
        )

    # The shared-brain governance doc must exist.
    assert (PROJECT_ROOT / "SHARING.md").exists(), "SHARING.md must exist at repo root"


def test_document_types_sync_intact() -> None:
    """Office/PDF documents dropped in imports/ are marked binary so git never
    applies line-ending conversion (which corrupts ZIP-based Office files), and
    imports/ itself is not gitignored — so documents sync to the team intact."""
    for name in ("deck.pptx", "plan.docx", "model.xlsx", "report.pdf"):
        result = run_command("git", "check-attr", "binary", "--", f"imports/{name}")
        assert "binary: set" in result.stdout, (
            f"imports/{name} must be marked binary in .gitattributes (else it can be "
            f"corrupted on a Windows clone)"
        )

    ignored = subprocess.run(
        ["git", "check-ignore", "imports/example.pdf"],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
    )
    assert ignored.returncode != 0, "imports/ must not be gitignored — documents must sync"


def test_new_scripts_importable() -> None:
    """The new retrieval/maintenance modules import cleanly (no syntax/import
    errors) and are import-side-effect-free. Behavior is covered by each
    module's own test_*.py; this is just a fast wiring guard."""
    import importlib

    for mod in (
        "scripts.context_select",
        "scripts.wiki_query",
        "scripts.garden",
        "scripts.link_pass",
        "scripts.sync_status",
        "scripts.conflicts",
        "scripts.scaffold_private",
        "scripts.github_status",
    ):
        importlib.import_module(mod)


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
        test_maintenance_commands_have_skill_parity,
        test_company_mode_wiring,
        test_document_types_sync_intact,
        test_new_scripts_importable,
    ]

    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
