# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**mitig8** is a Python-based MCP (Model Context Protocol) server built with FastMCP. It exposes Python functions as callable tools to Claude and other MCP-compatible clients.

## Environment Setup

```bash
# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
python server.py
```

## Architecture

The entire server is defined in `server.py`. The pattern is:

1. Create a `FastMCP` instance with the server name
2. Decorate Python functions with `@mcp.tool()` to expose them as MCP tools
3. Call `mcp.run()` to start the server over stdio (the transport Claude Code uses)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mitig8")

@mcp.tool()
def my_tool() -> str:
    """Tool description shown to clients"""
    return "result"

if __name__ == "__main__":
    mcp.run()
```

## MCP Integration with Claude Code

The server is registered in `.claude/settings.local.json`. When adding new tools, add the corresponding permission entry:

```json
{
  "permissions": {
    "allow": ["mcp__mitig8__<tool_name>"]
  }
}
```

## Key Dependencies

- `mcp` — FastMCP framework for building MCP servers
- `starlette` + `uvicorn` — pulled in by the SDK; unused on the stdio path (only needed for HTTP transport)
- `pydantic` — data validation for tool inputs/outputs
- `python-dotenv` — environment variable management via `.env`

## Working conventions

- After writing non-trivial code, explain it line by line.
- Prefer clarity over cleverness. No abstractions or features beyond the current phase.
- Ecosystem is PyPI only.
- Never commit `.env` or embed API keys in code.
- RAG reference: `@notebook.ipynb` (course pipeline — a map, not a copy source).

## Current phase

Phase 1 — data sourcing. Fetching changelog data into `data/raw/` via the GitHub Releases API. Two tools planned: `search_changes`, `what_breaks`. Not built yet.
