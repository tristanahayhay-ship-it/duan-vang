"""Macro and economic indicators page."""
from __future__ import annotations

import streamlit as st

from app.components.metric_cards import render_metric_cards
from app.services.market_service import get_market_snapshot


def render_macro_page() -> None:
    st.title("Macro & Dữ Liệu Kinh Tế")
    st.caption("Phân tích chỉ số kinh tế vĩ mô, lãi suất, tỷ giá, vàng và cảm xúc thị trường.")

    snapshot = get_market_snapshot()
    metrics = [
        {
            "label": "Gold",
            "value": snapshot["gold"]["price"],
            "delta": snapshot["gold"]["change"],
            "help": "Giá vàng thế giới",
        },
        {
            "label": "DXY",
            "value": snapshot["dxy"]["price"],
            "delta": snapshot["dxy"]["change"],
            "help": "Chỉ số đô la Mỹ",
        },
        {
            "label": "US 10Y",
            "value": snapshot["us10y"]["price"],
            "delta": snapshot["us10y"]["change"],
            "help": "Lãi suất trái phiếu Mỹ 10 năm",
        },
        {
            "label": "VIX",
            "value": snapshot["vix"]["price"],
            "delta": snapshot["vix"]["change"],
            "help": "Chỉ số lo ngại thị trường",
        },
    ]
    render_metric_cards(metrics)

    st.subheader("Macro context")
    st.markdown(
        """
        - Theo dõi xu hướng vàng, DXY, lãi suất 10Y và kỳ vọng FED.
        - Kết hợp các signal vĩ mô để định hướng triển vọng khi thị trường dao động.
        - Có thể mở rộng sang CPI, PPI, NFP, GDP, PMI, và lịch kinh tế theo thời gian.
        """
    )

    tab1, tab2, tab3 = st.tabs(["Market View", "Calendar", "Notes"])

    with tab1:
        st.info("Chức năng biểu đồ và lịch kinh tế có thể được bổ sung theo từng data source cụ thể.")
    with tab2:
        st.dataframe(
            [
                {"Date": "2026-10-28", "Event": "Fed decision", "Impact": "High"},
                {"Date": "2026-10-30", "Event": "CPI", "Impact": "High"},
                {"Date": "2026-11-02", "Event": "NFP", "Impact": "Medium"},
            ]
        )
    with tab3:
        st.write("Lưu ý: cập nhật dữ liệu macro cần tách riêng giữa real data và mock data để tránh nhầm lẫn." )
