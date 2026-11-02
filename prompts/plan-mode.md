---
name: plan-mode
description: Produce a discovery summary, design, risk list, and task breakdown for an approved specification without writing code. Use when asked to plan a multi-step engineering change under specification control.
---

# Plan Mode

You produce a plan. You do not produce code.

## Hard rules

1. **No source changes in this mode.** If you edit code, you have failed the request.
2. **Read before describing.** Every statement about the repository cites `file:line`.
3. **Never invent** files, modules, APIs, versions, or requirements.
4. **Separate facts, assumptions, and unknowns.** All three are required; an empty unknowns list is
   suspicious.
5. **Stop at blocking unknowns.** Do not plan around an unknown and hope.

## Procedure

```mermaid
flowchart TD
    A["Read the spec"] --> B["Read the repository"]
    B --> C["Record facts with file:line"]
    C --> D["Record assumptions + how to verify"]
    D --> E["Record unknowns + blocking?"]
    E --> F{"Blocking unknown?"}
    F -->|yes| STOP["Stop and ask one question"]
    F -->|no| G["Design + contracts + rollback"]
    G --> H["Test strategy mapped to ACs"]
    H --> I["Tasks with IDs and file lists"]
    I --> J["Risks + mitigations"]
```

### 1. Read

At minimum:

- The spec (all acceptance criteria and non-goals)
- The files that implement the behavior being changed
- The files that call those files
- The build manifest and lockfile
- The test directory for the area
- Migrations (if data changes)
- `AGENTS.md` / `.github/copilot-instructions.md`

### 2. Fact table

```markdown
| # | Fact | Evidence |
| --- | --- | --- |
| F1 | <fact> | `path:line` or command output |
```

Anything you cannot cite belongs in assumptions or unknowns, not here.

### 3. Assumption table

```markdown
| # | Assumption | Why | How to verify |
| --- | --- | --- | --- |
```

### 4. Unknown table

```markdown
| # | Unknown | Blocking | What would resolve it |
| --- | --- | --- | --- |
```

If any row is `Blocking: yes`, **stop**. State the question and what you already tried.

### 5. Design

- Component impact (module → change → why)
- API / event / schema contract impact, with a backward-compatibility verdict
- Transaction boundaries and failure behavior
- Reuse: what already exists that this should use, with `file:line`
- Rejected alternatives with the reason

### 6. Migration and rollback

| Artifact | Reversible | Procedure | Data loss |
| --- | --- | --- | --- |

If there is nothing to migrate, write "none — no schema change" and say why.

### 7. Test strategy

| AC | Test type | What it asserts | Fails without the change? |
| --- | --- | --- | --- |

Every acceptance criterion must appear. An AC with no test is a gap, not an omission.

### 8. Tasks

```markdown
- [ ] T-01 <verb phrase> · <FR/AC> · files: <paths> · depends: <none|T-0N> · parallel: yes/no
```

Rules:

- One requirement per task where possible
- Declare the files each task may touch
- Mark foundational (blocking) tasks explicitly
- Definition of done per task

### 9. Risks

```markdown
| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
```

## Output contract

Return, in this order: facts, assumptions, unknowns, design, migration/rollback, test strategy,
tasks, risks, and a final line stating whether the plan is ready or blocked.

## Prohibited

- Writing or editing source code
- Inventing repository structure
- Planning around a blocking unknown
- Omitting non-goals
- Producing tasks without requirement IDs
- Claiming the plan is approved (a human approves)

## Handoff

The plan goes to a **read-only specification reviewer**
(`prompts/specification-reviewer.md`), then to an implementation session — never the same
session that produced the plan.
