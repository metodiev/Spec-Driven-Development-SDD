# docs/ — the SDD handbook

This directory holds the chapter content. The **authoritative index is
[00-index.md](./00-index.md)**: learning path, full chapter table, the nine rules, the maturity
model, and the validation log. This page exists so that browsing the folder on GitHub does not
drop you into a bare file list.

> **New here?** Start at the repository [README](../README.md) for what SDD is and why it beats
> prompting, then read [01 — Fundamentals](./01-fundamentals.md).

---

## Where to go

| If you want… | Start at |
| --- | --- |
| The full chapter table and reading order | [00-index.md](./00-index.md) |
| The vocabulary and principles | [01 — Fundamentals](./01-fundamentals.md) |
| The phase model A–H | [02 — Engineering lifecycle](./02-engineering-lifecycle.md) |
| To choose a tool | [04 — Tool comparison](./04-tool-comparison.md) |
| Your language's commands and failure modes | [language-guides/](../language-guides/README.md) |
| Plan / implement / verify wording | [36 — Agent prompt playbook](./36-agent-prompt-playbook.md) |
| What an agent must do when it cannot verify | [37 — Escaping hallucination](./37-agent-anti-hallucination.md) |
| A complete worked ticket | [33 — End-to-end walkthrough](./33-end-to-end-walkthrough.md) |
| IDE setup | [29 — IDE overview](./29-ide-setup.md) |

Chapters are numbered `01`–`37`. **There is no `13`**: the language guides live in
[language-guides/](../language-guides/README.md) so that each guide can be linked and versioned on
its own.

## Conventions used in every chapter

Each chapter follows the same shape, so you can skim: purpose → when to use it → the body →
references. Chapters that make checkable claims about tools, versions, or commands also carry a
**verification** section stating exactly what was and was not executed; a chapter with nothing to
verify omits it rather than padding. Every chapter ends with a **Previous / Next / Back to index**
footer, so you can read straight through or jump out at any point.

- Claims about tool behaviour are dated and cite the primary source.
- Examples that were not executed are labelled as illustrative.
- Evidence status uses one vocabulary throughout: `VERIFIED`, `PARTIALLY VERIFIED`, `UNVERIFIED`,
  `CONTRADICTED`.

## Validate before you trust

```bash
python3 tools/validate_docs.py          # from the repository root
```

Links, anchors, code fences, table columns, JSON, YAML, front matter, and Mermaid structure are
checked mechanically. The current state is recorded in
[00-index.md § 8](./00-index.md#8-validation-status).
