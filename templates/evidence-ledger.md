# Evidence Ledger: `<change-id>`

> One row per significant claim. If a claim is not here, it is not evidenced.

| Field | Value |
| --- | --- |
| **Change** | `<change-id>` |
| **Commit range** | `<base>..<head>` |
| **Owner** | `<name>` |
| **Updated** | `<YYYY-MM-DD>` |

---

## 1. Ledger

| # | Claim | Evidence | Method | Status | Confidence |
| --- | --- | --- | --- | --- | --- |
| 1 | `<claim>` | `<file:line / command output / doc URL + version>` | inspection / test / static analysis / docs | VERIFIED | 9/10 |
| 2 | `<claim>` | `<...>` | `<...>` | PARTIALLY VERIFIED | 7/10 |
| 3 | `<claim>` | `not executed` | — | UNVERIFIED | — |
| 4 | `<claim>` | `<contradicting evidence>` | test | CONTRADICTED | 8/10 |

---

## 2. Status definitions

| Status | Definition | May be reported as done? |
| --- | --- | --- |
| `VERIFIED` | Direct evidence for this exact claim and version | Yes |
| `PARTIALLY VERIFIED` | Evidence exists; scope limited | Yes, with the limit stated |
| `UNVERIFIED` | No evidence | **No** |
| `CONTRADICTED` | Evidence contradicts the claim | **No — blocker** |

---

## 3. Confidence rubric

| Score | Basis |
| --- | --- |
| 9–10 | Executed proof (test/scan) or static certainty |
| 7–8 | Strong reading of code/contract with supporting evidence |
| 4–6 | Inference from partial evidence; plausible alternative exists |
| 1–3 | Speculation |

---

## 4. Unverified and contradicted items

### UNVERIFIED

| # | Claim | What is needed | Owner | Blocking? |
| --- | --- | --- | --- | --- |
| 3 | `<claim>` | `<test / environment>` | `<name>` | yes/no |

### CONTRADICTED

| # | Claim | Contradicting evidence | Resolution |
| --- | --- | --- | --- |
| 4 | `<claim>` | `<evidence>` | `<action>` |

---

## 5. External sources

| Claim | Source | Version | Date checked |
| --- | --- | --- | --- |
| `<framework behavior>` | `<official docs URL>` | `<x.y.z>` | `<YYYY-MM-DD>` |

---

## 6. Change log

| Date | Change | By |
| --- | --- | --- |
| `<date>` | `<what changed>` | `<name>` |

---

*Template version: 1.0 · See [chapter 23](../23-hallucination-prevention.md).*
