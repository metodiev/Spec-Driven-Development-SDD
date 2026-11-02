---
name: review-prompts
description: Copy-paste prompt blocks for the ten review types. Use when you need a focused review of requirements, specs, architecture, database design, APIs, security, performance, code, tests, or documentation.
---

# Review Prompt Pack

Ten focused prompts sharing one contract. Pick the block you need and paste it with the artifact.

## Shared contract (prepend to every block)

```text
Read-only review. You may read files, search the repository, and run read-only checks.
You must not edit files, run formatters with --fix, commit, push, or change issue state.
For every finding report: severity (CRITICAL/HIGH/MEDIUM/LOW/INFO), confidence 1-10 with basis,
location, requirement, evidence, impact, remediation, verification.
Never invent APIs, versions, or test results. Mark unverifiable claims UNVERIFIED.
State the read-only enforcement level and what you did not verify.
```

---

## 1. Requirements review

```text
Review the intake/request below as a requirements reviewer.

Check: is the problem stated without a solution bias; are affected users and the cost of
inaction identified; is success measurable; is scope bounded by non-goals; are constraints
(compliance, deadline, budget) explicit; is any requester-proposed solution recorded as a
requirement.

Output: findings, then a rewritten problem statement if the original is solution-biased.
```

## 2. Specification review

```text
Use prompts/specification-reviewer.md.

For each requirement, apply the two-implementation test: describe two implementations that both
satisfy the literal text. If they behave differently, report ambiguity with both readings.

Check completeness (edge cases, failures, security, performance, compatibility, rollback,
observability) and testability (can you write an assertion without asking the author?).
```

## 3. Architecture review

```text
Use prompts/architecture-reviewer.md.

Produce: NFR trace table (NFR -> design answer -> evidence), data ownership table, failure-mode
table (slow/down/garbage/duplicate for each dependency), five quality-attribute scenarios, and
trade-off analysis for the chosen option.
```

## 4. Database design review

```text
Review the schema change and migrations as a database reviewer.

Check: normalization justified; keys/constraints named; index strategy matches query patterns;
lock behavior on production-sized tables; DDL separated from data backfill; backfill batched,
idempotent, resumable; down() real and tested; expand/contract for renames and drops;
old and new application versions can run simultaneously; retention and PII handling.

Evidence required: EXPLAIN output, table size estimates, migration timing.
Report irreversible operations explicitly.
```

## 5. API review

```text
Review the API contract as an API reviewer.

Check: resource naming and verbs; status codes (no 200-with-error); consistent error model;
pagination and hard caps; idempotency for retryable writes; versioning and deprecation;
authorization documented per operation; rate limits; timeouts and retry semantics.

For every change classify it as additive, behavior-changing, or breaking, and state the
consumer impact. Quote the contract file with line references.
```

## 6. Security review

```text
Use prompts/security-reviewer.md.

Start with a data-flow diagram and trust boundaries. Apply STRIDE per boundary. Verify
authentication, object-level authorization, input validation, output encoding, secret handling,
logging hygiene, and abuse resistance. Run the project's scanners and record exact commands and
results. A scanner result is not a risk decision: state exploitability in this context.
```

## 7. Performance review

```text
Review the performance design and evidence as a performance reviewer.

Check: the NFR has a number, a condition, and a measurement method; dataset size and workload
model stated; hot path identified with a profile or trace; complexity and query counts bounded;
pool sizes, timeouts, and memory ceilings defined; baseline recorded.

If no measurement exists, mark the NFR UNVERIFIED and say what is needed. Do not accept
"it will scale". Require p95/p99, not averages.
```

## 8. Code review

```text
Use prompts/read-only-code-reviewer.md.

Read the diff, then the surrounding code and every caller of changed symbols. Verify the tests
would fail if the code were wrong. Look for regressions outside the diff (renamed fields,
changed defaults, changed error types, changed ordering).
```

## 9. Test review

```text
Review the tests as a test reviewer.

For each test: what behavior does it assert; would it fail if the behavior were wrong; would it
survive a refactor; does it cover a boundary or only the happy path; is it deterministic;
does it name the acceptance criterion.

Flag tests that assert only mocks, tests that cannot fail, sleeps used for synchronization,
order dependence, and assertions removed or weakened in the diff.
Suggest the smallest test that would have caught the defect.
```

## 10. Documentation review

```text
Review the documentation as a documentation reviewer.

Check: statements match the implementation (cite code); commands are executable and current;
version-sensitive claims have a version and date; relative links resolve; anchors exist;
examples are labeled illustrative vs verified; no contradictions with other docs; no duplicated
rules with divergent wording; no secrets or real customer data.

Report each mismatch with the doc location and the code location that contradicts it.
```

---

## Output

Use the matching report template:

| Review | Template |
| --- | --- |
| Requirements / specification | [`specification-review-report.md`](../templates/specification-review-report.md) |
| Architecture | [`specification-review-report.md`](../templates/specification-review-report.md) plus ADR update |
| Code / security | [`code-review-report.md`](../templates/code-review-report.md) |
| Database / API / performance / test / docs | [`code-review-report.md`](../templates/code-review-report.md) with severity + evidence |
