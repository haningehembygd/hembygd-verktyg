"""Metadata shared by domain objects."""

from dataclasses import dataclass
from datetime import datetime

from hembygd.domain._validation import validate_optional_text


@dataclass(frozen=True, slots=True, kw_only=True)
class Metadata:
    """Optional descriptive information attached to a domain object."""

    author: str | None = None
    language: str | None = None
    license: str | None = None
    category: str | None = None
    tags: tuple[str, ...] = ()
    created_at: datetime | None = None
    modified_at: datetime | None = None
    source: str | None = None
    attributes: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        """Normalize immutable collections and validate provided text."""
        object.__setattr__(self, "tags", tuple(self.tags))
        object.__setattr__(self, "attributes", tuple(self.attributes))

        for field_name in ("author", "language", "license", "category", "source"):
            validate_optional_text(getattr(self, field_name), field_name)

        for tag in self.tags:
            validate_optional_text(tag, "tag")

        keys: set[str] = set()
        for key, value in self.attributes:
            validate_optional_text(key, "attribute key")
            validate_optional_text(value, "attribute value")
            if key in keys:
                raise ValueError(f"duplicate metadata attribute: {key}")
            keys.add(key)
