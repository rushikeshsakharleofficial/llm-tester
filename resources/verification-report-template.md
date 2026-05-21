# Verification Report Template

Use this at the end of a task that generated or changed files.

```text
Implemented:
- <short summary of changes>

Change category:
- <frontend/backend/script/schema/database tuning/OS tuning/etc.>

Testing/verification performed:
- Command/check: <command or manual check>
  Result: <passed/failed/skipped>
  Notes: <important output, failure, or limitation>

Tests added or updated:
- <file/path or none>

Remaining risk:
- <none, or exact unverified behavior>

User-run checks, if needed:
- <exact command/manual step>
```

## Reporting rules

- Do not hide failures.
- Do not say tests passed unless they actually ran and passed.
- If tests were skipped, explain why.
- If a command is destructive or unsafe, provide a dry-run or manual review path instead.
- Keep output short but include enough detail for the user to trust the result.
