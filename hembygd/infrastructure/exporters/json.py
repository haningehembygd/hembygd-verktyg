"""Versioned JSON export for the domain model."""

import json
import os
from datetime import date, datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from hembygd.domain import Asset, Document, Entry, Metadata, Site

SCHEMA_VERSION = 1


class JsonExportError(RuntimeError):
    """Raised when a JSON export cannot be written safely."""


class JsonSiteExporter:
    """Write a site using the stable JSON export schema."""

    def export(self, *, site: Site, destination: Path) -> None:
        """Atomically write UTF-8 JSON to the destination."""
        temporary_path: Path | None = None
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=destination.parent,
                prefix=f".{destination.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(
                    _site_document(site),
                    temporary_file,
                    ensure_ascii=False,
                    indent=2,
                )
                temporary_file.write("\n")
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
            temporary_path.replace(destination)
        except OSError as error:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise JsonExportError(f"could not write JSON to {destination}: {error}") from error


def _site_document(site: Site) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "site": {
            "name": site.name,
            "base_url": site.base_url,
            "language": site.language,
            "description": site.description,
            "metadata": _metadata(site.metadata),
            "entries": [_entry(entry) for entry in site.entries],
        },
    }


def _entry(entry: Entry) -> dict[str, Any]:
    return {
        "title": entry.title,
        "type": entry.entry_type.value,
        "description": entry.description,
        "date": _isoformat(entry.date),
        "category": entry.category,
        "metadata": _metadata(entry.metadata),
        "documents": [_resource(document) for document in entry.documents],
        "assets": [_resource(asset) for asset in entry.assets],
    }


def _resource(resource: Document | Asset) -> dict[str, Any]:
    return {
        "title": resource.title,
        "url": resource.url,
        "filename": resource.filename,
        "mime_type": resource.mime_type,
        "size_bytes": resource.size_bytes,
        "checksum": resource.checksum,
        "local_path": str(resource.local_path) if resource.local_path is not None else None,
        "metadata": _metadata(resource.metadata),
    }


def _metadata(metadata: Metadata) -> dict[str, Any]:
    return {
        "author": metadata.author,
        "language": metadata.language,
        "license": metadata.license,
        "category": metadata.category,
        "tags": list(metadata.tags),
        "created_at": _isoformat(metadata.created_at),
        "modified_at": _isoformat(metadata.modified_at),
        "source": metadata.source,
        "attributes": dict(metadata.attributes),
    }


def _isoformat(value: date | datetime | None) -> str | None:
    return value.isoformat() if value is not None else None
