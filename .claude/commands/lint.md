# /lint — Wiki Health Check

You are performing a health check on the wiki to ensure it stays accurate, complete, and well-connected as it grows.

This is one of the three core wiki operations (ingest, query, lint). Run it periodically to keep the wiki healthy.

---

## Before You Start

Read:
- `wiki/index.md` — the full catalog
- `wiki/log.md` — recent operations

Then scan all articles in `wiki/concepts/` and `wiki/connections/`.

---

## Health Checks

### 1. Broken Links

Scan all articles for `[[wikilinks]]` that point to non-existent articles. Report each one.

### 2. Orphan Pages

Find articles with zero inbound links — no other article references them. These may be disconnected knowledge or missing cross-references.

### 3. Unprocessed Sources

Check `imports/` for documents that haven't been ingested (not referenced in `wiki/log.md`). Check `daily/` for session logs that haven't been compiled.

### 4. Stale Articles

Look for articles whose source material has changed or been superseded by newer information. Cross-reference article dates with recent daily logs and new imports.

### 5. Missing Backlinks

If article A links to article B, check whether B links back to A when appropriate. Asymmetric links often indicate missing cross-references.

### 6. Sparse Articles

Find articles under ~200 words that might need more detail. These could be stubs created during a fast ingest that deserve expansion.

### 7. Contradictions

The most valuable check. Look for claims in different articles that conflict with each other. This requires reading and comparing content, not just checking links.

---

## Output Format

```markdown
## Wiki Health Report — [date]

### Summary
- Total articles: [count]
- Broken links: [count]
- Orphan pages: [count]
- Unprocessed sources: [count]
- Stale articles: [count]
- Missing backlinks: [count]
- Sparse articles: [count]
- Contradictions found: [count]

### Issues (by priority)

#### Critical (fix now)
- [contradictions, broken links to important articles]

#### Important (fix soon)
- [orphan pages, stale articles, unprocessed sources]

#### Minor (fix when convenient)
- [missing backlinks, sparse articles]

### Suggested Research
- [gaps in the wiki that could be filled with a web search or founder interview]
```

---

## After the Report

> "Here's your wiki health report. [X] issues found, [Y] critical.
>
> Want me to fix the critical issues now?"

If they say yes:
- Fix broken links by creating missing articles or correcting references
- Resolve contradictions by asking the founder which version is correct
- Ingest unprocessed sources
- Add missing cross-references

After fixing, update `wiki/log.md`:

```markdown
## [YYYY-MM-DD] lint | Health check
- Fixed: [what was fixed]
- Remaining: [what still needs attention]
```
