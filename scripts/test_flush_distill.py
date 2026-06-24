#!/usr/bin/env python3
"""Tests for flush distillation + provenance (Lane E). Stdlib only — no network."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts import flush


def test_flush_prompt_has_durability_signal_noise_and_sources() -> None:
    prompt = flush.FLUSH_PROMPT.lower()
    for needle in ("[durable]", "[ephemeral]", "signal", "noise", "sources"):
        assert needle in prompt, f"FLUSH_PROMPT missing {needle!r}"


def test_append_to_daily_log_writes_provenance_footer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        daily_dir = Path(tmp)
        flush.append_to_daily_log(
            "**Context:** test entry [durable]",
            session_id="test-session-42",
            daily_dir=daily_dir,
        )
        log_files = list(daily_dir.glob("*.md"))
        assert len(log_files) == 1
        text = log_files[0].read_text(encoding="utf-8")
        assert "_provenance:" in text
        assert "session=test-session-42" in text
        assert "captured=" in text


def test_parse_args_preserves_positional_and_distill_only() -> None:
    default_args = flush.parse_args(["ctx.md", "sess-abc"])
    assert default_args.context_file == Path("ctx.md")
    assert default_args.session_id == "sess-abc"
    assert default_args.distill_only is False

    distill_args = flush.parse_args(["ctx.md", "sess-abc", "--distill-only"])
    assert distill_args.distill_only is True


def test_distill_only_skips_daily_log_and_compilation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        context_file = Path(tmp) / "context.md"
        context_file.write_text("User discussed pricing strategy.", encoding="utf-8")

        async def fake_run_flush(_context: str) -> str:
            return "**Context:** pricing [durable]"

        with patch.object(flush, "run_flush", fake_run_flush):
            with patch.object(flush, "append_to_daily_log") as mock_append:
                with patch.object(flush, "maybe_trigger_compilation") as mock_compile:
                    with patch.object(flush, "save_flush_state") as mock_save:
                        exit_code = flush.run_flush_pipeline(
                            context_file,
                            "sess-distill",
                            distill_only=True,
                        )

        assert exit_code == 0
        mock_append.assert_not_called()
        mock_compile.assert_not_called()
        mock_save.assert_not_called()
        assert context_file.exists(), "distill-only should not delete the context file"


def main() -> None:
    tests = [
        test_flush_prompt_has_durability_signal_noise_and_sources,
        test_append_to_daily_log_writes_provenance_footer,
        test_parse_args_preserves_positional_and_distill_only,
        test_distill_only_skips_daily_log_and_compilation,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")
    print(f"\n{len(tests)} passed")


if __name__ == "__main__":
    main()