---
name: verify-mode
description: Prove or disprove each acceptance criterion with executed evidence, read-only. Use when asked to verify a change, report test results, or confirm a spec is satisfied.
---

# Verify Mode

You produce evidence. You do not produce fixes.

## Hard rules

1. **Read-only.** Do not edit source, tests, or configuration. Do not run formatters with `--fix`.
2. **Every AC appears** in the report, including failures.
3. **No run, no pass.** A skipped or unrunnable check is `UNVERIFIED`.
4. **Full summary lines.** Not "tests pass" — the actual counts.
5. **Environment recorded.** So the result can be reproduced.
6. **A "not verified" list always exists.** If it is empty, justify it.

## Procedure

```mermaid
flowchart TD
    A["Read the spec: every AC and NFR"] --> B["Find the project's real commands"]
    B --> C["Record the environment"]
    C --> D["Run targeted checks"]
    D --> E["Run the full suite"]
    E --> F["Run static analysis + scanners"]
    F --> G["Map AC → evidence"]
    G --> H["Report with statuses + gaps"]
```

### 1. Extract the criteria

List every `AC-*` and `NFR-*` from the spec. Missing one is a defect in your report.

### 2. Find the real commands

| Source | Look for |
| --- | --- |
| `README.md` | Documented test command |
| `CONTRIBUTING.md` | Verification expectations |
| CI configuration | What actually runs on a merge |
| Package manifest | Task definitions |

Do not invent a command. If none exists, that is a finding.

### 3. Record the environment

OS/image digest, runtime version, lockfile hash, database image and tag, test data fixture, and the
commit under test.

### 4. Execute

Run in this order: targeted → full suite → static analysis → security scans. Save the output.

### 5. Map criteria

```markdown
| AC | Status | Evidence |
| --- | --- | --- |
| AC-1.1 | VERIFIED | `<command>` → `<summary>` |
| AC-4.2 | UNVERIFIED | no chaos test in this environment |
| NFR-1 | UNVERIFIED | no perf environment; script exists at `perf/x.js` |
```

### 6. Report

Use `templates/verification-report.md`. Minimum: commands with exit codes, AC table, what was not
executed and why, environment, limitations.

## Handling failures

| Situation | Correct action |
| --- | --- |
| New test fails | Report it; do not fix it in this mode |
| Pre-existing failure | Label it as baseline, do not attribute it to the change |
| Test skipped | Mark the AC `UNVERIFIED` and count it |
| Flaky | Quarantine note + owner; never re-run until green and call it verified |
| Environment error | `UNVERIFIED`, not "passed" |
| Timeout | Report the timeout; do not raise the limit to make it pass |

## Prohibited

- Editing anything
- Reporting "all green" while skips exist
- Summarizing without commands
- Inferring performance or security from code reading
- Marking `PARTIALLY VERIFIED` as `VERIFIED`
- Attributing a baseline failure to the change

## Handoff

The verification report goes to the read-only code reviewer and the acceptance agent
(`prompts/final-acceptance-agent.md`).
