"""Flow-of-funds / smart money page."""
from __future__ import annotations

import streamlit as st

from app.components.metric_cards import render_metric_cards


def render_flow_of_funds_page() -> None:
    st.title("Dòng Tiền (Flow of Funds)")
    st.caption("Theo dõi dòng tiền, xu hướng tổ chức, và sự phân kỳ giữa thị trường tài sản.")

    metrics = [
        {"label": "ETF Flow", "value": "+$2.1B", "delta": "+1.8%", "help": "Dòng tiền quỹ ETF"},
        {"label": "Smart Money", "value": "Bullish", "delta": "+0.5", "help": "Xu hướng tổ chức"},
        {"label": "Risk Appetite", "value": "Moderate", "delta": "+1.2", "help": "Mức độ chấp nhận rủi ro"},
        {"label": "Correlation", "value": "0.74", "delta": "+0.06", "help": "Tương quan giữa các tài sản"},
    ]
    render_metric_cards(metrics)

    st.dataframe(
        [
            {"Asset": "Gold", "Flow": "+$800M", "Trend": "Up"},
            {"Asset": "USD", "Flow": "-$1.2B", "Trend": "Down"},
            {"Asset": "Equity", "Flow": "+$1.4B", "Trend": "Up"},
        ]
    )
