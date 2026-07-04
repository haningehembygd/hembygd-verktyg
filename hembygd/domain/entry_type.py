"""Supported entry classifications."""

from enum import StrEnum


class EntryType(StrEnum):
    """Classify the kind of information represented by an entry."""

    MEETING = "meeting"
    EVENT = "event"
    NEWS = "news"
    PUBLICATION = "publication"
    ARTICLE = "article"
    PAGE = "page"
    OTHER = "other"
