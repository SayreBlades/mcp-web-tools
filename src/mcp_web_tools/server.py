"""MCP Server providing web search and fetch tools."""

from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .tools import web_fetch, web_search


def create_server() -> Server:
    """Create and configure the MCP server."""
    server = Server("web-tools")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """Return the list of available tools."""
        return [
            Tool(
                name="web_search",
                description=(
                    "Search the web using DuckDuckGo. Returns a list of search "
                    "results with titles, URLs, and snippets."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query",
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 10)",
                            "default": 10,
                        },
                        "region": {
                            "type": "string",
                            "description": "Region for search results (e.g., 'us-en', 'uk-en')",
                            "default": "wt-wt",
                        },
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="web_fetch",
                description=(
                    "Fetch the content of a web page. Returns the raw text content "
                    "of the page, suitable for reading articles and documentation."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to fetch",
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Request timeout in seconds (default: 30)",
                            "default": 30,
                        },
                    },
                    "required": ["url"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Handle tool calls."""
        if name == "web_search":
            result = await web_search(
                query=arguments["query"],
                max_results=arguments.get("max_results", 10),
                region=arguments.get("region", "wt-wt"),
            )
        elif name == "web_fetch":
            result = await web_fetch(
                url=arguments["url"],
                timeout=arguments.get("timeout", 30),
            )
        else:
            result = f"Unknown tool: {name}"

        return [TextContent(type="text", text=result)]

    return server


async def _run_server() -> None:
    """Run the MCP server (async entry point)."""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """Run the MCP server (sync entry point for console script)."""
    import asyncio

    asyncio.run(_run_server())


if __name__ == "__main__":
    main()
