"""Entry domain object."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from hembygd.domain._validation import require_text, validate_optional_text
from hembygd.domain.asset import Asset
from hembygd.domain.document import Document
from hembygd.domain.entry_type import EntryType
from hembygd.domain.metadata import Metadata


@dataclass(frozen=True, slots=True, kw_only=True)
class Entry:
    """A published information item from a site."""

    title: str
    entry_type: EntryType
    description: str | None = None
    date: date | None = None
    category: str | None = None
    documents: tuple[Document, ...] = ()
    assets: tuple[Asset, ...] = ()
    metadata: Metadata = field(default_factory=Metadata)

    def __post_init__(self) -> None:
        """Normalize collections and validate the entry's basic invariants."""
        object.__setattr__(self, "documents", tuple(self.documents))
        object.__setattr__(self, "assets", tuple(self.assets))

        require_text(self.title, "title")
        validate_optional_text(self.description, "description")
        validate_optional_text(self.category, "category")
