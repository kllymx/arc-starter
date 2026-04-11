# /ingest — Process a Document into the Wiki

You are helping a founder add new knowledge to the wiki by processing a document from `imports/`.

This is one of the three core wiki operations (ingest, query, lint). A single ingest might touch 10-15 wiki pages.

---

## Before You Start

Read:
- `context/workspace.md`
- `wiki/index.md` — know what's already in the wiki

Check `imports/` for documents to process. If the founder specified a particular document, process that one. If they said "ingest everything" or "process new imports," check which files haven't been processed yet (cross-reference with `wiki/log.md`).

If `imports/` is empty:

> "There's nothing in the imports folder yet. Drop any document there — pitch decks, articles, meeting notes, competitor research, anything — and tell me to ingest it."

---

## Ingest Process

For each document:

### Step 1 — Read the raw source

Read the full document. This is immutable — you never modify files in `imports/`.

### Step 2 — Extract key information

Identify: concepts, entities, claims, data points, strategies, tools, people, relationships.

### Step 3 — Discuss with the founder (optional)

If the document is substantial, briefly share key takeaways before filing:

> "Here's what I'm pulling from this document: [2-3 key points]. Anything I should emphasize or skip?"

For simple documents, proceed directly.

### Step 4 — Create or update wiki articles

- **New concepts** → create articles in `wiki/concepts/`
- **New entities** (people, companies, tools) → create articles in `wiki/concepts/`
- **Existing articles** → update with new information from this source
- **Cross-cutting insights** → create articles in `wiki/connections/`

Every article must:
- Use YAML frontmatter with `source: import`
- Include `[[wikilinks]]` to related articles
- Have a `## Related` section

### Step 5 — Flag contradictions

If new information conflicts with existing wiki content, flag it explicitly:

> "This document says [X], but the wiki currently says [Y]. Which is correct?"

Update the wiki based on the founder's answer, or note the contradiction in both articles if unresolved.

### Step 6 — Update the index

Add all new articles to `wiki/index.md` with one-line summaries. Update summaries for any modified articles.

### Step 7 — Log the ingest

Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | [Document Name]
- Source: imports/[filename]
- Created: [[article1]], [[article2]], ...
- Updated: [[article3]] — added [what]
- Flagged: [any contradictions]
```

---

## After the Ingest

> "Done. I've created [X] new articles and updated [Y] existing ones from [document name]. The wiki now has [total] articles.
>
> Here's what's new: [brief list of articles created/updated]"

If the ingest revealed gaps worth investigating:

> "This document also raised some questions I couldn't answer from the wiki. Want me to research: [question]?"

If they say yes, do the research and file the results back into the wiki (the compounding loop).
