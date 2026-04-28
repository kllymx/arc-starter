---
name: business-snapshot
description: Generate a visual business snapshot from the ARC context layer and wiki. Trigger when the user asks for a business snapshot, HTML summary, ARC snapshot, or uses /business-snapshot.
metadata:
  short-description: Visual HTML snapshot from ARC context
---

# business-snapshot

Follow the same workflow as `.claude/commands/business-snapshot.md`.

Read that command file first, then execute it. The required output is:

- `reports/business-snapshot.html`
- `reports/business-snapshot.md`

Respect demo mode if the user supplies `--demo <path>`: read only that
folder and label the output as demo/sanitized.
