"""OpenRouter API client for making LLM requests."""

import httpx
import asyncio
from typing import List, Dict, Any, Optional
from .config import OPENROUTER_API_KEY, OPENROUTER_API_URL


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    system_prompt: Optional[str] = None,
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via OpenRouter API.

    Args:
        model: OpenRouter model identifier (e.g., "anthropic/claude-sonnet-4.5")
        messages: List of message dicts with 'role' and 'content'
        system_prompt: Optional system prompt to prepend
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    full_messages = messages
    if system_prompt:
        full_messages = [{"role": "system", "content": system_prompt}] + messages

    payload = {
        "model": model,
        "messages": full_messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }

    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel (legacy helper, kept for compatibility).
    """
    tasks = [query_model(model, messages) for model in models]
    responses = await asyncio.gather(*tasks)
    return {model: response for model, response in zip(models, responses)}


async def query_agents_parallel(
    agents: List[Dict[str, Any]],
    messages: List[Dict[str, str]],
    model: str
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple cognitive agents in parallel using the same base model but different system prompts.

    Args:
        agents: List of agent dicts, each with 'key' and 'system_prompt'
        messages: List of message dicts to send to each agent
        model: The base model to use for all agents

    Returns:
        Dict mapping agent key to response dict (or None if failed)
    """
    tasks = [
        query_model(model, messages, agent.get('system_prompt'))
        for agent in agents
    ]
    responses = await asyncio.gather(*tasks)
    return {agent['key']: response for agent, response in zip(agents, responses)}
