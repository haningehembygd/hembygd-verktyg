from datetime import date
from pathlib import Path

import pytest

from hembygd.domain import EntryType
from hembygd.infrastructure.parsers import HembygdParseError, HembygdParser

FIXTURE_PATH = Path(__file__).parents[2] / "fixtures" / "hembygd_documents.html"
SOURCE_URL = "https://www.hembygd.se/haninge-hembygdsgille/foreningsdokument"


@pytest.fixture
def parsed_site():
    html = FIXTURE_PATH.read_text(encoding="utf-8")
    return HembygdParser().parse(
        html=html,
        source_url=SOURCE_URL,
        site_name="Haninge Hembygdsgille",
    )


def test_parser_reads_site_metadata(parsed_site) -> None:
    assert parsed_site.name == "Haninge Hembygdsgille"
    assert parsed_site.base_url == SOURCE_URL
    assert parsed_site.language == "sv"
    assert parsed_site.metadata.author == "Haninge Hembygdsgille"


def test_parser_creates_publication_and_meeting_entries(parsed_site) -> None:
    assert [entry.entry_type for entry in parsed_site.entries] == [
        EntryType.PUBLICATION,
        EntryType.MEETING,
        EntryType.MEETING,
        EntryType.MEETING,
    ]
    assert parsed_site.entries[0].title == "Föreningens stadgar"


def test_parser_reads_full_and_year_only_meeting_dates(parsed_site) -> None:
    assert parsed_site.entries[1].date == date(2026, 3, 29)
    assert parsed_site.entries[2].date == date(2022, 4, 24)
    assert parsed_site.entries[3].date is None
    assert parsed_site.entries[3].metadata.attributes == (("meeting_year", "2013"),)


def test_parser_creates_documents_and_normalizes_values(parsed_site) -> None:
    meeting = parsed_site.entries[1]

    assert len(meeting.documents) == 2
    assert meeting.documents[0].url == "https://www.hembygd.se/documents/dagordning.pdf"
    assert meeting.documents[0].mime_type == "application/pdf"
    assert meeting.documents[1].title == "Protokoll"
    assert meeting.documents[1].filename == "protokoll 2026.pdf"


def test_parser_ignores_links_outside_page_content(parsed_site) -> None:
    titles = [document.title for entry in parsed_site.entries for document in entry.documents]

    assert "Lyssna" not in titles
    assert "Kontakta oss" not in titles


def test_parser_rejects_page_without_content_container() -> None:
    with pytest.raises(HembygdParseError, match="#read_page"):
        HembygdParser().parse(
            html="<html><body></body></html>",
            source_url=SOURCE_URL,
            site_name="Haninge Hembygdsgille",
        )


def test_parser_rejects_content_without_document_entries() -> None:
    with pytest.raises(HembygdParseError, match="does not contain any document entries"):
        HembygdParser().parse(
            html='<html><body><div id="read_page"><p>Inga dokument</p></div></body></html>',
            source_url=SOURCE_URL,
            site_name="Haninge Hembygdsgille",
        )
