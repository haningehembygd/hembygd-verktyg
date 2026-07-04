"""Application contract and use case for parsing HTML sources."""

from dataclasses import dataclass
from typing import Protocol

from hembygd.domain import Site


class SiteParser(Protocol):
    """Translate source HTML into the shared domain model."""

    def parse(self, *, html: str, source_url: str, site_name: str) -> Site:
        """Parse one HTML source into a site."""
        ...


@dataclass(slots=True)
class ImportHtml:
    """Import already-fetched HTML through a configured parser."""

    parser: SiteParser

    def execute(self, *, html: str, source_url: str, site_name: str) -> Site:
        """Return the domain representation of the supplied HTML."""
        return self.parser.parse(html=html, source_url=source_url, site_name=site_name)
