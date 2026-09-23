import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]


class ReferenceContractsTest(unittest.TestCase):
    def assert_contains(self, name: str, phrases: list[str]):
        text = (ROOT / "references" / name).read_text(encoding="utf-8")
        for phrase in phrases:
            self.assertIn(phrase, text, f"{name} missing {phrase!r}")

    def test_project_detection_contract(self):
        self.assert_contains("project-detection.md", [
            "## Evidence order", "## Effect detection", "## Stop conditions",
            "vendored installed source", "exact installed version",
            "Effect is installed but does not resolve to 4.x",
            "exact installed version or release channel cannot be resolved",
            "Effect 3 or another Effect 4 RC by analogy",
        ])

    def test_fcis_contract(self):
        self.assert_contains("fcis-architecture.md", [
            "## Functional core", "## Imperative shell", "## Capability boundaries",
            "## Architecture exception", "If every external fact were already available",
        ])

    def test_effect_contract(self):
        self.assert_contains("effect-4.md", [
            "Effect<A, E, R>", "Context.Service", "Layer.effect",
            "## Composition roots", "## Effect testing", "it.effect",
            "Effect.exit", "TestClock", "test Layers",
            "## Resources and concurrency",
        ])

    def test_error_contract(self):
        self.assert_contains("error-model.md", [
            "## Expected failures", "## Foreign failures", "## Defects",
            "## Interruptions", "## Retry and idempotency", "## Serialized sinks",
        ])

    def test_testing_contract(self):
        self.assert_contains("testing.md", [
            "## Core-first vertical slice", "## Pure decision tests",
            "## Shell orchestration tests", "## Adapter integration tests",
            "## Wire contract tests",
        ])

    def test_generic_testing_reference_has_no_effect_specific_guidance(self):
        text = (ROOT / "references" / "testing.md").read_text(encoding="utf-8")
        for phrase in ("Effect", "Context.Service", "Layer", "TestClock", "it.effect"):
            self.assertNotIn(phrase, text)

    def test_artifact_contract(self):
        self.assert_contains("artifact-contracts.md", [
            "## Glossary", "## Decision ledger", "## ADR", "## Specification",
            "Architecture exceptions",
        ])
