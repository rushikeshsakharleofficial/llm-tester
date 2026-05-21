#!/usr/bin/env python3
"""Validate the minimum structure required for this Codex skill."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

MAX_NAME_LENGTH = 64


def read_frontmatter(skill_md: pathlib.Path) -> tuple[dict[str, str], str | None]:
    if not skill_md.exists():
        return {}, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return {}, "SKILL.md must start with YAML frontmatter"

    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(match.group(1).splitlines(), start=2):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            return {}, f"Invalid frontmatter line {line_number}: {raw_line}"
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            return {}, f"Invalid empty frontmatter key on line {line_number}"
        values[key] = value

    return values, None


def validate_skill(root: pathlib.Path) -> list[str]:
    errors: list[str] = []
    frontmatter, error = read_frontmatter(root / "SKILL.md")
    if error:
        return [error]

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()

    if not name:
        errors.append("SKILL.md frontmatter is missing name")
    elif not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", name):
        errors.append("Skill name must use lowercase letters, digits, and hyphens")
    elif "--" in name:
        errors.append("Skill name must not contain consecutive hyphens")
    elif len(name) > MAX_NAME_LENGTH:
        errors.append(f"Skill name must be {MAX_NAME_LENGTH} characters or fewer")

    if not description:
        errors.append("SKILL.md frontmatter is missing description")

    agents_metadata = root / "agents" / "openai.yaml"
    if not agents_metadata.exists():
        errors.append("agents/openai.yaml is missing")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate this skill repository")
    parser.add_argument("root", nargs="?", default=".", help="Skill repository root")
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    errors = validate_skill(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
