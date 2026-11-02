# 24 — Multi-Agent Engineering

> More agents is not more quality. It is more context, more coordination cost, and more places
> for a claim to go unverified. Add a role only when it owns a distinct decision.

---

## 1. Purpose

Define a role-based architecture for agents working under SDD: who decides what, who shares
context, who must be isolated, and where human gates sit.

```mermaid
flowchart TB
    subgraph Authority["Human authority"]
        H["Product owner / engineering lead"]
    end
    subgraph Plan["Planning roles"]
        PA["Product analyst"]
        RE["Requirements engineer"]
        AR["Software architect"]
        SR["Specification reviewer"]
    end
    subgraph Build["Execution roles"]
        IA["Implementation agent"]
        TE["Test engineer"]
    end
    subgraph Verify["Verification roles"]
        CR["Code reviewer"]
        SEC["Security reviewer"]
        REL["Release engineer"]
    end
    H --> PA --> RE --> AR --> SR --> IA --> TE --> CR --> SEC --> REL --> H
```

---

## 2. When to use multi-agent (and when not to)

| Use multi-agent | Use a single agent |
| --- | --- |
| Independent review is required | Small, low-risk change |
| Specialist knowledge (security, DB) | One module, one developer |
| Parallel work packages with no overlap | Sequential work in one file |
| Regulated audit trail | Prototype |
| High blast radius | Documentation edit |

```mermaid
flowchart TD
    Q1{"Is there a decision<br/>one agent cannot make<br/>independently?"}
    Q1 -->|no| S["Single agent + human review"]
    Q1 -->|yes| Q2{"Does the role need<br/>different permissions?"}
    Q2 -->|yes| M["Multi-agent with access separation"]
    Q2 -->|no| Q3{"Does it need isolated<br/>context to be honest?"}
    Q3 -->|yes| M
    Q3 -->|no| S
```

### Trade-offs

| Dimension | Single agent | Multi-agent |
| --- | --- | --- |
| Cost | Lower | Higher (context, tokens, coordination) |
| Latency | Lower | Higher |
| Independence | Weak (self-review) | Strong (separate context) |
| Context fidelity | High (one thread) | Lower (handoffs lose nuance) |
| Auditability | Lower | Higher (artifacts per role) |
| Failure modes | Rationalization | Handoff drift, duplicated work, conflicting edits |

> **Default:** one implementation agent + one independent reviewer. That single split captures
> most of the benefit at a fraction of the coordination cost.

---

## 3. Role definitions

| Role | Owns | Must not | Access |
| --- | --- | --- | --- |
| **Product analyst** | Problem statement, users, success metrics | Specify implementation | Read + product docs |
| **Requirements engineer** | `spec.md`, acceptance criteria | Choose architecture | Read + spec write |
| **Software architect** | `plan.md`, ADRs, task breakdown | Implement | Read + plan write |
| **Specification reviewer** | Spec finding report | Edit the spec | **Read-only** |
| **Implementation agent** | Code + tests within scope | Approve own work, change architecture silently | Read/write in worktree |
| **Test engineer** | Test design, coverage mapping | Weaken tests to pass | Read/write tests |
| **Security reviewer** | Threat model, security findings | Apply fixes | **Read-only** + scanners |
| **Code reviewer** | Diff findings, verdict | Edit files | **Read-only** |
| **Release engineer** | Branch, PR, CI, release notes | Merge without approval | Git write to agent branch |

### Access matrix

| Artifact | PA | RE | AR | SpecRev | Impl | Test | SecRev | CodeRev | Rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intake | W | R | R | R | R | R | R | R | R |
| `spec.md` | R | **W** | R | **R-only** | R | R | R | R | R |
| `plan.md` | R | R | **W** | **R-only** | R | R | R | R | R |
| Source code | — | — | R | **R-only** | **W** | R | **R-only** | **R-only** | R |
| Tests | — | — | R | R | **W** | **W** | R | R | R |
| ADRs | — | R | **W** | R | R | R | R | R | R |
| Review reports | — | R | R | **W** | R | R | **W** | **W** | R |

`W` = may write · `R` = may read · `R-only` = read but must not modify · `—` = no access needed

---

## 4. Context sharing vs isolation

```mermaid
flowchart LR
    subgraph Shared["Shared context (artifacts)"]
        S1["spec.md"]
        S2["plan.md"]
        S3["tasks.md"]
        S4["ADRs"]
        S5["evidence ledger"]
    end
    subgraph Isolated["Isolated context (independent judgment)"]
        I1["Implementation session"]
        I2["Reviewer session"]
        I3["Security session"]
    end
    Shared --> I1
    Shared --> I2
    Shared --> I3
    I1 -.->|"diff + verification"| Shared
    I2 -.->|"findings"| Shared
```

| Context | Share? | Why |
| --- | --- | --- |
| Specification | **Yes** | It is the contract |
| Plan and ADRs | **Yes** | Decisions must be consistent |
| Evidence ledger | **Yes** | Prevents duplicate verification |
| Implementation chat history | **No** | Reviewer independence |
| Reviewer's reasoning chain | **No** | Author must respond to findings, not vibes |
| Security findings | **Partial** | Share remediation requirements, not exploit detail |
| Personal preferences | **No** | Not policy |

> **Handoff rule:** pass **artifacts**, not conversation. If a role needs the chat transcript to
> do its job, the artifacts are incomplete.

---

## 5. Artifact-based handoff

```mermaid
sequenceDiagram
    participant RE as Requirements
    participant SR as Spec reviewer
    participant IA as Implementation
    participant CR as Code reviewer
    participant H as Human

    RE->>SR: spec.md + plan.md (commit SHA)
    SR-->>RE: findings report
    RE->>RE: revise and record responses
    RE->>IA: approved spec + tasks + constitution
    IA-->>IA: implement in worktree
    IA->>CR: diff + verification report + evidence ledger
    CR-->>IA: findings report (read-only)
    IA->>IA: fix or dispute with evidence
    IA->>H: final report + unresolved disputes
```

### Handoff contract

| Sender | Must provide | Receiver must not need |
| --- | --- | --- |
| Requirements → Spec reviewer | Spec, plan, constitution, discovery note | Chat history |
| Spec reviewer → Author | Findings with severity, evidence, requirement | Verbal discussion |
| Author → Implementation | Approved spec, tasks, ADRs, non-goals | Design intent in someone's head |
| Implementation → Code reviewer | Diff range, verification report, ledger, spec | Author's explanation |
| Code reviewer → Author | Findings with file:line, evidence, remediation | Reviewer's reasoning chain |
| Author → Human | Completion report, deviations, unverified items | Hope |

---

## 6. Resolving disagreements

```mermaid
stateDiagram-v2
    [*] --> FindingRaised
    FindingRaised --> Accepted: author agrees
    FindingRaised --> Disputed: author provides evidence
    Disputed --> Accepted: evidence contradicts finding
    Disputed --> Escalated: evidence insufficient
    Escalated --> HumanDecision
    HumanDecision --> Accepted
    HumanDecision --> Rejected
    Rejected --> [*]
    Accepted --> Fixed
    Fixed --> ReReview
    ReReview --> [*]
```

| Rule | Reason |
| --- | --- |
| Disputes are resolved with **evidence**, not insistence | Prevents "I'm right" loops |
| The implementer **cannot close its own finding** | Independence |
| Escalation is a human decision with a recorded rationale | Audit trail |
| A rejected finding stays in the report with the reason | Learning, audit |
| Re-review covers only changed items unless the change is large | Efficiency |

### Dispute template

```markdown
## Dispute — C-01 (IDOR on export)

**Reviewer claim:** `visible_to()` filters by project only; record ACL ignored.
**Author response:** `OrderQuery.visible_to_user` already joins `RecordAcl` at `repo.py:118`.
**Evidence provided:** `repo.py:112-140`; test `test_acl_matrix::test_viewer_without_acl`.
**Reviewer resolution:** ACCEPTED — finding withdrawn. Confidence was 6/10 (based on
`service.py` without reading the query builder).
**Process note:** reviewer should have followed the call chain into the repository.
```

> A withdrawn finding is a **success** of the evidence process, not an embarrassment.

---

## 7. Prioritizing findings

```mermaid
flowchart TD
    F["Findings"] --> S["Sort by severity"]
    S --> C["Within severity: confidence"]
    C --> B["Within confidence: blast radius"]
    B --> O["Order of fix"]
    O --> G{"Any CRITICAL/HIGH<br/>unresolved?"}
    G -->|yes| BLOCK["Block merge"]
    G -->|no| OK["Proceed with recorded acceptances"]
```

| Priority | Severity | Confidence | Action |
| --- | --- | --- | --- |
| 1 | CRITICAL | ≥ 7 | Fix before anything else |
| 2 | HIGH | ≥ 7 | Fix before merge |
| 3 | CRITICAL/HIGH | < 7 | Verify first, then fix or dismiss with evidence |
| 4 | MEDIUM | any | Fix or record acceptance with owner |
| 5 | LOW/INFO | any | Follow-up ticket |

---

## 8. Human approval gates

```mermaid
flowchart LR
    G1["Spec approved"] --> G2["Architecture accepted"]
    G2 --> G3["Implementation complete"]
    G3 --> G4["Review clean"]
    G4 --> G5["Verification complete"]
    G5 --> G6["Merge approved"]
    G6 --> G7["Release approved"]
    G7 --> G8["Deploy approved"]
```

| Gate | Human must see | Cannot be delegated to |
| --- | --- | --- |
| Spec approval | Problem, goals, non-goals, criteria | Implementation agent |
| Architecture | Trade-offs, rollback, failure modes | Same agent that designed it |
| Merge | Review report, verification, deviations | Implementer |
| Release | Changelog, risk, rollback plan | CI alone |
| Deploy | Environment, blast radius, window | The agent that wrote the code |

> **Never** let the implementation agent mark its own review findings as approved, even if it
> "ran the same checks". Independence is the control.

---

## 9. Parallel execution

```mermaid
flowchart TD
    T["tasks.md"] --> G["Build dependency graph"]
    G --> W1["Wave 1 (independent)"]
    W1 --> W2["Wave 2"]
    W2 --> W3["Wave 3"]
    W1 --> WT1["worktree A"]
    W1 --> WT2["worktree B"]
    W2 --> WT3["worktree C"]
```

| Rule | Reason |
| --- | --- |
| Parallel tasks must not touch the same files | Merge conflicts and lost work |
| Each parallel task gets its own worktree | Isolation |
| Foundational tasks are serialized | Everything depends on them |
| A coordinator owns the merge order | Prevents races |
| Integration test after each wave | Detects cross-task breakage early |

> Kiro calls these dependency **waves**; Spec Kitty uses **work packages** with worktrees; Spec Kit
> marks parallel tasks in `tasks.md`. The concept is the same: independence must be **declared**,
> not assumed.

---

## 10. Anti-patterns

| Anti-pattern | Problem | Fix |
| --- | --- | --- |
| Agent swarm on one file | Conflicting edits | One owner per file |
| Reviewer with write access | Silent fixes | Read-only + report |
| Handoff via chat summary | Loses nuance, invites invention | Artifact-only handoff |
| Same model instance for author and reviewer | Rationalization | Separate context |
| Nine roles for a one-line fix | Overhead | Default two-role split |
| Voting between agents | No ground truth | Evidence + human decision |
| Agent approving its own findings | No independence | Structural separation |

---

## 11. Cost control

| Lever | Effect |
| --- | --- |
| Two-role default | Captures most value |
| Artifact handoff (no transcripts) | Fewer tokens |
| Re-review only changed items | Less duplication |
| Specialist roles only when triggered (security for sensitive diffs) | Avoid idle agents |
| Cap parallel waves by file ownership | Avoid merge churn |
| Cache verification evidence in the ledger | Avoid re-running everything |

---

## 12. Verification

| Check | How | Expected |
| --- | --- | --- |
| Reviewer independence | Different session/agent, no shared transcript | Confirmed |
| Read-only enforced | Tool config or FS mount | Confirmed |
| Handoff completeness | Receiver can act from artifacts alone | Yes |
| No self-approval | Finding closure requires reviewer/human | Yes |
| Parallel safety | File ownership disjoint | Yes |
| Audit trail | Spec, review, verification, approval recorded | Present |

---

## 13. References

- [Chapter 02 — Engineering lifecycle](./02-engineering-lifecycle.md)
- [Chapter 17 — Review without implementation](./17-specification-review.md)
- [Chapter 22 — Git and commit policy](./22-git-and-commit-policy.md)
- [templates/agent-role-definition.md](./templates/agent-role-definition.md)
- [prompts/](./prompts/)
- Spec Kitty multi-agent architecture — <https://github.com/spec-kitty/spec-kitty/blob/main/docs/architecture/multi-agent-orchestration.md>
- BMAD multi-agent discussions — <https://docs.bmad-method.org/customize/run-multi-agent-discussions/>
- Superpowers subagent-driven development — <https://github.com/obra/superpowers>

---

**Previous:** [23 — Hallucination prevention](./23-hallucination-prevention.md) ·
**Next:** [25 — CI/CD integration](./25-ci-cd-integration.md)
