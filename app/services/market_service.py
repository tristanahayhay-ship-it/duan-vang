"""Service layer for market logic."""
from __future__ import annotations

from app.data.market_data import fetch_market_snapshot


def get_market_snapshot() -> dict:
    """Return a clean market snapshot for UI consumption."""
    raw = fetch_market_snapshot()
    return {
        "gold": {
            "price": raw["gold"].get("price", "--"),
            "change": raw["gold"].get("change", "0.00%"),
        },
        "dxy": {
            "price": raw["dxy"].get("price", "--"),
            "change": raw["dxy"].get("change", "0.00%"),
        },
        "us10y": {
            "price": raw["us10y"].get("price", "--"),
            "change": raw["us10y"].get("change", "0.00%"),
        },
        "vix": {
            "price": raw["vix"].get("price", "--"),
            "change": raw["vix"].get("change", "0.00%"),
        },
    }
