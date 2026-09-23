import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "run_pi_triggers.py"
spec = importlib.util.spec_from_file_location("run_pi_triggers", SCRIPT)
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(runner)


class PiTriggerParserTest(unittest.TestCase):
    def test_detects_read_inside_target_skill(self):
        transcript = json.dumps({
            "type": "tool_execution_start",
            "toolName": "read",
            "args": {"path": "/tmp/project/.agents/skills/fp/fp-tdd/SKILL.md"},
        })
        self.assertTrue(runner.detect_load(transcript, "fp-tdd"))

    def test_ignores_skill_name_in_session_text(self):
        transcript = json.dumps({"type": "session", "skills": ["fp-tdd"]})
        self.assertFalse(runner.detect_load(transcript, "fp-tdd"))

    def test_ignores_reads_of_another_skill(self):
        transcript = json.dumps({
            "type": "tool_execution_start",
            "toolName": "read",
            "args": {
                "path": "/tmp/project/.agents/skills/fp/fp-code-review/SKILL.md"
            },
        })
        self.assertFalse(runner.detect_load(transcript, "fp-tdd"))


class PiTriggerExecutionTest(unittest.TestCase):
    def run_once_with_stdout(self, stdout, returncode=0):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            suite_root = root / "suite"
            (suite_root / "references").mkdir(parents=True)
            (suite_root / "fp-tdd").mkdir()
            (suite_root / "fp-tdd" / "SKILL.md").write_text("# TDD\n")
            prompt_path = root / "artifacts" / "prompt.txt"
            transcript_path = root / "artifacts" / "transcript.jsonl"
            completed = subprocess.CompletedProcess(
                [], returncode, stdout=stdout, stderr=""
            )

            with (
                patch.object(runner.shutil, "which", return_value="/usr/bin/pi"),
                patch.object(runner.subprocess, "run", return_value=completed),
            ):
                result = runner.run_once(
                    suite_root=suite_root,
                    skill_name="fp-tdd",
                    query="negative query",
                    timeout=60,
                    prompt_path=prompt_path,
                    transcript_path=transcript_path,
                )

            self.assertEqual(transcript_path.read_text(), stdout)
            return result

    def test_run_once_reports_empty_successful_stdout_as_no_events(self):
        result = self.run_once_with_stdout("")
        self.assertEqual(result["status"], "infrastructure_error")
        self.assertEqual(result["reason"], "Pi emitted no JSON events")

    def test_run_once_reports_whitespace_only_successful_stdout_as_no_events(self):
        result = self.run_once_with_stdout(" \n\t\n")
        self.assertEqual(result["status"], "infrastructure_error")
        self.assertEqual(result["reason"], "Pi emitted no JSON events")

    def test_run_once_prioritizes_nonzero_status_over_empty_stdout(self):
        result = self.run_once_with_stdout("", returncode=17)
        self.assertEqual(result["status"], "infrastructure_error")
        self.assertEqual(result["reason"], "pi exited with status 17")

    def test_run_once_accepts_a_valid_json_object(self):
        transcript = json.dumps({"type": "session"}) + "\n"
        result = self.run_once_with_stdout(transcript)
        self.assertEqual(result, {"status": "completed", "loaded": False})

    def test_run_once_rejects_a_json_primitive(self):
        result = self.run_once_with_stdout("42\n")
        self.assertEqual(result["status"], "infrastructure_error")
        self.assertEqual(result["reason"], "Pi emitted a non-object JSON event")

    def test_run_once_rejects_a_malformed_line(self):
        transcript = json.dumps({"type": "session"}) + "\nnot-json\n"
        result = self.run_once_with_stdout(transcript)
        self.assertEqual(result["status"], "infrastructure_error")
        self.assertEqual(result["reason"], "Pi emitted malformed JSON")

    def test_pi_command_isolates_to_the_copied_target_skill(self):
        skill_path = Path("/tmp/fp/fp-tdd")
        self.assertEqual(
            runner.pi_command(skill_path, "test-first"),
            [
                "pi",
                "--mode",
                "json",
                "--no-session",
                "--no-extensions",
                "--no-skills",
                "--skill",
                str(skill_path),
                "test-first",
            ],
        )

    def test_run_batch_preserves_query_and_run_order(self):
        queries = [
            {"query": "first", "should_trigger": True},
            {"query": "second", "should_trigger": False},
        ]

        def fake_run_once(**kwargs):
            return {"query": kwargs["query"], "run": kwargs["prompt_path"].parent.name}

        with tempfile.TemporaryDirectory() as temporary_directory:
            with patch.object(runner, "run_once", side_effect=fake_run_once):
                outcomes = runner.run_batch(
                    suite_root=Path("/suite"),
                    skill_name="fp-tdd",
                    queries=queries,
                    runs=2,
                    timeout=60,
                    output_directory=Path(temporary_directory),
                    workers=2,
                )

        self.assertEqual(
            outcomes,
            [
                [
                    {"query": "first", "run": "query-001-run-001"},
                    {"query": "first", "run": "query-001-run-002"},
                ],
                [
                    {"query": "second", "run": "query-002-run-001"},
                    {"query": "second", "run": "query-002-run-002"},
                ],
            ],
        )
