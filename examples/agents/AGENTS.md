# AGENTS.md (example)

> **Example only.** This file is not active in this repository. Copy it into your project root and
> replace every `<placeholder>`. See [chapter 12](../../12-coding-agent-integration.md).

## Project

`<Project name>` — `<one-line description>`.

## Non-negotiables

1. Never commit secrets. `.env*` is gitignored; document variables in `.env.example`.
2. Specification before implementation. Read `specs/<id>/spec.md` before changing code.
3. Every behavior change needs a test that fails before and passes after.
4. Do not add dependencies without approval and an ADR.
5. Never run destructive Git commands (`reset --hard`, `clean`, `checkout --`, force-push).
6. Report unverified claims as `UNVERIFIED`; never fabricate test or build results.

## Commands

| Purpose | Command |
| --- | --- |
| Install | `<install command>` |
| Test | `<test command>` |
| Lint | `<lint command>` |
| Type check | `<typecheck command>` |
| Build | `<build command>` |

> Replace these with the commands that actually work in this repository. Verify by running them.

## Architecture boundaries

- `<layer A>` may depend on `<layer B>`, never the reverse.
- HTTP handlers live in `<path>` and must not import from `<infra path>`.
- Domain logic lives in `<path>` and has no framework imports.

## Conventions

- Language/runtime: `<version>`
- Formatter: `<tool>` — run in check mode; do not reformat unrelated files.
- Test naming: `<pattern>`

## Git mode

**Active mode: `<1 | 2 | 3 | 4>`** — see `22-git-and-commit-policy.md`.

## Where to look

- Process: `README.md`
- Review rules: `19-read-only-code-review.md`
- Evidence rules: `23-hallucination-prevention.md`
- ADRs: `docs/adr/`
