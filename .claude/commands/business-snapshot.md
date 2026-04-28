---
description: Generate a visual business snapshot from the ARC context layer and wiki
argument-hint: [--demo <path>] [optional focus]
---

# /business-snapshot

Generate a polished business snapshot that reflects what ARC has learned.
Argument: **$ARGUMENTS**

## Purpose

This is the Session 3 capstone "mirror" moment. The founder should see
their business, workflows, priorities, and AI leverage areas reflected
back from the context they have built across Sessions 1 and 2.

The output is a single local HTML file plus a short markdown note.

## Inputs

If the argument includes `--demo <path>`, use only that demo context folder.
This is for workshop demos with curated/sanitized context. Do not read
outside that folder unless explicitly asked.

Otherwise read, in order:

1. `context/`
   - `workspace.md`
   - `overview.md`
   - `memory.md`
   - `setup-status.md`
2. `wiki/index.md`, then relevant wiki articles
3. `audit-results.md` if present
4. `explorations/` if present
5. `.claude/commands/` and `.codex/skills/` names only, to understand
   available capabilities

If the context layer is mostly placeholders or the wiki is empty, stop
and tell the founder to run setup/reflect first. Do not invent a snapshot.

## Privacy Classification

Separate what ARC knows into:

- **Founder/operator context**: personal preferences, private routines,
  personal working style, individual leverage.
- **Business context**: product, customers, team, tools, priorities,
  workflows, market, operating bottlenecks.
- **Company-relevant signals**: things that might eventually become shared
  knowledge or internal tooling.
- **Keep personal**: sensitive/private material that should not be
  copied into a company system.

Be conservative. If something feels personal, label it as personal.

## HTML Requirements

Create:

`reports/business-snapshot.html`

Use a self-contained HTML file with embedded CSS. No external assets,
no network calls, no build step.

Visual style:

- Dark, polished founder/operator dashboard
- Clear cards and sections
- Subtle accent colors, not a rainbow
- Professional typography using system fonts
- Responsive enough to open on a laptop browser
- Include simple CSS-only visuals such as bars, score cards, matrices,
  and roadmap lanes

Sections:

1. **Executive Snapshot**
   - Business summary
   - Current stage
   - Current operating focus
2. **What ARC Knows**
   - Founder/operator context
   - Business context
   - Tools and data sources
   - Workflows/routines already identified or built
3. **Leverage Map**
   - Personal leverage
   - Shared knowledge opportunities
   - Internal tool opportunities
4. **Bottleneck Radar**
   - 3-6 likely bottlenecks, scored qualitatively
5. **AI Leverage Pathways**
   - Personal leverage path
   - Shared knowledge path
   - Internal tool path
   - Recommended path, with rationale
6. **Next 30 Days**
   - 3 concrete next moves
7. **Open Questions**
   - Missing context that would improve recommendations

## Markdown Summary

Also create:

`reports/business-snapshot.md`

Include:

- Sources read
- What was treated as personal
- What was treated as business/company-relevant
- Recommended follow-up command:
  - `/ai-leverage-brief` if there is enough context
  - `/reflect` or `/audit` if context is too thin

## Guardrails

- Do not include raw private notes, secrets, credentials, personal phone
  numbers, private emails, or sensitive financial details.
- Do not claim the business is ready for company rollout unless evidence
  supports it.
- Do not make generic AI strategy recommendations. Everything should tie
  back to the founder's actual context.
- If using demo context, clearly label the output as demo/sanitized.
