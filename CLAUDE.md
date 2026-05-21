# CLAUDE.md

This file provides guidance to Claude Code and Codex when working with code in this repository.

## What this repo is

A Codex/Claude Code skill that enforces mandatory testing and verification for every artifact the agent generates or modifies. It ships as a skill (`SKILL.md`) plus supporting resources, metadata, validation checks, and helper scripts.

## Skill invocation

Users install this skill then invoke it in any project:

```text
/llm-tester For every change you make, run the appropriate tests before finalizing.
```

Codex users can invoke:

```text
$llm-tester For every change you make, run the appropriate tests before finalizing.
```

The `$ARGUMENTS` placeholder in `SKILL.md` receives whatever the user passes after `/llm-tester`.

## File roles

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill — defines the full workflow Claude must follow |
| `resources/testing-matrix.md` | Category-to-verification mapping (referenced from SKILL.md) |
| `resources/verification-report-template.md` | Final-response template |
| `resources/safety-checklist.md` | Destructive-operation guardrails |
| `scripts/detect_test_commands.py` | Dependency-free Python helper that inspects a repo and emits likely safe test commands as JSON |
| `scripts/validate_skill.py` | Dependency-free validator for skill frontmatter and metadata |
| `agents/openai.yaml` | OpenAI-compatible agent interface definition |
| `tests/` | Unit tests for helper scripts |
| `Makefile` | Local check, test, detect, and validate targets |

## Verifying changes to this repo

Use the repository Makefile:

```bash
make validate        # full suite: compile + validate + test + detect
make test            # unit tests only
make check           # compile + validate only
make detect          # run detect_test_commands.py against this repo
```

Run a single test file:

```bash
python3 -m unittest tests.test_detect_test_commands
python3 -m unittest tests.test_validate_skill
```

`make validate` runs Python syntax compilation, skill metadata validation, unit tests, and command detection.

## Skill structure contract

`SKILL.md` must:
- Have a valid YAML frontmatter block with `name` and `description`.
- Contain the `$ARGUMENTS` placeholder (receives user-supplied task text).
- Reference resources by their exact relative paths (`resources/`, `scripts/`).
- Keep `agents/openai.yaml` present for Codex UI metadata.

Skill name rules (enforced by `validate_skill.py`):
- Lowercase letters, digits, and hyphens only (`[a-z0-9][a-z0-9-]*[a-z0-9]`).
- No consecutive hyphens (`--` is invalid).
- Maximum 64 characters.

When editing `SKILL.md`, run `make check` to validate frontmatter and confirm all referenced resource paths still exist.

## detect_test_commands.py design rules

- Zero external dependencies — only stdlib.
- Outputs `{"root": "...", "commands": [...]}` JSON to stdout.
- Never runs discovered commands itself; only prints them.
- Each detected command entry has `command`, `reason`, and `source` keys.
- Detection functions (`detect_js`, `detect_python`, `detect_go`, `detect_rust`, `detect_shell`, `detect_iac`, `detect_make`, `detect_skill`) are isolated — add new language support as a new function called from `main()`.
- `detect_skill` fires when `SKILL.md` and `scripts/validate_skill.py` both exist — emits `python3 scripts/validate_skill.py .`.
- Deduplication is enforced by `add()`: same command string never added twice.

## validate_skill.py design rules

- Zero external dependencies — only stdlib.
- Exits `0` on success, `1` on any error; prints `ERROR: <message>` to stderr per failure.
- Validates: frontmatter parses, `name` present and format-valid, `description` present, `agents/openai.yaml` exists.
- Takes an optional `root` positional argument (defaults to `.`).

## tests/ coverage

| Test file | Covers |
|-----------|--------|
| `test_detect_test_commands.py` | JS/npm detection, Python detection, pytest vs unittest selection, Makefile target detection, skill validation detection |
| `test_validate_skill.py` | Valid skill passes, missing `agents/openai.yaml` fails, invalid name format fails |

Tests use `tempfile.TemporaryDirectory` — no fixtures committed, no network calls.
