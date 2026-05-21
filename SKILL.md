---
name: llm-tester
description: Require testing and verification for anything Claude Code creates or changes, including frontend, backend, scripts, schemas, database tuning, OS tuning, infrastructure, configuration, documentation examples, and generated assets. Use whenever work includes code generation, edits, automation, migration, tuning, or operational instructions.
---

# LLM Tester

Use this skill to make testing and verification mandatory for every generated or modified artifact.

The goal is simple: do not call work finished until it has a suitable test, validation, dry run, lint, type check, syntax check, smoke test, or clearly documented manual verification path.

## Requested task

$ARGUMENTS

If no explicit arguments are provided, apply this testing policy to the current Claude Code task and repository state.

## Core rule

For every generated or changed thing, Claude must produce and run the strongest safe verification available in the current environment.

If tests cannot be run, Claude must clearly state:

1. What should be tested.
2. Why it could not be tested here.
3. The exact command or manual steps the user should run.
4. What successful output should look like.
5. What risk remains unverified.

Never silently skip testing.

## Required workflow

### 1. Classify the change

Before finishing, classify the generated or edited work into one or more categories:

- Frontend UI
- Backend/API
- CLI or shell script
- Python/Node/Go/Rust/Java/etc. library code
- Database schema or migration
- Database tuning/query optimization
- OS tuning/sysctl/systemd/security configuration
- Infrastructure/IaC/Docker/Kubernetes/Ansible/Terraform
- CI/CD workflow
- Config/env changes
- Documentation with runnable commands or examples
- Generated data, fixtures, or schemas

### 2. Find existing test tools

Inspect project files for test and verification commands:

- `package.json`, lockfiles, `vite`, `next`, `jest`, `vitest`, `playwright`, `cypress`, `eslint`, `tsc`
- `pyproject.toml`, `pytest`, `tox`, `nox`, `ruff`, `mypy`, `unittest`
- `go.mod`, `go test`, `go vet`, `staticcheck`
- `Cargo.toml`, `cargo test`, `cargo check`, `cargo clippy`
- `pom.xml`, `build.gradle*`, Maven/Gradle test tasks
- `Makefile`, `justfile`, `Taskfile.yml`
- `.github/workflows`, `.gitlab-ci.yml`, CI commands
- Dockerfiles, Compose files, Helm charts, K8s manifests, Terraform/Ansible files
- Existing `tests/`, `spec/`, `__tests__/`, `e2e/`, `fixtures/`, `examples/`

Prefer project-native commands over generic guesses.

### 3. Add or update tests when appropriate

If the change introduces behavior, add or update tests near the existing test structure.

Do not create noisy or fake tests just to satisfy a checkbox. Tests must assert real behavior, catch regressions, or validate safety.

If the project has no test setup, create the smallest appropriate verification harness or document exact manual verification.

### 4. Run safe verification

Run the strongest safe checks available. Examples:

- Syntax check
- Lint
- Type check
- Unit tests
- Integration tests
- Build
- Migration dry run
- Query plan validation
- Config validation
- Container build or compose config check
- Terraform validate/plan without apply
- Ansible syntax check/check mode
- Kubernetes dry-run validation
- ShellCheck or `bash -n`
- Python `compileall`
- SQL parse/dry-run where supported
- Systemd `systemd-analyze verify`
- Nginx/Apache/Postfix config test where relevant

Never run destructive commands, production deploys, live migrations, OS tuning application, package removals, firewall changes, or service restarts unless the user explicitly requested and the target is confirmed safe.

### 5. Report verification results

End with a concise verification report:

```text
Testing/verification performed:
- Command: <command>
  Result: passed/failed/skipped
  Notes: <important output or reason>

Remaining risk:
- <unverified area or none>
```

If something failed, fix it and rerun the relevant checks when possible. If it cannot be fixed within scope, explain the failure clearly.

## Category-specific requirements

### Frontend

Minimum checks:

- Type check when TypeScript exists.
- Lint when configured.
- Unit/component tests when available.
- Production build or framework build check when practical.
- Manual smoke test steps for UI flows that cannot be browser-tested.

Preferred commands:

- `npm run test`, `npm run lint`, `npm run typecheck`, `npm run build`
- `pnpm test`, `pnpm lint`, `pnpm typecheck`, `pnpm build`
- `yarn test`, `yarn lint`, `yarn build`
- `npx playwright test` or `npm run e2e` when configured

Validate accessibility basics when UI is changed: labels, keyboard path, focus states, contrast-sensitive classes, empty/loading/error states.

### Backend/API

Minimum checks:

- Unit tests for changed logic.
- API handler/service tests where available.
- Schema/validation tests for request/response changes.
- Lint/type check/build.
- Manual curl/httpie smoke examples when integration tests are unavailable.

Verify auth, error handling, validation, pagination, idempotency, and security-sensitive branches when relevant.

### Scripts and CLIs

Minimum checks:

- Syntax check: `bash -n`, `python -m py_compile`, `node --check`, etc.
- Lint if available: ShellCheck, ruff, eslint, shfmt.
- Dry run or `--help` execution when safe.
- Test with representative input and failure input.

Do not execute scripts that modify the host, delete files, rotate logs, change firewall rules, install packages, or restart services without explicit permission and a safe target.

### Database schemas and migrations

Minimum checks:

- Syntax validation or migration dry run.
- Backward compatibility review.
- Rollback/down migration check if the framework supports it.
- Index/constraint impact review.
- Fixture or local database test when available.

Never run migrations against production unless explicitly requested and confirmed safe. Prefer generated SQL review and local/test database execution.

### Database tuning and query optimization

Minimum checks:

- Capture baseline query or plan when possible.
- Explain expected impact.
- Validate indexes do not duplicate existing indexes.
- Use `EXPLAIN`/`EXPLAIN ANALYZE` only in safe environments.
- For config tuning, document rollback and risk.

Do not apply global database tuning directly without user confirmation.

### OS tuning and system configuration

Minimum checks:

- Syntax/validation commands where available.
- Confirm target OS/version when possible.
- Show current value read commands before change commands.
- Provide rollback commands.
- Prefer dry-run or config test mode.

Examples:

- `sysctl -a | grep <key>` before proposing `sysctl -w`
- `nginx -t`, `apachectl configtest`, `postfix check`
- `systemd-analyze verify file.service`
- `sshd -t -f <config>`

Do not apply OS tuning, firewall, kernel, systemd, SSH, sudoers, or security policy changes directly unless explicitly authorized.

### Infrastructure/IaC

Minimum checks:

- Terraform: `terraform fmt -check`, `terraform validate`, `terraform plan` only with safe vars/backend.
- Ansible: `ansible-playbook --syntax-check`, check mode when safe.
- Docker: `docker compose config`, Dockerfile lint/build when practical.
- Kubernetes: `kubectl apply --dry-run=client/server`, `helm lint`, `helm template`.
- GitHub Actions: YAML syntax and action version sanity.

Never apply infrastructure changes automatically unless the user explicitly requested apply/deploy.

### Schemas and generated data

Minimum checks:

- Validate JSON/YAML/TOML syntax.
- Validate JSON Schema/OpenAPI/GraphQL/protobuf where tooling exists.
- Add sample valid and invalid examples when useful.
- Ensure backward compatibility for public schemas.

### Documentation examples

If documentation includes commands, code snippets, SQL, curl examples, YAML, JSON, or config, validate syntax and paths where practical. Mark untested examples clearly.

## Test command selection priority

Use this priority order:

1. Existing project test commands documented in README, Makefile, CI, package scripts, or contributing docs.
2. Framework-standard commands inferred from manifests.
3. Language syntax/build checks.
4. Minimal smoke test or dry run.
5. Manual verification instructions.

## Safety policy

Allowed by default:

- Read-only inspection.
- Syntax checks.
- Local unit tests.
- Local builds.
- Dry runs.
- Formatting checks.
- Static analysis.

Require explicit user confirmation before:

- Production deploys.
- Database migrations against shared/live DBs.
- OS/kernel/network/firewall tuning.
- Restarting services.
- Installing/removing packages globally.
- Deleting or overwriting user data.
- Running unknown scripts with side effects.
- Changing cloud resources.

## Completion gate

Before final response, confirm all applicable gates:

- The change category was identified.
- Existing tests/checks were discovered or absence was noted.
- New tests were added when behavior changed and a test location existed.
- Safe checks were run.
- Failures were fixed or reported.
- Unrun checks have exact commands and reasons.
- Remaining risk is stated.

If any gate is missing, do not claim the task is fully done.

## Built-in resources

Use these files when helpful:

- `resources/testing-matrix.md` — category-to-test mapping.
- `resources/verification-report-template.md` — final reporting template.
- `resources/safety-checklist.md` — destructive-operation guardrails.
- `scripts/detect_test_commands.py` — dependency-free helper to infer likely test commands.

## Final response format

Prefer this concise ending:

```text
Implemented: <summary>

Testing/verification performed:
- <command/check>: <result>

Remaining risk:
- <none or exact limitation>
```
