"""Market data access layer.

This layer is intentionally thin: it fetches raw market data from data providers and
returns normalized dictionaries/dataframes for the service layer to consume.
"""
from __future__ import annotations

import time
from typing import Any

import pandas as pd
import yfinance as yf

from app.config import MARKET_CONFIG


def _fetch_with_retry(symbol: str, period: str, interval: str, retries: int = 3) -> pd.DataFrame:
    """Fetch ticker history with a lightweight retry loop."""
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            data = yf.Ticker(symbol).history(period=period, interval=interval, auto_adjust=False)
            if not data.empty:
                return data
        except Exception as exc:  # pragma: no cover - defensive fallback
            last_error = exc
        if attempt < retries - 1:
            time.sleep(0.5 * (attempt + 1))

    if last_error is not None:
        raise last_error
    return pd.DataFrame()


def _safe_price(symbol: str) -> dict[str, Any]:
    """Fetch a price snapshot for a ticker with graceful fallback."""
    try:
        hist = _fetch_with_retry(symbol, period="5d", interval="1d")
        if hist.empty:
            return {"price": "--", "change": "0.00%", "raw": 0.0, "change_value": 0.0}

        latest = hist.iloc[-1]
        prev = hist.iloc[-2] if len(hist) > 1 else latest
        price = float(latest["Close"]) if "Close" in latest else 0.0
        prev_close = float(prev["Close"]) if "Close" in prev and float(prev["Close"]) else price
        change = ((price - prev_close) / prev_close) * 100 if prev_close else 0.0

        return {
            "price": f"{price:,.2f}",
            "change": f"{change:+.2f}%",
            "raw": float(price),
            "change_value": float(change),
        }
    except Exception:
        return {"price": "--", "change": "0.00%", "raw": 0.0, "change_value": 0.0}


def fetch_market_snapshot() -> dict[str, Any]:
    """Fetch a normalized snapshot for the main macro indicators."""
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
        return _fetch_with_retry(symbol, period=period, interval=interval)
    except Exception:
        return pd.DataFrame()
