# Verification Report: `<change-id>`

| Field | Value |
| --- | --- |
| **Commit** | `<sha>` |
| **Branch** | `<name>` |
| **Specification** | `<link>` |
| **Environment** | `<CI runner / OS / runtime / DB / image digest>` |
| **Executed at** | `<ISO-8601 UTC>` |
| **Executor** | `<agent/human>` |
| **Status** | COMPLETE / PARTIAL / BLOCKED |

---

## 1. Commands executed

| # | Command | Exit | Summary |
| --- | --- | --- | --- |
| 1 | `<command>` | 0 | `<n> passed, <n> skipped` |
| 2 | `<command>` | 0 | `<result>` |
| 3 | `<command>` | 1 | `<failure summary>` |

> Paste the actual summary line. If it was not executed, say so in §4.

---

## 2. Acceptance criteria

| AC | Status | Evidence | Notes |
| --- | --- | --- | --- |
| AC-1.1 | VERIFIED | `<test>::<name>` → passed | |
| AC-1.2 | VERIFIED | `<test>::<name>` → passed | |
| AC-2.1 | PARTIALLY VERIFIED | unit only | integration blocked by env |
| AC-3.1 | UNVERIFIED | — | perf environment unavailable |

**Coverage:** `<verified>` / `<total>` (`<percent>`)

---

## 3. Non-functional requirements

| NFR | Target | Measured | Status |
| --- | --- | --- | --- |
| NFR-1 | p95 < 300 ms | `<value>` | VERIFIED / UNVERIFIED |
| NFR-2 | no connection leak over 1h | `<observation>` | |
| NFR-3 | no HIGH CVEs | `<scan summary>` | |

---

## 4. Not performed

| Check | Reason | Risk accepted by |
| --- | --- | --- |
| `<check>` | `<reason>` | `<name/date>` |

---

## 5. Static analysis and security

| Tool | Result | Findings |
| --- | --- | --- |
| `<linter>` | clean | 0 |
| `<type checker>` | clean | 0 |
| `<SAST>` | `<n>` | `<severity breakdown>` |
| `<SCA>` | `<n>` | `<severity breakdown>` |
| `<secret scan>` | clean | 0 |

---

## 6. Regression checks

| Check | Result |
| --- | --- |
| Baseline suite (pre-change) | `<n> passed, <n> failed` |
| Current suite | `<n> passed, <n> failed` |
| New failures explained | yes/no |
| Flaky tests quarantined with owner | yes/no/n/a |

---

## 7. Environment reproducibility

| Input | Value |
| --- | --- |
| OS/image | `<digest>` |
| Runtime | `<version>` |
| Dependency lock | `<lockfile hash>` |
| Database | `<image + tag>` |
| Test data | `<fixture set / seed>` |

---

## 8. Limitations

- `<limitation with impact>`

---

## 9. Conclusion

`<One paragraph: what is proven, what is not, and what must happen before acceptance.>`

---

*Template version: 1.0 · See [chapter 20](../docs/20-testing-and-verification.md).*
