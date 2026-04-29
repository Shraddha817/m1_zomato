## Dataset Contract (v1) — Zomato Restaurant Recommendation Dataset

### Dataset source
- **Dataset**: `ManikaSaini/zomato-restaurant-recommendation`
- **Link**: `https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation`

### Purpose of this contract
This document defines:
- which dataset fields are required for Milestone 1
- how raw values are normalized into the canonical `Restaurant` model
- what to do when fields are missing or malformed

This prevents later phases from depending on undocumented dataset behavior.

---

## Canonical model (internal)
The ingestion layer must produce a canonical `Restaurant` record with at least:
- `id` (string): stable synthetic identifier (must be stable across runs)
- `name` (string)
- `location` (string): city (preferred) or best available locality field
- `cuisines` (string[]): normalized list
- `rating` (float | null): numeric rating if available
- `cost` (number | null): numeric cost if available (units must be documented)
- `budget_band` ("low" | "medium" | "high" | null): derived from `cost` if possible
- `raw` (object | null): optional selected raw fields for debugging/prompting

---

## Field mapping (raw → canonical)
Because dataset schemas can change, the ingestion layer should map from raw columns to canonical fields using a mapping table.

### Required v1 fields (minimum)
The system must be able to produce these fields for most rows:
- **name**: restaurant name
- **location**: city or locality
- **cuisines**: one or more cuisines
- **rating**: numeric rating (or null if not available)
- **cost**: numeric cost or a derivable proxy (or null)

### Mapping rules (v1)
- **name**
  - Choose the most specific restaurant name field available.
  - Trim whitespace; collapse repeated spaces.
- **location**
  - Prefer city-level value when available; otherwise use best available locality field.
  - Normalize common variants (e.g., “Bangalore” vs “Bengaluru”) using a small alias map (optional).
- **cuisines**
  - If a single string: split on commas and slashes, trim tokens, drop empty tokens.
  - Normalize casing (title case or lower case), but keep display-friendly form consistent.
  - Drop placeholder values like “Not Available” / “NA” (configurable).
- **rating**
  - Accept numeric values.
  - If string:
    - extract a leading float when possible (e.g., “4.2/5” → 4.2)
    - treat “NEW”, “—”, empty as null
  - Clamp or nullify out-of-range values (<0 or >5).
- **cost**
  - If numeric: accept as-is and document units.
  - If string: extract digits and interpret consistently (e.g., “₹500 for two” → 500).
  - Treat unparseable or negative values as null.

---

## Derived fields

### budget_band
Derive `budget_band` from `cost` using configurable thresholds.
Example (placeholder thresholds; finalize after inspecting data distribution):
- low: cost <= 300
- medium: 301–700
- high: > 700

Boundary behavior must be defined (inclusive/exclusive) and tested.

---

## Row inclusion/exclusion rules (v1)
- Exclude rows when:
  - `name` is missing/blank, or
  - `location` is missing/blank
- Keep rows with missing rating/cost, but surface “Unknown” downstream.

---

## Stability requirements
- **Stable ID**: `id` must be stable across runs and independent of row ordering.
  - Recommended: deterministic hash of `(normalized_name, normalized_location, optional_address_or_latlng_if_present)`
  - Avoid using dataset row index as the only ID.
- **Revision pinning (recommended)**:
  - If feasible, pin a dataset revision in config/docs to reduce schema drift.

---

## Phase 1 verification checklist
When Phase 1 is implemented, update this contract with the observed dataset columns and final thresholds:
- Record raw column names actually used for each canonical field
- Confirm rating range and parsing rules with examples
- Confirm cost parsing rules and units
- Finalize budget band thresholds based on data distribution

