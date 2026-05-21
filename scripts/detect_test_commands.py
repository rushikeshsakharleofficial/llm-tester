#!/usr/bin/env python3
"""Infer likely safe test/verification commands for a repository.

Dependency-free helper for the llm-tester Claude Code skill.
It prints JSON with discovered commands and the files that implied them.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
from typing import Any


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def read_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        return json.loads(read_text(path))
    except Exception:
        return {}


def add(commands: list[dict[str, str]], command: str, reason: str, source: str) -> None:
    if command and command not in {item["command"] for item in commands}:
        commands.append({"command": command, "reason": reason, "source": source})


def detect_js(root: pathlib.Path, commands: list[dict[str, str]]) -> None:
    pkg_path = root / "package.json"
    if not pkg_path.exists():
        return
    pkg = read_json(pkg_path)
    scripts = pkg.get("scripts", {}) if isinstance(pkg, dict) else {}
    manager = "npm"
    if (root / "pnpm-lock.yaml").exists():
        manager = "pnpm"
    elif (root / "yarn.lock").exists():
        manager = "yarn"
    elif (root / "bun.lockb").exists():
        manager = "bun"

    def run_script(name: str) -> str:
        if manager == "npm":
            return f"npm run {name}"
        if manager == "bun":
            return f"bun run {name}"
        return f"{manager} {name}"

    for name in ["test", "lint", "typecheck", "type-check", "check", "build", "e2e"]:
        if name in scripts:
            add(commands, run_script(name), f"package.json script: {name}", "package.json")

    if "test" not in scripts and any((root / d).exists() for d in ["__tests__", "tests", "test"]):
        add(commands, run_script("test"), "tests directory exists but no explicit script was found", "heuristic")


def detect_python(root: pathlib.Path, commands: list[dict[str, str]]) -> None:
    py_files = list(root.glob("*.py")) + list(root.glob("src/**/*.py"))[:5]
    has_py = bool(py_files or (root / "pyproject.toml").exists() or (root / "requirements.txt").exists())
    if not has_py:
        return
    add(commands, "python -m compileall .", "Python syntax check", "heuristic")
    if any((root / d).exists() for d in ["tests", "test"]):
        add(commands, "pytest", "Python tests directory detected", "heuristic")
    text = read_text(root / "pyproject.toml")
    if "ruff" in text:
        add(commands, "ruff check .", "ruff configuration detected", "pyproject.toml")
    if "mypy" in text:
        add(commands, "mypy .", "mypy configuration detected", "pyproject.toml")


def detect_go(root: pathlib.Path, commands: list[dict[str, str]]) -> None:
    if (root / "go.mod").exists():
        add(commands, "go test ./...", "Go module detected", "go.mod")
        add(commands, "go vet ./...", "Go module detected", "go.mod")


def detect_rust(root: pathlib.Path, commands: list[dict[str, str]]) -> None:
    if (root / "Cargo.toml").exists():
        add(commands, "cargo check", "Rust project detected", "Cargo.toml")
        add(commands, "cargo test", "Rust project detected", "Cargo.toml")
        add(commands, "cargo clippy -- -D warnings", "Rust project detected", "Cargo.toml")


def detect_shell(root: pathlib.Path, commands: list[dict[str, str]]) -> None:
    shell_files = list(root.glob("*.sh")) + list(root.glob("scripts/*.sh"))
    for file in shell_files[:10]:
        add(commands, f"bash -n {file.as_posix()}", "Shell syntax check", file.as_posix())
    if shell_files:
        add(commands, "shellcheck scripts/*.sh *.sh", "Shell lint if shellcheck is installed", "heuristic")


def detect_iac(root: pathlib.Path, commands: list[dict[str, str]]) -> None:
    if list(root.glob("*.tf")):
        add(commands, "terraform fmt -check", "Terraform files detected", "*.tf")
        add(commands, "terraform validate", "Terraform files detected", "*.tf")
    if (root / "docker-compose.yml").exists() or (root / "docker-compose.yaml").exists():
        add(commands, "docker compose config", "Docker Compose file detected", "docker-compose")
    if (root / "Dockerfile").exists():
        add(commands, "docker build --check .", "Dockerfile detected; supported by newer Docker versions", "Dockerfile")
    if list(root.glob("*.yml")) or list(root.glob("*.yaml")):
        add(commands, "python -c 'import yaml, pathlib; [yaml.safe_load(p.read_text()) for p in pathlib.Path(\".\").glob(\"*.y*ml\")]'", "YAML syntax check if PyYAML is installed", "heuristic")


def detect_make(root: pathlib.Path, commands: list[dict[str, str]]) -> None:
    makefile = root / "Makefile"
    if not makefile.exists():
        return
    text = read_text(makefile)
    targets = re.findall(r"^([A-Za-z0-9_.-]+):(?:\s|$)", text, re.M)
    for preferred in ["test", "lint", "check", "build", "validate"]:
        if preferred in targets:
            add(commands, f"make {preferred}", f"Makefile target: {preferred}", "Makefile")


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect likely repository test commands")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    commands: list[dict[str, str]] = []

    detect_make(root, commands)
    detect_js(root, commands)
    detect_python(root, commands)
    detect_go(root, commands)
    detect_rust(root, commands)
    detect_shell(root, commands)
    detect_iac(root, commands)

    print(json.dumps({"root": str(root), "commands": commands}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
