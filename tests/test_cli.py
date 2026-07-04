import importlib
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


def test_import_html_reports_imported_counts(capsys) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "hembygd_documents.html"

    exit_code = main(["import-html", str(fixture_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Imported 4 entries and 7 documents from Haninge Hembygdsgille\n"


def test_import_html_reports_missing_file(capsys) -> None:
    exit_code = main(["import-html", "missing.html"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Could not import HTML:" in captured.err


def test_import_url_fetches_and_reports_counts(capsys, monkeypatch) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "hembygd_documents.html"

    def fake_fetch(self, *, url: str) -> FetchedPage:
        return FetchedPage(html=fixture_path.read_text(), final_url=url)

    monkeypatch.setattr(UrlLibPageFetcher, "fetch", fake_fetch)

    exit_code = main(["import-url"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Imported 4 entries and 7 documents from Haninge Hembygdsgille\n"


def test_declared_console_script_resolves() -> None:
    pyproject_path = Path(__file__).parents[1] / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    entry_point = pyproject["project"]["scripts"]["hembygd"]
    module_name, separator, callable_name = entry_point.partition(":")

    assert separator == ":"

    module = importlib.import_module(module_name)

    assert callable(getattr(module, callable_name))
