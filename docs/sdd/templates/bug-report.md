# Bug Report: `<short title>`

> One bug per report. If you find two, file two.

| Field | Value |
| --- | --- |
| **Bug ID** | `<BUG-000>` |
| **Status** | NEW / REPRODUCED / ROOT-CAUSED / FIXED / VERIFIED / CLOSED / WONTFIX |
| **Severity** | S1 outage · S2 major · S3 minor · S4 cosmetic |
| **Priority** | P1 immediate · P2 this sprint · P3 backlog |
| **Affected versions** | `<x.y.z>` |
| **First seen** | `<YYYY-MM-DD HH:MM TZ>` |
| **Environment** | `<prod / staging / OS / runtime / config>` |
| **Reporter** | `<name>` |
| **Owner** | `<name>` |

---

## 1. Symptom

`<What the user observes. Include exact error text, status code, or screenshot reference.>`

## 2. Expected vs actual

| | Description |
| --- | --- |
| **Expected** | `<behavior>` |
| **Actual** | `<behavior>` |

## 3. Reproduction

**Preconditions:** `<data, user role, feature flags, versions>`

```text
1. ...
2. ...
3. ...
```

**Automated reproduction**

```text
<failing test path / curl command / script>
```

**Reproduction rate:** `<always / 1 in N / environment-specific>`

## 4. Evidence

| Type | Content |
| --- | --- |
| Logs | `<excerpt with correlation ID, redacted>` |
| Trace | `<trace ID>` |
| Metrics | `<dashboard link / query>` |
| Stack trace | `<relevant frames>` |
| Data | `<query + result>` |

## 5. Impact

| Dimension | Assessment |
| --- | --- |
| Users affected | `<all / cohort / count>` |
| Data integrity | `<none / corrupt / lost>` |
| Security | `<none / possible exposure>` |
| Financial | `<none / estimate>` |
| Workaround | `<description or none>` |

## 6. Root cause

**Status:** `UNVERIFIED` / `PARTIALLY VERIFIED` / `VERIFIED` / `CONTRADICTED`

**Mechanism:** `<what actually happens, step by step>`

**Evidence**

- `<file:line>`
- `<command output>`
- `<git log -S result>`

**Ruled out**

- `<alternative cause>` — ruled out by `<evidence>`

## 7. Fix

| Field | Value |
| --- | --- |
| Approach | `<minimal change>` |
| Files | `<paths>` |
| Why this is minimal | `<what it deliberately does not change>` |
| Risk | `<what could break>` |
| Approved by | `<name>` (if required) |

## 8. Regression test

| Field | Value |
| --- | --- |
| Test | `<path::name>` |
| Fails on base commit | `<yes — verified by: command>` |
| Passes on fix commit | `<yes — verified by: command>` |
| Asserts | `<user-visible behavior>` |

## 9. Verification

| Check | Command | Result |
| --- | --- | --- |
| Reproduction | `<command>` | PASS |
| Regression test | `<command>` | PASS |
| Full suite | `<command>` | `<n> passed, <m> skipped` |
| Static analysis | `<command>` | clean |
| Monitoring | `<query>` | recovered at `<time>` |

## 10. Follow-ups

| Item | Owner | Ticket |
| --- | --- | --- |
| `<same pattern elsewhere>` | `<name>` | `<link>` |
| `<missing test coverage>` | `<name>` | `<link>` |

---

## 11. Timeline (incidents)

| Time (UTC) | Event |
| --- | --- |
| `<HH:MM>` | Alert fired |
| `<HH:MM>` | Triaged |
| `<HH:MM>` | Mitigated |
| `<HH:MM>` | Root cause confirmed |
| `<HH:MM>` | Fix deployed |

---

*Template version: 1.0 · See [chapter 15](../15-bug-fixing.md) for the workflow.*
