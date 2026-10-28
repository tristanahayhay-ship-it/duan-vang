"""Vietnam gold pricing demo data layer."""
from __future__ import annotations

from typing import Any


def get_vietnam_gold_prices() -> dict[str, Any]:
    """Return a simple fallback for gold prices in VN context."""
    return {
        "buy": 94000,
        "sell": 96000,
        "last_update": "N/A",
    }
