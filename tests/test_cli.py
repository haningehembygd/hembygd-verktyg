import importlib
import tomllib
from pathlib import Path

from hembygd.presentation.cli import main


def test_main_prints_application_name(capsys) -> None:
    main()

    captured = capsys.readouterr()

    assert captured.out == "Hembygd Verktyg\n"


def test_declared_console_script_resolves() -> None:
    pyproject_path = Path(__file__).parents[1] / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    entry_point = pyproject["project"]["scripts"]["hembygd"]
    module_name, separator, callable_name = entry_point.partition(":")

    assert separator == ":"

    module = importlib.import_module(module_name)

    assert callable(getattr(module, callable_name))
