---
name: implement-mode
description: Implement exactly one approved task with tests and executed evidence. Use after a plan is approved, within a declared Git mode.
---

# Implement Mode

You implement **one task**. The plan is approved; you do not redesign it.

## Hard rules

1. **One task per turn.** Stop when the task's definition of done is met.
2. **Only declared files may change.** Anything else is out of scope — report, do not edit.
3. **Test first where possible.** The test must fail before the change.
4. **Evidence or silence.** Paste commands and summary lines.
5. **No silent deviation.** If the plan is wrong, stop and record it.
6. **Never weaken a test** to make it pass.
7. **Obey the declared Git mode.** Mode 2 means no commits.

## Procedure

```mermaid
flowchart TD
    A["Read the task + spec"] --> B["Read the files and their callers"]
    B --> C["Write/adjust the test"]
    C --> D["Run it: must fail for the right reason"]
    D --> E["Minimal implementation"]
    E --> F["Compile / type check"]
    F --> G["Run the targeted test"]
    G --> H{"Green?"}
    H -->|no| E
    H -->|yes| I["Run the full suite + static analysis"]
    I --> J["Report: diff, commands, deviations"]
```

### 1. Read

- The task entry (requirement ID, files, definition of done)
- The spec sections it cites
- The declared files, **in full**
- Every caller of the symbols you will change
- The existing tests in that area, to match their style

### 2. Test first

Name the test after the acceptance criterion where one exists.

```text
Test:  OrderExportIT.excludesUnreadableOrders   (AC-2.1)
Base:  fails with "expected <0> but was <1>"
```

If the test cannot be written first (UI, timing, data), write a scripted reproduction and record
the commands and observed output.

### 3. Implement

- Smallest change that satisfies the acceptance criterion
- Reuse the existing pattern; cite it
- No refactoring, renaming, or reformatting of untouched code
- No new dependency without approval

### 4. Verify locally

```bash
# Use the repository's real commands
<targeted test command>
<full suite command>
<static analysis command>
```

Paste the command and the summary line. Not a paraphrase.

### 5. Report

```markdown
## T-04 — <title>

### Test first
<test name> — fails on base with: <failure excerpt>

### Change
<files>:<lines> — <what changed and why>

### Verification
    <command>  → <summary line>
    <command>  → <summary line>

### Deviation
None. | <trigger + evidence + proposed correction + approval needed>

### Not done
<what remains, by task id>
```

## When the plan is wrong

Stop. Do not adapt silently.

```markdown
## Deviation D-<n>

- **Trigger:** <what you found>
- **Evidence:** <file:line or command output>
- **Why the plan cannot be followed:** <one paragraph>
- **Smallest correction:** <proposal>
- **Reversible:** yes/no
- **Needs approval from:** <role>
```

## Blocked

Two distinct attempts, then report:

```markdown
## Blocked

**Tried:** 1. … 2. …
**Observed:** …
**Unknown:** …
**Needed:** …
```

## Prohibited

- Editing files outside the declared list
- Changing assertions to make a test pass
- Adding `sleep`, retries, or `--no-verify` to bypass a failure
- `git reset --hard`, `git clean`, force-push, `stash drop`
- Claiming a run that did not happen
- Fixing unrelated pre-existing defects (report them instead)
- Marking your own work as reviewed or approved
