## Phase‑Wise Architecture — AI Restaurant Recommendation (Milestone 1)

### Purpose
This document defines a **phase-wise architecture** for the system described in `docs/problemstatement.md`. Each phase produces concrete artifacts and stable interfaces so later phases can build without rework.

---

## Phase 0 — Scope, stack, and contracts

### Goal
Lock scope, decide the stack, and define the contracts that every later phase depends on.

### Key decisions
- **Runtime/stack**: language, framework, dependency manager, test runner.
- **Secrets**: API keys via environment variables; provide `.env.example`; never commit real keys.
- **Dataset contract**: define the minimum columns supported in v1 and how they map into the canonical model.
- **Input surface (Milestone 1)**: basic web UI is the primary source of user input; CLI is optional for diagnostics.

### Outputs (artifacts)
- `docs/phase0-scope.md`
- `docs/dataset-contract.md`
- `README.md`
- `.env.example`

### Exit criteria
- Documented v1 scope + non-goals
- Documented dataset → canonical field mapping (including missing/unknown handling)
- Clear “how to run locally” instructions (even if later phases are stubbed)

---

## Phase 1 — Data ingestion and canonical restaurant model

### Goal
Load the Hugging Face dataset and normalize it into a stable, queryable internal representation.

### Components
- **Dataset loader**
  - Pulls `ManikaSaini/zomato-restaurant-recommendation` (optionally pinned to a revision)
  - Supports local caching for fast iteration
- **Normalizer**
  - Enforces types: rating → number, cuisines → list of strings, cost → numeric or budget band
  - Handles missing values and deduplication
- **Canonical model**
  - `Restaurant` with at minimum:
    - `id` (stable synthetic key)
    - `name`
    - `location` (city/area; whatever the dataset supports)
    - `cuisines[]`
    - `cost` and/or `budget_band`
    - `rating`
    - `raw` (optional: kept fields for prompting/debug)

### Inputs / outputs
- **Input**: Hugging Face dataset rows
- **Output**: `restaurants[]` (in-memory list/table) + basic dataset stats (row count, missingness)

### Testing
- Parsing tests for a small sample of rows
- Smoke test that loads \(N\) rows successfully

### Exit criteria
- A single importable ingestion entrypoint that returns normalized restaurants
- Basic tests passing and a simple smoke run documented

---

## Phase 2 — User preferences and validation

### Goal
Define a single validated preference object used everywhere: UI, API, CLI.

### Preference model (v1)
- `location` (required)
- `budget_band` (optional; low/medium/high)
- `cuisines[]` (optional)
- `min_rating` (optional; numeric range validated)
- `additional_preferences_text` (optional free text)

### Validation rules
- Required fields present (at minimum: location)
- Rating numeric and within allowed range
- Budget band must be one of the supported values
- Cuisines normalized (case/whitespace)

### Inputs / outputs
- **Input**: user form payload (and/or CLI args)
- **Output**: `UserPreferences` or a list of user-facing validation errors

### Exit criteria
- Preferences can be created from UI input consistently
- Validation errors are clear and user-friendly

---

## Phase 3 — Integration layer (retrieval + prompt assembly)

### Goal
Bridge deterministic retrieval with LLM reasoning: produce a grounded candidate set and a strict prompt payload.

### Components
- **Deterministic filter**
  - Filters by location, min rating, budget, cuisine overlap
  - Produces a **bounded** candidate list \(N\) (e.g., 15–50)
- **Pre-ranking (optional)**
  - Sort by rating or composite score so the LLM sees a sensible ordering
- **Prompt builder**
  - Packages:
    - preferences (structured)
    - candidates (structured table/JSON)
    - strict rules (“only recommend from candidates”)
    - strict output schema (prefer JSON)

### Candidate selection contract
- Input: `restaurants[]`, `UserPreferences`
- Output:
  - `candidates[]` (subset of restaurants with stable `id`s)
  - `prompt_payload` (system/user messages or a single structured prompt)

### Edge cases to handle
- No matches (return empty with helpful message; do not call LLM)
- Too many matches (cap and explain cap in logs/diagnostics)
- Missing fields in dataset rows (exclude or fallback to safe defaults)

### Exit criteria
- Stable candidate generation without calling the LLM
- Tests for filter correctness and edge cases

---

## Phase 4 — Recommendation engine (LLM)

### Goal
Call the LLM with the prompt payload and return structured ranked recommendations grounded in candidates.

### Components
- **LLM client**
  - Reads API key from environment
  - Controls timeout, max tokens, temperature
  - Retries transient failures
- **Output schema + parser**
  - Prefer JSON output:
    - `recommendations`: array of `{ restaurant_id, rank, explanation }`
  - Validate:
    - IDs exist in `candidates[]`
    - Explanations non-empty
    - Ranking unique and within bounds
- **Fallback strategy**
  - If LLM fails: return deterministic top-k + templated explanations

### Inputs / outputs
- Input: `prompt_payload`, `candidates[]`
- Output: ranked `recommendations[]` enriched with display fields

### Exit criteria
- End-to-end call returns valid structured output
- Grounding enforced (no hallucinated restaurants)
- Graceful degradation works

---

## Phase 5 — Frontend Application (Web UI)

### Goal
Provide a clean user journey from preference input to recommendations with proper backend/frontend separation.

### Backend Services (Phases 1-4)
- **Data Layer**: Restaurant ingestion and normalization (Phase 1)
- **Business Logic**: Preference validation, filtering, LLM integration (Phases 2-4)
- **API Layer**: Clean interfaces for frontend consumption

### Frontend Application (Phase 5)
- **UI Components**: Modular component architecture
- **State Management**: Session state and user journey handling
- **Service Integration**: Backend API communication
- **Presentation Layer**: User interface and experience

### UI screens/states (minimum)
- **Input form**
  - Location, budget band, cuisines, min rating, additional preferences
  - Real-time validation and autocomplete
- **Results view**
  - Top \(k\) recommendations with:
    - name, cuisines, rating, cost/budget
    - AI explanation (expandable)
    - Processing statistics
- **Empty/error states**
  - "No restaurants match your filters"
  - "We couldn't generate AI explanations right now; here are the best matches"
  - Graceful fallback handling

### Backend-Frontend API Contracts
- **Restaurant Data API**: `load_restaurants()`, `get_available_locations()`
- **Preferences API**: `validate_preferences()`, `normalize_preferences()`
- **Filtering API**: `filter_candidates()`, `build_prompt_payload()`
- **Recommendation API**: `get_recommendations()`, fallback handling

### Observability (light)
- Log: candidate counts, filter counts, LLM latency, token usage (if available)
- Frontend metrics: processing time, user interactions, error rates
- Avoid logging user free-text beyond what's necessary

### Exit criteria
- Demo path works in one run: input → results
- Output includes all required fields from `problemstatement.md`
- Clean backend/frontend separation with proper API contracts
- Comprehensive error handling and fallback mechanisms

---

## Phase 6 — Hardening (optional, recommended)

### Goal
Make the project robust, testable, and easy to hand off.

### Additions
- Test fixtures for LLM JSON parsing and fallback behavior
- Document performance/cost controls: candidate cap, caching, model choice
- Pin dataset revision and record it in docs/config

### Exit criteria
- Repeatable local run + stable tests
- Clear limitations and future improvements listed

---

## Phase 7 — Frontend (web UI)

### Goal
Build a modern, user-friendly web interface that consumes the Phase 6 hardened backend API, providing a complete restaurant recommendation experience.

### Concern
- **Approach**: Browser-only frontend that talks to Phase 6 API
- **Role**: Primary user-facing surface with preference form + results list, per phase0-scope.md

### Data Flow
- **Browser only talks to Phase 6 API**: Map form fields to API JSON schema (location, budget band, cuisines, minimum rating, optional additional text)
- **UI**: Results show name, cuisines, rating, estimated cost, AI explanation for each row; reuse Phase 5 empty-state semantics ("no filter match" vs "model returned no grounded picks") with clear, distinct copy

### UX Requirements
- **Loading states**: Progress indicators during API calls
- **Validation errors**: Inline error display with helpful messages
- **Disabled submit**: Submit button disabled while pending
- **Optional features**: "Copy as Markdown" for demo

### Stack
- **Choose one and stay consistent**: e.g., React + Vite (SPA) or HTMX + server templates (minimal JS)
- **Local hosting**: Host locally for milestone 1; no production SLA required in Phase 0

### Exit criteria
- **Demo path**: One demo path in README: start API + UI, submit preferences, see ranked results or an intentional empty state
- **Implementation status**: pending — e.g., apps/web/ or frontend/ + README section "Run the web app"

---

## Phase 8 - Streamlit Deployment

### Goal
Deploy the restaurant recommendation system using Streamlit as a unified web interface, providing an alternative to the Next.js frontend with easier deployment and maintenance.

### Concern
- **Approach**: Single-file Python web application using Streamlit
- **Role**: Alternative deployment option for rapid prototyping and demos
- **Deployment**: Streamlit Community Cloud (free) or self-hosted

### Data Flow
- **Direct integration**: Streamlit app directly imports and uses Phase 6 backend modules
- **UI components**: Streamlit widgets for preference form and results display
- **No separate API**: Eliminates frontend-backend separation for simpler deployment

### UX Requirements
- **Streamlit widgets**: Use st.select_slider, st.multiselect, st.number_input for preferences
- **Real-time updates**: Show loading spinners during recommendation generation
- **Results display**: Use st.dataframe or custom cards for restaurant recommendations
- **Export functionality**: "Download as CSV" or "Copy results" buttons

### Stack
- **Streamlit**: Python web framework for rapid prototyping
- **Deployment**: Streamlit Community Cloud (free tier) or Docker container
- **Integration**: Direct import of Phase 6 modules, no separate API server

### Implementation Plan
1. **Create streamlit_app.py** in project root
2. **Import Phase 6 modules** for recommendation logic
3. **Design Streamlit UI** with preference widgets
4. **Add results display** with formatting and export options
5. **Deploy to Streamlit Cloud** with environment variables

### Deployment Options
- **Streamlit Community Cloud**: Free hosting, GitHub integration
- **Docker**: Self-hosted deployment with Docker Compose
- **Heroku/Railway**: Alternative cloud platforms

### Environment Variables
- `XAI_API_KEY`: Groq API key for LLM calls
- `DATASET_PATH`: Path to restaurant dataset
- `DEBUG_MODE`: Enable/disable debug features

### Exit criteria
- **Working Streamlit app**: Functional UI with preference form and results
- **Deployment ready**: App deployed on Streamlit Community Cloud
- **Documentation**: README section for Streamlit deployment
- **Performance**: Acceptable response times for demo usage

---

## Phase dependency rules (guardrails)
- Phase 3 (filtering/prompt assembly) should not depend on Phase 4. Business rules belong in filtering, not in the LLM.
- Phase 4 must not invent entities outside the Phase 3 candidate list (strict grounding).
- Phase 5 should render outputs from Phase 4 but also support Phase 4 fallback.
- Phase 6 should provide stable API contracts for Phase 7 frontend consumption.
- Phase 7 should only communicate with Phase 6 API, not directly with earlier phases.
- Phase 8 can directly import Phase 6 modules for simplified deployment, bypassing the API layer.

