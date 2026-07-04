from email.message import Message
from urllib.error import URLError

import pytest

from hembygd.infrastructure.http import PageFetchError, UrlLibPageFetcher, urllib_fetcher


class FakeResponse:
    def __init__(
        self,
        body: bytes,
        *,
        content_type: str = "text/html",
        charset: str = "utf-8",
        final_url: str = "https://example.test/final",
        content_length: int | None = None,
    ) -> None:
        self._body = body
        self._final_url = final_url
        self.headers = Message()
        self.headers.set_type(content_type)
        self.headers.set_param("charset", charset)
        if content_length is not None:
            self.headers["Content-Length"] = str(content_length)

    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        return None

    def read(self, limit: int) -> bytes:
        return self._body[:limit]

    def geturl(self) -> str:
        return self._final_url


def test_fetcher_returns_decoded_html_and_final_url(monkeypatch) -> None:
    response = FakeResponse("<p>Årsmöte</p>".encode())
    observed_user_agent = None

    def fake_urlopen(request, *, timeout: float):
        nonlocal observed_user_agent
        observed_user_agent = request.get_header("User-agent")
        assert timeout == 5
        return response

    monkeypatch.setattr(urllib_fetcher, "urlopen", fake_urlopen)

    page = UrlLibPageFetcher(timeout_seconds=5).fetch(url="https://example.test/start")

    assert page.html == "<p>Årsmöte</p>"
    assert page.final_url == "https://example.test/final"
    assert observed_user_agent == urllib_fetcher.USER_AGENT


def test_fetcher_rejects_non_http_url() -> None:
    with pytest.raises(PageFetchError, match="http or https"):
        UrlLibPageFetcher().fetch(url="file:///tmp/page.html")


def test_fetcher_rejects_non_html_content(monkeypatch) -> None:
    monkeypatch.setattr(
        urllib_fetcher,
        "urlopen",
        lambda request, timeout: FakeResponse(b"data", content_type="application/pdf"),
    )

    with pytest.raises(PageFetchError, match="expected HTML"):
        UrlLibPageFetcher().fetch(url="https://example.test/file.pdf")


def test_fetcher_rejects_oversized_content_length(monkeypatch) -> None:
    monkeypatch.setattr(
        urllib_fetcher,
        "urlopen",
        lambda request, timeout: FakeResponse(b"", content_length=101),
    )

    with pytest.raises(PageFetchError, match="exceeds 100 bytes"):
        UrlLibPageFetcher(max_bytes=100).fetch(url="https://example.test/page")


def test_fetcher_rejects_oversized_stream(monkeypatch) -> None:
    monkeypatch.setattr(
        urllib_fetcher,
        "urlopen",
        lambda request, timeout: FakeResponse(b"x" * 101),
    )

    with pytest.raises(PageFetchError, match="exceeds 100 bytes"):
        UrlLibPageFetcher(max_bytes=100).fetch(url="https://example.test/page")


def test_fetcher_reports_network_errors(monkeypatch) -> None:
    def failing_urlopen(request, timeout):
        raise URLError("offline")

    monkeypatch.setattr(urllib_fetcher, "urlopen", failing_urlopen)

    with pytest.raises(PageFetchError, match="offline"):
        UrlLibPageFetcher().fetch(url="https://example.test/page")
