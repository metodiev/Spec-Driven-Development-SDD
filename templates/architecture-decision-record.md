# ADR-`<number>`: `<short decision title>`

| Field | Value |
| --- | --- |
| **Status** | Proposed / Accepted / Deprecated / Superseded by `<ADR-n>` |
| **Date** | `<YYYY-MM-DD>` |
| **Deciders** | `<names/roles>` |
| **Consulted** | `<names>` |
| **Informed** | `<names>` |
| **Supersedes** | `<ADR-n or none>` |
| **Review date** | `<YYYY-MM-DD>` |

---

## 1. Context

`<What forces are at play? Business constraint, technical constraint, NFRs, timeline, team size.
State facts with evidence; avoid advocacy.>`

### Requirements driving this decision

| ID | Requirement |
| --- | --- |
| `<FR-x>` | `<summary>` |
| `<NFR-x>` | `<summary>` |

### Constraints

- `<constraint>`
- `<constraint>`

---

## 2. Decision

`<One paragraph, active voice: "We will …".>`

```mermaid
flowchart LR
    C["<Context>"] --> A["<Component A>"]
    A --> B["<Component B>"]
```

---

## 3. Alternatives considered

| Option | Pros | Cons | Rejected because |
| --- | --- | --- | --- |
| `<A>` | `<pros>` | `<cons>` | `<reason>` |
| `<B>` | `<pros>` | `<cons>` | `<reason>` |
| `<C>` (chosen) | `<pros>` | `<cons>` | — |

> "Do nothing" is a legitimate alternative. Record it if considered.

---

## 4. Consequences

### Positive

- `<consequence>`

### Negative

- `<consequence>`

### Neutral

- `<consequence>`

### Follow-up actions

| Action | Owner | Due |
| --- | --- | --- |
| `<action>` | `<name>` | `<date>` |

---

## 5. Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `<risk>` | low/med/high | low/med/high | `<mitigation>` |

---

## 6. Reversibility

| Aspect | Reversible? | Cost to reverse |
| --- | --- | --- |
| `<data model>` | no | `<migration + downtime>` |
| `<API contract>` | no | `<version + deprecation>` |
| `<library>` | yes | `<days>` |

---

## 7. Validation

`<How will we know this decision was right? Metric, date, threshold.>`

| Metric | Target | Reviewed on |
| --- | --- | --- |
| `<metric>` | `<target>` | `<date>` |

---

## 8. References

- `<spec link>`
- `<official docs link, version-checked>`
- `<benchmark / spike result>`

---

*Template version: 1.0 · See [chapter 18](../18-architecture-review.md).*
