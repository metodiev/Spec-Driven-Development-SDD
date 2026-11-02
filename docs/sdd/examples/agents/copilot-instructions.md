# Repository rules (example)

> **Example only.** Copy to `.github/copilot-instructions.md` and adapt.
> See [chapter 12](../../12-coding-agent-integration.md).

## Non-negotiables

- Never commit secrets or credentials.
- Read the relevant specification before changing behavior.
- Every change to `src/` requires a test.
- Do not add a dependency without an ADR in `docs/adr/`.
- Do not run `git reset --hard`, `git clean -fd`, or `git push --force`.

## Commands

- Test: `<test command>`
- Lint: `<lint command>`
- Type check: `<typecheck command>`

## Architecture

- HTTP handlers: `src/api/` — must not import `src/infra/`.
- Domain: `src/domain/` — no framework imports.
- Persistence: `src/infra/` — the only place that talks to the database.

## Evidence

- Quote command output when reporting test results.
- Label claims `VERIFIED`, `PARTIALLY VERIFIED`, `UNVERIFIED`, or `CONTRADICTED`.
- If you cannot run a check, say so instead of assuming it passes.

## Deeper documentation

- Process: `docs/sdd/README.md`
- Review: `docs/sdd/19-read-only-code-review.md`
- Evidence rules: `docs/sdd/23-hallucination-prevention.md`
