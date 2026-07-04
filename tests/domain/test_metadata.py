from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from hembygd.domain import Metadata


def test_metadata_defaults_are_empty() -> None:
    assert Metadata() == Metadata(tags=(), attributes=())


def test_metadata_stores_supported_values() -> None:
    created_at = datetime(2026, 7, 4, tzinfo=UTC)
    metadata = Metadata(
        author="Haninge Hembygdsgille",
        language="sv",
        tags=("arkiv", "historia"),
        created_at=created_at,
        attributes=(("source_id", "42"),),
    )

    assert metadata.author == "Haninge Hembygdsgille"
    assert metadata.tags == ("arkiv", "historia")
    assert metadata.created_at == created_at
    assert metadata.attributes == (("source_id", "42"),)


def test_metadata_rejects_duplicate_attribute_keys() -> None:
    with pytest.raises(ValueError, match="duplicate metadata attribute"):
        Metadata(attributes=(("source_id", "42"), ("source_id", "43")))


def test_metadata_rejects_empty_optional_text() -> None:
    with pytest.raises(ValueError, match="author must not be empty"):
        Metadata(author=" ")


def test_metadata_is_immutable() -> None:
    metadata = Metadata(author="Author")

    with pytest.raises(FrozenInstanceError):
        metadata.author = "Another author"  # type: ignore[misc]
