# LLM Tester

A Claude Code and Codex skill that makes testing and verification mandatory for anything the agent generates or changes: frontend, backend, scripts, schemas, database tuning, OS tuning, infrastructure, CI/CD, configuration, and documentation examples.

**Repository:** https://github.com/rushikeshsakharleofficial/llm-tester

## What it enforces

LLM Tester prevents generated work from being treated as finished without proof. It instructs the agent to classify each change, discover project-native test commands, run the strongest safe verification available, and report exactly what passed, failed, or could not be run.

| Change type | Minimum verification |
|-------------|---------------------|
| Frontend | lint, typecheck, build; unit/component/e2e when available |
| Backend/API | unit tests, lint/typecheck/build; integration and smoke tests |
| Scripts/CLI | syntax check, dry run, representative input/failure tests |
| Schemas/migrations | syntax validation, dry run, rollback review |
| Database tuning | baseline/changed plan review, duplicate-index check |
| OS tuning | config syntax validation, current-value check, rollback steps |
| Infrastructure | Terraform/Ansible/Docker/Kubernetes validate and dry-run flows |
| Docs examples | syntax and path validation for runnable snippets |

## Requirements

- Python 3.7 or later (for helper scripts and tests — no third-party packages required)
- Git (for installation)
- Claude Code or Codex (to invoke the skill)

## Installation

### Personal skill — Claude Code

```bash
git clone https://github.com/rushikeshsakharleofficial/llm-tester.git
mkdir -p ~/.claude/skills
cp -R llm-tester ~/.claude/skills/
```

### Personal skill — Codex

```bash
git clone https://github.com/rushikeshsakharleofficial/llm-tester.git
mkdir -p ~/.codex/skills
cp -R llm-tester ~/.codex/skills/
```

### Project skill — Claude Code

Run from your repository root:

```bash
git clone https://github.com/rushikeshsakharleofficial/llm-tester.git /tmp/llm-tester
mkdir -p .claude/skills
cp -R /tmp/llm-tester .claude/skills/llm-tester
```

Commit `.claude/skills/llm-tester/` to share the skill across your team.

## Quick start

After installing, invoke the skill inside any project:

```text
/llm-tester For every change you make, add or run the appropriate tests before the final answer.
```

Codex users:

```text
$llm-tester For every change you make, add or run the appropriate tests before the final answer.
```

## Usage examples

```text
/llm-tester Review the last generated backend changes and run the safest verification checks available.
```

```text
/llm-tester Validate this OS tuning proposal without applying unsafe changes.
```

```text
/llm-tester Check this database migration with dry-run or local validation only.
```

Text after `/llm-tester` becomes the task description passed to the skill. Omit it to apply the testing policy to the current task and repository state.

## Report format

Every task ends with a structured verification report:

```text
Implemented: <summary>

Change category:
- <frontend / backend / script / schema / database tuning / etc.>

Testing/verification performed:
- Command/check: <command or manual check>
  Result: <passed / failed / skipped>
  Notes: <important output, failure, or limitation>

Tests added or updated:
- <file/path or none>

Remaining risk:
- <none, or exact unverified behavior>

User-run checks, if needed:
- <exact command / manual step>
```

## Safety

The skill requires verification but does not permit reckless execution. The following require explicit user confirmation and a confirmed safe target before the agent proceeds:

- Production deploys
- Database migrations against shared or live databases
- OS/kernel/network/firewall tuning
- Service restarts
- Package installation or removal
- Cloud resource changes

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill — defines the full workflow the agent must follow |
| `agents/openai.yaml` | UI metadata for Codex skill lists and default prompt |
| `resources/testing-matrix.md` | Category-to-verification mapping |
| `resources/verification-report-template.md` | Final-response template |
| `resources/safety-checklist.md` | Destructive-operation guardrails |
| `scripts/detect_test_commands.py` | Dependency-free helper that infers likely verification commands from repo files |
| `scripts/validate_skill.py` | Dependency-free validator for skill frontmatter and metadata |
| `tests/` | Unit tests for the helper scripts |
| `Makefile` | Local `test`, `check`, `detect`, and `validate` targets |
| `CLAUDE.md` | Repository guidance for agent sessions working on this repo |

## Testing

Validate this repository with:

```bash
make validate
```

This runs Python syntax compilation, skill metadata validation, unit tests, and command detection. Run steps individually:

```bash
make check     # compile + metadata validation
make test      # unit tests only
make detect    # run detect_test_commands.py against this repo
```

Run a single test module:

```bash
python3 -m unittest tests.test_detect_test_commands
python3 -m unittest tests.test_validate_skill
```

## Contributing

To add support for a new language or ecosystem in `scripts/detect_test_commands.py`:

1. Add a new `detect_<language>(root, commands)` function following the pattern of existing detectors.
2. Call it from `main()`.
3. Add corresponding test cases in `tests/test_detect_test_commands.py` using `tempfile.TemporaryDirectory`.
4. Run `make validate` to confirm all checks pass.

Skill name constraints (enforced by `validate_skill.py`): lowercase letters, digits, and hyphens only; no consecutive hyphens; maximum 64 characters.

## License

No license file was found in this repository. See `Maintainer TODOs` below.

## Maintainer TODOs

- **License**: Add a `LICENSE` file and update the License section above with the correct license name and a link to the file.
