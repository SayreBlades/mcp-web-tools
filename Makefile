.PHONY: install uninstall test clean

PREFIX ?= $(HOME)/.local
BINDIR = $(PREFIX)/bin
SCRIPT = mcp-web-tools

install:
	@echo "Installing $(SCRIPT) to $(BINDIR)..."
	@mkdir -p $(BINDIR)
	@uv tool install --force --quiet .
	@echo "Updating Claude global MCP configuration..."
	@mkdir -p $(HOME)/.claude
	@echo '{"mcpServers":{"web-tools":{"command":"$(SCRIPT)"}}}' | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin), indent=2))" > $(HOME)/.claude/mcp.json
	@echo "Done. Restart Claude Code to use the new MCP server."

uninstall:
	@echo "Uninstalling $(SCRIPT)..."
	@uv tool uninstall mcp-web-tool 2>/dev/null || true
	@echo "Note: Claude MCP config at ~/.claude/mcp.json left unchanged."
	@echo "Done."

test:
	uv run pytest -v

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
