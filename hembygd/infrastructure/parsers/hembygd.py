"""Parser for document pages on Hembygd.se."""

import mimetypes
import re
from datetime import date
from pathlib import PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit

from bs4 import BeautifulSoup, NavigableString, Tag

from hembygd.domain import Document, Entry, EntryType, Metadata, Site

_MEETING_PATTERN = re.compile(
    r"^Årsmöte(?: den)? "
    r"(?:(?P<day>\d{1,2}) (?P<month>[a-zåäö]+) (?P<year>\d{4})|(?P<year_only>\d{4}))",
    re.IGNORECASE,
)
_SWEDISH_MONTHS = {
    "januari": 1,
    "februari": 2,
    "mars": 3,
    "april": 4,
    "maj": 5,
    "juni": 6,
    "juli": 7,
    "augusti": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "december": 12,
}


class HembygdParseError(ValueError):
    """Raised when a Hembygd.se page cannot be translated safely."""


class HembygdParser:
    """Parse a Hembygd.se document page into domain objects."""

    def parse(self, *, html: str, source_url: str, site_name: str) -> Site:
        """Parse document links grouped by meeting paragraphs."""
        soup = BeautifulSoup(html, "html.parser")
        content = soup.select_one("#read_page")
        if content is None:
            raise HembygdParseError("page does not contain #read_page")

        entries: list[Entry] = []
        for paragraph in content.find_all("p"):
            heading = _text_before_first_break(paragraph)
            links = paragraph.find_all("a", href=True)
            if not links:
                continue

            meeting = _MEETING_PATTERN.match(heading)
            if meeting is not None:
                entries.append(
                    _meeting_entry(
                        heading=heading,
                        meeting=meeting,
                        links=links,
                        source_url=source_url,
                    )
                )
            else:
                entries.extend(_publication_entries(links=links, source_url=source_url))

        if not entries:
            raise HembygdParseError("#read_page does not contain any document entries")

        language = _optional_attribute(soup.html, "lang")
        author = _meta_content(soup, "author")
        return Site(
            name=site_name,
            base_url=source_url,
            language=language,
            metadata=Metadata(author=author, language=language, source=source_url),
            entries=tuple(entries),
        )


def _meeting_entry(
    *,
    heading: str,
    meeting: re.Match[str],
    links: list[Tag],
    source_url: str,
) -> Entry:
    year = meeting.group("year") or meeting.group("year_only")
    if year is None:
        raise HembygdParseError(f"meeting heading has no year: {heading}")
    return Entry(
        title=heading,
        entry_type=EntryType.MEETING,
        date=_meeting_date(meeting),
        category="Årsmöte",
        documents=tuple(_document(link, source_url) for link in links),
        metadata=Metadata(source=source_url, attributes=(("meeting_year", year),)),
    )


def _publication_entries(*, links: list[Tag], source_url: str) -> tuple[Entry, ...]:
    entries = []
    for link in links:
        document = _document(link, source_url)
        entries.append(
            Entry(
                title=document.title,
                entry_type=EntryType.PUBLICATION,
                documents=(document,),
                metadata=Metadata(source=source_url),
            )
        )
    return tuple(entries)


def _document(link: Tag, source_url: str) -> Document:
    title = _normalized_text(link)
    href = link.get("href")
    if not isinstance(href, str) or not href.strip():
        raise HembygdParseError("document link has no URL")
    if not title:
        raise HembygdParseError(f"document link has no title: {href}")

    url = urljoin(source_url, href.strip())
    filename = PurePosixPath(unquote(urlsplit(url).path)).name
    if not filename:
        raise HembygdParseError(f"document URL has no filename: {url}")

    mime_type, _ = mimetypes.guess_type(filename)
    return Document(
        title=title,
        url=url,
        filename=filename,
        mime_type=mime_type,
        metadata=Metadata(source=source_url),
    )


def _meeting_date(meeting: re.Match[str]) -> date | None:
    day = meeting.group("day")
    month_name = meeting.group("month")
    year = meeting.group("year")
    if day is None or month_name is None or year is None:
        return None

    month = _SWEDISH_MONTHS.get(month_name.casefold())
    if month is None:
        raise HembygdParseError(f"unknown Swedish month: {month_name}")
    try:
        return date(int(year), month, int(day))
    except ValueError as error:
        raise HembygdParseError(f"invalid meeting date: {meeting.group(0)}") from error


def _text_before_first_break(paragraph: Tag) -> str:
    parts: list[str] = []
    for descendant in paragraph.descendants:
        if isinstance(descendant, Tag) and descendant.name == "br":
            break
        if isinstance(descendant, NavigableString):
            parts.append(str(descendant))
    return _normalize(" ".join(parts))


def _normalized_text(tag: Tag) -> str:
    return _normalize(tag.get_text(" ", strip=True))


def _normalize(value: str) -> str:
    return " ".join(value.split())


def _meta_content(soup: BeautifulSoup, name: str) -> str | None:
    meta = soup.find("meta", attrs={"name": name})
    return _optional_attribute(meta, "content")


def _optional_attribute(tag: Tag | None, attribute: str) -> str | None:
    if tag is None:
        return None
    value = tag.get(attribute)
    if not isinstance(value, str):
        return None
    normalized = _normalize(value)
    return normalized or None
