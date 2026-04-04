# Privacy and Imports

ARC works best when it has real business context, but you should still be thoughtful about what you import.

---

## Good Things To Import

These are usually safe and useful:
- pitch decks
- one-pagers
- website copy
- positioning docs
- strategy memos
- process notes
- meeting notes
- operating documents
- example emails or briefs you wrote yourself

These help ARC learn how your business works and how you communicate.

---

## Be Careful With

Think twice before importing:
- customer PII
- employee-sensitive information
- raw HR documents
- legal agreements
- medical or regulated data
- secrets, credentials, tokens, or passwords
- anything you would not want copied into an AI-assisted workflow

If you do need ARC to work with sensitive material, use the minimum necessary detail and review outputs carefully.

---

## A Good Rule Of Thumb

Ask yourself:

> "Would I be comfortable using this document in an AI-assisted working session with review?"

If the answer is no, do not import it as-is.

Instead:
- redact it
- summarize it
- strip out sensitive fields
- or give ARC a higher-level description instead

---

## Imported Documents Are Context, Not Truth

Anything in `imports/` should be treated as a source, not as the final source of truth.

That means:
- ARC should extract useful facts from imports
- ARC should confirm important details with the founder when needed
- corrected context files should override outdated imports

If a document is old, partial, or aspirational, ARC should not blindly treat it as current reality.

---

## Best Practice For Founders

For workshop use, the best pattern is:

1. import a few useful documents
2. let ARC extract the important context
3. confirm or correct what matters
4. keep the structured context files current over time

That gives you the value of imports without turning the workspace into a messy document dump.
