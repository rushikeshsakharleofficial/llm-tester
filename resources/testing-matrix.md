# Testing Matrix

Use this matrix to choose verification for generated or edited work.

| Change type | Minimum verification | Stronger verification |
| --- | --- | --- |
| Frontend UI | lint/typecheck/build when configured | unit/component/e2e tests, accessibility smoke test |
| Backend/API | unit tests, lint/typecheck/build | integration tests, API smoke tests, auth/error-path tests |
| CLI/script | syntax check, help/dry-run | representative input/output tests, lint, failure-path tests |
| Library code | unit tests, typecheck/build | coverage for public API and edge cases |
| DB schema/migration | syntax or migration dry-run | local migration up/down, fixtures, constraint/index review |
| DB tuning | baseline plan, proposed plan, rollback note | safe EXPLAIN ANALYZE, load-sensitive validation |
| OS tuning | config syntax validation, rollback steps | test on staging, current-value capture, service health check |
| Infrastructure/IaC | validate/fmt/lint/dry-run | plan review, check mode, policy/security scan |
| CI/CD | YAML syntax, local action/lint where possible | dry-run workflow, validate secrets assumptions |
| Config/env | parser validation, sample config check | app start with sample config |
| Schemas | JSON/YAML/TOML parse, schema validator | valid/invalid sample tests, compatibility checks |
| Docs examples | syntax/path validation | execute examples in a safe sandbox |

## Rule of thumb

If the work can break runtime behavior, it needs at least one executable check. If an executable check is unsafe or impossible, provide precise manual verification steps and remaining risk.
