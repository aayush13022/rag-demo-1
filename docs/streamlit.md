# Streamlit App — Mutual Fund FAQ Assistant

Single Python app that combines the **UI and RAG backend** (no separate FastAPI or Next.js).

## Run locally

```bash
# From repo root — API keys and corpus paths in .env
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501).

Ensure the FastAPI backend is **not** required — chat calls `rag.generator.answer()` in-process.

## Environment

Same as the FastAPI backend (see `.env.example`):

| Variable | Required | Notes |
|----------|----------|-------|
| `GROQ_API_KEY` | Yes | LLM generation |
| `EMBEDDING_PROVIDER` | Yes | `bge` or `openai` |
| `CHROMA_PERSIST_DIR` | Yes | `./data/chroma` locally |
| `METADATA_DB_PATH` | Yes | `./data/metadata.db` locally |

## Deploy on Railway

The repo `Procfile` and `railway.toml` start Streamlit:

```bash
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

Health check: `/_stcore/health`

Use the same Railway env vars as the FastAPI deployment (Groq key, Chroma paths, volume mount at `/data`).

## Architecture

```text
Browser → Streamlit (streamlit_app.py)
              → stapp/chat_handler.py  (guardrails)
              → rag/generator.py         (retrieve + LLM)
```

The old **Next.js + FastAPI** stack under `ui/` and `api/` is kept for reference but is no longer the default deploy path.

## Features

- Disclaimer banner
- Welcome block + 5 supported schemes
- 3 example question buttons
- Chat history with source links and refusal handling
- Dark theme (`.streamlit/config.toml`)
