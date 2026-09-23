import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "validate_suite.py"
spec = importlib.util.spec_from_file_location("validate_suite", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class ValidateSuiteTest(unittest.TestCase):
    def make_suite(self) -> Path:
        root = Path(tempfile.mkdtemp()) / "fp"
        (root / "references").mkdir(parents=True)
        (root / "references" / "fcis-architecture.md").write_text("# FCIS\n", encoding="utf-8")
        skill = root / "fp-example"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: fp-example\n"
            "description: Example discipline. Use when designing an example.\n"
            "---\n\n"
            "Read `../references/fcis-architecture.md`.\n",
            encoding="utf-8",
        )
        (root / "suite.json").write_text(json.dumps({
            "schema_version": 1,
            "references": ["fcis-architecture.md"],
            "skills": {
                "fp-example": {
                    "path": "fp-example",
                    "release": 1,
                    "user_invoked": False,
                    "references": ["fcis-architecture.md"],
                }
            },
        }), encoding="utf-8")
        return root

    def test_valid_suite_passes(self):
        report = validator.validate(self.make_suite(), through=1)
        self.assertEqual(report["findings"], [])

    def test_missing_reference_fails(self):
        root = self.make_suite()
        (root / "references" / "fcis-architecture.md").unlink()
        report = validator.validate(root, through=1)
        self.assertIn("missing-reference", {f["code"] for f in report["findings"]})

    def test_skill_tool_instruction_fails(self):
        root = self.make_suite()
        path = root / "fp-example" / "SKILL.md"
        path.write_text(path.read_text() + "\nCall the Skill tool.\n", encoding="utf-8")
        report = validator.validate(root, through=1)
        self.assertIn("skill-tool-instruction", {f["code"] for f in report["findings"]})

    def test_user_invoked_requires_disable_flag(self):
        root = self.make_suite()
        manifest = json.loads((root / "suite.json").read_text())
        manifest["skills"]["fp-example"]["user_invoked"] = True
        (root / "suite.json").write_text(json.dumps(manifest), encoding="utf-8")
        report = validator.validate(root, through=1)
        self.assertIn("invocation-policy", {f["code"] for f in report["findings"]})

    def test_model_invoked_rejects_disable_flag(self):
        root = self.make_suite()
        path = root / "fp-example" / "SKILL.md"
        path.write_text(path.read_text().replace("description:", "disable-model-invocation: true\ndescription:"), encoding="utf-8")
        report = validator.validate(root, through=1)
        self.assertIn("invocation-policy", {f["code"] for f in report["findings"]})

    def test_release_filter_ignores_later_missing_skill(self):
        root = self.make_suite()
        manifest = json.loads((root / "suite.json").read_text())
        manifest["skills"]["fp-later"] = {
            "path": "fp-later", "release": 2, "user_invoked": False,
            "references": ["fcis-architecture.md"],
        }
        (root / "suite.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.assertEqual(validator.validate(root, through=1)["findings"], [])

    def run_cli(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--suite-root", str(root), "--through", "1"],
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_configuration_error(self, result: subprocess.CompletedProcess[str]):
        self.assertEqual(result.returncode, 2)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["findings"][0]["code"], "configuration-error")

    def test_cli_malformed_json_is_configuration_error(self):
        root = self.make_suite()
        (root / "suite.json").write_text("{", encoding="utf-8")
        self.assert_configuration_error(self.run_cli(root))

    def test_cli_malformed_manifest_is_configuration_error(self):
        root = self.make_suite()
        (root / "suite.json").write_text(json.dumps({"references": []}), encoding="utf-8")
        self.assert_configuration_error(self.run_cli(root))

    def test_release_one_real_suite_validates_when_complete(self):
        suite_root = Path(__file__).parents[2]
        report = validator.validate(suite_root, through=1)
        missing = {f["path"] for f in report["findings"] if f["code"] == "missing-skill"}
        self.assertNotIn(str(suite_root / "fp-domain-modeling" / "SKILL.md"), missing)

    def test_release_two_contains_tdd(self):
        suite_root = Path(__file__).parents[2]
        report = validator.validate(suite_root, through=2)
        missing = {Path(f["path"]).parts[-2] for f in report["findings"] if f["code"] == "missing-skill"}
        self.assertNotIn("fp-tdd", missing)
