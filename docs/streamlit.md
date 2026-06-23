# Streamlit App — Mutual Fund FAQ Assistant

Single Python app that combines the **UI and RAG backend** (no separate FastAPI or Next.js).

## Run locally

```bash
# From repo root — API keys and corpus paths in .env
pip install -r requirements.txt
cp .env.example .env        # add GROQ_API_KEY
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501).

The FastAPI backend is **not** required — chat calls `rag.generator.answer()` in-process.

## Environment

See `.env.example` for the full list. Key variables:

| Variable | Required | Notes |
|----------|----------|-------|
| `GROQ_API_KEY` | Yes | LLM generation |
| `EMBEDDING_PROVIDER` | Yes | `bge` or `openai` |
| `CHROMA_PERSIST_DIR` | Yes | `./data/chroma` locally |
| `METADATA_DB_PATH` | Yes | `./data/metadata.db` locally |
| `CHAT_HISTORY_PATH` | No | `./data/chat_history.json` — persistent chat sidebar |
| `BGE_KEEP_SINGLE_MODEL` | Recommended | Lower memory on Railway / Streamlit Cloud |

## Features

- Groww-branded header (logo + gradient title + scheme badge)
- Disclaimer banner, welcome screen, "What you can ask" guide
- 3 example question chips, persistent chat history sidebar
- Text input only (voice/mic removed)
- Dark theme (`.streamlit/config.toml` + custom CSS in `streamlit_app.py`)

## Deploy on Streamlit Community Cloud

1. [share.streamlit.io](https://share.streamlit.io) → **Create app** → repo `aayush13022/rag-demo-1`, branch `main`, main file `streamlit_app.py`.
2. **Secrets** (TOML): at least `GROQ_API_KEY = "gsk_..."`.
3. Deploy. Health endpoint: `/_stcore/health`.

> **Stale build:** Reboot the app after pushes if you see `ImportError` for new `stapp/` modules.

> **Memory:** Keep `BGE_KEEP_SINGLE_MODEL=true`. For more RAM, use Railway (see [deployment-plan.md](./deployment-plan.md)).

## Deploy on Railway

See [deployment-plan.md](./deployment-plan.md) for full steps. Start command:

```bash
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

Health check: `/_stcore/health`

## Architecture

```text
Browser → Streamlit (streamlit_app.py)
              → stapp/chat_handler.py  (guardrails)
              → rag/generator.py         (retrieve + LLM)
              → stapp/history.py         (chat persistence)
```

The **Next.js + FastAPI** stack under `ui/` and `api/` is kept for reference but is no longer the default deploy path.
