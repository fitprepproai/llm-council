"""Parsing logic for structured decompression reports from Stage 3."""

import json
import re
from typing import Dict, Any, Optional


def parse_decompression_json(response_text: str) -> Optional[Dict[str, Any]]:
    """Extract the JSON data block from the decompression report."""
    match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            print(f"Failed to parse decompression JSON: {e}")
    return None


def strip_json_block(response_text: str) -> str:
    """Remove the JSON block from the response text for clean display."""
    cleaned = re.sub(r'```json\s*.*?\s*```', '', response_text, flags=re.DOTALL)
    return cleaned.strip()
