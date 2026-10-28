"""Overview page for the dashboard."""
from __future__ import annotations

import streamlit as st

from app.components.metric_cards import render_metric_cards
from app.services.market_service import get_market_snapshot


def render_overview_page() -> None:
    st.title("Dashboard Tổng Quan")
    st.caption("Bản khung kiến trúc mới: dữ liệu, service, UI được tách riêng để dễ mở rộng và bảo trì.")

    snapshot = get_market_snapshot()

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
    ]

    render_metric_cards(metrics)

    st.subheader("Tóm tắt hệ thống")
    st.markdown(
        """
        - Dữ liệu thị trường được tách ra một layer riêng để fetch và chuẩn hóa.
        - Service layer xử lý logic và định dạng dữ liệu cho UI.
        - UI page chỉ hiển thị dữ liệu và component.
        - Bước tiếp theo: thêm module Macro, News, AI Analysis, Demo Trade, và database.
        """
    )
