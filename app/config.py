"""App configuration and defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass

APP_TITLE = "Kinh Tế Vĩ Mô & Giá Vàng"
APP_ICON = "📈"

DEFAULT_TZ = "Asia/Ho_Chi_Minh"
API_TIMEOUT = 10
CACHE_TTL_SHORT = 30
CACHE_TTL_MEDIUM = 120
CACHE_TTL_LONG = 600

DEFAULT_SYMBOLS = {
    "gold": "GC=F",
    "dxy": "DX-Y.NYB",
    "us10y": "^TNX",
    "vix": "^VIX",
    "sp500": "^GSPC",
    "wti": "CL=F",
    "vn_index": "^VNINDEX",
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")


@dataclass
class MarketConfig:
    gold_symbol: str = DEFAULT_SYMBOLS["gold"]
    dxy_symbol: str = DEFAULT_SYMBOLS["dxy"]
    us10y_symbol: str = DEFAULT_SYMBOLS["us10y"]
    vix_symbol: str = DEFAULT_SYMBOLS["vix"]
    sp500_symbol: str = DEFAULT_SYMBOLS["sp500"]
    wti_symbol: str = DEFAULT_SYMBOLS["wti"]
    vn_index_symbol: str = DEFAULT_SYMBOLS["vn_index"]


MARKET_CONFIG = MarketConfig()
