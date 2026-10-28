"""Curated data layer for news and macro content."""
from __future__ import annotations

from typing import Any


def get_demo_news_feed() -> list[dict[str, Any]]:
    """Return sample market/news records used before live feed integration."""
    return [
        {"title": "Gold holds above key support", "source": "Demo Feed", "summary": "Bullish continuation supported by weaker USD and stronger safe haven demand."},
        {"title": "US 10Y yield near range high", "source": "Demo Feed", "summary": "Rates remain a key driver for risk sentiment and gold pricing."},
        {"title": "Vietnam market watch", "source": "Demo Feed", "summary": "Local sentiment depends on policy clarity and foreign fund flows."},
    ]
