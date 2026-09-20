from pathlib import Path

from msr_cli.main import main


FIXTURE = Path(__file__).parents[1] / "tests" / "fixtures"


def test_validate_accepts_valid_manifest(capsys):
    assert main(["validate", str(FIXTURE / "valid.json")]) == 0
    assert "valid (MSR JSON 2.0)" in capsys.readouterr().out


def test_validate_reports_schema_errors(capsys):
    assert main(["validate", str(FIXTURE / "invalid.json")]) == 1
    assert "unexpected" in capsys.readouterr().out
