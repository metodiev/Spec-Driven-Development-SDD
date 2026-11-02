# Feature Specification: `<change-id>`

> Template. Replace all `<...>` placeholders. Delete guidance blockquotes before merging.
> Keep requirement IDs stable once review starts.

| Field | Value |
| --- | --- |
| **Spec ID** | `<sdd-000>` |
| **Author** | `<name>` |
| **Status** | DRAFT / IN REVIEW / APPROVED / IMPLEMENTED / SUPERSEDED |
| **Created** | `<YYYY-MM-DD>` |
| **Approved by** | `<name>` on `<YYYY-MM-DD>` |
| **Related ADRs** | `<ADR-0001>` |

---

## 1. Problem statement

> Who is affected, what is broken or missing, what it costs. **No solution language.**

`<2–5 sentences. Include the current workaround and its cost.>`

### Evidence of the problem

| Source | Observation |
| --- | --- |
| `<support tickets / analytics / interview>` | `<quantified observation>` |

---

## 2. Goals

- **G-1** `<measurable outcome>`
- **G-2** `<measurable outcome>`

## 3. Non-goals

- **NG-1** `<explicit exclusion>`
- **NG-2** `<explicit exclusion>`

> If the non-goals list is empty, the scope is unbounded.

---

## 4. Users and scenarios

| Actor | Scenario | Value |
| --- | --- | --- |
| `<role>` | `<what they do>` | `<why it matters>` |

---

## 5. Functional requirements

### FR-1 `<short title>`

`<Normative statement. Use SHALL / MUST for obligations.>`

**Acceptance criteria**

- **AC-1.1** Given `<precondition>`, when `<action>`, then `<observable outcome>`.
- **AC-1.2** Given `<precondition>`, when `<action>`, then `<observable outcome>`.

**Edge cases**

| Case | Expected behavior |
| --- | --- |
| `<empty / max / duplicate / unauthorized>` | `<behavior>` |

**Failure scenarios**

| Failure | Detection | Behavior | Recovery |
| --- | --- | --- | --- |
| `<dependency down>` | `<signal>` | `<response>` | `<action>` |

### FR-2 `<short title>`

`...`

---

## 6. Non-functional requirements

| ID | Category | Target | Condition | Verification |
| --- | --- | --- | --- | --- |
| NFR-1 | Performance | p95 `< 300 ms` | `<50 RPS, 5M rows>` | `<load test path>` |
| NFR-2 | Availability | `99.9%/month` | `<production>` | `<SLO dashboard>` |
| NFR-3 | Security | `<control>` | `<threat>` | `<test / scan>` |
| NFR-4 | Compatibility | `<contract>` | `<consumers>` | `<contract test>` |

> Every NFR needs a number, a condition, and a verification method. Without the third, it is a wish.

---

## 7. Security requirements

| Concern | Requirement |
| --- | --- |
| Authentication | `<required mechanism>` |
| Authorization | `<resource-level rule>` |
| Data classification | `<public/internal/confidential/restricted>` |
| Audit | `<what is logged, where, retention>` |
| Secrets | `<source>` |

---

## 8. Compatibility requirements

| Surface | Change | Backward compatible? | Mitigation |
| --- | --- | --- | --- |
| Public API | `<add/change/remove>` | `<yes/no>` | `<versioning / shim>` |
| Database schema | `<migration>` | `<yes/no>` | `<expand/contract>` |
| Events | `<topic/schema>` | `<yes/no>` | `<versioned topic>` |
| Config | `<key>` | `<yes/no>` | `<default preserved>` |

---

## 9. Observability requirements

| Signal | What it must answer |
| --- | --- |
| Metrics | `<is it failing, how often, how slow>` |
| Logs | `<who did what, with correlation ID, no PII>` |
| Traces | `<where time is spent across services>` |
| Alerts | `<what pages a human, with runbook link>` |

---

## 10. Rollback and migration

| Artifact | Reversible? | Procedure | Time | Data loss |
| --- | --- | --- | --- | --- |
| Deploy | `<yes/no>` | `<steps>` | `<minutes>` | `<none/description>` |
| Migration | `<yes/no>` | `<steps>` | `<minutes>` | `<description>` |
| Feature flag | `<yes/no>` | `<flag name>` | `<seconds>` | `<none>` |

---

## 11. Open questions

| ID | Question | Blocking? | Owner | Status |
| --- | --- | --- | --- | --- |
| Q-1 | `<question>` | yes/no | `<name>` | OPEN / ANSWERED / DEFERRED |

> Non-blocking questions must state the default that will be assumed.

---

## 12. Traceability

| Requirement | Tasks | Tests | Evidence |
| --- | --- | --- | --- |
| FR-1 | `<T-01, T-02>` | `<test names>` | `<ledger row>` |
| FR-2 | `<T-03>` | `<test names>` | `<ledger row>` |

---

## 13. Review record

| Reviewer | Date | Findings | Status |
| --- | --- | --- | --- |
| `<name>` | `<date>` | `<count by severity>` | `<approved / changes requested>` |

---

*Template version: 1.0 · See [chapter 14](../docs/14-feature-development.md) for usage guidance.*
