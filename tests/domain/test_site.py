import pytest

from hembygd.domain import Entry, EntryType, Metadata, Site


def test_site_stores_entries_and_metadata() -> None:
    entry = Entry(title="Nyhet", entry_type=EntryType.NEWS)
    metadata = Metadata(language="sv")
    site = Site(
        name="Exempel",
        base_url="https://example.test",
        language="sv",
        entries=(entry,),
        metadata=metadata,
    )

    assert site.entries == (entry,)
    assert site.metadata is metadata


@pytest.mark.parametrize("field_name", ["name", "base_url"])
def test_site_rejects_empty_required_text(field_name: str) -> None:
    values = {"name": "Exempel", "base_url": "https://example.test"}
    values[field_name] = " "

    with pytest.raises(ValueError, match=f"{field_name} must not be empty"):
        Site(**values)
