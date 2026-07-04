from dataclasses import dataclass

from hembygd.application import ImportHtml
from hembygd.domain import Site


@dataclass
class RecordingParser:
    html: str | None = None

    def parse(self, *, html: str, source_url: str, site_name: str) -> Site:
        self.html = html
        return Site(name=site_name, base_url=source_url)


def test_import_html_delegates_to_configured_parser() -> None:
    parser = RecordingParser()
    use_case = ImportHtml(parser=parser)

    site = use_case.execute(
        html="<html></html>",
        source_url="https://example.test/documents",
        site_name="Example",
    )

    assert parser.html == "<html></html>"
    assert site.name == "Example"
