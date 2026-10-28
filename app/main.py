"""Macro and economic indicators page."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app.services.market_service import get_market_snapshot


def render_macro_page() -> None:
    st.title("Macro & Dữ Liệu Kinh Tế")
    st.caption("Theo dõi diễn biến kinh tế vĩ mô, lãi suất, USD và vàng trong một dashboard có cấu trúc rõ ràng.")

    snapshot = get_market_snapshot()

    metrics = [
        {"label": "Gold", "value": snapshot["gold"]["price"], "delta": snapshot["gold"]["change"], "help": "Giá vàng thế giới"},
        {"label": "DXY", "value": snapshot["dxy"]["price"], "delta": snapshot["dxy"]["change"], "help": "Sức mạnh USD"},
        {"label": "US 10Y", "value": snapshot["us10y"]["price"], "delta": snapshot["us10y"]["change"], "help": "Lãi suất 10 năm"},
        {"label": "VIX", "value": snapshot["vix"]["price"], "delta": snapshot["vix"]["change"], "help": "Cảm xúc rủi ro"},
    ]

    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            st.metric(
                label=metric["label"],
                value=metric["value"],
                delta=metric["delta"],
                help=metric["help"],
            )

    st.markdown("---")

    macro_table = pd.DataFrame(
        [
            {"Indicator": "Gold", "Value": snapshot["gold"]["price"], "Signal": "Bullish if DXY weakens"},
            {"Indicator": "DXY", "Value": snapshot["dxy"]["price"], "Signal": "Strong USD = pressure on gold"},
            {"Indicator": "US 10Y", "Value": snapshot["us10y"]["price"], "Signal": "Yield trend matters for real rates"},
            {"Indicator": "VIX", "Value": snapshot["vix"]["price"], "Signal": "Risk sentiment pressure"},
        ]
    )

    st.subheader("Macro signal board")
    st.dataframe(macro_table, hide_index=True, use_container_width=True)

    st.subheader("Economic calendar (sample)")
    st.dataframe(
        pd.DataFrame(
            [
                {"Date": "2026-10-28", "Event": "Fed decision", "Impact": "High"},
                {"Date": "2026-10-30", "Event": "CPI", "Impact": "High"},
                {"Date": "2026-11-02", "Event": "Payrolls", "Impact": "High"},
                {"Date": "2026-11-10", "Event": "GDP", "Impact": "Medium"},
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.caption("Mục đích của page này là tập trung vào logic macro: DXY, yield, VIX, gold và event calendar theo thời gian.")
