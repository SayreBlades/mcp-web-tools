"""Tests for web tools implementations."""

import pytest

from mcp_web_tools.tools import extract_text_from_html, web_fetch, web_search


class TestWebSearch:
    """Tests for web_search function."""

    async def test_returns_formatted_results(self):
        """Search should return formatted results with query header."""
        result = await web_search("python programming", max_results=3)

        assert "Search results for: python programming" in result
        assert "URL:" in result

    async def test_respects_max_results(self):
        """Search should limit results to max_results."""
        result = await web_search("python programming", max_results=3)

        # Count numbered results (1., 2., 3., etc.)
        lines_with_numbers = [l for l in result.split("\n") if l and l[0].isdigit()]
        assert len(lines_with_numbers) <= 3

    async def test_returns_message_for_no_results(self):
        """Search should return a message when no results found."""
        # Using a very unlikely search query
        result = await web_search("xyzzy12345nonexistent98765qwerty")

        # Either no results message or search results (depends on DDG)
        assert "Search results" in result or "No results" in result


class TestWebFetch:
    """Tests for web_fetch function."""

    async def test_returns_page_content(self):
        """Fetch should return page content with URL header."""
        result = await web_fetch("https://httpbin.org/html")

        assert "Content from https://httpbin.org/html" in result
        assert "Herman Melville" in result  # httpbin's test HTML contains this

    async def test_formats_json_responses(self):
        """Fetch should format JSON responses with indentation."""
        result = await web_fetch("https://httpbin.org/json")

        assert "slideshow" in result  # httpbin's test JSON contains this

    async def test_handles_timeout(self):
        """Fetch should return timeout error for slow responses."""
        result = await web_fetch("https://httpbin.org/delay/10", timeout=1)

        assert "Timeout" in result

    async def test_handles_connection_error(self):
        """Fetch should return error for invalid domains."""
        result = await web_fetch("https://this-domain-does-not-exist-12345.com")

        assert "error" in result.lower()

    async def test_handles_http_errors(self):
        """Fetch should return error for HTTP error responses."""
        result = await web_fetch("https://httpbin.org/status/404")

        assert "HTTP error 404" in result


class TestExtractTextFromHtml:
    """Tests for HTML text extraction."""

    def test_extracts_text_content(self):
        """Should extract text from HTML."""
        html = "<html><body><p>Hello World</p></body></html>"
        result = extract_text_from_html(html)

        assert "Hello World" in result

    def test_removes_script_tags(self):
        """Should remove script content."""
        html = "<html><body><script>alert('bad')</script><p>Good</p></body></html>"
        result = extract_text_from_html(html)

        assert "Good" in result
        assert "alert" not in result

    def test_removes_style_tags(self):
        """Should remove style content."""
        html = "<html><body><style>.red{color:red}</style><p>Text</p></body></html>"
        result = extract_text_from_html(html)

        assert "Text" in result
        assert "color" not in result

    def test_handles_empty_html(self):
        """Should handle empty HTML gracefully."""
        result = extract_text_from_html("")

        assert result == "" or result is not None

    def test_collapses_whitespace(self):
        """Should collapse excessive whitespace."""
        html = "<html><body><p>Hello</p>   \n\n\n   <p>World</p></body></html>"
        result = extract_text_from_html(html)

        # Should have reasonable whitespace, not excessive
        assert "\n\n\n" not in result
