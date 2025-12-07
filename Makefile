.PHONY: install uninstall test clean

PREFIX ?= $(HOME)/.local
BINDIR = $(PREFIX)/bin
SCRIPT = mcp-web-tools

install:
	@echo "Installing $(SCRIPT) to $(BINDIR)..."
	@mkdir -p $(BINDIR)
	@uv tool install --force --quiet .
	@echo "Registering MCP server with Claude Code..."
	@claude mcp add --scope user web-tools $(SCRIPT)
	@echo "Done. Restart Claude Code to use the new MCP server."

uninstall:
	@echo "Uninstalling $(SCRIPT)..."
	@uv tool uninstall mcp-web-tools 2>/dev/null || true
	@claude mcp remove --scope user web-tools 2>/dev/null || true
	@echo "Done."

test:
	uv run pytest -v

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
