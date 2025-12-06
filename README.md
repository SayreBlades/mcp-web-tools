# MCP Web Tools

A Model Context Protocol (MCP) server that provides web search and fetch capabilities for AI assistants like Claude Code.

This is useful when you want your code-generation tool to make web requests directly from your machine, rather than having those requests proxied through an external server you don't control. The MCP server runs locally on your host, so all web requests originate from your own network.

## Features

- **web_search** - Search the web using DuckDuckGo
  - Returns formatted results with titles, URLs, and snippets
  - Configurable result count and region

- **web_fetch** - Fetch and extract content from web pages
  - Automatic HTML-to-text conversion (removes scripts, styles, navigation)
  - JSON response formatting
  - Configurable timeout

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd mcp-web-tools

# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

## Usage

### Running the Server Directly

```bash
# With uv
uv run mcp-web-tools

# Or if installed with pip
mcp-web-tools
```

### Registering with Claude Code

Add the server to your Claude Code MCP configuration. Create or edit `.mcp.json` in your project directory:

```json
{
  "mcpServers": {
    "web-tools": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/mcp-web-tools",
        "mcp-web-tools"
      ]
    }
  }
}
```

Or for a global installation, edit `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "web-tools": {
      "command": "mcp-web-tools"
    }
  }
}
```

After adding the configuration, restart Claude Code. The tools will be available as:
- `mcp__web-tools__web_search`
- `mcp__web-tools__web_fetch`

## Tool Reference

### web_search

Search the web using DuckDuckGo.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | Yes | - | The search query |
| max_results | integer | No | 10 | Maximum number of results |
| region | string | No | "wt-wt" | Region for results (e.g., "us-en", "uk-en") |

**Example response:**

```
Search results for: python mcp server

1. Building MCP Servers in Python
   URL: https://example.com/article
   Learn how to build Model Context Protocol servers...

2. MCP Documentation
   URL: https://modelcontextprotocol.io/docs
   Official documentation for the Model Context Protocol...
```

### web_fetch

Fetch the content of a web page.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| url | string | Yes | - | The URL to fetch |
| timeout | integer | No | 30 | Request timeout in seconds |

**Example response:**

```
Content from https://example.com/article:

Building MCP Servers
This guide covers the basics of creating an MCP server...
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run a specific test file
uv run pytest tests/test_tools.py
```

### Project Structure

```
mcp-web-tools/
  src/
    mcp_web_tools/
      __init__.py       # Package metadata
      server.py         # MCP server implementation
      tools.py          # Tool implementations (search, fetch)
  tests/
    test_tools.py       # Unit tests
  pyproject.toml        # Project configuration
  .mcp.json             # Local MCP registration example
```

## Dependencies

- [mcp](https://pypi.org/project/mcp/) - Model Context Protocol SDK
- [ddgs](https://pypi.org/project/ddgs/) - DuckDuckGo Search API
- [httpx](https://pypi.org/project/httpx/) - Async HTTP client
- [lxml](https://pypi.org/project/lxml/) - HTML parsing (optional; falls back to regex-based extraction if not installed)

## License

MIT
