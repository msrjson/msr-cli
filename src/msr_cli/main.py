"""The intentionally small reference CLI; validation lives in msr-validator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from msr_validator import validate


def _validate(path: Path) -> int:
    try:
        result = validate(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        print(f"{path}: invalid input: {error}")
        return 2
    if result.valid:
        print(f"{path}: valid (MSR JSON 2.0)")
        return 0
    for error in result.errors:
        print(f"{path}{error.path}: {error.message}")
    return 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="msr", description="Reference tooling for MSR JSON")
    subcommands = parser.add_subparsers(dest="command", required=True)
    validate_parser = subcommands.add_parser("validate", help="validate a manifest against MSR JSON 2.0")
    validate_parser.add_argument("manifest", type=Path, help="path to msr.json")
    arguments = parser.parse_args(argv)
    if arguments.command == "validate":
        return _validate(arguments.manifest)
    parser.error("unsupported command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
