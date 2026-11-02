# Documentation Tooling

Two validators, deliberately separated by dependency weight.

| Tool | Requires | What it checks |
| --- | --- | --- |
| [`validate_docs.py`](./validate_docs.py) | Python 3.8+ standard library | Links, anchors, code fences, table columns, JSON, YAML structure, YAML front matter, Mermaid structure |
| [`check_mermaid.mjs`](./check_mermaid.mjs) | Node + `mermaid` + `jsdom` in a scratch dir | Real Mermaid parsing (syntax errors) |

## Running

The default root is the repository root (`.`), so no arguments are required. Vendor and build
directories (`.git`, `.github`, `node_modules`, `dist`, `build`, `target`, `__pycache__`, `.venv`)
are skipped automatically.

```bash
# Standard, dependency-free
python3 tools/validate_docs.py

# Machine-readable
python3 tools/validate_docs.py --json

# Strict (warnings fail)
python3 tools/validate_docs.py --strict
```

```bash
# Optional Mermaid parser check (nothing installed into the repo)
mkdir -p "$TMPDIR/mmcheck" && cd "$TMPDIR/mmcheck" && npm init -y && npm i mermaid@11 jsdom
node tools/check_mermaid.mjs . "$TMPDIR/mmcheck/node_modules"
```

## What each check can and cannot prove

| Check | Proves | Does not prove |
| --- | --- | --- |
| Links | Targets exist, anchors resolve | The target still says what you think |
| Fences | Balanced and labeled | The code compiles |
| Tables | Every row has the header's column count | The content is correct |
| JSON | Parses as JSON | The values are correct |
| YAML (fenced and front matter) | Parses (with PyYAML) or is structurally plausible | Schema validity, CI semantic correctness |
| Mermaid structure | Diagram type and `subgraph`/`end` balance | Renderability |
| Mermaid parse | The parser accepts the syntax | Visual layout quality |

> **YAML note:** without PyYAML the validator performs structural checks only and says so. For a
> full parse in CI, install `pyyaml` in the CI environment.

## Adding a new chapter

1. Create the Markdown file with a language tag on every fence.
2. Add it to the chapter index in [`docs/00-index.md`](../docs/00-index.md).
3. Run `python3 tools/validate_docs.py` and, if Mermaid changed, the parser check.
4. Verify every external link you add is the official source and note the version/date.

## Limitations

- External URLs are never fetched (offline-safe by design).
- The link checker ignores links inside code fences.
- Anchor slugification approximates GitHub; unusual heading punctuation may produce a false
  positive.
- No spell check, no prose linter, no accessibility check.
