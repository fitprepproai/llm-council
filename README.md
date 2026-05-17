# Cognitive Council

> **"Karpathy built a council for better answers. This fork gives it a brain that works like ours actually does."**

A fork of [karpathy/llm-council](https://github.com/karpathy/llm-council) that replaces generic multi-model deliberation with **cognitively specialized agents** modeled after how human emotional compression works in decision-making.

## The Core Idea

Emotions are ultra-compacted decision trees — lossy compressions of experience that enable fast action but introduce systematic bias. When you have a gut feeling about a decision, four distinct heuristics are usually firing at once:

- 🛡️ **Sentinel** — "Something could go wrong" (threat detection, loss aversion)
- 🔭 **Scout** — "This could be huge" (opportunity detection, novelty bias)
- 📚 **Historian** — "I've seen this before" (pattern matching, base rates)
- 🪞 **Mirror** — "Does this feel like us?" (familiarity bias, comfort reasoning)

The Cognitive Council runs all four of these lenses simultaneously, cross-examines them against each other, then produces a **Decompression Report** — a structured analysis of which instincts are firing, how calibrated they are for your specific decision, and where they conflict.

## How It Works

When you submit a decision or question, the pipeline runs three stages:

1. **Stage 1 — Cognitive Analysis.** All four agents analyze your input in parallel. Each uses the same underlying model (`claude-sonnet-4.5`) but with a distinct system prompt encoding its cognitive bias. You see four tab-views: Sentinel's threat analysis, Scout's opportunity map, Historian's precedent review, and Mirror's familiarity audit.

2. **Stage 2 — Cross-Examination.** Each agent reviews the other three agents' anonymized analyses through its own bias lens — evaluating substance, over-compression, and what others missed. Rankings are extracted.

3. **Stage 3 — Decompression Report.** A chairman model synthesizes everything into a structured report:
   - **Decision Summary** — what the core decision actually is
   - **Compression Map** — what each gut instinct is telling you and how well-calibrated it is (HIGH/MEDIUM/LOW signal quality)
   - **Key Tensions** — where the lenses directly conflict and what that reveals
   - **Decompressed Recommendation** — synthesized recommendation with explicit reasoning about which instincts it follows vs. overrides
   - **What to Investigate** — 2-3 specific things to check before committing

The report also renders a **Decision Intelligence Dashboard** with a radar chart showing compression intensity per lens and signal quality cards.

## Example Decisions to Try

- *"Should we migrate our analytics platform from Snowflake to Databricks? Costs growing 20% YoY, ML team wants it, data engineering team is skeptical. $500K budget, end-of-quarter deadline."*
- *"We're evaluating a candidate with strong technical skills but the team has mixed feelings about culture fit."*
- *"Our biggest client wants us to build a custom feature that would take 3 months. Should we do it?"*
- *"Should we adopt an AI coding assistant for the engineering team?"*

## Setup

### 1. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for Python and npm for the frontend.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

Get your API key at [openrouter.ai](https://openrouter.ai/).

### 3. Configure the Base Model (Optional)

Edit `backend/config.py` to swap the underlying model all agents use:

```python
COGNITIVE_BASE_MODEL = "anthropic/claude-sonnet-4.5"
CHAIRMAN_MODEL = "anthropic/claude-sonnet-4.5"
```

Any OpenRouter model works. Use a cheaper model (e.g. `google/gemini-2.5-flash`) during development to reduce API costs.

## Running

**Option 1: Start script**
```bash
./start.sh
```

**Option 2: Manual**

Terminal 1 (Backend — port 8001):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend — port 5173):
```bash
cd frontend
npm run dev
```

Then open [http://localhost:5173](http://localhost:5173).

## Running Tests

```bash
uv run pytest
```

Tests cover the parsing functions — decompression JSON extraction, ranking parsing, and aggregate score calculation — all of which run without API calls.

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), async httpx, OpenRouter API
- **Frontend:** React + Vite, Recharts (radar visualization), react-markdown
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv (Python), npm (JavaScript)

## Architecture

```
User Input
    ↓
Stage 1: 4 parallel queries → same model, 4 different system prompts
         [🛡️ Sentinel] [🔭 Scout] [📚 Historian] [🪞 Mirror]
    ↓
Stage 2: Anonymized cross-examination → each agent critiques the others
    ↓
Stage 3: Chairman decompressor synthesizes report + JSON data block
    ↓
Frontend: Decompression dashboard (radar chart + signal cards + tensions)
```

The key architectural difference from the original: rather than querying multiple different LLMs, all four agents use the **same base model** differentiated entirely by system prompt. The insight lives in the prompts, not the models.
