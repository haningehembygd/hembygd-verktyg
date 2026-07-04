"""Bounded HTTP page fetching with the Python standard library."""

from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from hembygd.application import FetchedPage

DEFAULT_MAX_BYTES = 10 * 1024 * 1024
DEFAULT_TIMEOUT_SECONDS = 30.0
USER_AGENT = "Hembygd-Verktyg/0.1 (+https://github.com/haningehembygd/hembygd-verktyg)"
_HTML_CONTENT_TYPES = {"text/html", "application/xhtml+xml"}


class PageFetchError(RuntimeError):
    """Raised when an HTML page cannot be fetched safely."""


class UrlLibPageFetcher:
    """Fetch bounded HTML responses over HTTP or HTTPS."""

    def __init__(
        self,
        *,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        max_bytes: int = DEFAULT_MAX_BYTES,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        self._timeout_seconds = timeout_seconds
        self._max_bytes = max_bytes

    def fetch(self, *, url: str) -> FetchedPage:
        """Fetch, validate and decode one HTML page."""
        scheme = urlsplit(url).scheme.casefold()
        if scheme not in {"http", "https"}:
            raise PageFetchError("URL must use http or https")

        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=self._timeout_seconds) as response:
                content_type = response.headers.get_content_type()
                if content_type not in _HTML_CONTENT_TYPES:
                    raise PageFetchError(f"expected HTML but received {content_type}")

                content_length = response.headers.get("Content-Length")
                if content_length is not None and int(content_length) > self._max_bytes:
                    raise PageFetchError(f"response exceeds {self._max_bytes} bytes")

                body = response.read(self._max_bytes + 1)
                if len(body) > self._max_bytes:
                    raise PageFetchError(f"response exceeds {self._max_bytes} bytes")

                charset = response.headers.get_content_charset() or "utf-8"
                final_url = response.geturl()
        except HTTPError as error:
            raise PageFetchError(f"HTTP {error.code} while fetching {url}") from error
        except URLError as error:
            raise PageFetchError(f"could not fetch {url}: {error.reason}") from error
        except TimeoutError as error:
            raise PageFetchError(f"timed out while fetching {url}") from error
        except (UnicodeDecodeError, LookupError) as error:
            raise PageFetchError(f"could not decode HTML from {url}") from error
        except ValueError as error:
            raise PageFetchError(f"invalid HTTP response from {url}: {error}") from error

        try:
            html = body.decode(charset)
        except (UnicodeDecodeError, LookupError) as error:
            raise PageFetchError(f"could not decode HTML from {url}") from error
        return FetchedPage(html=html, final_url=final_url)
