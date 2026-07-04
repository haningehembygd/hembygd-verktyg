from dataclasses import dataclass
from pathlib import Path

from hembygd.application import ExportSite
from hembygd.domain import Site


@dataclass
class RecordingExporter:
    exported_site: Site | None = None
    destination: Path | None = None

    def export(self, *, site: Site, destination: Path) -> None:
        self.exported_site = site
        self.destination = destination


def test_export_site_delegates_to_configured_exporter(tmp_path: Path) -> None:
    exporter = RecordingExporter()
    site = Site(name="Example", base_url="https://example.test")
    destination = tmp_path / "archive.json"

    ExportSite(exporter=exporter).execute(site=site, destination=destination)

    assert exporter.exported_site is site
    assert exporter.destination == destination
