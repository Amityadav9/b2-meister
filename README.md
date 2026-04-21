# b2-meister

Personal German B2 study companion. Upload a grammar reference + workbook PDF, and get page-scoped practice, tests, answer keys, and explanations — all grounded in exactly what your class is covering.

![mode: Practice / Test / HW Check / Lösungen / Erklären](https://img.shields.io/badge/modes-5-blue)

## What it does

Five modes, all scoped to whatever page of whichever PDF you've selected in the sidebar:

| Mode | Purpose |
|---|---|
| 📝 **Practice** | Agent generates 3–5 exercises from the page → you answer → graded ✅/❌ with German + English explanation |
| 🧪 **Test** | Fresh questions on the same topic, different examples (not copied from the book) |
| ✅ **HW Check** | You type the answers you wrote on paper → agent compares to the book's expected answers |
| 🔑 **Lösungen** | Clean answer key for every exercise on the current page |
| 📖 **Erklären** | Summarize the rule on this page + 3 fresh examples, DE + EN gloss |

Memory is on by default (`update_memory_on_run=True`) — the agent remembers your patterns across sessions.

## Stack

- **UI:** [Streamlit](https://streamlit.io/)
- **Agent framework:** [Agno](https://docs.agno.com/) 2.x (Knowledge + Memory + Agent)
- **LLM:** [Groq](https://console.groq.com/) — Llama 4 Scout by default, Qwen3-32B and GPT-OSS-120B also selectable. Ollama local models as offline fallback.
- **Embeddings:** Ollama `nomic-embed-text-v2-moe` (multilingual, local)
- **Vector DB:** Postgres + pgvector (Docker)
- **PDF rendering:** pymupdf
- **Dep manager:** [uv](https://docs.astral.sh/uv/)

## Setup

```bash
# 1. Clone
git clone https://github.com/Amityadav9/b2-meister.git
cd b2-meister

# 2. Config
cp .env.example .env
# then open .env and paste your Groq API key

# 3. Start Postgres
docker compose up -d

# 4. Pull the embedding model
ollama pull nomic-embed-text-v2-moe

# 5. Drop your PDFs into pdfs/
#    (grammar reference + workbook; any filenames)

# 6. Install deps + ingest
uv sync
uv run python -m ingestion.embed

# 7. Run
uv run streamlit run app/main.py
```

Open http://localhost:8501.

## Project layout

```
b2-meister/
├── app/
│   ├── main.py          # Streamlit UI
│   ├── agent.py         # Agno agent factory + per-mode instructions
│   └── models.py        # Groq + Ollama model registry
├── ingestion/
│   ├── knowledge.py     # Agno Knowledge / PgVector / OllamaEmbedder
│   ├── embed.py         # one-shot: loads all PDFs in pdfs/
│   └── extract.py       # render pages as PNG + extract page text
├── pdfs/                # your PDFs (gitignored)
├── docker-compose.yml   # pgvector on :5433
└── pyproject.toml
```

## Configuration

Set via `.env`:

| Variable | Default | Notes |
|---|---|---|
| `GROQ_API_KEY` | *(required)* | https://console.groq.com/keys |
| `DATABASE_URL` | `postgresql+psycopg://b2meister:b2meister@localhost:5433/b2meister` | Matches docker-compose |
| `OLLAMA_HOST` | `http://localhost:11434` | Where Ollama is reachable |
| `EMBED_MODEL` | `nomic-embed-text-v2-moe` | Multilingual, 768-dim |
| `DEFAULT_MODEL` | `groq:meta-llama/llama-4-scout-17b-16e-instruct` | Prefix `groq:` or `ollama:` |

## Notes

- The app injects the **actual page text** into the prompt so the agent can't invent content from other pages. RAG search is off — deterministic page scoping.
- `max_results=5` on Knowledge keeps context under Qwen3's 6K TPM cap.
- PDFs are gitignored (copyright). Bring your own.

## License

Personal project — no license yet.
