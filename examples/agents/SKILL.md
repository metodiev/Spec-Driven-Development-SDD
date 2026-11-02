---
name: read-only-code-review
description: Review a git diff without modifying files. Use when asked to review code, a branch, a commit, or a pull request.
---

# Read-only code review (example skill)

> **Example only.** Install by copying this directory into your agent's skills folder,
> e.g. `.github/skills/read-only-code-review/SKILL.md`.

## Constraints

- Do **not** edit any file. Do not run formatters or linters with `--fix`.
- Do **not** commit, push, branch, or change issue state.
- Record `git status --short` before and after; any change is a process failure.

## Procedure

1. `git --no-pager diff --stat <base>...HEAD` and `git --no-pager diff <base>...HEAD`.
2. For each hunk, read the surrounding code and every caller of the changed symbol.
3. Map each change to a requirement (`FR-*`/`AC-*`) or a reported defect.
4. Verify the tests assert the acceptance criteria, not just that mocks were called.
5. Run the risk passes relevant to the diff: correctness, concurrency, data, security,
   contracts, operability, maintainability.
6. Produce findings with severity, confidence, `file:line`, evidence, impact, remediation,
   and verification.

## Severity

| Severity | Criteria |
| --- | --- |
| CRITICAL | Data loss, security breach, outage, silently wrong core results |
| HIGH | Broken requirement, regression outside the diff, authorization gap |
| MEDIUM | Plausible correctness risk, missing key test, maintainability hazard |
| LOW | Naming, dead code, minor duplication |
| INFO | Question or alternative |

## Output

Use `templates/code-review-report.md`. End with an explicit list of what was **not**
verified.
