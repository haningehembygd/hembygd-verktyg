import json
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from hembygd.domain import Asset, Document, Entry, EntryType, Metadata, Site
from hembygd.infrastructure.exporters import JsonExportError, JsonSiteExporter


def test_exporter_writes_versioned_domain_document(tmp_path: Path) -> None:
    metadata = Metadata(
        author="Haninge Hembygdsgille",
        language="sv",
        tags=("årsmöte",),
        created_at=datetime(2026, 3, 29, 10, 30, tzinfo=UTC),
        source="https://example.test/documents",
        attributes=(("source_id", "42"),),
    )
    document = Document(
        title="Protokoll",
        url="https://example.test/protokoll.pdf",
        filename="protokoll.pdf",
        mime_type="application/pdf",
        size_bytes=123,
        checksum="sha256:abc",
        local_path=Path("archive/protokoll.pdf"),
        metadata=metadata,
    )
    asset = Asset(
        title="Fotografi",
        url="https://example.test/photo.jpg",
        filename="photo.jpg",
        mime_type="image/jpeg",
    )
    site = Site(
        name="Haninge Hembygdsgille",
        base_url="https://example.test/documents",
        language="sv",
        metadata=metadata,
        entries=(
            Entry(
                title="Årsmöte 2026",
                entry_type=EntryType.MEETING,
                date=date(2026, 3, 29),
                documents=(document,),
                assets=(asset,),
            ),
        ),
    )
    destination = tmp_path / "nested" / "archive.json"

    JsonSiteExporter().export(site=site, destination=destination)

    exported = json.loads(destination.read_text(encoding="utf-8"))
    assert exported == {
        "schema_version": 1,
        "site": {
            "name": "Haninge Hembygdsgille",
            "base_url": "https://example.test/documents",
            "language": "sv",
            "description": None,
            "metadata": {
                "author": "Haninge Hembygdsgille",
                "language": "sv",
                "license": None,
                "category": None,
                "tags": ["årsmöte"],
                "created_at": "2026-03-29T10:30:00+00:00",
                "modified_at": None,
                "source": "https://example.test/documents",
                "attributes": {"source_id": "42"},
            },
            "entries": [
                {
                    "title": "Årsmöte 2026",
                    "type": "meeting",
                    "description": None,
                    "date": "2026-03-29",
                    "category": None,
                    "metadata": _empty_metadata(),
                    "documents": [
                        {
                            "title": "Protokoll",
                            "url": "https://example.test/protokoll.pdf",
                            "filename": "protokoll.pdf",
                            "mime_type": "application/pdf",
                            "size_bytes": 123,
                            "checksum": "sha256:abc",
                            "local_path": "archive/protokoll.pdf",
                            "metadata": {
                                "author": "Haninge Hembygdsgille",
                                "language": "sv",
                                "license": None,
                                "category": None,
                                "tags": ["årsmöte"],
                                "created_at": "2026-03-29T10:30:00+00:00",
                                "modified_at": None,
                                "source": "https://example.test/documents",
                                "attributes": {"source_id": "42"},
                            },
                        },
                    ],
                    "assets": [
                        {
                            "title": "Fotografi",
                            "url": "https://example.test/photo.jpg",
                            "filename": "photo.jpg",
                            "mime_type": "image/jpeg",
                            "size_bytes": None,
                            "checksum": None,
                            "local_path": None,
                            "metadata": _empty_metadata(),
                        },
                    ],
                },
            ],
        },
    }
    assert "Årsmöte" in destination.read_text(encoding="utf-8")
    assert list(destination.parent.iterdir()) == [destination]


def test_exporter_reports_destination_errors(tmp_path: Path) -> None:
    destination = tmp_path / "archive.json"
    destination.mkdir()

    with pytest.raises(JsonExportError, match="could not write JSON"):
        JsonSiteExporter().export(
            site=Site(name="Example", base_url="https://example.test"),
            destination=destination,
        )

    assert not list(tmp_path.glob(".archive.json.*.tmp"))


def _empty_metadata() -> dict[str, object]:
    return {
        "author": None,
        "language": None,
        "license": None,
        "category": None,
        "tags": [],
        "created_at": None,
        "modified_at": None,
        "source": None,
        "attributes": {},
    }
