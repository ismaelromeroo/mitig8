# mitig8

An MCP server that answers *"what breaks if I upgrade this dependency, and what do I change?"* — grounded in real changelogs, classified by change type, and cited back to the source release.

## Tools

| Tool | Description |
|---|---|
| `search_changes` | Returns relevant changelog chunks between two versions |
| `what_breaks` | Returns a cited, classified migration report |

## Install

```bash
claude mcp add mitig8 -- python /path/to/server.py
```

## Status

Work in progress — Phase 1 (data sourcing) underway.
