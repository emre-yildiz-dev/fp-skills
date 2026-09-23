#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
REF = re.compile(r"\.\./references/([a-z0-9-]+\.md)")
FORBIDDEN = {
    "Call the Skill tool": "skill-tool-instruction",
    "call the Skill tool": "skill-tool-instruction",
    "Commit your work": "automatic-commit",
}
MANIFEST_FIELDS = {"schema_version", "references", "skills"}
SKILL_FIELDS = {"path", "release", "user_invoked", "references"}


class ConfigurationError(Exception):
    def __init__(self, path: Path, detail: str):
        self.path = path
        self.detail = detail


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if match is None:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def finding(code: str, path: Path, detail: str) -> dict[str, str]:
    return {"code": code, "path": str(path), "detail": detail}


def configuration_report(error: ConfigurationError) -> dict[str, object]:
    return {"status": "error", "findings": [finding("configuration-error", error.path, error.detail)]}


def load_manifest(manifest_path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ConfigurationError(manifest_path, str(error)) from error
    if not isinstance(manifest, dict):
        raise ConfigurationError(manifest_path, "manifest must be an object")
    return manifest


def validate_manifest(manifest: dict[str, object], manifest_path: Path) -> None:
    if set(manifest) != MANIFEST_FIELDS:
        raise ConfigurationError(manifest_path, f"manifest fields must be {sorted(MANIFEST_FIELDS)}")
    if not isinstance(manifest["schema_version"], int) or isinstance(manifest["schema_version"], bool) or manifest["schema_version"] != 1:
        raise ConfigurationError(manifest_path, "schema_version must be 1")
    references = manifest["references"]
    skills = manifest["skills"]
    if not isinstance(references, list) or not all(isinstance(reference, str) and reference for reference in references):
        raise ConfigurationError(manifest_path, "references must be a list of non-empty strings")
    if not isinstance(skills, dict):
        raise ConfigurationError(manifest_path, "skills must be an object")
    for name, cfg in skills.items():
        if not isinstance(name, str) or not name or not isinstance(cfg, dict) or set(cfg) != SKILL_FIELDS:
            raise ConfigurationError(manifest_path, f"invalid skill entry: {name!r}")
        if not isinstance(cfg["path"], str) or not cfg["path"]:
            raise ConfigurationError(manifest_path, f"{name}.path must be a non-empty string")
        if not isinstance(cfg["release"], int) or isinstance(cfg["release"], bool) or cfg["release"] not in (1, 2):
            raise ConfigurationError(manifest_path, f"{name}.release must be 1 or 2")
        if not isinstance(cfg["user_invoked"], bool):
            raise ConfigurationError(manifest_path, f"{name}.user_invoked must be a boolean")
        if not isinstance(cfg["references"], list) or not all(isinstance(reference, str) and reference for reference in cfg["references"]):
            raise ConfigurationError(manifest_path, f"{name}.references must be a list of non-empty strings")


def validate(root: Path, through: int) -> dict[str, object]:
    manifest_path = root / "suite.json"
    if not manifest_path.is_file():
        return {"status": "fail", "findings": [finding("missing-manifest", manifest_path, "suite.json is required")]}
    manifest = load_manifest(manifest_path)
    validate_manifest(manifest, manifest_path)
    findings: list[dict[str, str]] = []

    for ref_name in manifest["references"]:
        ref_path = root / "references" / ref_name
        if not ref_path.is_file():
            findings.append(finding("missing-reference", ref_path, ref_name))

    for name, cfg in manifest["skills"].items():
        if int(cfg["release"]) > through:
            continue
        skill_path = root / cfg["path"] / "SKILL.md"
        if not skill_path.is_file():
            findings.append(finding("missing-skill", skill_path, name))
            continue
        try:
            text = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ConfigurationError(skill_path, str(error)) from error
        fm = parse_frontmatter(text)
        if fm.get("name") != name or not fm.get("description"):
            findings.append(finding("frontmatter", skill_path, "name/description mismatch"))
        disabled = fm.get("disable-model-invocation") == "true"
        if disabled != bool(cfg["user_invoked"]):
            findings.append(finding("invocation-policy", skill_path, f"user_invoked={cfg['user_invoked']}"))
        for phrase, code in FORBIDDEN.items():
            if phrase in text:
                findings.append(finding(code, skill_path, phrase))
        declared = set(REF.findall(text))
        required = set(cfg["references"])
        if declared != required:
            findings.append(finding("reference-contract", skill_path, f"declared={sorted(declared)} required={sorted(required)}"))
        if len(text) // 4 > 2500:
            findings.append(finding("token-budget", skill_path, "estimated SKILL.md tokens exceed 2500"))

    return {"status": "pass" if not findings else "fail", "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite-root", type=Path, required=True)
    parser.add_argument("--through", type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    try:
        report = validate(args.suite_root.resolve(), args.through)
    except ConfigurationError as error:
        print(json.dumps(configuration_report(error), indent=2))
        return 2
    except OSError as error:
        print(json.dumps(configuration_report(ConfigurationError(args.suite_root, str(error))), indent=2))
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
