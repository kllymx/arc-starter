#!/usr/bin/env python3
"""Stdlib-only tests for company-mode behavior: mode resolution, compile
target routing, and private-tier retrieval surfacing."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import scripts.config as config  # noqa: E402
from scripts.wiki_query import WikiPaths, iter_article_paths  # noqa: E402


def assert_equal(actual, expected, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


import contextlib  # noqa: E402


@contextlib.contextmanager
def _config_files(sharing: str | None = None, workspace: str | None = None,
                  env: dict | None = None):
    """Point config at temp sharing.md/workspace.md and control the relevant env
    vars; restore everything on exit. A None text means the file does not exist."""
    orig_s, orig_w = config.SHARING_CONFIG_FILE, config.WORKSPACE_FILE
    prior = {k: os.environ.get(k) for k in ("ARC_MODE", "ARC_SYNC_STRATEGY")}
    with tempfile.TemporaryDirectory() as tmp:
        s = Path(tmp) / "sharing.md"
        w = Path(tmp) / "workspace.md"
        if sharing is not None:
            s.write_text(sharing)
        if workspace is not None:
            w.write_text(workspace)
        config.SHARING_CONFIG_FILE = s
        config.WORKSPACE_FILE = w
        for k in ("ARC_MODE", "ARC_SYNC_STRATEGY"):
            os.environ.pop(k, None)
        if env:
            os.environ.update(env)
        try:
            yield
        finally:
            config.SHARING_CONFIG_FILE, config.WORKSPACE_FILE = orig_s, orig_w
            for k, v in prior.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


def test_default_mode_is_personal() -> None:
    with _config_files(workspace="# Workspace\n\nNo mode here.\n"):
        assert_equal(config.get_mode(), "personal", "missing Mode defaults to personal")


def test_sharing_file_mode_company() -> None:
    with _config_files(sharing="- Mode: company\n"):
        assert_equal(config.get_mode(), "company", "sharing.md Mode: company is read")


def test_sharing_takes_precedence_over_workspace() -> None:
    with _config_files(sharing="- Mode: company\n", workspace="- Mode: personal\n"):
        assert_equal(config.get_mode(), "company", "sharing.md wins over workspace.md")


def test_workspace_mode_is_backcompat_fallback() -> None:
    # No sharing.md → fall back to a legacy workspace.md Mode line.
    with _config_files(workspace="## Sharing\n\n- Mode: company\n"):
        assert_equal(config.get_mode(), "company", "workspace.md Mode is a fallback")


def test_env_overrides_files() -> None:
    with _config_files(sharing="- Mode: company\n", env={"ARC_MODE": "personal"}):
        assert_equal(config.get_mode(), "personal", "ARC_MODE overrides files")


def test_sync_strategy_default_and_sources() -> None:
    with _config_files():
        assert_equal(config.get_sync_strategy(), "pr", "default sync strategy is pr")
    with _config_files(sharing="- Mode: company\n- Sync: direct\n"):
        assert_equal(config.get_sync_strategy(), "direct", "sharing.md Sync is read")
    with _config_files(sharing="- Sync: direct\n", env={"ARC_SYNC_STRATEGY": "pr"}):
        assert_equal(config.get_sync_strategy(), "pr", "env overrides sync strategy")


def _install_fake_sdk(captured: dict[str, str]):
    """Replace claude_agent_sdk with a stub that records the compile prompt and
    yields nothing, so compile_daily_log runs without an API call."""
    import types

    fake = types.ModuleType("claude_agent_sdk")

    async def _query(*, prompt, options):  # noqa: ANN001
        captured["prompt"] = prompt
        if False:  # pragma: no cover — makes this an async generator
            yield

    class _Options:
        def __init__(self, **_kwargs):
            pass

    fake.query = _query
    fake.ClaudeAgentOptions = _Options
    fake.AssistantMessage = type("AssistantMessage", (), {})
    fake.ResultMessage = type("ResultMessage", (), {})
    fake.TextBlock = type("TextBlock", (), {})
    return fake


def test_compile_target_is_mode_aware() -> None:
    """compile.py must route new-article writes to private/wiki/ in company mode
    and to wiki/ otherwise. Assert the prompt the agent receives reflects this
    without invoking the LLM or touching the repo's state.json."""
    import asyncio

    import scripts.compile as compile_mod

    captured: dict[str, str] = {}
    original_get_mode = compile_mod.get_mode
    original_save_state = compile_mod.save_state
    prior_sdk = sys.modules.get("claude_agent_sdk")
    try:
        sys.modules["claude_agent_sdk"] = _install_fake_sdk(captured)
        compile_mod.save_state = lambda *_a, **_k: None  # don't write repo state.json

        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "2026-06-25.md"
            log.write_text("## Session\n\nWe decided on annual pricing.\n")

            compile_mod.get_mode = lambda: "company"
            asyncio.run(compile_mod.compile_daily_log(log, {}))
            prompt = captured["prompt"]
            assert_true("private/wiki/concepts" in prompt, "company mode targets private/wiki")
            assert_true("COMPANY" in prompt, "company mode prompt names the mode")

            captured.clear()
            compile_mod.get_mode = lambda: "personal"
            asyncio.run(compile_mod.compile_daily_log(log, {}))
            prompt = captured["prompt"]
            assert_true("wiki/concepts" in prompt, "personal mode targets shared wiki")
            assert_true("private/wiki" not in prompt, "personal mode never routes to private")
    finally:
        compile_mod.get_mode = original_get_mode
        compile_mod.save_state = original_save_state
        if prior_sdk is not None:
            sys.modules["claude_agent_sdk"] = prior_sdk
        else:
            sys.modules.pop("claude_agent_sdk", None)


def test_retrieval_includes_private_dirs() -> None:
    """iter_article_paths must search extra_dirs (private tier) when present."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        concepts = root / "wiki" / "concepts"
        connections = root / "wiki" / "connections"
        qa = root / "wiki" / "qa"
        priv_concepts = root / "private" / "wiki" / "concepts"
        for d in (concepts, connections, qa, priv_concepts):
            d.mkdir(parents=True)
        (concepts / "shared.md").write_text("# Shared\n")
        (priv_concepts / "secret.md").write_text("# Secret\n")

        paths = WikiPaths(
            wiki_dir=root / "wiki",
            concepts_dir=concepts,
            connections_dir=connections,
            qa_dir=qa,
            wiki_index=root / "wiki" / "index.md",
            project_root=root,
            extra_dirs=(priv_concepts,),
        )
        found = {p.name for p in iter_article_paths(paths)}
        assert_true("shared.md" in found, "shared article is found")
        assert_true("secret.md" in found, "private article is surfaced locally")


def test_user_branch_shape() -> None:
    branch = config.get_user_branch()
    assert_true(branch.startswith("arc/"), "personal branch is namespaced under arc/")
    slug = branch[len("arc/"):]
    assert_true(slug != "", "slug must be non-empty")
    assert_true(
        all(c.isalnum() or c in "._-" for c in slug),
        f"slug must be branch-safe, got {slug!r}",
    )


def test_sync_status_empty_in_personal_mode() -> None:
    import scripts.sync_status as sync_status

    prior = os.environ.get("ARC_MODE")
    try:
        os.environ["ARC_MODE"] = "personal"
        assert_equal(sync_status.build_sync_status(), "", "no sync reminder in personal mode")
    finally:
        if prior is None:
            os.environ.pop("ARC_MODE", None)
        else:
            os.environ["ARC_MODE"] = prior


def _run_git(repo: Path, *args: str) -> None:
    import subprocess

    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *args],
        cwd=str(repo),
        check=True,
        capture_output=True,
        text=True,
    )


def test_conflicts_detection_and_stages() -> None:
    """conflicts.py detects an unmerged file and exposes ours/theirs stages."""
    import subprocess

    import scripts.conflicts as conflicts

    original_root = conflicts.PROJECT_ROOT
    try:
        # ignore_cleanup_errors: git may leave a background fsmonitor/socket that
        # races with rmtree of the temp .git on some platforms.
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            repo = Path(tmp)
            _run_git(repo, "init", "-b", "main")
            _run_git(repo, "config", "user.email", "t@example.com")
            _run_git(repo, "config", "user.name", "Tester")

            article = repo / "wiki" / "concepts" / "pricing.md"
            article.parent.mkdir(parents=True)
            article.write_text("# Pricing\n\nBase price is 10.\n")
            _run_git(repo, "add", "-A")
            _run_git(repo, "commit", "-m", "base")

            _run_git(repo, "checkout", "-b", "feature")
            article.write_text("# Pricing\n\nBase price is 12.\n")
            _run_git(repo, "add", "-A")
            _run_git(repo, "commit", "-m", "feature change")

            _run_git(repo, "checkout", "main")
            article.write_text("# Pricing\n\nBase price is 15.\n")
            _run_git(repo, "add", "-A")
            _run_git(repo, "commit", "-m", "main change")

            # Merge feature into main → conflict on the same line.
            merge = subprocess.run(
                ["git", "merge", "feature"],
                cwd=str(repo),
                capture_output=True,
                text=True,
            )
            assert_true(merge.returncode != 0, "merge should conflict")

            conflicts.PROJECT_ROOT = repo
            files = conflicts.conflicted_files()
            assert_true(
                any(f.endswith("pricing.md") for f in files),
                f"pricing.md should be conflicted, got {files}",
            )
            assert_equal(conflicts.operation_state(), "merge", "merge in progress")

            stages = conflicts.file_stages("wiki/concepts/pricing.md")
            assert_true(stages["ours"] is not None, "ours stage present")
            assert_true(stages["theirs"] is not None, "theirs stage present")
            assert_true("15" in (stages["ours"] or ""), "ours holds main's value")
            assert_true("12" in (stages["theirs"] or ""), "theirs holds feature's value")
    finally:
        conflicts.PROJECT_ROOT = original_root


def test_scaffold_private_idempotent() -> None:
    """scaffold_private creates the tier and never overwrites existing files."""
    import scripts.scaffold_private as sp

    saved = {
        name: getattr(sp, name)
        for name in (
            "PROJECT_ROOT",
            "PRIVATE_DIR",
            "PRIVATE_WIKI_DIR",
            "PRIVATE_CONCEPTS_DIR",
            "PRIVATE_CONNECTIONS_DIR",
            "PRIVATE_QA_DIR",
            "PRIVATE_CONTEXT_DIR",
            "PRIVATE_WIKI_INDEX",
        )
    }
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            priv = root / "private"
            wiki = priv / "wiki"
            sp.PROJECT_ROOT = root
            sp.PRIVATE_DIR = priv
            sp.PRIVATE_WIKI_DIR = wiki
            sp.PRIVATE_CONCEPTS_DIR = wiki / "concepts"
            sp.PRIVATE_CONNECTIONS_DIR = wiki / "connections"
            sp.PRIVATE_QA_DIR = wiki / "qa"
            sp.PRIVATE_CONTEXT_DIR = priv / "context"
            sp.PRIVATE_WIKI_INDEX = wiki / "index.md"

            created = sp.scaffold_private()
            assert_true(len(created) > 0, "first run creates files")
            assert_true((priv / "README.md").exists(), "README created")
            assert_true((wiki / "concepts" / ".gitkeep").exists(), "concepts gitkeep")
            assert_true((priv / "context" / ".gitkeep").exists(), "context gitkeep")

            # Mutate a file, then re-run: must not overwrite.
            (wiki / "index.md").write_text("CUSTOM\n")
            created_again = sp.scaffold_private()
            assert_equal(created_again, [], "second run creates nothing")
            assert_equal(
                (wiki / "index.md").read_text(),
                "CUSTOM\n",
                "existing files are never overwritten",
            )
    finally:
        for name, value in saved.items():
            setattr(sp, name, value)


def test_sync_status_suggests_join_on_fresh_clone() -> None:
    """On main, in company mode, with no personal branch → suggest /join-company."""
    import scripts.sync_status as sync_status

    original_root = sync_status.PROJECT_ROOT
    original_priv = sync_status.PRIVATE_DIR
    prior_mode = os.environ.get("ARC_MODE")
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            repo = Path(tmp)
            _run_git(repo, "init", "-b", "main")
            _run_git(repo, "config", "user.email", "joiner@example.com")
            _run_git(repo, "config", "user.name", "Joiner")
            (repo / "README.md").write_text("# Company brain\n")
            _run_git(repo, "add", "-A")
            _run_git(repo, "commit", "-m", "base")
            # An origin must exist for the reminder to engage (value need not resolve).
            _run_git(repo, "remote", "add", "origin", str(repo / "origin.git"))

            sync_status.PROJECT_ROOT = repo
            # No private tier on this machine yet → the "not set up" join nudge.
            sync_status.PRIVATE_DIR = repo / "private"
            os.environ["ARC_MODE"] = "company"
            out = sync_status.build_sync_status()
            assert_true("join the company brain" in out, f"expected join nudge, got: {out!r}")
    finally:
        sync_status.PROJECT_ROOT = original_root
        sync_status.PRIVATE_DIR = original_priv
        if prior_mode is None:
            os.environ.pop("ARC_MODE", None)
        else:
            os.environ["ARC_MODE"] = prior_mode


def test_union_merge_keeps_both_appends() -> None:
    """The .gitattributes union driver auto-merges concurrent appends to log.md
    without a conflict, keeping both lines."""
    import subprocess

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        repo = Path(tmp)
        _run_git(repo, "init", "-b", "main")
        _run_git(repo, "config", "user.email", "t@example.com")
        _run_git(repo, "config", "user.name", "Tester")
        (repo / ".gitattributes").write_text("wiki/log.md merge=union\n")
        log = repo / "wiki" / "log.md"
        log.parent.mkdir(parents=True)
        log.write_text("# Log\n\n- base entry\n")
        _run_git(repo, "add", "-A")
        _run_git(repo, "commit", "-m", "base")

        _run_git(repo, "checkout", "-b", "feature")
        log.write_text("# Log\n\n- base entry\n- feature entry\n")
        _run_git(repo, "add", "-A")
        _run_git(repo, "commit", "-m", "feature entry")

        _run_git(repo, "checkout", "main")
        log.write_text("# Log\n\n- base entry\n- main entry\n")
        _run_git(repo, "add", "-A")
        _run_git(repo, "commit", "-m", "main entry")

        merge = subprocess.run(
            ["git", "merge", "feature"],
            cwd=str(repo), capture_output=True, text=True,
        )
        assert_equal(merge.returncode, 0, f"union merge should not conflict: {merge.stderr}")
        merged = log.read_text()
        assert_true("feature entry" in merged, "feature line kept")
        assert_true("main entry" in merged, "main line kept")


def test_github_status_shape() -> None:
    """github_status.collect() returns the expected keys and never throws,
    whether or not gh is installed/authenticated."""
    import scripts.github_status as gh

    status = gh.collect()
    for key in (
        "gh_installed",
        "authenticated",
        "login",
        "scopes",
        "can_create_repo",
        "can_admin_org",
        "orgs",
        "origin",
        "origin_visibility",
    ):
        assert_true(key in status, f"github_status missing key {key}")
    assert_true(isinstance(status["scopes"], list), "scopes is a list")
    assert_true(isinstance(status["orgs"], list), "orgs is a list")
    # render() must produce a string regardless of state.
    assert_true(isinstance(gh.render(status), str), "render returns a string")


def main() -> int:
    test_default_mode_is_personal()
    test_sharing_file_mode_company()
    test_sharing_takes_precedence_over_workspace()
    test_workspace_mode_is_backcompat_fallback()
    test_env_overrides_files()
    test_sync_strategy_default_and_sources()
    test_compile_target_is_mode_aware()
    test_retrieval_includes_private_dirs()
    test_user_branch_shape()
    test_sync_status_empty_in_personal_mode()
    test_conflicts_detection_and_stages()
    test_scaffold_private_idempotent()
    test_github_status_shape()
    test_sync_status_suggests_join_on_fresh_clone()
    test_union_merge_keeps_both_appends()
    print("All company_mode tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
