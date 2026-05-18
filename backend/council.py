"""3-stage Power Council orchestration — a 48 Laws of Power decision framework."""

import asyncio
import re
from typing import List, Dict, Any, Tuple
from .openrouter import query_agents_parallel, query_model
from .config import COGNITIVE_AGENTS, COGNITIVE_BASE_MODEL, CHAIRMAN_MODEL
from .decompression import parse_decompression_json, strip_json_block


def _agent_list() -> List[Dict[str, Any]]:
    """Return agents as a list with 'key' field injected."""
    return [
        {"key": k, **v}
        for k, v in COGNITIVE_AGENTS.items()
    ]


async def stage1_collect_responses(user_query: str) -> List[Dict[str, Any]]:
    """
    Stage 1: Each cognitive agent analyzes the query through its specialized lens.
    All agents use the same base model but different system prompts.
    """
    messages = [{"role": "user", "content": user_query}]
    agents = _agent_list()

    responses = await query_agents_parallel(agents, messages, COGNITIVE_BASE_MODEL)

    stage1_results = []
    for agent in agents:
        response = responses.get(agent['key'])
        if response is not None:
            stage1_results.append({
                "agent": agent['key'],
                "name": agent['name'],
                "icon": agent['icon'],
                "color": agent['color'],
                "description": agent['description'],
                "response": response.get('content', '')
            })

    return stage1_results


async def stage2_collect_rankings(
    user_query: str,
    stage1_results: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, str]]]:
    """
    Stage 2: Each cognitive agent cross-examines the other agents' anonymized analyses.

    Returns:
        Tuple of (rankings list, label_to_agent mapping)
    """
    labels = [chr(65 + i) for i in range(len(stage1_results))]

    label_to_agent = {
        f"Response {label}": {
            "key": result['agent'],
            "name": result['name'],
            "icon": result['icon'],
            "color": result['color'],
        }
        for label, result in zip(labels, stage1_results)
    }

    responses_text = "\n\n".join([
        f"Response {label}:\n{result['response']}"
        for label, result in zip(labels, stage1_results)
    ])

    ranking_prompt = f"""You are reviewing strategic analyses from other power advisors examining the following decision:

Question: {user_query}

Each analysis below comes from a different strategic lens — leverage identification, power dynamics, long-game architecture, or liberation auditing (anonymized):

{responses_text}

Your task:
1. Evaluate the STRATEGIC QUALITY of each analysis — is the reasoning sound? Does it identify real leverage or real constraints?
2. Identify where each analysis might be MISSING THE POINT — focusing on surface features while missing the structural power dynamics
3. Identify where each analysis surfaces something the others MISSED that could be decisive
4. Rank the analyses by how much actionable strategic insight they provide toward gaining leverage and autonomy

IMPORTANT: Your final ranking MUST be formatted EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list the responses from best to worst as a numbered list
- Each line should be: number, period, space, then ONLY the response label (e.g., "1. Response A")
- Do not add any other text or explanations in the ranking section

Example format:

Response A correctly identifies the leverage point but underestimates the political risk...
Response B misses the structural trap and optimizes within it instead of escaping...

FINAL RANKING:
1. Response A
2. Response B

Now provide your strategic cross-examination and ranking:"""

    messages = [{"role": "user", "content": ranking_prompt}]
    agents = _agent_list()

    responses = await query_agents_parallel(agents, messages, COGNITIVE_BASE_MODEL)

    stage2_results = []
    for result in stage1_results:
        agent_key = result['agent']
        response = responses.get(agent_key)
        if response is not None:
            full_text = response.get('content', '')
            parsed = parse_ranking_from_text(full_text)
            stage2_results.append({
                "agent": agent_key,
                "name": result['name'],
                "icon": result['icon'],
                "color": result['color'],
                "ranking": full_text,
                "parsed_ranking": parsed
            })

    return stage2_results, label_to_agent


async def stage3_synthesize_final(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Stage 3: The Strategist synthesizes a structured Strategic Power Report.
    """
    stage1_text = "\n\n".join([
        f"[{result['icon']} {result['name']} — {result['description']}]\n{result['response']}"
        for result in stage1_results
    ])

    stage2_text = "\n\n".join([
        f"[Cross-examination by {result['icon']} {result['name']}]\n{result['ranking']}"
        for result in stage2_results
    ])

    chairman_prompt = f"""You are the Strategist — the synthesis layer integrating four power analysis frameworks to produce a concrete path toward leverage, autonomy, and freedom from compulsory labor.

You have received four analyses of a decision from different strategic lenses:
- ⚡ Leverage Hunter: identifies compounding assets, leverage points, linear vs. leveraged income
- ♟️ Power Reader: maps power dynamics, hidden agendas, dependency ratios, political positioning
- 🏗️ The Architect: traces long-game trajectories, path dependency, ownership thresholds
- 🔓 Liberation Auditor: evaluates each option for autonomy delta, prestige traps, golden handcuffs

Original Question: {user_query}

STAGE 1 — Strategic Analyses:
{stage1_text}

STAGE 2 — Cross-Examinations:
{stage2_text}

Produce a STRATEGIC POWER REPORT. Be direct and specific — this is the advice a trusted strategic advisor gives when they have no reason to sugarcoat.

## Situation Assessment
Where is the decision-maker positioned in the power hierarchy right now? What leverage do they have vs. what they're missing?

## Power Map
For each of the four lenses (Leverage, Power, Architecture, Liberation), give one sentence on what it sees and how confident we should be in that signal.

## The Liberation Vector
Which available option most directly points toward owning your time, reducing compulsory labor, and building compounding leverage? If none do this well, say so directly.

## Strategic Recommendation
The concrete recommendation — what to do and what to negotiate for. Include specific moves, not just direction.

## The 3 Power Moves
Three specific actions — executable regardless of which choice is made — that increase leverage and freedom. These run in parallel with whatever is decided.

After your report, output a JSON block tagged with ```json:
{{
  "power_map": {{
    "leverage": {{ "signal": "one sentence summary", "quality": "HIGH|MEDIUM|LOW", "weight": 0.0 }},
    "position": {{ "signal": "one sentence summary", "quality": "HIGH|MEDIUM|LOW", "weight": 0.0 }},
    "architect": {{ "signal": "one sentence summary", "quality": "HIGH|MEDIUM|LOW", "weight": 0.0 }},
    "freedom": {{ "signal": "one sentence summary", "quality": "HIGH|MEDIUM|LOW", "weight": 0.0 }}
  }},
  "liberation_score": 0.0,
  "tensions": [
    {{ "agent_a": "leverage", "agent_b": "freedom", "description": "brief description of the tension" }}
  ],
  "strategic_alignment": {{
    "aligns_with": ["leverage", "architect"],
    "overrides": ["position"]
  }}
}}

liberation_score: 0.0 = this situation/recommended path is deep in the foot-soldier trap; 1.0 = clear path to owning your time and capital.
weight: 0.0–1.0, how strongly each strategic signal fires for this specific decision.

Provide your strategic power report now:"""

    messages = [{"role": "user", "content": chairman_prompt}]
    response = await query_model(CHAIRMAN_MODEL, messages)

    if response is None:
        return {
            "model": CHAIRMAN_MODEL,
            "response": "Error: Unable to generate strategic power report.",
            "decompression_data": None
        }

    raw_content = response.get('content', '')
    decompression_data = parse_decompression_json(raw_content)
    clean_response = strip_json_block(raw_content)

    return {
        "model": CHAIRMAN_MODEL,
        "response": clean_response,
        "decompression_data": decompression_data
    }


def parse_ranking_from_text(ranking_text: str) -> List[str]:
    """Parse the FINAL RANKING section from the model's response."""
    if "FINAL RANKING:" in ranking_text:
        parts = ranking_text.split("FINAL RANKING:")
        if len(parts) >= 2:
            ranking_section = parts[1]
            numbered_matches = re.findall(r'\d+\.\s*Response [A-Z]', ranking_section)
            if numbered_matches:
                return [re.search(r'Response [A-Z]', m).group() for m in numbered_matches]
            matches = re.findall(r'Response [A-Z]', ranking_section)
            return matches

    return re.findall(r'Response [A-Z]', ranking_text)


def calculate_aggregate_rankings(
    stage2_results: List[Dict[str, Any]],
    label_to_agent: Dict[str, Dict[str, str]]
) -> List[Dict[str, Any]]:
    """Calculate aggregate rankings across all cognitive agents' cross-examinations."""
    from collections import defaultdict

    agent_positions = defaultdict(list)
    agent_meta = {}

    for ranking in stage2_results:
        parsed_ranking = parse_ranking_from_text(ranking['ranking'])
        for position, label in enumerate(parsed_ranking, start=1):
            if label in label_to_agent:
                agent_info = label_to_agent[label]
                agent_key = agent_info['key']
                agent_positions[agent_key].append(position)
                agent_meta[agent_key] = agent_info

    aggregate = []
    for agent_key, positions in agent_positions.items():
        if positions:
            avg_rank = sum(positions) / len(positions)
            meta = agent_meta.get(agent_key, {})
            aggregate.append({
                "agent": agent_key,
                "name": meta.get('name', agent_key),
                "icon": meta.get('icon', ''),
                "color": meta.get('color', '#666'),
                "average_rank": round(avg_rank, 2),
                "rankings_count": len(positions)
            })

    aggregate.sort(key=lambda x: x['average_rank'])
    return aggregate


async def generate_conversation_title(user_query: str) -> str:
    """Generate a short title for a conversation based on the first user message."""
    title_prompt = f"""Generate a very short title (3-5 words maximum) that summarizes the following question.
The title should be concise and descriptive. Do not use quotes or punctuation in the title.

Question: {user_query}

Title:"""

    messages = [{"role": "user", "content": title_prompt}]
    response = await query_model("google/gemini-2.5-flash", messages, timeout=30.0)

    if response is None:
        return "New Conversation"

    title = response.get('content', 'New Conversation').strip().strip('"\'')
    if len(title) > 50:
        title = title[:47] + "..."

    return title


async def run_full_council(user_query: str) -> Tuple[List, List, Dict, Dict]:
    """Run the complete 3-stage cognitive council process."""
    stage1_results = await stage1_collect_responses(user_query)

    if not stage1_results:
        return [], [], {
            "model": "error",
            "response": "All agents failed to respond. Please try again.",
            "decompression_data": None
        }, {}

    stage2_results, label_to_agent = await stage2_collect_rankings(user_query, stage1_results)

    aggregate_rankings = calculate_aggregate_rankings(stage2_results, label_to_agent)

    stage3_result = await stage3_synthesize_final(
        user_query,
        stage1_results,
        stage2_results
    )

    metadata = {
        "label_to_agent": label_to_agent,
        "aggregate_rankings": aggregate_rankings
    }

    return stage1_results, stage2_results, stage3_result, metadata
