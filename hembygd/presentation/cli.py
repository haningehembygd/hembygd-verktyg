"""Command-line presentation adapter."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from hembygd.application import ImportHtml
from hembygd.infrastructure.parsers import HembygdParseError, HembygdParser

DEFAULT_SOURCE_URL = "https://www.hembygd.se/haninge-hembygdsgille/foreningsdokument"
DEFAULT_SITE_NAME = "Haninge Hembygdsgille"


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments:
        print("Hembygd Verktyg")
        return 0

    parser = _argument_parser()
    namespace = parser.parse_args(arguments)
    if namespace.command == "import-html":
        return _import_html(namespace)
    parser.error(f"unknown command: {namespace.command}")


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hembygd")
    subparsers = parser.add_subparsers(dest="command", required=True)
    import_parser = subparsers.add_parser(
        "import-html",
        help="parse a saved Hembygd.se document page",
    )
    import_parser.add_argument("path", type=Path, help="path to a saved HTML file")
    import_parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL)
    import_parser.add_argument("--site-name", default=DEFAULT_SITE_NAME)
    return parser


def _import_html(namespace: argparse.Namespace) -> int:
    try:
        html = namespace.path.read_text(encoding="utf-8")
        site = ImportHtml(parser=HembygdParser()).execute(
            html=html,
            source_url=namespace.source_url,
            site_name=namespace.site_name,
        )
    except (OSError, UnicodeError, HembygdParseError) as error:
        print(f"Could not import HTML: {error}", file=sys.stderr)
        return 1

    document_count = sum(len(entry.documents) for entry in site.entries)
    print(f"Imported {len(site.entries)} entries and {document_count} documents from {site.name}")
    return 0
