"""News and market headlines page."""
from __future__ import annotations

import streamlit as st

from app.services.news_service import fetch_market_news


def render_news_page() -> None:
    st.title("Tin Tức & Cổ Phiếu")
    st.caption("Tin tức tài chính, thị trường và cổ phiếu được sắp xếp theo danh mục và độ ưu tiên.")

    category = st.selectbox("Chọn danh mục", ["business", "technology", "general", "health", "sports"])
    articles = fetch_market_news(category)

    for idx, article in enumerate(articles, start=1):
        with st.container():
            st.markdown(f"### {idx}. {article.get('title', 'Untitled article')}")
            st.caption(f"Nguồn: {article.get('source', 'n/a')}")
            st.write(article.get('summary', article.get('description', 'No summary available.')))
            st.markdown("---")
