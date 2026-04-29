## AI‑Powered Restaurant Recommendation System (Zomato‑Inspired)

### Background
Build an AI-powered restaurant recommendation service inspired by Zomato. The system should suggest restaurants based on user preferences by combining a **real restaurant dataset** (structured data) with a **Large Language Model (LLM)** (natural-language ranking + explanations).

### Objective
Design and implement an application that:
- Collects user preferences (location, budget, cuisine, minimum rating, and optional extra preferences)
- Retrieves relevant restaurants from a real-world dataset
- Uses an LLM to generate **personalized, human-like recommendations** grounded in the filtered dataset
- Presents results clearly to the user

### Data Source
- **Dataset**: Hugging Face `ManikaSaini/zomato-restaurant-recommendation`
- **Link**: `https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation`

### Scope (v1 / Milestone 1)
- **In scope**
  - Load and preprocess the dataset (basic cleaning + normalization)
  - Collect user preferences via a basic web UI (primary) and/or CLI (optional for diagnostics)
  - Filter candidates deterministically using the preferences
  - Prompt an LLM with the candidate list and preferences to rank and explain recommendations
  - Display top recommendations with key fields and an AI-generated explanation

- **Out of scope (explicit non-goals)**
  - User accounts / saved favorites / personalization over time
  - Live Zomato API integration
  - Maps, routing, or real-time availability
  - Payments, ordering, or delivery workflows

## Functional Requirements (Workflow)

### 1) Data ingestion
The system must:
- Load the dataset from Hugging Face
- Extract/derive the fields needed for recommendations (at minimum: **restaurant name, location, cuisine, cost/budget, rating**)
- Normalize types and handle missing values (e.g., rating as number, cuisines as list, cost as numeric or band)

### 2) User input
The system must collect:
- **Location** (e.g., Delhi, Bangalore)
- **Budget** (low / medium / high)
- **Cuisine** (e.g., Italian, Chinese; support multiple if available)
- **Minimum rating**
- **Additional preferences (optional)** (free text; e.g., “family-friendly”, “quick service”)

### 3) Integration layer (retrieval + prompt preparation)
The system must:
- Apply deterministic filters based on user input (location, min rating, budget, cuisine overlap)
- Cap the candidate set to a reasonable \(N\) for LLM context (example: 15–50)
- Create a prompt payload that includes:
  - The user preferences (structured)
  - The candidate list (structured; markdown table or JSON)
  - Instructions to **only recommend from the provided candidates**
  - A strict output format for easy parsing

### 4) Recommendation engine (LLM)
The system must use an LLM to:
- Rank the candidates (top \(k\))
- Provide short explanations describing why each recommendation matches the preferences
- Optionally summarize the overall choice set

**Grounding constraint**: The LLM must only recommend restaurants included in the provided candidate list.

### 5) Output display
The system must present recommendations in a user-friendly format, showing for each result:
- Restaurant name
- Cuisine(s)
- Rating
- Estimated cost / budget band
- AI-generated explanation

## Non-Functional Requirements (Minimum)
- **Reliability**: if the LLM fails, the system should degrade gracefully (e.g., show deterministic top \(k\) with templated explanations).
- **Security**: API keys must come from environment variables (e.g., `.env`) and must not be committed.
- **Latency/cost awareness**: limit candidate count and control model parameters (timeout, max tokens).
- **Reproducibility**: pin dataset revision if practical; document the dataset → internal field mapping.

## Phase‑Wise Architecture (Implementation Plan)
This phase breakdown maps directly to the workflow above: ingestion → preferences → filtering/prompting → LLM ranking → presentation.

### Phase 0 — Scope and foundations
- **Outcome**
  - Decide stack and local run path
  - Define dataset field contract and v1 features
  - Establish secrets handling and basic repo documentation
- **Exit criteria**
  - Written assumptions (stack, v1 UI, supported preference fields)
  - Project runs locally end-to-end once later phases exist
- **Suggested artifacts**
  - `phase0-scope.md`, `dataset-contract.md`, `README.md`, `.env.example`

### Phase 1 — Data ingestion and canonical model
- **Outcome**
  - Load dataset, normalize fields, and expose a canonical `Restaurant` model
- **Exit criteria**
  - A module that loads restaurants into a typed structure/table
  - Parsing/normalization covered by a few unit tests and a smoke run

### Phase 2 — User preferences and validation
- **Outcome**
  - Define a `UserPreferences` model and validation rules
- **Exit criteria**
  - Preferences can be read from UI/CLI into a single object
  - Validation errors are clearly reported to the user

### Phase 3 — Integration layer (filtering + prompt assembly)
- **Outcome**
  - Deterministic filtering to produce a stable candidate set and prompt payload
- **Exit criteria**
  - Tests cover edge cases (no matches, too many matches, missing fields)
  - Produces `candidates[]` and `prompt_payload` without calling the LLM

### Phase 4 — Recommendation engine (LLM)
- **Outcome**
  - LLM call that returns ranked results with explanations in a strict format (prefer JSON)
- **Exit criteria**
  - Parsed/validated structured output
  - Retries/fallback behavior implemented for failures

### Phase 5 — Output and experience
- **Outcome**
  - UI displays results with good empty/error states
- **Exit criteria**
  - Demo flow from user input → recommendations in one run

### Phase 6 — Hardening and handoff (optional)
- Add automated tests for prompt/output parsing with fixtures
- Document cost/latency considerations and candidate cap strategy

## Traceability (Workflow → Phase)
- **Data ingestion** → Phase 1  
- **User input** → Phase 2  
- **Integration layer** → Phase 3  
- **Recommendation engine** → Phase 4  
- **Output display** → Phase 5  
