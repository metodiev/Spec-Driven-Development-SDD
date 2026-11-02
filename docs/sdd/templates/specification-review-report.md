# Specification Review Report

| Field | Value |
| --- | --- |
| **Artifact under review** | `spec.md`, `plan.md`, `tasks.md` @ `<commit>` |
| **Reviewer** | `<agent/human>` |
| **Independent of author** | yes / no |
| **Read-only enforcement** | technical / tool-level / worktree / instruction-only |
| **Read-only verified** | no files modified: yes / no |
| **Date** | `<YYYY-MM-DD>` |
| **Verdict** | APPROVE / APPROVE WITH COMMENTS / REQUEST CHANGES / BLOCK |

**Summary:** `<n>` CRITICAL, `<n>` HIGH, `<n>` MEDIUM, `<n>` LOW, `<n>` INFO

---

## 1. Dimension results

| Dimension | Result | Notes |
| --- | --- | --- |
| Ambiguity | PASS / FAIL | `<notes>` |
| Completeness | PASS / FAIL | |
| Consistency | PASS / FAIL | |
| Testability | PASS / FAIL | |
| Security coverage | PASS / FAIL | |
| Performance coverage | PASS / FAIL | |
| Compatibility coverage | PASS / FAIL | |
| Operability coverage | PASS / FAIL | |
| Scope / non-goals | PASS / FAIL | |
| Traceability | PASS / FAIL | |

---

## 2. Findings

### `<S-01>` — `<title>`

- **Severity:** HIGH · **Confidence:** `<1–10>`
- **Requirement:** `<FR-x / AC-x.y / section>`
- **Finding:** `<what is wrong>`
- **Evidence:** `<quote from the spec with line/section>`
- **Why it matters:** `<implementation risk if unresolved>`
- **Recommendation:** `<specific rewrite or addition>`

---

## 3. Ambiguity probes

For each requirement, record the two-implementation test result.

| Requirement | Implementation A | Implementation B | Ambiguous? |
| --- | --- | --- | --- |
| `<FR-1>` | `<interpretation>` | `<interpretation>` | yes/no |
| `<FR-2>` | `<interpretation>` | `<interpretation>` | yes/no |

---

## 4. Missing content checklist

| Expected content | Present? | Location if missing |
| --- | --- | --- |
| Problem statement without solution bias | yes/no | |
| Measurable goals | yes/no | |
| Explicit non-goals | yes/no | |
| Acceptance criteria per requirement | yes/no | |
| Edge cases | yes/no | |
| Failure scenarios | yes/no | |
| Security requirements | yes/no | |
| Performance requirements (with numbers) | yes/no | |
| Compatibility requirements | yes/no | |
| Rollback / migration plan | yes/no | |
| Observability requirements | yes/no | |
| Task traceability | yes/no | |

---

## 5. Contradictions found

| ID | Statement A | Statement B | Resolution needed |
| --- | --- | --- | --- |
| `<X-01>` | `<spec:line>` | `<spec:line>` | `<question for author>` |

---

## 6. Author response record

| Finding | Response | Evidence | Status |
| --- | --- | --- | --- |
| `S-01` | `<accepted / disputed>` | `<evidence>` | OPEN / RESOLVED / WITHDRAWN |

> Withdrawn findings stay in the record with the reason. A withdrawn finding is a success of the
> evidence process.

---

## 7. Gate decision

| Condition | Met? |
| --- | --- |
| No open CRITICAL | yes/no |
| No open HIGH | yes/no |
| Every requirement has ≥ 1 AC | yes/no |
| Every NFR has a verification method | yes/no |
| Non-goals are specific | yes/no |

**Decision:** `<APPROVE / BLOCK>` — `<rationale>`

---

*Template version: 1.0 · See [chapter 17](../17-specification-review.md).*
