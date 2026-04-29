## Milestone 1 — AI‑Powered Restaurant Recommendation System

This repository contains **Milestone 1** of an AI-powered restaurant recommendation system inspired by Zomato. The system combines:
- **Structured restaurant data** (from a Hugging Face dataset), and
- A **Large Language Model (LLM)** to produce grounded, human-like recommendations.

See:
- `docs/problemstatement.md` (problem statement + requirements)
- `docs/phased-architecture.md` (phase-wise architecture)
- `docs/edge-cases.md` (edge cases + test checklist)

---

## Phase 0 (implemented)
Phase 0 establishes scope, stack assumptions, and the dataset contract:
- `docs/phase0-scope.md`
- `docs/dataset-contract.md`
- `.env.example`

---

## Stack assumptions (v1)
These are the default choices for Milestone 1 implementation (can be revised later if needed):
- **Language**: Python 3.11+
- **UI**: Streamlit (simple web UI for collecting preferences and showing results)
- **Dataset**: Hugging Face `datasets` library
- **LLM provider**: OpenAI-compatible API (provider-agnostic as long as it supports chat completions)

---

## Local setup (Phase 0)
There is no runnable app yet in Phase 0. This section prepares your environment for later phases.

### 1) Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# PowerShell
.\.venv\Scripts\Activate.ps1
```

### 2) Configure environment variables
- Copy `.env.example` → `.env`
- Fill in your LLM API key and (optionally) model/base URL

> Important: never commit `.env` with real keys.

---

## Next steps
- Implement Phase 1 (dataset ingestion + canonical `Restaurant` model)
- Implement Phase 2 (validated `UserPreferences`)
- Implement Phase 3–5 (filtering/prompting → LLM → UI)

---

## Phase 1 smoke test (dataset ingestion)
After installing dependencies, you can verify Hugging Face loading + normalization:

```bash
# PowerShell
$env:PYTHONPATH="src"
python -m milestone1.ingestion.smoke --limit 3
```

Optional: print the loaded rows as JSON:

```bash
$env:PYTHONPATH="src"
python -m milestone1.ingestion.smoke --limit 3 --json
```

