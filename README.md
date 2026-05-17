# Power Council

> **"Most people optimize within the prison. This tool shows you the door."**

A fork of [karpathy/llm-council](https://github.com/karpathy/llm-council) that transforms multi-model deliberation into a **strategic decision framework** grounded in Robert Greene's *48 Laws of Power* — focused specifically on the transition from compulsory labor to leverage, autonomy, and freedom.

## The Problem It Solves

Most career and business decisions are evaluated on surface metrics: salary, title, prestige, growth. But these metrics optimize for position within the foot-soldier economy — the game where you compete harder for incremental advancement while trading more time for marginally more money.

The Power Council analyzes every decision through four lenses that most people never consciously apply:

- **⚡ Leverage Hunter** — Where is the compounding leverage? What in this situation can be owned, systematized, or made scarce? (Law 11: Make others dependent on you)
- **♟️ Power Reader** — Who actually holds power here, what do they want, and how does each path affect the dependency ratio? (Law 3: Conceal your intentions; Law 33: Find each person's pressure point)
- **🏗️ The Architect** — Where does each path lead in 5-10 years if followed consistently? Which options build toward ownership vs. higher rungs on the same ladder? (Law 29: Plan all the way to the end)
- **🔓 Liberation Auditor** — Does this option actually increase your autonomy and leisure, or does it optimize within the trap? (Law 20: Do not commit to anyone; Law 34: Be royal in your own fashion)

## How It Works

Submit a decision, career move, or situation. Three stages run automatically:

1. **Stage 1 — Strategic Analysis.** All four advisors analyze your input in parallel. Each uses the same underlying model (`claude-sonnet-4.5`) but with a distinct system prompt encoding its power lens. Four tab-views: leverage map, power dynamics, long-game trajectory, liberation audit.

2. **Stage 2 — Strategic Cross-Examination.** Each advisor critiques the other three's analyses — anonymized to prevent groupthink. Rankings extracted to see which lens identified the most actionable insight.

3. **Stage 3 — Strategic Power Report.** A Strategist synthesizes everything into:
   - **Situation Assessment** — where you actually stand in the power hierarchy
   - **Power Map** — one signal per lens with confidence rating (HIGH/MEDIUM/LOW)
   - **The Liberation Vector** — which option most directly points toward owning your time
   - **Strategic Recommendation** — concrete moves, not general direction
   - **The 3 Power Moves** — actions that increase leverage regardless of which choice you make

   The report also renders a **Power Analysis Dashboard** with a radar chart showing signal intensity per lens, signal quality cards, and a **Liberation Score** (0–100%) measuring how directly the recommended path leads toward autonomy.

## Example Decisions to Run

- *"I have a $120K job offer at a FAANG company and a $90K offer plus 0.5% equity at a 20-person startup. Which do I take?"*
- *"My manager keeps blocking my promotion. I've been passed over twice. What do I do?"*
- *"I want to start a consulting practice on the side. Should I tell my employer?"*
- *"I'm 35, have $80K saved, and want to stop trading time for money within 5 years. What's the move?"*
- *"My biggest client wants me to take on 3x the work at the same rate. How do I handle this?"*

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

Edit `backend/config.py` to change the underlying model all advisors use:

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

Tests cover the parsing functions — strategic JSON extraction, ranking parsing, and aggregate score calculation — all without API calls.

## Architecture

```
User Input (decision, career move, situation)
    ↓
Stage 1: 4 parallel queries → same model, 4 power-lens system prompts
         [⚡ Leverage] [♟️ Power] [🏗️ Architect] [🔓 Liberation]
    ↓
Stage 2: Anonymized cross-examination → each advisor critiques the others
    ↓
Stage 3: The Strategist synthesizes → Strategic Power Report + JSON data
    ↓
Frontend: Power Analysis Dashboard
         [Liberation Score meter] [Radar chart] [Signal quality cards]
         [Strategic tensions] [Alignment summary]
```

All four advisors use the **same base model** differentiated entirely by system prompt. The intelligence is in the prompts, not model selection.

## Intellectual Grounding

The four advisors correspond to the most actionable themes in Robert Greene's *48 Laws of Power* as applied to economic freedom:

| Advisor | Core Law(s) | The Question It Answers |
|---------|-------------|------------------------|
| Leverage Hunter | Law 11 (Make others dependent) | Where is the compounding leverage? |
| Power Reader | Laws 1, 3, 5, 7, 33 | What is the hidden power game being played? |
| The Architect | Law 29 (Plan to the end) | Where does this path actually lead? |
| Liberation Auditor | Laws 20, 28, 34 | Does this increase or decrease your autonomy? |

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), async httpx, OpenRouter API
- **Frontend:** React + Vite, Recharts (radar visualization), react-markdown
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv (Python), npm (JavaScript)
