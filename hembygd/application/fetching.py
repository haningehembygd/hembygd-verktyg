"""Application contract and use case for importing remote pages."""

from dataclasses import dataclass
from typing import Protocol

from hembygd.application.parsing import SiteParser
from hembygd.domain import Site


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchedPage:
    """HTML returned by a page fetcher after redirects."""

    html: str
    final_url: str


class PageFetcher(Protocol):
    """Fetch an HTML page from an external source."""

    def fetch(self, *, url: str) -> FetchedPage:
        """Fetch one page and return decoded HTML."""
        ...


@dataclass(slots=True)
class ImportUrl:
    """Fetch and parse an HTML page into the domain model."""

    fetcher: PageFetcher
    parser: SiteParser

    def execute(self, *, url: str, site_name: str) -> Site:
        """Fetch a URL and parse its final representation."""
        page = self.fetcher.fetch(url=url)
        return self.parser.parse(
            html=page.html,
            source_url=page.final_url,
            site_name=site_name,
        )
