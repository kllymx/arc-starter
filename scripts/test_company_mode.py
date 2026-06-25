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


def test_default_mode_is_personal() -> None:
    original = config.WORKSPACE_FILE
    prior_env = os.environ.pop("ARC_MODE", None)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            # Placeholder workspace with no Mode line.
            workspace = Path(tmp) / "workspace.md"
            workspace.write_text("# Workspace Context\n\nNo mode set here.\n")
            config.WORKSPACE_FILE = workspace
            assert_equal(config.get_mode(), "personal", "missing Mode defaults to personal")
    finally:
        config.WORKSPACE_FILE = original
        if prior_env is not None:
            os.environ["ARC_MODE"] = prior_env


def test_workspace_mode_company() -> None:
    original = config.WORKSPACE_FILE
    prior_env = os.environ.pop("ARC_MODE", None)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace.md"
            workspace.write_text("# Workspace Context\n\n## Sharing\n\n- Mode: company\n")
            config.WORKSPACE_FILE = workspace
            assert_equal(config.get_mode(), "company", "workspace Mode: company is read")
    finally:
        config.WORKSPACE_FILE = original
        if prior_env is not None:
            os.environ["ARC_MODE"] = prior_env


def test_env_overrides_workspace() -> None:
    original = config.WORKSPACE_FILE
    prior_env = os.environ.get("ARC_MODE")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace.md"
            workspace.write_text("- Mode: company\n")
            config.WORKSPACE_FILE = workspace
            os.environ["ARC_MODE"] = "personal"
            assert_equal(config.get_mode(), "personal", "ARC_MODE overrides workspace")
    finally:
        config.WORKSPACE_FILE = original
        if prior_env is None:
            os.environ.pop("ARC_MODE", None)
        else:
            os.environ["ARC_MODE"] = prior_env


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


def main() -> int:
    test_default_mode_is_personal()
    test_workspace_mode_company()
    test_env_overrides_workspace()
    test_compile_target_is_mode_aware()
    test_retrieval_includes_private_dirs()
    print("All company_mode tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
