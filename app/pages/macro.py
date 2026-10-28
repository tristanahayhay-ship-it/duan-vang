"""Overview page for the dashboard."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app.services.market_service import get_dashboard_summary, get_market_snapshot


def render_overview_page() -> None:
    st.title("Dashboard Tổng Quan")
    st.caption("Tổng quan thị trường theo dữ liệu real-time từ Yahoo Finance và layer service chuẩn hóa.")

    snapshot = get_market_snapshot()
    summary = get_dashboard_summary()

    metrics = [
        {
            "label": "Gold",
            "value": snapshot["gold"]["price"],
            "delta": snapshot["gold"]["change"],
            "help": "Giá vàng giao ngay",
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
        {
            "label": "S&P 500",
            "value": snapshot["sp500"]["price"],
            "delta": snapshot["sp500"]["change"],
            "help": "Chỉ số chứng khoán lớn nhất Mỹ",
        },
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

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Market sentiment")
        st.info(
            f"Bias hiện tại: <b>{summary['market_bias']}</b>. "
            "DXY, bond yield, gold và VIX là các biến số chính đang định hướng tâm lý thị trường.",
            icon="📊",
        )

        watchlist = pd.DataFrame(
            [
                {"Asset": "Gold", "Price": snapshot["gold"]["price"], "Change": snapshot["gold"]["change"]},
                {"Asset": "DXY", "Price": snapshot["dxy"]["price"], "Change": snapshot["dxy"]["change"]},
                {"Asset": "US 10Y", "Price": snapshot["us10y"]["price"], "Change": snapshot["us10y"]["change"]},
                {"Asset": "VIX", "Price": snapshot["vix"]["price"], "Change": snapshot["vix"]["change"]},
                {"Asset": "WTI", "Price": snapshot["wti"]["price"], "Change": snapshot["wti"]["change"]},
            ]
        )
        st.dataframe(watchlist, hide_index=True, use_container_width=True)

    with right_col:
        st.subheader("AI summary")
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #0f172a, #111827); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 12px; color: #e2e8f0;">
                <strong>Macro read:</strong><br>
                Gold đang là tâm điểm nếu DXY đi xuống và yield không tăng quá mạnh. <br><br>
                <strong>Market score:</strong> {summary['score']}/100<br>
                <strong>Bias:</strong> {summary['market_bias']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("Quick notes")
        st.markdown(
            """
            - Track gold vs DXY
            - Watch US 10Y and real yield
            - Use VIX as risk-off sentiment proxy
            - Keep an eye on oil when inflation risk rises
            """
        )

    st.markdown("---")
    st.subheader("Portfolio / market checklist")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("Gold: risk hedge / safe-haven")
    with col2:
        st.warning("DXY: USD strength is the main pressure valve")
    with col3:
        st.info("10Y yield: key signal for real-rate pressure")

    st.markdown("---")
    st.caption("Bản kiến trúc này đã tách riêng: dữ liệu → service → UI để dễ nâng cấp và bảo trì.")
