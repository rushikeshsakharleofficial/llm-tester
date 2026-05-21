from __future__ import annotations

import importlib.util
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_skill.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_skill", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateSkillTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = load_validator()
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmpdir.name)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def write_skill(self, frontmatter: str) -> None:
        (self.root / "SKILL.md").write_text(f"---\n{frontmatter}---\n# Body\n", encoding="utf-8")
        agents = self.root / "agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text('interface:\n  display_name: "Example"\n', encoding="utf-8")

    def test_valid_skill_passes(self) -> None:
        self.write_skill("name: example-skill\ndescription: Example skill\n")

        self.assertEqual([], self.validator.validate_skill(self.root))

    def test_missing_openai_metadata_fails(self) -> None:
        (self.root / "SKILL.md").write_text(
            "---\nname: example\ndescription: Example\n---\n",
            encoding="utf-8",
        )

        self.assertIn("agents/openai.yaml is missing", self.validator.validate_skill(self.root))

    def test_invalid_name_fails(self) -> None:
        self.write_skill("name: Bad_Name\ndescription: Example\n")

        errors = self.validator.validate_skill(self.root)

        self.assertTrue(any("Skill name must use" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
