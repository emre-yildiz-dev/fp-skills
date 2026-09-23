#!/usr/bin/env python3
"""Run Pi skill-trigger queries in isolated, suite-complete workspaces.

Each query is evaluated against a copied `.agents/skills/fp` package. Pi's JSON
stream is the only source of trigger evidence: a target skill loaded only when
Pi starts a `read` of that skill's `SKILL.md`.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


RESULT_STATUSES = {"pass", "fail", "skipped", "infrastructure_error"}


def detect_load(transcript: str, skill_name: str) -> bool:
    marker = f"/{skill_name}/"
    for line in transcript.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "tool_execution_start":
            continue
        if event.get("toolName") != "read":
            continue
        path = str((event.get("args") or {}).get("path", ""))
        if marker in path.replace("\\", "/") and path.endswith("/SKILL.md"):
            return True
    return False


def load_queries(path: Path) -> list[dict[str, object]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read queries from {path}: {error}") from error
    if not isinstance(data, list):
        raise ValueError("queries must be a JSON list")
    for index, item in enumerate(data):
        if not isinstance(item, dict) or set(item) != {"query", "should_trigger"}:
            raise ValueError(
                "query "
                f"{index} must be exactly {{\"query\": string, \"should_trigger\": bool}}"
            )
        query = item["query"]
        should_trigger = item["should_trigger"]
        if not isinstance(query, str) or not isinstance(should_trigger, bool):
            raise ValueError(
                "query "
                f"{index} must be exactly {{\"query\": string, \"should_trigger\": bool}}"
            )
    return data


def transcript_error(transcript: str) -> str | None:
    """Return the structural problem in a Pi JSON-mode stream, if any."""
    event_count = 0
    for line in transcript.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return "Pi emitted malformed JSON"
        if not isinstance(event, dict):
            return "Pi emitted a non-object JSON event"
        event_count += 1
    if event_count == 0:
        return "Pi emitted no JSON events"
    return None


def transcript_is_malformed(transcript: str) -> bool:
    return transcript_error(transcript) is not None


def write_artifact(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def output_text(value: str | bytes | None) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def copy_suite(suite_root: Path, cwd: Path) -> Path:
    destination = cwd / ".agents" / "skills" / "fp"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(suite_root, destination)
    return destination


def pi_command(skill_path: Path, query: str) -> list[str]:
    return [
        "pi",
        "--mode",
        "json",
        "--no-session",
        "--no-extensions",
        "--no-skills",
        "--skill",
        str(skill_path),
        query,
    ]


def run_once(
    suite_root: Path,
    skill_name: str,
    query: str,
    timeout: int,
    prompt_path: Path,
    transcript_path: Path,
) -> dict[str, object]:
    write_artifact(prompt_path, query + "\n")
    if shutil.which("pi") is None:
        write_artifact(transcript_path, "")
        return {"status": "skipped", "reason": "pi is not available on PATH"}

    with tempfile.TemporaryDirectory(prefix="fp-pi-trigger-") as temporary_cwd:
        cwd = Path(temporary_cwd)
        copied_suite = copy_suite(suite_root, cwd)
        try:
            completed = subprocess.run(
                pi_command(copied_suite / skill_name, query),
                cwd=cwd,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            write_artifact(transcript_path, output_text(error.stdout))
            return {
                "status": "infrastructure_error",
                "reason": f"pi timed out after {timeout} seconds",
            }
        except FileNotFoundError:
            write_artifact(transcript_path, "")
            return {"status": "skipped", "reason": "pi is not available on PATH"}
        except OSError as error:
            write_artifact(transcript_path, "")
            return {"status": "infrastructure_error", "reason": f"pi could not start: {error}"}

    write_artifact(transcript_path, completed.stdout)
    if completed.returncode != 0:
        return {
            "status": "infrastructure_error",
            "reason": f"pi exited with status {completed.returncode}",
        }
    if problem := transcript_error(completed.stdout):
        return {"status": "infrastructure_error", "reason": problem}
    return {"status": "completed", "loaded": detect_load(completed.stdout, skill_name)}


def run_batch(
    suite_root: Path,
    skill_name: str,
    queries: list[dict[str, object]],
    runs: int,
    timeout: int,
    output_directory: Path,
    workers: int,
) -> list[list[dict[str, object]]]:
    jobs = [
        (query_index, run_index, str(query["query"]))
        for query_index, query in enumerate(queries, start=1)
        for run_index in range(1, runs + 1)
    ]

    def execute(job: tuple[int, int, str]) -> dict[str, object]:
        query_index, run_index, query = job
        artifact_directory = output_directory / "runs" / (
            f"query-{query_index:03d}-run-{run_index:03d}"
        )
        return run_once(
            suite_root=suite_root,
            skill_name=skill_name,
            query=query,
            timeout=timeout,
            prompt_path=artifact_directory / "prompt.txt",
            transcript_path=artifact_directory / "transcript.jsonl",
        )

    with ThreadPoolExecutor(max_workers=workers) as executor:
        outcomes = list(executor.map(execute, jobs))
    return [outcomes[index : index + runs] for index in range(0, len(outcomes), runs)]


def query_result(
    runs: list[dict[str, object]], should_trigger: bool
) -> tuple[str, bool | None]:
    statuses = {str(run["status"]) for run in runs}
    if "infrastructure_error" in statuses:
        return "infrastructure_error", None
    if statuses == {"skipped"}:
        return "skipped", None
    if "skipped" in statuses:
        return "infrastructure_error", None
    loaded = [bool(run["loaded"]) for run in runs]
    passed = all(value == should_trigger for value in loaded)
    return ("pass" if passed else "fail"), passed


def resolve_skill(args: argparse.Namespace, parser: argparse.ArgumentParser) -> tuple[Path, str]:
    if args.skill_path is not None:
        skill_path = args.skill_path.resolve()
        suite_root = skill_path.parent
        skill_name = skill_path.name
        if args.suite_root is not None or args.skill is not None:
            parser.error("--skill-path cannot be combined with --suite-root or --skill")
    else:
        if args.suite_root is None or args.skill is None:
            parser.error("provide --skill-path or both --suite-root and --skill")
        suite_root = args.suite_root.resolve()
        skill_name = args.skill
        skill_path = suite_root / skill_name
    if not (suite_root / "references").is_dir() or not (skill_path / "SKILL.md").is_file():
        parser.error("skill path must be a skill inside a complete fp suite")
    return suite_root, skill_name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-path", type=Path)
    parser.add_argument("--suite-root", type=Path)
    parser.add_argument("--skill")
    parser.add_argument("--queries", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args(argv)
    if args.runs < 1:
        parser.error("--runs must be at least 1")
    if args.timeout < 1:
        parser.error("--timeout must be at least 1")
    if args.workers < 1:
        parser.error("--workers must be at least 1")

    suite_root, skill_name = resolve_skill(args, parser)
    try:
        queries = load_queries(args.queries)
    except ValueError as error:
        parser.error(str(error))

    dated_directory = args.output_dir / datetime.now(UTC).strftime("%Y-%m-%dT%H%M%S-%fZ")
    dated_directory.mkdir(parents=True, exist_ok=False)
    results: list[dict[str, Any]] = []
    batch_outcomes = run_batch(
        suite_root=suite_root,
        skill_name=skill_name,
        queries=queries,
        runs=args.runs,
        timeout=args.timeout,
        output_directory=dated_directory,
        workers=args.workers,
    )
    for query, runs in zip(queries, batch_outcomes, strict=True):
        status, passed = query_result(runs, bool(query["should_trigger"]))
        if status not in RESULT_STATUSES:
            raise RuntimeError(f"unexpected result status: {status}")
        results.append(
            {
                "query": query["query"],
                "should_trigger": query["should_trigger"],
                "status": status,
                "passed": passed,
                "runs": runs,
            }
        )

    output = {
        "created_at": datetime.now(UTC).isoformat(),
        "skill": skill_name,
        "runs_per_query": args.runs,
        "results": results,
    }
    result_path = dated_directory / "trigger-results.json"
    write_artifact(result_path, json.dumps(output, indent=2) + "\n")
    print(result_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
