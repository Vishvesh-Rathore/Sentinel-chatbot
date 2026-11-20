# Project: Sentinel, a local RAG chatbot (Phase 1 only)

## Context

Sentinel is a chatbot that answers questions from a company's own data (PDFs/Word docs, spreadsheets/database exports, website/FAQ pages, wiki pages such as Notion/Confluence). It must be accurate, cite its sources, and say "I don't know based on the available documents." when it has no evidence. The developer is a B.Tech student building this end to end as their first company project, so code must be simple, readable, well commented and easy to explain and defend.

## Hard constraints

- **Local only:** company data must never leave the machine. No OpenAI/Anthropic/Cohere or any external API for embeddings, LLM, or logging. Use local models only (Ollama for the LLM, a local sentence-transformers model for embeddings).
- **Near-zero budget:** open-source and free tools only.
- **Phase 1 only:** build only what is described here. Do NOT implement hybrid search, reranking, query rewriting, fine-tuning, a rules router, or human handoff. If you have an idea for those, add a line to `FUTURE_IDEAS.md` instead of building it.
- **Python 3.11+**, type hints, docstrings, short comments explaining *why*.
- Never commit data, logs, models or secrets. Keep `data/`, `logs/`, `.env` in `.gitignore`.

## Tech stack (defaults; all selectable in config)

- LLM runtime: Ollama (default model `qwen2.5:7b-instruct`; fall back to a smaller model such as `qwen2.5:3b-instruct` if hardware is weak)
- Embeddings: sentence-transformers, default `BAAI/bge-m3` (fallback `BAAI/bge-small-en-v1.5`)
- Vector DB: Qdrant in local mode (on-disk path, no server required)
- Parsing: pypdf, python-docx, pandas (spreadsheets/CSV), requests + BeautifulSoup (web)
- API: FastAPI. UI: Streamlit. Logs: SQLite. Config: YAML. Tests: pytest.

## Architecture (follow exactly)

Offline ingestion: Sources -> Loaders -> Cleaner -> Chunker -> Embedder -> Vector store.
Online query: Question -> embed -> Retriever (top-k + score threshold) -> if no evidence: return the refusal text; else Prompt builder -> Local LLM -> Answer validator (citations must map to retrieved chunks) -> Answer + citations -> Logger.

## Project structure

```text
sentinel/
  configs/          sentinel.yaml, prompts/v1.txt
  data/             raw/, processed/        (git-ignored)
  sentinel/
    interfaces.py   abstract base classes
    schemas.py      Document, Chunk, Hit, Answer dataclasses
    ingest/         loaders.py, cleaner.py, chunker.py, pipeline.py
    index/          embedder.py, store.py
    retrieval/      retriever.py
    generation/     prompt.py, llm.py, validator.py
    logging_db/     db.py
    api/            main.py
  app/              streamlit_app.py
  eval/             questions.jsonl, run_eval.py, metrics.py, experiments.md
  tests/
  FUTURE_IDEAS.md, README.md, requirements.txt, .gitignore
```

## Swappable interfaces (in `sentinel/interfaces.py`)

Every component sits behind a simple abstract class, chosen by name in `configs/sentinel.yaml`:

- `Loader.load(source) -> list[Document]`
- `Chunker.split(doc) -> list[Chunk]`
- `Embedder.embed(texts) -> list[list[float]]`
- `VectorStore.upsert(chunks, vectors)` and `.search(vector, k, filters=None) -> list[Hit]`
- `LLM.generate(prompt, **params) -> str`

Provide one implementation of each now. Changing a model or DB must need only a new class and a config change.

## Data schemas

- **Chunk payload:** chunk_id, doc_id, text, source_type, source_name, title, section, page_or_row, url_or_path, last_updated, ingested_at, index_version, access_groups (list; empty = everyone).
- **Interaction log table:** id, timestamp, session_id, question, retrieved (chunk ids + scores), prompt_version, prompt_text, answer, citations, refused (bool), latency_ms, llm_model, embedder_model, index_version, feedback (up/down), feedback_comment. Log EVERY question from day one; these logs become Phase 3 training data.
- **Eval question (JSONL):** qid, question, answerable (bool), expected_answer, source_doc_ids, notes.

## Behaviour rules

1. **Chunking baseline:** about 500 tokens, 50-100 overlap, split on headings/paragraphs. A FAQ pair or a spreadsheet row (with column headers repeated) is its own chunk. All values come from config.
2. **Retrieval:** cosine similarity, top-k (default 5), minimum score threshold from config. If the best score is below the threshold, do not call the LLM; return the refusal text.
3. **Grounding prompt (`configs/prompts/v1.txt`):** answer only from the numbered context; cite as [1], [2]; if the context lacks the answer reply exactly "I don't know based on the available documents."; no outside knowledge; no guessing; quote figures exactly. Low temperature (0.1).
4. **Validator:** every citation number must exist in the retrieved context; if the answer has no valid citation, retry once, then return the refusal text.
5. **Ingestion is idempotent:** re-ingesting a document replaces its old chunks. Record `index_version`.
6. **Privacy:** no network calls in the pipeline except to local Ollama and (for web sources) fetching the pages the user configured. Never log secrets.

## Evaluation (build early, keep fixed)

- `eval/run_eval.py` runs the fixed `questions.jsonl` and reports: retrieval recall@k and MRR (retrieval only), then full-pipeline faithfulness, citation accuracy, refusal accuracy (on unanswerable questions), and latency.
- `eval/experiments.md` is an experiment log table: #, date, ONE change, hypothesis, before -> after scores, keep/revert, notes.
- Change one thing at a time and re-run the eval after each change.

## Working style (important)

- Work **one step at a time**, in the order below. After each step: summarize in this format and then STOP and wait for approval:

1. What was done  2. Why  3. Output (files created, how to run)  4. A one-line explanation I can give my company.
- Do not skip ahead and do not build later steps early.
- When a choice is needed (tool, model, parameter), give a short comparison and a recommendation with the reason, and ask before assuming company-specific details (users, document types, privacy rules, hardware).
- Keep code simple. Prefer clarity over cleverness. Add tests for each module.
- Point out risks (hallucination, privacy, scope creep, cost) when you see them.

## Steps

- **Step 0:** project skeleton, `.gitignore`, `requirements.txt`, config loader, interfaces and schemas, README with run instructions.
- **Step 1:** data audit template (`docs/data_inventory.md`: source, owner, format, size, sensitivity, update frequency) and sample data folder.
- **Step 2:** evaluation set format, a small example `questions.jsonl`, and `run_eval.py` scaffold (metrics code with tests).
- **Step 3:** loaders (PDF, DOCX, spreadsheet/CSV, web/FAQ, wiki export) and cleaner, each with metadata.
- **Step 4:** chunker (baseline) with tests.
- **Step 5:** embedder and Qdrant store, plus the `ingest` command.
- **Step 6:** retriever with threshold; add retrieval evaluation and record the **baseline** in `experiments.md`.
- **Step 7:** prompt builder, Ollama LLM wrapper, validator, and `answer(question)`.
- **Step 8:** SQLite logging and feedback capture.
- **Step 9:** full evaluation run and baseline report with failure analysis.
- **Step 10:** controlled improvement loop (one change at a time, logged).
- **Step 11:** FastAPI endpoint, Streamlit demo, architecture doc, runbook, known limits.
