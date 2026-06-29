# Mitig8

MCP server: answers "what breaks if I upgrade this dependency, and what do I change" — grounded in changelogs with citations.

## Stack
FastMCP over stdio. Chroma (dense) + rank_bm25 (lexical) + RRF fusion. Generation behind a swappable provider interface.

## Layout
- `server.py` — FastMCP instance, all tools decorated with `@mcp.tool()`
- `data/raw/*.json` — GitHub Releases per package (tag_name, published_at, body, html_url)
- `data/processed/` — chunked + cleaned output (lands Day 3)

## Run
```bash
.venv\Scripts\activate
python server.py
```

## Conventions
- Clarity over cleverness. No abstractions beyond the current phase.
- packaging.Version for all version comparisons. Never string compare.
- PyPI only. Never commit .env or embed API keys.

## Gotchas
- New tools need a permission entry in `.claude/settings.local.json`: `mcp__mitig8__<tool_name>`
- starlette + uvicorn are pulled in by the SDK but unused on the stdio path — ignore them.

## References
@PLAN.md — roadmap, read on demand
@notebook.ipynb — RAG course pipeline, map not copy-source