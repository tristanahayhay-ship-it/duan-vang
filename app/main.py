"""Main Streamlit entry point for the dashboard application."""
from __future__ import annotations

import streamlit as st

from app.config import APP_ICON, APP_TITLE
from app.pages.overview import render_overview_page


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title(f"{APP_ICON} {APP_TITLE}")
    menu = st.sidebar.radio(
        "Chọn chuyên mục:",
        [
            "Dashboard Tổng Quan",
            "Macro & Dữ Liệu Kinh Tế",
            "Dòng Tiền (Flow of Funds)",
            "Tin Tức & Cổ Phiếu",
            "Địa Chính Trị & Chiến Tranh",
            "Demo Trade",
        ],
    )

    if menu == "Dashboard Tổng Quan":
        render_overview_page()
    else:
        st.info(f"Chuyên mục '{menu}' đang được chuẩn hóa trong cấu trúc mới. Vui lòng tiếp tục phát triển theo từng page module riêng.")


if __name__ == "__main__":
    main()
