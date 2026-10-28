"""Market data access layer."""
from __future__ import annotations

from typing import Any

import pandas as pd
import yfinance as yf

from app.config import CACHE_TTL_MEDIUM, MARKET_CONFIG


def _safe_price(symbol: str) -> dict[str, Any]:
    """Fetch a price snapshot for a ticker with graceful fallback."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", interval="1d")
        if hist.empty:
            return {"price": "--", "change": "0.00%"}

        latest = hist.iloc[-1]
        prev = hist.iloc[-2] if len(hist) > 1 else latest
        price = float(latest["Close"])
        change = ((price - float(prev["Close"])) / float(prev["Close"])) * 100

        return {
            "price": f"{price:,.2f}",
            "change": f"{change:+.2f}%",
            "raw": float(price),
            "change_value": float(change),
        }
    except Exception:
        return {"price": "--", "change": "0.00%", "raw": 0.0, "change_value": 0.0}


def fetch_market_snapshot() -> dict[str, Any]:
    """Fetch a normalized snapshot for major macro indicators."""
    return {
        "gold": _safe_price(MARKET_CONFIG.gold_symbol),
        "dxy": _safe_price(MARKET_CONFIG.dxy_symbol),
        "us10y": _safe_price(MARKET_CONFIG.us10y_symbol),
        "vix": _safe_price(MARKET_CONFIG.vix_symbol),
        "sp500": _safe_price(MARKET_CONFIG.sp500_symbol),
        "wti": _safe_price(MARKET_CONFIG.wti_symbol),
    }


def fetch_history(symbol: str, period: str = "90d", interval: str = "1d") -> pd.DataFrame:
    """Return price history as a DataFrame for charting."""
    try:
        return yf.Ticker(symbol).history(period=period, interval=interval)
    except Exception:
        return pd.DataFrame()
