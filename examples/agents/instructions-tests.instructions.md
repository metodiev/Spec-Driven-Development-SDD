---
applyTo: "tests/**/*"
---

# Test rules (example)

> **Example only.** Copy to `.github/instructions/tests.instructions.md` and adapt.
> Copilot attaches this file when the `applyTo` glob matches files being changed.

- One behavior per test; name it after the behavior and condition.
- Never call external networks. Use fixtures, fakes, or containers.
- No `sleep`/`Thread.sleep`/`time.sleep`; synchronize on a signal instead.
- Assert observable outcomes, not implementation details.
- A new test must fail before the change and pass after it.
- Do not weaken or delete an existing assertion without a documented reason.
- Test names should reference the acceptance criterion where one exists, e.g.
  `test_export_without_role_returns_403` for `AC-3.2`.
