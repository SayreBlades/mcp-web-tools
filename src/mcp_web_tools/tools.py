"""Web tools implementations - core logic separated for testability."""

import json
import re
from typing import Any

import httpx
from ddgs import DDGS


async def web_search(
    query: str,
    max_results: int = 10,
    region: str = "wt-wt",
) -> str:
    """Execute a web search using DuckDuckGo.

    Args:
        query: The search query.
        max_results: Maximum number of results to return.
        region: Region for search results (e.g., 'us-en', 'uk-en').

    Returns:
        Formatted search results as a string.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region=region, max_results=max_results))

        if not results:
            return f"No results found for: {query}"

        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result.get('title', 'No title')}\n"
                f"   URL: {result.get('href', 'No URL')}\n"
                f"   {result.get('body', 'No description')}"
            )

        return f"Search results for: {query}\n\n" + "\n\n".join(formatted_results)

    except Exception as e:
        return f"Search error: {e!s}"


async def web_fetch(url: str, timeout: int = 30) -> str:
    """Fetch content from a URL.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        The page content as a string.
    """
    try:
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")

            if "application/json" in content_type:
                try:
                    data = response.json()
                    text = json.dumps(data, indent=2)
                except json.JSONDecodeError:
                    text = response.text
            elif "text/html" in content_type:
                text = extract_text_from_html(response.text)
            else:
                text = response.text

            return f"Content from {url}:\n\n{text}"

    except httpx.TimeoutException:
        return f"Timeout fetching URL: {url}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error {e.response.status_code} for URL: {url}"
    except Exception as e:
        return f"Fetch error: {e!s}"


def extract_text_from_html(html: str) -> str:
    """Extract readable text from HTML content."""
    try:
        from lxml import html as lxml_html
        from lxml.etree import strip_elements

        doc = lxml_html.fromstring(html)
        strip_elements(doc, "script", "style", "nav", "footer", "header", "aside")
        text = doc.text_content()

        lines = []
        for line in text.split("\n"):
            line = line.strip()
            if line:
                lines.append(line)

        return "\n".join(lines)

    except Exception:
        # Fallback: basic tag stripping
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
