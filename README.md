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
- [uv](https://github.com/astral-sh/uv)

## Installation

### Quick Install (Recommended)

```bash
# Clone the repository
git clone <repo-url>
cd mcp-web-tools

# Install globally and configure Claude Code
make install
```

This will:
1. Install `mcp-web-tools` as a global executable via `uv tool install`
2. Update `~/.claude/mcp.json` with the MCP server configuration
3. The executable will be available at `~/.local/bin/mcp-web-tools`

Restart Claude Code after installation.

### Manual Installation

```bash
# Install dependencies
uv sync

# Run directly from project
uv run mcp-web-tools
```

## Makefile Targets

| Target | Description |
|--------|-------------|
| `make install` | Install globally and configure Claude Code |
| `make uninstall` | Remove the global installation |
| `make test` | Run tests with pytest |
| `make clean` | Remove build artifacts |

## Claude Code Configuration

After running `make install`, your `~/.claude/mcp.json` will contain:

```json
{
  "mcpServers": {
    "web-tools": {
      "command": "mcp-web-tools"
    }
  }
}
```

The tools will be available in Claude Code as:
- `mcp__web-tools__web_search`
- `mcp__web-tools__web_fetch`

### Alternative: Project-Local Configuration

If you prefer to run from the project directory, create `.mcp.json` in your project:

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
make test

# Or directly
uv run pytest -v
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
  Makefile              # Install/uninstall automation
```

## Dependencies

- [mcp](https://pypi.org/project/mcp/) - Model Context Protocol SDK
- [ddgs](https://pypi.org/project/ddgs/) - DuckDuckGo Search API
- [httpx](https://pypi.org/project/httpx/) - Async HTTP client
- [lxml](https://pypi.org/project/lxml/) - HTML parsing (optional; falls back to regex-based extraction if not installed)

## License

MIT
