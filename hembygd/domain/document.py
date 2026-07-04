"""Document domain object."""

from dataclasses import dataclass, field
from pathlib import Path

from hembygd.domain._validation import require_text, validate_optional_text
from hembygd.domain.metadata import Metadata


@dataclass(frozen=True, slots=True, kw_only=True)
class Document:
    """A document associated with an entry."""

    title: str
    url: str
    filename: str
    mime_type: str | None = None
    size_bytes: int | None = None
    checksum: str | None = None
    local_path: Path | None = None
    metadata: Metadata = field(default_factory=Metadata)

    def __post_init__(self) -> None:
        """Validate the document's basic invariants."""
        require_text(self.title, "title")
        require_text(self.url, "url")
        require_text(self.filename, "filename")
        validate_optional_text(self.mime_type, "mime_type")
        validate_optional_text(self.checksum, "checksum")
        if self.size_bytes is not None and self.size_bytes < 0:
            raise ValueError("size_bytes must not be negative")
