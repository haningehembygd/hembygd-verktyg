"""Application contract and use case for exporting sites."""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from hembygd.domain import Site


class SiteExporter(Protocol):
    """Persist a site in an external representation."""

    def export(self, *, site: Site, destination: Path) -> None:
        """Export a site to the requested destination."""
        ...


@dataclass(slots=True)
class ExportSite:
    """Export one site through a configured adapter."""

    exporter: SiteExporter

    def execute(self, *, site: Site, destination: Path) -> None:
        """Persist the supplied site."""
        self.exporter.export(site=site, destination=destination)
