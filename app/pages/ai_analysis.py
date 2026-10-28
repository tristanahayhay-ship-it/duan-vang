"""AI analysis page for generating macro summary."""
from __future__ import annotations

import streamlit as st

from app.services.gemini_service import summarize_macro_context


def render_ai_analysis_page() -> None:
    st.title("AI Analysis")
    st.caption("Nhận định theo bối cảnh macro, vàng, lãi suất, DXY và tin tức thị trường.")

    context = st.text_area(
        "Nhập bối cảnh phân tích",
        value=(
            "Gold đang giữ mức hỗ trợ quan trọng; DXY suy yếu; lãi suất 10Y tăng vừa phải; "
            "vốn chờ Fed và dữ liệu việc làm."
        ),
        height=180,
    )

    if st.button("Tạo nhận định AI"):
        result = summarize_macro_context(context)
        st.markdown("### Kết quả AI")
        st.write(result)
