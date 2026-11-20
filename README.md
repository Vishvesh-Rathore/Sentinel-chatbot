# Sentinel

Sentinel is a local retrieval-augmented generation (RAG) chatbot for answering
questions from a company's documents. It is being built in small, reviewable
steps; this initial version contains the project foundation only.

## Privacy and scope

- Document processing and model inference are intended to run locally.
- Ollama is the planned local LLM runtime; embeddings use a local
  sentence-transformers model.
- The only planned network access is to a local Ollama instance and to web pages
  explicitly configured as ingestion sources.
- Do not add company documents, logs, model files, or credentials to Git.
- This repository currently provides configuration, interfaces, schemas, and
  tests. Ingestion, indexing, retrieval, generation, and user interfaces are
  added in later project steps.

## Requirements

- Python 3.11 or newer
- Git
- Ollama (needed once local LLM generation is implemented)

Install the Python dependencies in a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configuration

Project defaults and tunable settings are in [`configs/sentinel.yaml`](configs/sentinel.yaml).
Load the YAML configuration from Python:

```python
from sentinel.config import load_config

config = load_config("configs/sentinel.yaml")
print(config["retrieval"]["top_k"])
```

## Run tests

```powershell
python -m pytest
```

## Development status

Only Step 0 (project foundation) is implemented. No document ingestion,
embedding, vector search, answering endpoint, or UI is available yet. See
[`.github/copilot-instructions.md`](.github/copilot-instructions.md) for the
approved Phase 1 architecture and staged implementation plan.
