"""News fetching service."""
from __future__ import annotations

from typing import Any

import requests

from app.config import NEWS_API_KEY


def fetch_market_news(category: str = "business") -> list[dict[str, Any]]:
    """Return a list of headlines from NewsAPI when configured; otherwise use demo fallback."""
    api_key = NEWS_API_KEY or None
    if not api_key:
        return [
            {"title": "News source not configured", "source": "local", "summary": "Add NEWS_API_KEY to enable live headlines."},
            {"title": "Macro trend watch", "source": "demo", "summary": "DXY, gold, and bond yields are the key macro drivers to monitor."},
        ]

    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {"category": category, "country": "us", "apiKey": api_key}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
        return payload.get("articles", [])[:5]
    except Exception:
        return [
            {"title": "Fallback news feed", "source": "fallback", "summary": "Unable to reach news API, using local fallback."}
        ]
