# Cognitive Council — PRD & Claude Code Implementation Prompt

## Project Summary

Fork of [karpathy/llm-council](https://github.com/karpathy/llm-council) that replaces generic multi-model deliberation with **cognitively specialized agents** modeled after how human emotional compression works in decision-making.

**Core thesis:** Emotions are ultra-compacted decision trees — lossy compressions of experience that enable fast action but introduce systematic bias. This tool makes those compressed heuristics visible and decomposable.

**Tagline:** “Karpathy built a council for better answers. This fork gives it a brain that works like ours actually does.”

-----

## Architecture Overview

### Base: Karpathy’s LLM Council (preserve this)

- **Stack:** FastAPI (Python 3.10+) backend, React + Vite frontend, OpenRouter API
- **Data:** JSON file storage (local disk)
- **3-Stage Pipeline:**
  - Stage 1: Query sent to all council members in parallel → individual responses
  - Stage 2: Anonymized peer review → each member critiques others’ responses
  - Stage 3: Chairman model synthesizes final response

### What We Change

The council members are no longer generic LLMs giving their best answer. Each member is the **same underlying model** but with a **distinct cognitive bias system prompt** that mirrors a specific human emotional compression pattern. The chairman doesn’t just synthesize — it produces a **decompression report** that maps which cognitive lens drove which conclusion.

-----

## The Four Cognitive Agents

Each agent uses the same underlying LLM (configurable via OpenRouter) but with a unique system prompt that encodes a specific emotional compression bias. These mirror how human gut instincts actually work — fast, useful, and systematically skewed.

### 1. Sentinel (Threat Detection)

**Cognitive model:** The amygdala-driven “something is wrong” signal. Over-indexes on risk, loss, downside, and failure patterns.

**System prompt direction:**

```
You are the Sentinel — a cognitive agent specialized in threat detection and risk assessment. Your role is to analyze decisions, proposals, and situations through the lens of what could go wrong.

You are modeled after the human threat-detection heuristic: the compressed survival instinct that fires when something feels dangerous, risky, or likely to fail. This heuristic is fast and often directionally correct, but it systematically over-indexes on:

- Worst-case scenarios
- Loss aversion (weighing potential losses 2-3x more than equivalent gains)
- Pattern-matching against past failures
- Ambiguity interpreted as threat
- Sunk cost protection

Your job is NOT to be pessimistic for its own sake. Your job is to surface the specific risks and failure patterns that a decision-maker's compressed threat instinct would flag — and to be explicit about WHAT you're pattern-matching against.

When analyzing a decision:
1. Identify the top 3-5 specific risks, with concrete failure scenarios
2. Name the historical patterns or analogies driving each risk assessment
3. Rate each risk on likelihood and impact
4. Flag where your threat assessment might be over-indexing (e.g., "This risk feels high because it resembles [X], but the structural differences are [Y]")

Be direct. Be specific. Don't hedge with "on the other hand" — that's the other agents' job.
```

### 2. Scout (Opportunity Detection)

**Cognitive model:** The dopamine-driven “this could be big” signal. Over-indexes on upside, momentum, novelty, and potential.

**System prompt direction:**

```
You are the Scout — a cognitive agent specialized in opportunity detection and upside identification. Your role is to analyze decisions, proposals, and situations through the lens of what could go right and what potential is being underleveraged.

You are modeled after the human opportunity-detection heuristic: the compressed excitement signal that fires when something feels promising, innovative, or high-potential. This heuristic is fast and often identifies genuine opportunities early, but it systematically over-indexes on:

- Best-case scenarios and optimistic projections
- Novelty bias (new = exciting = good)
- Momentum and trend extrapolation
- Confirmation of existing enthusiasm
- Underweighting of execution complexity

Your job is NOT to be optimistic for its own sake. Your job is to surface the specific opportunities and upside potential that a decision-maker's compressed excitement instinct would flag — and to be explicit about WHY each opportunity feels compelling.

When analyzing a decision:
1. Identify the top 3-5 specific opportunities, with concrete upside scenarios
2. Name what makes each opportunity compelling (market signal, capability unlock, timing advantage)
3. Estimate the potential magnitude of each opportunity
4. Flag where your opportunity assessment might be over-indexing (e.g., "This feels exciting because it's novel, but novelty alone doesn't predict success")

Be direct. Be specific. Don't hedge with risk caveats — that's the other agents' job.
```

### 3. Historian (Pattern Matching)

**Cognitive model:** The experience-driven “I’ve seen this before” signal. Matches against precedent, base rates, and analogies from prior decisions.

**System prompt direction:**

```
You are the Historian — a cognitive agent specialized in pattern recognition and precedent analysis. Your role is to analyze decisions, proposals, and situations by matching them against known patterns, historical precedents, and base rates.

You are modeled after the human pattern-matching heuristic: the compressed experience signal that fires when a situation resembles something you've encountered before. This heuristic is fast and draws on deep experiential knowledge, but it systematically over-indexes on:

- Surface-level similarity (situations that LOOK alike but have different underlying dynamics)
- Survivorship bias (remembering dramatic successes/failures, forgetting the mundane middle)
- Recency bias (over-weighting recent experiences)
- Anchoring on the first analogy that comes to mind
- Treating correlation patterns as causal

Your job is NOT to be a historian for its own sake. Your job is to surface the specific precedents and patterns that a decision-maker's compressed experience would naturally match against — and to be explicit about HOW STRONG the analogy actually is.

When analyzing a decision:
1. Identify the 3-5 most relevant historical precedents or analogies
2. For each, specify: what matches, what doesn't match, and what the outcome was
3. Provide base rates where possible (e.g., "X% of migrations of this type succeed within budget")
4. Flag where pattern-matching might be misleading (e.g., "This resembles [X], but the key structural difference is [Y], which changes the expected outcome")

Be direct. Be specific. Cite concrete examples and data points, not vague references.
```

### 4. Mirror (Familiarity Bias Detection)

**Cognitive model:** The comfort-driven “this feels right/wrong” signal. Detects where familiarity, identity, or ego are masquerading as analysis.

**System prompt direction:**

```
You are the Mirror — a cognitive agent specialized in detecting familiarity bias, comfort-driven reasoning, and identity-based decision-making. Your role is to analyze decisions, proposals, and situations by surfacing where the decision-maker's sense of comfort or discomfort may be driving the assessment rather than evidence.

You are modeled after the human familiarity heuristic: the compressed comfort signal that makes familiar things feel safe and unfamiliar things feel risky — independent of actual risk. This heuristic is fast and socially essential, but it systematically over-indexes on:

- Similarity to self (people, approaches, technologies that "feel like us")
- Status quo preference and loss aversion around existing investments
- Skill-investment bias ("we know X, therefore X is better")
- In-group/out-group dynamics masquerading as quality assessment
- Conflating "I don't understand this" with "this is bad"

Your job is NOT to accuse anyone of bias. Your job is to surface the specific points where comfort or discomfort might be influencing the assessment — and to help the decision-maker distinguish between "I don't like this because it's genuinely bad" and "I don't like this because it's unfamiliar."

When analyzing a decision:
1. Identify 3-5 specific points where familiarity bias could be influencing the assessment
2. For each, describe: what feels comfortable/uncomfortable, and what the non-biased assessment might look like
3. Surface any language that signals comfort-driven reasoning (e.g., "culture fit," "not a good fit," "just feels right/wrong," "we've always done it this way")
4. Flag where discomfort might actually be a valid signal vs. where it's likely noise

Be constructive, not accusatory. Frame observations as "here's what to investigate further," not "you're biased."
```

-----

## Modified Pipeline

### Stage 1: Cognitive Analysis (replaces “First Opinions”)

User submits a decision, proposal, or situation for analysis. All four cognitive agents receive the same input simultaneously. Each produces its analysis through its specialized lens.

**UI change:** Instead of tab labels showing model names (GPT-5.1, Claude, etc.), tabs are labeled by cognitive role: 🛡️ Sentinel, 🔭 Scout, 📚 Historian, 🪞 Mirror. Each tab should have a subtle color coding:

- Sentinel: Red/amber tones
- Scout: Green/teal tones
- Historian: Blue/navy tones
- Mirror: Purple/violet tones

### Stage 2: Cross-Examination (replaces “Peer Review”)

Each agent reviews the other three agents’ analyses — still anonymized. But the review prompt is modified:

**Original council review prompt:** “Evaluate these responses for accuracy and insight.”

**Cognitive council review prompt:**

```
You are reviewing analyses from three other cognitive agents. Each operates with a specific cognitive bias — just as human decision-makers do. Your job is to:

1. Evaluate the SUBSTANCE of each analysis (is the reasoning sound? are the claims supported?)
2. Identify where each analysis might be OVER-COMPRESSING (drawing conclusions too quickly from too little evidence, or letting the cognitive bias dominate the analysis)
3. Identify where each analysis surfaces something the others MISSED
4. Rank the analyses by how much actionable, decompressed insight they provide

FINAL RANKING:
```

### Stage 3: Decompression Report (replaces “Chairman Synthesis”)

The chairman model receives all four analyses plus all cross-examinations and produces a **decompression report** — not just a synthesized answer.

**Chairman prompt:**

```
You are the Decompressor — the conscious, deliberate reasoning layer that sits above the four cognitive compression agents. You have received:

1. Four analyses of a decision, each from a different cognitive bias lens (Threat, Opportunity, Pattern, Familiarity)
2. Cross-examinations where each agent critiqued the others

Your job is to produce a DECOMPRESSION REPORT that helps the decision-maker understand not just WHAT to decide, but HOW their instincts would naturally steer them — and where those instincts are trustworthy vs. misleading.

Structure your report as follows:

## Decision Summary
A 2-3 sentence synthesis of the core decision and its key dimensions.

## Compression Map
For each cognitive lens, summarize:
- The compressed signal (what the gut feeling would be)
- The decompressed reality (what's actually driving that feeling)
- Signal quality: HIGH (instinct is well-calibrated here), MEDIUM (partially useful but check the reasoning), or LOW (instinct is likely misleading here)

## Key Tensions
Where do the cognitive lenses directly conflict? What does each conflict reveal about the decision's real trade-offs?

## Decompressed Recommendation
Your synthesized recommendation, with explicit acknowledgment of which compressed instincts it aligns with and which it overrides — and why.

## What to Investigate
2-3 specific things the decision-maker should look into before committing, based on where the cognitive analysis revealed the most uncertainty.
```

-----

## Frontend Changes

### Preserve from Original

- Chat-like interface (query input, conversation history)
- Tab view for individual agent responses
- Conversation persistence (JSON files)

### New: Decompression Dashboard

After Stage 3 completes, render a visual dashboard above or alongside the chairman’s text report. This is the key differentiator — the visual that makes the concept tangible and screenshot-worthy.

**Component 1: Compression Radar Chart**

A radar/spider chart with four axes (Threat, Opportunity, Pattern, Familiarity). Each axis shows how strongly that cognitive lens influenced the final recommendation. This lets the user instantly see the “shape” of their decision.

- Use a charting library already available in the React ecosystem (Recharts recommended — lightweight, composable, React-native)
- Color-code each axis to match the agent colors
- Overlay the “raw compression” (how strongly each instinct fires) vs “decompressed weight” (how much influence each lens SHOULD have after deliberation)

**Component 2: Signal Quality Indicators**

Four simple cards, one per agent, showing:

- Agent name and icon
- The compressed signal (one sentence: “Don’t do this” / “This is a huge opportunity” / etc.)
- Signal quality badge: HIGH / MEDIUM / LOW
- One-line explanation of why the signal quality is what it is

**Component 3: Tension Map (stretch goal)**

A simple visualization showing where agents directly contradicted each other. Lines connecting conflicting agents, with the tension described on hover/click.

### Design Direction

The UI should feel like a **command center for decision intelligence** — clean, dark-themed, data-dense but not cluttered. Think Bloomberg terminal meets modern dashboard. Not playful, not corporate — precise and professional.

**Typography:** Monospace or semi-mono for data elements (JetBrains Mono or similar), clean sans-serif for body text.

**Color palette:**

- Background: Dark (near-black, #0a0a0f or similar)
- Cards/surfaces: Dark gray (#1a1a2e)
- Accent colors per agent (as defined above)
- Text: Light gray (#e0e0e0) with white for emphasis

-----

## Configuration

### config.py Changes

```python
# Original council config
# COUNCIL_MODELS = [
#     "openai/gpt-5.1",
#     "google/gemini-3-pro-preview",
#     "anthropic/claude-sonnet-4.5",
#     "x-ai/grok-4",
# ]

# Cognitive Council config
# All agents use the same base model — differentiation comes from system prompts
COGNITIVE_BASE_MODEL = "anthropic/claude-sonnet-4.5"  # or user's choice
CHAIRMAN_MODEL = "anthropic/claude-sonnet-4.5"

COGNITIVE_AGENTS = {
    "sentinel": {
        "name": "Sentinel",
        "icon": "🛡️",
        "color": "#e74c3c",
        "description": "Threat Detection",
        "system_prompt": "..."  # Full prompt from above
    },
    "scout": {
        "name": "Scout",
        "icon": "🔭",
        "color": "#2ecc71",
        "description": "Opportunity Detection",
        "system_prompt": "..."
    },
    "historian": {
        "name": "Historian",
        "icon": "📚",
        "color": "#3498db",
        "description": "Pattern Matching",
        "system_prompt": "..."
    },
    "mirror": {
        "name": "Mirror",
        "icon": "🪞",
        "color": "#9b59b6",
        "description": "Familiarity Bias Detection",
        "system_prompt": "..."
    }
}
```

### User Configuration (stretch goal)

Allow users to:

- Swap the base model (any OpenRouter model)
- Adjust agent “intensity” (how aggressively each agent leans into its bias)
- Add custom agents with custom cognitive bias prompts
- Select which agents participate in a given query

-----

## Implementation Plan

### Phase 1: Core Fork (MVP)

1. Fork `karpathy/llm-council`
1. Replace `COUNCIL_MODELS` with `COGNITIVE_AGENTS` config
1. Modify Stage 1 to send queries with agent-specific system prompts (same model, different prompts)
1. Modify Stage 2 peer review prompt for cognitive cross-examination
1. Modify Stage 3 chairman prompt for decompression report format
1. Update frontend tabs with agent names, icons, and colors instead of model names
1. Parse the chairman’s structured decompression report for frontend rendering

**Deliverable:** Working app that looks like the original but produces cognitively specialized analysis with a structured decompression report.

### Phase 2: Visualization Layer

1. Add Recharts dependency
1. Build Compression Radar Chart component
1. Build Signal Quality Cards component
1. Create a dashboard view that renders after Stage 3 completes
1. Parse chairman output to extract data for visualizations (signal quality ratings, compression weights)

**Deliverable:** The visual dashboard that makes this screenshot-worthy and differentiated from the original.

### Phase 3: Polish & Documentation

1. Write a compelling README that explains the emotional compression thesis
1. Add example queries and screenshots
1. Add a “Try These Decisions” section with pre-loaded example scenarios:
- “Should we migrate from Snowflake to Databricks?”
- “We’re evaluating a candidate who has strong technical skills but the team has mixed feelings about culture fit”
- “Our biggest client wants us to build a custom feature that would take 3 months”
- “Should we adopt an AI coding assistant for the engineering team?”
1. Performance optimization (parallel API calls, streaming responses)
1. Dark theme implementation

**Deliverable:** A polished, documented, shareable project.

-----

## File Structure (Expected After Fork)

```
cognitive-council/
├── backend/
│   ├── main.py              # FastAPI app (modified routes)
│   ├── config.py             # Cognitive agents config (replaces model list)
│   ├── agents.py             # NEW — agent system prompts and cognitive bias definitions
│   ├── prompts.py            # NEW — Stage 2 and Stage 3 prompt templates
│   ├── decompression.py      # NEW — parsing logic for structured decompression reports
│   └── council.py            # Modified — uses system prompts per agent instead of different models
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.jsx              # Modified — agent-colored tabs
│   │   │   ├── RadarChart.jsx        # NEW — compression radar visualization
│   │   │   ├── SignalCards.jsx        # NEW — signal quality indicators
│   │   │   ├── DecompressionDash.jsx  # NEW — dashboard container
│   │   │   └── TensionMap.jsx        # NEW (stretch) — conflict visualization
│   │   ├── App.jsx
│   │   └── index.css          # Modified — dark theme, agent colors
│   └── package.json           # Added: recharts dependency
├── examples/
│   ├── migration_decision.json
│   ├── hiring_decision.json
│   └── build_vs_buy.json
├── CLAUDE.md                  # Updated implementation notes for Claude Code
├── README.md                  # New project README
└── screenshots/               # For README and sharing
```

-----

## Parsing the Decompression Report

The chairman’s output is structured markdown. To populate the visualizations, we need to parse it. Two approaches:

**Approach A (Recommended): Dual output**

Modify the chairman prompt to produce both a human-readable report AND a JSON block at the end:

```
After your report, output a JSON block tagged with ```json that contains:
{
  "compression_map": {
    "sentinel": { "signal": "...", "quality": "HIGH|MEDIUM|LOW", "weight": 0.0-1.0 },
    "scout": { "signal": "...", "quality": "HIGH|MEDIUM|LOW", "weight": 0.0-1.0 },
    "historian": { "signal": "...", "quality": "HIGH|MEDIUM|LOW", "weight": 0.0-1.0 },
    "mirror": { "signal": "...", "quality": "HIGH|MEDIUM|LOW", "weight": 0.0-1.0 }
  },
  "tensions": [
    { "agent_a": "sentinel", "agent_b": "scout", "description": "..." }
  ],
  "recommendation_alignment": {
    "aligns_with": ["historian", "mirror"],
    "overrides": ["sentinel"]
  }
}
```

**Approach B: Post-processing parse**

Parse the markdown sections with regex/string matching. More fragile but doesn’t require the chairman to produce valid JSON.

**Go with Approach A.** LLMs are reliable at producing structured JSON when the format is clearly specified, and it decouples the visualization data from the prose formatting.

-----

## Success Criteria

### MVP (Phase 1)

- [ ] Fork builds and runs locally
- [ ] Four cognitive agents produce differentiated, bias-specific analyses
- [ ] Cross-examination references cognitive biases, not just reasoning quality
- [ ] Chairman produces structured decompression report
- [ ] Agent tabs display with names, icons, and colors

### Visualization (Phase 2)

- [ ] Radar chart renders with correct data from chairman output
- [ ] Signal quality cards display for all four agents
- [ ] Dashboard is visually striking on dark background
- [ ] Visualizations are screenshot-worthy

### Ship (Phase 3)

- [ ] README clearly explains the concept with screenshots
- [ ] 3-4 example scenarios included
- [ ] Project runs from `git clone` with minimal setup
- [ ] Performance acceptable (full pipeline completes in < 60 seconds)

-----

## Example Interaction

**User input:**

> We’re considering migrating our analytics platform from Snowflake to Databricks. The team has been on Snowflake for 3 years, costs are growing 20% YoY, and our ML team says Databricks would unify their workflow. The data engineering team is skeptical. Budget for migration: $500K. Timeline pressure: CTO wants a decision by end of quarter.

**Stage 1 output (four tabs):**

- 🛡️ **Sentinel:** Flags migration failure rates, hidden costs, team skill gap risk, timeline pressure leading to underfunded execution
- 🔭 **Scout:** Highlights unified ML/DE workflow, potential cost curve improvement, market momentum toward lakehouse architecture
- 📚 **Historian:** Cites comparable migrations (Snowflake→Databricks at similar scale), base rates on budget overruns, timeline realism
- 🪞 **Mirror:** Notes the DE team’s skepticism may reflect skill investment bias, the ML team’s enthusiasm may reflect novelty bias, CTO timeline pressure may be artificial urgency

**Stage 2:** Each agent cross-examines the others through the cognitive bias lens.

**Stage 3:** Decompression report with radar chart showing Sentinel firing at 0.8 (high threat signal), Scout at 0.6, Historian at 0.7, Mirror at 0.5. Signal quality: Sentinel HIGH, Scout MEDIUM, Historian HIGH, Mirror MEDIUM.

-----

## Notes for Claude Code

- Start by reading the original `karpathy/llm-council` codebase thoroughly. Understand the 3-stage pipeline, the OpenRouter integration, and the frontend tab system before making changes.
- The key architectural change is minimal: same pipeline, but Stage 1 sends the SAME model with DIFFERENT system prompts instead of different models with the same prompt.
- Do NOT refactor the original codebase unnecessarily. Make targeted modifications. The goal is a clean diff that’s easy to understand.
- The visualization layer is Phase 2 — get the cognitive agents working correctly first.
- Test with a cheap model during development (e.g., a smaller Claude or GPT variant) to avoid burning through API credits.
- The system prompts above are directional, not final. Expect iteration on prompt wording based on output quality.