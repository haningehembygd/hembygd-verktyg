"""Site domain object."""

from dataclasses import dataclass, field

from hembygd.domain._validation import require_text, validate_optional_text
from hembygd.domain.entry import Entry
from hembygd.domain.metadata import Metadata


@dataclass(frozen=True, slots=True, kw_only=True)
class Site:
    """An information source containing published entries."""

    name: str
    base_url: str
    language: str | None = None
    description: str | None = None
    metadata: Metadata = field(default_factory=Metadata)
    entries: tuple[Entry, ...] = ()

    def __post_init__(self) -> None:
        """Normalize collections and validate the site's basic invariants."""
        object.__setattr__(self, "entries", tuple(self.entries))

        require_text(self.name, "name")
        require_text(self.base_url, "base_url")
        validate_optional_text(self.language, "language")
        validate_optional_text(self.description, "description")
