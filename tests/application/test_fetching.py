from dataclasses import dataclass

from hembygd.application import FetchedPage, ImportUrl
from hembygd.domain import Site


@dataclass
class RecordingFetcher:
    requested_url: str | None = None

    def fetch(self, *, url: str) -> FetchedPage:
        self.requested_url = url
        return FetchedPage(html="<html></html>", final_url="https://example.test/final")


@dataclass
class RecordingParser:
    source_url: str | None = None

    def parse(self, *, html: str, source_url: str, site_name: str) -> Site:
        self.source_url = source_url
        return Site(name=site_name, base_url=source_url)


def test_import_url_fetches_and_parses_final_url() -> None:
    fetcher = RecordingFetcher()
    parser = RecordingParser()

    site = ImportUrl(fetcher=fetcher, parser=parser).execute(
        url="https://example.test/start",
        site_name="Example",
    )

    assert fetcher.requested_url == "https://example.test/start"
    assert parser.source_url == "https://example.test/final"
    assert site.base_url == "https://example.test/final"
