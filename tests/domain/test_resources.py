from pathlib import Path

import pytest

from hembygd.domain import Asset, Document, Metadata


@pytest.mark.parametrize("resource_type", [Document, Asset])
def test_resource_stores_file_information(resource_type) -> None:
    metadata = Metadata(language="sv")
    resource = resource_type(
        title="Årsmötesprotokoll",
        url="https://example.test/protokoll.pdf",
        filename="protokoll.pdf",
        mime_type="application/pdf",
        size_bytes=128,
        checksum="sha256:abc",
        local_path=Path("archive/protokoll.pdf"),
        metadata=metadata,
    )

    assert resource.title == "Årsmötesprotokoll"
    assert resource.size_bytes == 128
    assert resource.local_path == Path("archive/protokoll.pdf")
    assert resource.metadata is metadata


@pytest.mark.parametrize("resource_type", [Document, Asset])
@pytest.mark.parametrize("field_name", ["title", "url", "filename"])
def test_resource_rejects_empty_required_text(resource_type, field_name: str) -> None:
    values = {
        "title": "Titel",
        "url": "https://example.test/resource",
        "filename": "resource.bin",
    }
    values[field_name] = " "

    with pytest.raises(ValueError, match=f"{field_name} must not be empty"):
        resource_type(**values)


@pytest.mark.parametrize("resource_type", [Document, Asset])
def test_resource_rejects_negative_size(resource_type) -> None:
    with pytest.raises(ValueError, match="size_bytes must not be negative"):
        resource_type(
            title="Titel",
            url="https://example.test/resource",
            filename="resource.bin",
            size_bytes=-1,
        )
