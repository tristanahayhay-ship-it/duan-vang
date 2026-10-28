"""Service layer for market logic."""
from __future__ import annotations

from typing import Any

from app.data.market_data import fetch_history, fetch_market_snapshot


def _safe_metric(value: Any, default: str = "--") -> str:
    return value if value is not None else default


def get_market_snapshot() -> dict[str, dict[str, str]]:
    """Return a clean market snapshot for UI consumption."""
    raw = fetch_market_snapshot()
    return {
        "gold": {
            "price": _safe_metric(raw["gold"].get("price", "--")),
            "change": _safe_metric(raw["gold"].get("change", "0.00%")),
            "raw": raw["gold"].get("raw", 0.0),
        },
        "dxy": {
            "price": _safe_metric(raw["dxy"].get("price", "--")),
            "change": _safe_metric(raw["dxy"].get("change", "0.00%")),
            "raw": raw["dxy"].get("raw", 0.0),
        },
        "us10y": {
            "price": _safe_metric(raw["us10y"].get("price", "--")),
            "change": _safe_metric(raw["us10y"].get("change", "0.00%")),
            "raw": raw["us10y"].get("raw", 0.0),
        },
        "vix": {
            "price": _safe_metric(raw["vix"].get("price", "--")),
            "change": _safe_metric(raw["vix"].get("change", "0.00%")),
            "raw": raw["vix"].get("raw", 0.0),
        },
        "sp500": {
            "price": _safe_metric(raw["sp500"].get("price", "--")),
            "change": _safe_metric(raw["sp500"].get("change", "0.00%")),
            "raw": raw["sp500"].get("raw", 0.0),
        },
        "wti": {
            "price": _safe_metric(raw["wti"].get("price", "--")),
            "change": _safe_metric(raw["wti"].get("change", "0.00%")),
            "raw": raw["wti"].get("raw", 0.0),
        },
    }


def get_market_history(symbol: str, period: str = "90d", interval: str = "1d"):
    """Return a clean history frame for a selected symbol."""
    hist = fetch_history(symbol, period=period, interval=interval)
    if hist.empty:
        return hist
    return hist[["Close"]].copy().rename(columns={"Close": "close"})


def get_dashboard_summary() -> dict[str, Any]:
    """Return a compact summary used by the overview page."""
    snapshot = get_market_snapshot()

    def to_float(value: Any) -> float:
        try:
            return float(str(value).replace(",", ""))
        except Exception:
            return 0.0

    gold_price = to_float(snapshot["gold"]["price"])
    dxy_price = to_float(snapshot["dxy"]["price"])
    us10y_price = to_float(snapshot["us10y"]["price"])
    vix_price = to_float(snapshot["vix"]["price"])

    if gold_price and dxy_price:
        risk_bias = "Bullish Gold" if gold_price > 2000 and dxy_price < 105 else "Neutral"
    else:
        risk_bias = "Neutral"

    return {
        "market_bias": risk_bias,
        "gold": snapshot["gold"],
        "dxy": snapshot["dxy"],
        "us10y": snapshot["us10y"],
        "vix": snapshot["vix"],
        "sp500": snapshot["sp500"],
        "wti": snapshot["wti"],
        "score": 58 if risk_bias == "Bullish Gold" else 50,
    }
