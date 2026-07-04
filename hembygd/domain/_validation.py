"""Shared validation for domain values."""


def require_text(value: str, field_name: str) -> None:
    """Require a non-empty text value."""
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")


def validate_optional_text(value: str | None, field_name: str) -> None:
    """Reject empty text when an optional value is provided."""
    if value is not None:
        require_text(value, field_name)
