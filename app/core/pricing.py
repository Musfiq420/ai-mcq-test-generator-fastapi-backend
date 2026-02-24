# app/core/pricing.py

"""
OpenAI model pricing (USD per 1M tokens)

Supports:
- input tokens
- cached input tokens
- output tokens
"""

from typing import Optional

# USD per 1M tokens
MODEL_PRICING = {
    "gpt-5.2": {"input": 1.75, "cached_input": 0.175, "output": 14.00},
    "gpt-5.1": {"input": 1.25, "cached_input": 0.125, "output": 10.00},
    "gpt-5": {"input": 1.25, "cached_input": 0.125, "output": 10.00},
    "gpt-5-mini": {"input": 0.25, "cached_input": 0.025, "output": 2.00},
    "gpt-5-nano": {"input": 0.05, "cached_input": 0.005, "output": 0.40},

    "gpt-5.2-chat-latest": {"input": 1.75, "cached_input": 0.175, "output": 14.00},
    "gpt-5.1-chat-latest": {"input": 1.25, "cached_input": 0.125, "output": 10.00},
    "gpt-5-chat-latest": {"input": 1.25, "cached_input": 0.125, "output": 10.00},

    "gpt-5.2-codex": {"input": 1.75, "cached_input": 0.175, "output": 14.00},
    "gpt-5.1-codex-max": {"input": 1.25, "cached_input": 0.125, "output": 10.00},
    "gpt-5.1-codex": {"input": 1.25, "cached_input": 0.125, "output": 10.00},
    "gpt-5-codex": {"input": 1.25, "cached_input": 0.125, "output": 10.00},

    "gpt-5.2-pro": {"input": 21.00, "cached_input": None, "output": 168.00},
    "gpt-5-pro": {"input": 15.00, "cached_input": None, "output": 120.00},

    "gpt-4.1": {"input": 2.00, "cached_input": 0.50, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "cached_input": 0.10, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "cached_input": 0.025, "output": 0.40},

    "gpt-4o": {"input": 2.50, "cached_input": 1.25, "output": 10.00},
    "gpt-4o-2024-05-13": {"input": 5.00, "cached_input": None, "output": 15.00},
    "gpt-4o-mini": {"input": 0.15, "cached_input": 0.075, "output": 0.60},

    "gpt-realtime": {"input": 4.00, "cached_input": 0.40, "output": 16.00},
    "gpt-realtime-mini": {"input": 0.60, "cached_input": 0.06, "output": 2.40},

    "gpt-audio": {"input": 2.50, "cached_input": None, "output": 10.00},
    "gpt-audio-mini": {"input": 0.60, "cached_input": None, "output": 2.40},

    "o1": {"input": 15.00, "cached_input": 7.50, "output": 60.00},
    "o1-pro": {"input": 150.00, "cached_input": None, "output": 600.00},
    "o3-pro": {"input": 20.00, "cached_input": None, "output": 80.00},
    "o3": {"input": 2.00, "cached_input": 0.50, "output": 8.00},
    "o3-deep-research": {"input": 10.00, "cached_input": 2.50, "output": 40.00},

    "o4-mini": {"input": 1.10, "cached_input": 0.275, "output": 4.40},
    "o4-mini-deep-research": {"input": 2.00, "cached_input": 0.50, "output": 8.00},
    "o3-mini": {"input": 1.10, "cached_input": 0.55, "output": 4.40},
    "o1-mini": {"input": 1.10, "cached_input": 0.55, "output": 4.40},
}


TOKENS_PER_MILLION = 1_000_000


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: Optional[int] = 0,
):
    """
    Calculate cost in USD.

    Args:
        model: model name
        input_tokens: total input tokens
        output_tokens: output tokens
        cached_input_tokens: cached tokens if provided by API

    Returns:
        dict with cost breakdown
    """

    if model not in MODEL_PRICING:
        raise ValueError(f"Pricing not defined for model: {model}")

    pricing = MODEL_PRICING[model]

    # split cached vs normal input
    cached_input_tokens = cached_input_tokens or 0
    normal_input_tokens = max(input_tokens - cached_input_tokens, 0)

    # costs
    input_cost = (normal_input_tokens / TOKENS_PER_MILLION) * pricing["input"]

    cached_cost = 0
    if pricing["cached_input"] is not None:
        cached_cost = (
            cached_input_tokens / TOKENS_PER_MILLION
        ) * pricing["cached_input"]

    output_cost = (output_tokens / TOKENS_PER_MILLION) * pricing["output"]

    total_cost = input_cost + cached_cost + output_cost

    return {
        "input_cost_usd": round(input_cost, 6),
        "cached_input_cost_usd": round(cached_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(total_cost, 6),
    }