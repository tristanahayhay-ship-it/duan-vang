"""Geopolitical risk page."""
from __future__ import annotations

import streamlit as st


def render_geopolitical_page() -> None:
    st.title("Địa Chính Trị & Chiến Tranh")
    st.caption("Theo dõi rủi ro địa chính trị, xung đột và tác động lên thị trường tài chính.")

    risk_level = st.slider("Risk score", 0, 100, 58)
    st.progress(risk_level)

    st.subheader("Market impact snapshot")
    st.dataframe(
        [
            {"Driver": "Oil price", "Impact": "High", "Bias": "Risk-off"},
            {"Driver": "Risk sentiment", "Impact": "Medium", "Bias": "Cautious"},
            {"Driver": "Gold demand", "Impact": "High", "Bias": "Safe-haven"},
        ]
    )

    st.write("Mô hình này có thể phát triển thành bảng tin chiến tranh, bản đồ địa lý, và tín hiệu ảnh hưởng đến dầu, vàng, USD.")
