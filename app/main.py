"""Main Streamlit entry point for the dashboard application."""
from __future__ import annotations

import streamlit as st

from app.config import APP_ICON, APP_TITLE
from app.pages.ai_analysis import render_ai_analysis_page
from app.pages.demo_trade import render_demo_trade_page
from app.pages.flow_of_funds import render_flow_of_funds_page
from app.pages.geopolitical import render_geopolitical_page
from app.pages.macro import render_macro_page
from app.pages.news import render_news_page
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
            "AI Analysis",
            "Demo Trade",
        ],
    )

    if menu == "Dashboard Tổng Quan":
        render_overview_page()
    elif menu == "Macro & Dữ Liệu Kinh Tế":
        render_macro_page()
    elif menu == "Dòng Tiền (Flow of Funds)":
        render_flow_of_funds_page()
    elif menu == "Tin Tức & Cổ Phiếu":
        render_news_page()
    elif menu == "Địa Chính Trị & Chiến Tranh":
        render_geopolitical_page()
    elif menu == "AI Analysis":
        render_ai_analysis_page()
    elif menu == "Demo Trade":
        render_demo_trade_page()
    else:
        render_overview_page()


if __name__ == "__main__":
    main()
