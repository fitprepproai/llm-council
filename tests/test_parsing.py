"""Unit tests for decompression.py and council.py parsing functions."""

import pytest
from backend.decompression import parse_decompression_json, strip_json_block
from backend.council import parse_ranking_from_text, calculate_aggregate_rankings


# --- decompression.py tests ---

VALID_RESPONSE = """## Decision Summary
A company is deciding whether to migrate from Snowflake to Databricks.

## Compression Map
Sentinel fires HIGH on migration risk.

```json
{
  "compression_map": {
    "sentinel": {"signal": "High migration risk", "quality": "HIGH", "weight": 0.8},
    "scout": {"signal": "Unified ML workflow opportunity", "quality": "MEDIUM", "weight": 0.6},
    "historian": {"signal": "Similar migrations often overrun budget", "quality": "HIGH", "weight": 0.7},
    "mirror": {"signal": "DE team skepticism may be skill bias", "quality": "MEDIUM", "weight": 0.5}
  },
  "tensions": [
    {"agent_a": "sentinel", "agent_b": "scout", "description": "Risk vs opportunity framing"}
  ],
  "recommendation_alignment": {
    "aligns_with": ["historian", "mirror"],
    "overrides": ["sentinel"]
  }
}
```
"""

RESPONSE_NO_JSON = """## Decision Summary
No JSON block here.

## Recommendation
Go for it.
"""

RESPONSE_INVALID_JSON = """Some text.

```json
{"broken": json here
```
"""


def test_parse_decompression_json_valid():
    result = parse_decompression_json(VALID_RESPONSE)
    assert result is not None
    assert "compression_map" in result
    assert result["compression_map"]["sentinel"]["quality"] == "HIGH"
    assert result["compression_map"]["scout"]["weight"] == 0.6
    assert len(result["tensions"]) == 1
    assert result["tensions"][0]["agent_a"] == "sentinel"
    assert result["recommendation_alignment"]["aligns_with"] == ["historian", "mirror"]


def test_parse_decompression_json_missing():
    result = parse_decompression_json(RESPONSE_NO_JSON)
    assert result is None


def test_parse_decompression_json_invalid_json():
    result = parse_decompression_json(RESPONSE_INVALID_JSON)
    assert result is None


def test_parse_decompression_json_empty_string():
    result = parse_decompression_json("")
    assert result is None


def test_strip_json_block_removes_block():
    result = strip_json_block(VALID_RESPONSE)
    assert "```json" not in result
    assert "compression_map" not in result
    assert "Decision Summary" in result
    assert "Compression Map" in result


def test_strip_json_block_no_block():
    result = strip_json_block(RESPONSE_NO_JSON)
    assert "Decision Summary" in result
    assert result.strip() == RESPONSE_NO_JSON.strip()


def test_strip_json_block_returns_stripped():
    result = strip_json_block("  \n\n" + VALID_RESPONSE + "\n\n  ")
    assert not result.startswith(" ")
    assert not result.endswith(" ")


# --- council.py parsing tests ---

def test_parse_ranking_numbered_list():
    text = """Response A is thorough but wordy.
Response B is concise and accurate.
Response C misses key points.

FINAL RANKING:
1. Response B
2. Response A
3. Response C"""
    result = parse_ranking_from_text(text)
    assert result == ["Response B", "Response A", "Response C"]


def test_parse_ranking_four_responses():
    text = """FINAL RANKING:
1. Response C
2. Response A
3. Response D
4. Response B"""
    result = parse_ranking_from_text(text)
    assert result == ["Response C", "Response A", "Response D", "Response B"]


def test_parse_ranking_fallback_no_header():
    text = "I think Response B is best, then Response A, then Response C."
    result = parse_ranking_from_text(text)
    assert result == ["Response B", "Response A", "Response C"]


def test_parse_ranking_empty():
    result = parse_ranking_from_text("No ranking here at all.")
    assert result == []


def test_parse_ranking_extra_text_after_ranking():
    text = """FINAL RANKING:
1. Response A
2. Response B

Overall this was a good set of responses."""
    result = parse_ranking_from_text(text)
    assert result == ["Response A", "Response B"]


# --- calculate_aggregate_rankings tests ---

def _make_label_to_agent():
    return {
        "Response A": {"key": "sentinel", "name": "Sentinel", "icon": "🛡️", "color": "#e74c3c"},
        "Response B": {"key": "scout", "name": "Scout", "icon": "🔭", "color": "#2ecc71"},
        "Response C": {"key": "historian", "name": "Historian", "icon": "📚", "color": "#3498db"},
    }


def test_calculate_aggregate_rankings_basic():
    label_to_agent = _make_label_to_agent()
    stage2_results = [
        {"agent": "sentinel", "name": "Sentinel", "icon": "🛡️", "color": "#e74c3c",
         "ranking": "FINAL RANKING:\n1. Response B\n2. Response C\n3. Response A"},
        {"agent": "scout", "name": "Scout", "icon": "🔭", "color": "#2ecc71",
         "ranking": "FINAL RANKING:\n1. Response B\n2. Response A\n3. Response C"},
        {"agent": "historian", "name": "Historian", "icon": "📚", "color": "#3498db",
         "ranking": "FINAL RANKING:\n1. Response C\n2. Response B\n3. Response A"},
    ]
    result = calculate_aggregate_rankings(stage2_results, label_to_agent)
    assert len(result) == 3
    # scout (Response B) ranked 1st twice, 2nd once → avg 1.33
    scout = next(r for r in result if r["agent"] == "scout")
    assert scout["average_rank"] == round((1 + 1 + 2) / 3, 2)
    # should be sorted by average_rank
    avg_ranks = [r["average_rank"] for r in result]
    assert avg_ranks == sorted(avg_ranks)


def test_calculate_aggregate_rankings_unknown_labels():
    label_to_agent = _make_label_to_agent()
    stage2_results = [
        {"agent": "sentinel", "name": "Sentinel", "icon": "🛡️", "color": "#e74c3c",
         "ranking": "FINAL RANKING:\n1. Response Z\n2. Response B"},  # Response Z unknown
    ]
    result = calculate_aggregate_rankings(stage2_results, label_to_agent)
    # Only scout (Response B) should appear
    assert len(result) == 1
    assert result[0]["agent"] == "scout"


def test_calculate_aggregate_rankings_empty():
    result = calculate_aggregate_rankings([], {})
    assert result == []
