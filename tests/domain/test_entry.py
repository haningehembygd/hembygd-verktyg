from datetime import date

import pytest

from hembygd.domain import Asset, Document, Entry, EntryType, Metadata


def test_entry_stores_related_resources() -> None:
    document = Document(
        title="Protokoll",
        url="https://example.test/protokoll.pdf",
        filename="protokoll.pdf",
    )
    asset = Asset(
        title="Fotografi",
        url="https://example.test/foto.jpg",
        filename="foto.jpg",
    )
    metadata = Metadata(tags=("årsmöte",))
    entry = Entry(
        title="Årsmöte 2026",
        entry_type=EntryType.MEETING,
        description="Föreningens årsmöte",
        date=date(2026, 3, 15),
        category="Möten",
        documents=(document,),
        assets=(asset,),
        metadata=metadata,
    )

    assert entry.entry_type is EntryType.MEETING
    assert entry.documents == (document,)
    assert entry.assets == (asset,)
    assert entry.metadata is metadata


def test_entry_rejects_empty_title() -> None:
    with pytest.raises(ValueError, match="title must not be empty"):
        Entry(title=" ", entry_type=EntryType.OTHER)


def test_entry_type_has_stable_string_values() -> None:
    assert EntryType.MEETING.value == "meeting"
    assert EntryType.PAGE.value == "page"
