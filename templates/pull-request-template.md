## What & why

`<One paragraph tied to the spec or issue. State the problem and the chosen solution.>`

Refs: `<issue/spec link>`

## Specification

| Field | Value |
| --- | --- |
| Spec | `<specs/<id>/spec.md>` |
| Plan | `<specs/<id>/plan.md>` |
| ADRs | `<ADR-n>` |
| Requirements | `<FR-1, FR-2, NFR-1>` |

## Acceptance criteria

| AC | Status | Evidence |
| --- | --- | --- |
| AC-1.1 | VERIFIED | `<command>` → `<summary>` |
| AC-1.2 | VERIFIED | `<test>` → `<summary>` |
| AC-2.1 | UNVERIFIED | `<reason + owner + target date>` |

## Verification performed

| Check | Command | Result |
| --- | --- | --- |
| Tests | `<command>` | `<summary>` |
| Static analysis | `<command>` | clean |
| Security scan | `<command>` | `<summary>` |
| Migration | `<command>` | up/down verified |

## Risk & rollback

| Item | Detail |
| --- | --- |
| Risk | `<what could go wrong>` |
| Blast radius | `<services, users, data>` |
| Rollback | `<flag / revert / restore>` |
| Time to roll back | `<minutes>` |

## Deviations

| ID | Deviation from plan | Approved by |
| --- | --- | --- |
| `<D-1>` | `<description>` | `<name>` |

## Reviewer notes

- `<where to start reading>`
- `<what can be ignored (lockfile, generated)>`
- `<open questions>`

## Checklist

- [ ] One logical change
- [ ] Spec linked and requirements referenced
- [ ] Tests executed and results pasted
- [ ] No secrets or credentials
- [ ] No unrelated changes
- [ ] Migration reversible or forward-fix documented
- [ ] Documentation updated
- [ ] No `UNVERIFIED` presented as complete

---

*Template version: 1.0 · See [chapter 22](../docs/22-git-and-commit-policy.md).*
