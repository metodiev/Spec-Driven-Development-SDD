# Code Review Report

| Field | Value |
| --- | --- |
| **Artifact** | `<branch / PR link>` |
| **Range** | `<base>...<head>` (`<n>` files, `+<>` / `-<>`) |
| **Specification** | `<link or "none">` |
| **Reviewer** | `<agent/human>` |
| **Independent of author** | yes / no (explain) |
| **Read-only enforcement** | technical / tool-level / worktree / instruction-only |
| **Read-only verified** | `git status --short` identical before/after: yes / no |
| **Date** | `<YYYY-MM-DD>` |
| **Verdict** | APPROVE / APPROVE WITH COMMENTS / REQUEST CHANGES / BLOCK |

**Summary:** `<n>` CRITICAL, `<n>` HIGH, `<n>` MEDIUM, `<n>` LOW, `<n>` INFO

---

## Findings

### `<C-01>` — `<one-line title>`

- **Severity:** CRITICAL · **Confidence:** `<1–10>` (`executed proof | static certainty | strong reading | heuristic`)
- **Location:** `<path:line>`
- **Requirement:** `<FR-x / AC-x.y>` or `no requirement covers this`
- **Evidence:**
  ```
  <quoted code, diff hunk, command output, or test result>
  ```
- **Impact:** `<what breaks, for whom, under what conditions>`
- **Remediation:** `<smallest change that resolves it>`
- **Verification:** `<how to prove the fix>`

---

### `<H-01>` — `<title>`

(Repeat the structure above.)

---

## Coverage notes

| Area | Reviewed? | Notes |
| --- | --- | --- |
| Diff | yes | |
| Callers of changed symbols | yes | `<how searched>` |
| Tests | yes | `<which files>` |
| Migration | yes | `<up/down verified>` |
| Generated files | no | excluded intentionally |
| Performance | no | no environment available |

## What was not executed

| Check | Reason | Consequence |
| --- | --- | --- |
| `<load test>` | no perf env | NFR-2 remains UNVERIFIED |
| `<E2E>` | browser unavailable | journey unverified |

## Positive observations

- `<something done well>` (keeps reviews balanced and reinforces good patterns)

## Recommendations (non-blocking)

| ID | Recommendation | Owner |
| --- | --- | --- |
| `L-01` | `<suggestion>` | `<team>` |

---

## Verdict rationale

`<One or two sentences: why this verdict, referencing the highest-severity finding.>`

---

*Template version: 1.0 · See [chapter 19](../19-read-only-code-review.md).*
