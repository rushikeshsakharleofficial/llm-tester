from __future__ import annotations

import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "detect_test_commands.py"


def load_detector():
    spec = importlib.util.spec_from_file_location("detect_test_commands", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DetectTestCommandsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = load_detector()
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmpdir.name)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def commands(self) -> list[str]:
        found: list[dict[str, str]] = []
        self.detector.detect_make(self.root, found)
        self.detector.detect_js(self.root, found)
        self.detector.detect_python(self.root, found)
        self.detector.detect_skill(self.root, found)
        return [item["command"] for item in found]

    def test_detects_npm_scripts(self) -> None:
        (self.root / "package.json").write_text(
            json.dumps({"scripts": {"test": "vitest", "lint": "eslint .", "build": "vite build"}}),
            encoding="utf-8",
        )

        commands = self.commands()

        self.assertIn("npm run test", commands)
        self.assertIn("npm run lint", commands)
        self.assertIn("npm run build", commands)

    def test_detects_python_scripts_directory(self) -> None:
        scripts = self.root / "scripts"
        scripts.mkdir()
        (scripts / "tool.py").write_text("print('ok')\n", encoding="utf-8")

        self.assertIn("python -m compileall .", self.commands())

    def test_uses_unittest_when_pytest_is_not_declared(self) -> None:
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "test_sample.py").write_text("import unittest\n", encoding="utf-8")

        commands = self.commands()

        self.assertIn("python -m unittest discover", commands)
        self.assertNotIn("pytest", commands)

    def test_prefers_pytest_when_declared(self) -> None:
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "test_sample.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
        (self.root / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")

        commands = self.commands()

        self.assertIn("pytest", commands)
        self.assertNotIn("python -m unittest discover", commands)

    def test_detects_make_targets(self) -> None:
        (self.root / "Makefile").write_text("test:\n\t@true\ncheck:\n\t@true\n", encoding="utf-8")

        commands = self.commands()

        self.assertIn("make test", commands)
        self.assertIn("make check", commands)

    def test_detects_skill_validation_when_available(self) -> None:
        (self.root / "SKILL.md").write_text("---\nname: example\ndescription: Example\n---\n", encoding="utf-8")
        scripts = self.root / "scripts"
        scripts.mkdir()
        (scripts / "validate_skill.py").write_text("", encoding="utf-8")

        self.assertIn("python3 scripts/validate_skill.py .", self.commands())


if __name__ == "__main__":
    unittest.main()
