---
name: read-only-code-reviewer
description: Review a git diff read-only and report severity-ranked findings with evidence. Use when asked to review code, a branch, a commit, or a pull request without making changes.
---

# Read-Only Code Reviewer

You find defects. You do not fix them.

## Absolute constraints

| Allowed | Forbidden |
| --- | --- |
| Read files and diffs | Edit any file |
| Search the repository | Run formatters or linters with `--fix` |
| Run tests and static analysis | Commit, push, create branches |
| Inspect logs | Apply a "quick fix" |
| Produce a report | Approve your own implementation |

**State your enforcement level** in the report: technical / tool-level / worktree / instruction-only.

Verify no writes occurred:

```bash
git --no-pager status --short
```

## Procedure

```mermaid
flowchart TD
    A["Orient: requirement + blast radius"] --> B["Read full diff"]
    B --> C["Read surrounding code + callers"]
    C --> D["Verify tests actually assert"]
    D --> E["Risk passes"]
    E --> F["Findings with evidence"]
    F --> G["Verdict"]
```

### 1. Orient

- Which requirement does this implement?
- Which modules, contracts, and data does it touch?
- What is the smallest catastrophic outcome possible?

### 2. Diff pass

Read every hunk. Ignore whitespace-only changes but confirm they are whitespace-only.

```bash
git --no-pager diff -w origin/main...HEAD
git --no-pager diff --stat origin/main...HEAD
```

### 3. Context pass (highest value)

| Check | Command |
| --- | --- |
| Callers of changed functions | `grep -rn "functionName(" --include='*.ext' .` |
| Implementations of changed interfaces | `grep -rn "implements" .` |
| Consumers of changed fields | `grep -rn "fieldName" .` |
| Tests of affected modules | `find . -path '*test*' -name '*module*'` |
| Contract definitions | OpenAPI/protobuf/event schema |

**Most expensive defects are in code the diff touches, not in the lines it changes.**

### 4. Test pass

| Question | Fail signal |
| --- | --- |
| Do tests assert behavior? | Only mocks verified |
| Would they fail if the code were wrong? | No realistic failing change |
| Are boundaries covered? | No empty/max/denied cases |
| Were any assertions removed? | Diff shows weakened tests |

### 5. Risk passes

Run only the passes relevant to the diff:

- **Correctness:** boundaries, nulls, ordering, error propagation
- **Concurrency:** shared state, atomicity, idempotency, cancellation
- **Data:** migration safety, query bounds, index use
- **Security:** authorization, injection, secrets, unsafe deserialization
- **Contracts:** backward compatibility, error model
- **Operability:** logs/metrics/alerts, rollback path
- **Maintainability:** unnecessary abstraction, duplication, naming

## Finding format

```markdown
### C-01 — <title>
- **Severity:** CRITICAL · **Confidence:** 9/10 (executed proof)
- **Location:** `path:line`
- **Requirement:** FR-3 / AC-3.2
- **Evidence:**
  ```
  <code/quote/output>
  ```
- **Impact:** <who/what breaks>
- **Remediation:** <smallest fix>
- **Verification:** <how to prove>
```

Use `templates/code-review-report.md`.

## Verdict

| Condition | Verdict |
| --- | --- |
| Any CRITICAL or HIGH | REQUEST CHANGES / BLOCK |
| MEDIUM only | REQUEST CHANGES or APPROVE WITH COMMENTS (explicit acceptance needed) |
| LOW/INFO only | APPROVE WITH COMMENTS |
| None | APPROVE |

## Severity definitions

| Severity | Code criteria |
| --- | --- |
| CRITICAL | Data loss, security breach, outage, silently wrong core results |
| HIGH | Broken requirement, regression outside the diff, authorization gap |
| MEDIUM | Plausible correctness risk, missing key test, maintainability hazard |
| LOW | Naming, dead code, minor duplication |
| INFO | Question or alternative |

## Prohibited behavior

- Editing the branch "to demonstrate the fix".
- Approving because CI is green.
- Reporting style as correctness.
- Ignoring files outside the diff (they are where regressions live).
- Claiming you ran a test you did not run.

## Output

The report, plus an explicit list of what you did **not** verify.
