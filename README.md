# Mutual Fund RAG FAQ Assistant

A facts-only AI assistant that answers questions about 5 HDFC Mutual Fund schemes using source-backed data from Groww.

The project is built as a Retrieval-Augmented Generation (RAG) app: it retrieves relevant mutual fund facts from a local vector database, sends only grounded context to an LLM, and returns concise answers with source links. It refuses investment advice, predictions, comparisons, and out-of-scope questions.

## What This Project Does

Users can ask factual questions such as:

- What is the expense ratio of HDFC Defence Fund Direct Growth?
- What is the exit load on HDFC Mid Cap Fund Direct Growth?
- Who manages HDFC Large Cap Fund Direct Growth?
- What is the benchmark of HDFC Small Cap Fund Direct Growth?
- What is the minimum SIP amount?

The assistant responds with:

- A short factual answer
- A Groww source link
- A last-updated footer when available
- A facts-only disclaimer

If the user asks for investment advice, predictions, recommendations, or comparisons, the assistant refuses politely and provides an educational AMFI link.

## Supported Mutual Fund Schemes

1. HDFC Mid Cap Fund Direct Growth
2. HDFC Large Cap Fund Direct Growth
3. HDFC Small Cap Fund Direct Growth
4. HDFC Gold ETF Fund of Fund Direct Plan Growth
5. HDFC Defence Fund Direct Growth

## Key Features

- Facts-only RAG assistant for mutual fund FAQs
- Streamlit UI with Groww-inspired branding
- Persistent chat history in the sidebar
- "What you can ask" guide for supported topics
- Example questions that auto-send on click
- Guardrails to block investment advice and unsupported queries
- ChromaDB vector store for semantic retrieval
- BGE embeddings for local embedding generation
- Groq LLM for fast answer generation
- Railway-ready deployment configuration
- Legacy FastAPI + Next.js stack retained for reference

## Tech Stack

| Layer | Technology |
|------|------------|
| App UI | Streamlit |
| RAG Backend | Python |
| Vector Database | ChromaDB |
| Embeddings | BGE (`BAAI/bge-small-en-v1.5`, `BAAI/bge-large-en-v1.5`) |
| LLM | Groq |
| Metadata Store | SQLite |
| Ingestion | Python, httpx, BeautifulSoup |
| Deployment | Railway |
| Legacy UI/API | Next.js + FastAPI |

## Architecture

```text
User Browser
    |
    v
Streamlit App
    |
    v
stapp/chat_handler.py
    |
    |-- Guardrails: refuse advice / prediction / comparison
    |
    v
rag/generator.py
    |
    |-- Scheme-aware retrieval
    |-- Section-aware context selection
    |-- LLM prompt construction
    |
    v
ChromaDB + Groq LLM
    |
    v
Answer + Groww source link + disclaimer
```

The current production path is a single Streamlit app. The browser talks directly to Streamlit, and Streamlit calls the RAG pipeline in-process. This avoids CORS issues and removes the need for a separate frontend/backend deployment.

## Project Structure

```text
.
├── streamlit_app.py             # Main Streamlit app
├── stapp/
│   ├── chat_handler.py          # UI-to-RAG handler and error handling
│   ├── constants.py             # UI copy, examples, supported topics
│   └── history.py               # Persistent chat history
├── rag/
│   ├── generator.py             # RAG answer generation
│   ├── retriever.py             # Semantic retrieval
│   ├── guardrails.py            # Query refusal logic
│   └── prompts.py               # LLM prompt templates
├── ingestion/
│   ├── fetcher.py               # Fetch Groww pages
│   ├── parser.py                # Extract useful content
│   ├── chunker.py               # Create retrieval chunks
│   └── embedder.py              # Embedding providers
├── storage/
│   ├── vector_store.py          # ChromaDB wrapper
│   └── metadata_store.py        # SQLite metadata
├── config/
│   └── corpus.yaml              # Allowlisted funds and settings
├── assets/
│   └── groww-logo.png           # Logo used in the UI
├── docs/                        # Architecture, deployment, implementation docs
├── ui/                          # Legacy Next.js frontend
├── api/                         # Legacy FastAPI backend
├── data/                        # Local corpus, metadata, Chroma index
├── Procfile                     # Railway start command
├── railway.toml                 # Railway deployment config
└── requirements.txt             # Python dependencies
```

## Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Add your Groq API key:

```env
GROQ_API_KEY=gsk_...
```

### 3. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

## Build or Refresh the Corpus

If the local ChromaDB corpus is missing or stale, run:

```bash
python -m scheduler --once
```

This fetches the allowlisted Groww fund pages, parses the content, chunks it, embeds it, and stores it in ChromaDB.

## Deployment

The recommended deployment is a single Streamlit service on Railway.

Railway start command:

```bash
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

Recommended Railway environment variables:

```env
GROQ_API_KEY=...
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant
EMBEDDING_PROVIDER=bge
CHROMA_PERSIST_DIR=/data/chroma
METADATA_DB_PATH=/data/metadata.db
CHAT_HISTORY_PATH=/data/chat_history.json
BGE_KEEP_SINGLE_MODEL=true
TOKENIZERS_PARALLELISM=false
OMP_NUM_THREADS=1
```

Attach a Railway volume at `/data` so the ChromaDB index, metadata database, and chat history survive redeploys.

## Guardrails

The assistant is intentionally scoped to factual mutual fund information only.

It refuses:

- Investment advice
- Buy/sell/hold recommendations
- Return predictions
- Fund comparisons
- Portfolio allocation questions
- Out-of-scope general questions

This helps reduce hallucinations and keeps the project aligned with a compliance-first financial assistant design.

## Example Questions

- What is the expense ratio of HDFC Defence Fund Direct Growth?
- What is the exit load on HDFC Mid Cap Fund Direct Growth?
- Who manages HDFC Large Cap Fund Direct Growth?
- What is the benchmark of HDFC Small Cap Fund Direct Growth?
- What are the tax implications of HDFC Gold ETF Fund of Fund?

## Tests

Run the test suite:

```bash
pytest
```

Streamlit-specific tests:

```bash
pytest tests/test_streamlit.py tests/test_history.py -q
```

## Why I Built This

This project demonstrates an end-to-end RAG system for a real-world financial information use case. It covers ingestion, parsing, chunking, embeddings, vector search, retrieval logic, prompt design, guardrails, UI design, persistent history, and deployment.

The main learning was that building a useful AI assistant is not just about calling an LLM. The important parts are grounding, retrieval quality, clear scope, safe refusals, reliable deployment, and a simple user experience.

## Repository

GitHub: https://github.com/aayush13022/rag-demo-1

## Disclaimer

This assistant provides factual information only. It does not provide investment advice, recommendations, predictions, or financial planning guidance.
