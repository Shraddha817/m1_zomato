## Phase 0 — Scope and foundations (Milestone 1)

### Goal
Define a clear, implementable v1 scope and establish the foundations required for Phase 1–5:
- agreed stack assumptions
- secrets and configuration conventions
- dataset contract (what fields we rely on and how they are interpreted)

---

## Product slice (v1)

### Primary user journey
1. User enters preferences (location, budget, cuisines, minimum rating, optional notes)
2. System filters the dataset to a bounded candidate set
3. LLM ranks candidates and explains recommendations (grounded in candidates)
4. UI displays top results with key fields and explanations

### Input surface (v1)
- **Primary**: a basic web UI is the source of user input for Milestone 1.
- **Optional**: a CLI may exist for developer diagnostics/testing, but it is not the primary UX.

### Input fields (v1)
- **Location** (required)
- **Budget band** (optional): low / medium / high
- **Cuisines** (optional): one or more
- **Minimum rating** (optional)
- **Additional preferences** (optional): free text, trimmed to a safe length

### Output fields (v1)
For each recommended restaurant:
- name
- location
- cuisines
- rating
- cost/budget
- AI explanation (must reference user preferences)

---

## Stack assumptions (v1)
- **Language/runtime**: Python 3.11+
- **UI**: Streamlit (simple and fast iteration for Milestone 1)
- **Dataset access**: Hugging Face `datasets`
- **LLM access**: OpenAI-compatible chat API (key from environment variables)

---

## Data and model grounding principles
- **Deterministic rules first**: filtering and business rules live in Phase 3, not in the LLM.
- **Strict grounding**: the LLM can only recommend items from the candidate list.
- **Stable IDs**: each candidate must have a stable `id` so the LLM output can reference IDs (not names).

---

## Non-goals (explicitly out of scope for Milestone 1)
- User accounts, login, saved favorites, long-term personalization
- Live Zomato API integration
- Maps, navigation, real-time availability
- Ordering, payments, delivery tracking

---

## Secrets and configuration
- **Never commit secrets** (API keys, tokens).
- Use:
  - `.env.example` (committed template)
  - `.env` (local only; not committed)
- Configuration values should be read from environment variables with sensible defaults where safe.

---

## Definition of Done (Phase 0)
Phase 0 is complete when:
- This scope doc exists and matches `docs/problemstatement.md`
- `docs/dataset-contract.md` defines the dataset fields we rely on and normalization rules
- `.env.example` is present and documents required environment variables
- `README.md` explains the project and local environment setup

