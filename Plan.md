# Mitig8 — v1 build plan

> Working name "Mitig8" — rename once you pick (see name options).

**What it is:** an MCP server any coding agent can call to answer *"what breaks if I upgrade this dependency, and what do I change?"* — grounded in the real changelog, classified, and cited back to the source line.

**Success metric:** not user count. Real devs install it + a build-in-public arc + a number you can put on a résumé. Shipping it teaches you end-to-end MCP authoring.

---

## The fence (read this first)

v1 is **exactly** this, and nothing more:

- **One ecosystem**, ~5–8 curated libraries with good changelogs (pick PyPI *or* npm — not both).
- **Two tools:** `search_changes` and `what_breaks`.
- **Hybrid retrieval** (dense + BM25 + RRF) over the changelog corpus.
- **HF zero-shot classification** of each change (breaking / deprecation / feature / fix).
- **Claude generation with the citations API** for the final report.
- **A ~30-case eval** with reported recall/precision + citation faithfulness.
- **Installable via MCP + README + a demo + one LinkedIn post.**

**NOT in v1** (this is the v2 backlog — if you reach for any of these mid-build, that's the refine-don't-ship reflex; stop):

- Auto-parsing the user's lockfile / scanning their whole project
- A full agent loop (read deps → fetch → plan autonomously)
- A second ecosystem
- HF token-classification (code-symbol NER) — Claude handles symbol extraction in v1
- The fancy workflow patterns (routing / parallelization / evaluator-optimizer)
- Any web UI or dashboard

---

## Phases

### Phase 0 — Prove the round-trip (½ day)
Repo + venv. Stand up a Python MCP server with one dummy tool (`ping`). Connect it to Claude Code and call it. **Done when:** Claude Code invokes your tool and gets a response. Build *nothing* else until this works — the whole project rides on this plumbing.

### Phase 1 — Data + retrieval, the RAG core (~week 1)
- Pick 5–8 libraries with clean changelogs/migration guides.
- Fetch their change notes (GitHub Releases API or raw `CHANGELOG.md`), store locally.
- Chunk by version/release section (structure-based chunking).
- Embed with a small HF sentence-transformer → store vectors in Chroma or FAISS (local, no server).
- Implement `search_changes(package, from_version, to_version, query?)` → returns relevant chunks.
- **Closing step:** add BM25 (`rank_bm25`) and fuse with the dense results via reciprocal rank fusion.

**Done when:** you can ask for changes between two versions and get the right chunks back, dense + lexical fused.

### Phase 2 — Classify + the cited report (~week 2)
- HF zero-shot pipeline (e.g. an MNLI model) labels each retrieved change: breaking / deprecation / feature / fix.
- Claude generates `what_breaks(package, from_version, to_version, symbols?)` → a structured JSON report (what breaks, why, suggested fix) **grounded with the citations API** so every "this breaks" links to the exact changelog line.

**Done when:** `what_breaks(<lib>, <old>, <new>)` returns a cited, classified migration report. This is your demoable moment.

### Phase 3 — Eval harness (~3–4 days)
- Hand-build ~30 golden cases: `(package, from, to)` + the *real* breaking changes (verified against the actual migration guide).
- Run each through `what_breaks`. Score: **recall** (did it catch the real breaks?), **precision** (false alarms?), and **citation faithfulness** (does each cited line actually support the claim — LLM-as-judge).
- Iterate prompts against the score. Stop when it's solid, not perfect.

**Done when:** you have numbers you'd put on a résumé.

### Phase 4 — Polish + ship (~2–3 days)
- Add Anthropic prompt caching on the changelog document blocks (cost/latency win — a real "production" talking point).
- README: what it is, install via the standard `claude mcp add` flow, a short demo (GIF/asciinema of Claude Code using it on a real upgrade).
- Publish to GitHub + list on an MCP registry.
- Write the build-in-public LinkedIn post.

**Done when:** installable, documented, posted.

---

## Tech stack (lean, all Python — no web dev)

- Python MCP SDK (server + the two tools)
- Data: GitHub Releases API / raw `CHANGELOG.md` (github.com, api.github.com, raw.githubusercontent.com)
- Embeddings: HF sentence-transformer; vectors in Chroma or FAISS
- Lexical: `rank_bm25`; fuse with RRF
- Classification: HF zero-shot (MNLI model)
- Generation + citations + caching: Anthropic API (Claude)
- Eval: a plain Python harness + a YAML/JSON golden set

---

## Anthropic-course coverage (the learning payoff)

v1 exercises: **MCP server authoring**, **tool use**, **RAG** (structure chunking + embeddings + BM25 + RRF), **structured outputs**, **citations API**, **prompt caching**, and the **eval pipeline** (golden set + LLM-as-judge + iterate). The agent loop and the workflow patterns are the v2 sequel.

---

## Anti-slop rules (yours)

- Don't accept a line of generated code you can't explain. Step through the retrieval + classification pipeline with a debugger — that's the learning, not a chore.
- Changelog formats vary wildly. That's *why* you curate a small set first. Don't try to parse every format on day one.
- Don't rabbit-hole on model selection. Pick a known zero-shot model + a small embedding model, ship, measure, swap later only if the eval tells you to.
- Pick the smallest thing that works, get it end-to-end, then deepen. Phase 0 before anything.
