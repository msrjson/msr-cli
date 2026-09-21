from pathlib import Path

from msr_cli.main import main


FIXTURE = Path(__file__).parents[1] / "tests" / "fixtures"


def test_validate_accepts_valid_manifest(capsys):
    assert main(["validate", str(FIXTURE / "valid.json")]) == 0
    assert "valid (MSR JSON 2.0)" in capsys.readouterr().out


def test_validate_reports_schema_errors(capsys):
    assert main(["validate", str(FIXTURE / "invalid.json")]) == 1
    assert "unexpected" in capsys.readouterr().out


def test_validate_with_explicit_draft_schema(tmp_path, capsys):
    import json
    import pytest

    draft = Path(__file__).resolve().parents[2] / "msr-standard/spec/schemas/msr-2.1-draft.json"
    if not draft.exists():
        pytest.skip("specification checkout unavailable")
    manifest = json.loads((FIXTURE / "valid.json").read_text())
    manifest["$schema"] = "https://msrjson.org/schemas/msr-2.1-draft.json"
    manifest["entity"]["media"] = {"icon": {"png_256": "https://example.com/icon.png"}}
    path = tmp_path / "msr.json"
    path.write_text(json.dumps(manifest))
    assert main(["validate", str(path), "--schema", str(draft)]) == 0
    assert "msr-2.1-draft.json" in capsys.readouterr().out
