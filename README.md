# LLM Tester

A Claude Code skill that makes testing and verification mandatory for anything Claude generates or changes: frontend, backend, scripts, schemas, database tuning, OS tuning, infrastructure, CI/CD, configuration, and documentation examples.

## Marketplace URL

```text
https://github.com/rushikeshsakharleofficial/llm-tester
```

## Purpose

LLM Tester prevents generated work from being treated as finished without proof. It instructs Claude Code to classify the change, discover project-native test commands, run the strongest safe verification available, and report exactly what passed, failed, or could not be run.

## What it enforces

- Frontend: lint, typecheck, build, unit/component/e2e checks when available.
- Backend/API: unit/integration/API smoke checks, validation and error-path review.
- Scripts/CLI: syntax checks, dry runs, help output, representative input tests.
- Schemas/migrations: syntax validation, dry runs, rollback review, compatibility checks.
- Database tuning: baseline/changed plan review, duplicate-index checks, rollback notes.
- OS tuning: config syntax validation, current-value checks, rollback commands, safety gates.
- Infrastructure: Terraform/Ansible/Docker/Kubernetes validation and dry-run flows.
- Docs examples: syntax/path validation for runnable commands and snippets.

## Install as a personal Claude Code skill

```bash
git clone https://github.com/rushikeshsakharleofficial/llm-tester.git
mkdir -p ~/.claude/skills
cp -R llm-tester ~/.claude/skills/
```

Then run Claude Code in any project and invoke:

```text
/llm-tester Make sure this project is tested before finalizing changes
```

## Install as a project skill

From your repository root:

```bash
git clone https://github.com/rushikeshsakharleofficial/llm-tester.git /tmp/llm-tester
mkdir -p .claude/skills
cp -R /tmp/llm-tester .claude/skills/llm-tester
```

Commit `.claude/skills/llm-tester/` if you want the skill shared with the project.

## Example prompts

```text
/llm-tester For every change you make, add or run the appropriate tests before the final answer.
```

```text
/llm-tester Review the last generated backend changes and run the safest verification checks available.
```

```text
/llm-tester Validate this OS tuning proposal without applying unsafe changes.
```

```text
/llm-tester Check this database migration with dry-run or local validation only.
```

## Files

- `SKILL.md` — main Claude Code skill instructions.
- `resources/testing-matrix.md` — category-to-test mapping.
- `resources/verification-report-template.md` — final response template.
- `resources/safety-checklist.md` — destructive-operation guardrails.
- `scripts/detect_test_commands.py` — dependency-free helper to infer likely verification commands.

## Final-report format enforced by the skill

```text
Implemented: <summary>

Testing/verification performed:
- <command/check>: <result>

Remaining risk:
- <none or exact limitation>
```

## Safety note

The skill requires verification, but it does not permit reckless execution. Destructive operations, production deploys, live migrations, OS/kernel/network tuning, service restarts, package removals, or cloud-resource changes require explicit confirmation and a safe target.
