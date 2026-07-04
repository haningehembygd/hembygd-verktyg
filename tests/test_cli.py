import importlib
import json
import tomllib
from pathlib import Path

from hembygd.application import FetchedPage
from hembygd.infrastructure.http import UrlLibPageFetcher
from hembygd.presentation.cli import main


def test_main_prints_application_name(capsys) -> None:
    exit_code = main([])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Hembygd Verktyg\n"


def test_import_html_can_export_json(capsys, tmp_path: Path) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "hembygd_documents.html"
    destination = tmp_path / "archive.json"

    exit_code = main(["import-html", str(fixture_path), "--output", str(destination)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == (
        f"Exported JSON to {destination}\n"
        "Imported 4 entries and 7 documents from Haninge Hembygdsgille\n"
    )
    assert json.loads(destination.read_text())["schema_version"] == 1


def test_import_html_reports_missing_file(capsys) -> None:
    exit_code = main(["import-html", "missing.html"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Could not import HTML:" in captured.err


def test_import_url_fetches_and_can_export_json(capsys, monkeypatch, tmp_path: Path) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "hembygd_documents.html"
    destination = tmp_path / "archive.json"

    def fake_fetch(self, *, url: str) -> FetchedPage:
        return FetchedPage(html=fixture_path.read_text(), final_url=url)

    monkeypatch.setattr(UrlLibPageFetcher, "fetch", fake_fetch)

    exit_code = main(["import-url", "--output", str(destination)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == (
        f"Exported JSON to {destination}\n"
        "Imported 4 entries and 7 documents from Haninge Hembygdsgille\n"
    )
    assert json.loads(destination.read_text())["schema_version"] == 1


def test_declared_console_script_resolves() -> None:
    pyproject_path = Path(__file__).parents[1] / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    entry_point = pyproject["project"]["scripts"]["hembygd"]
    module_name, separator, callable_name = entry_point.partition(":")

    assert separator == ":"

    module = importlib.import_module(module_name)

    assert callable(getattr(module, callable_name))
