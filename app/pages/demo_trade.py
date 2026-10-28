"""Demo trading page."""
from __future__ import annotations

import streamlit as st


def render_demo_trade_page() -> None:
    st.title("Demo Trade")
    st.caption("Paper trading, vị thế giả, theo dõi PnL và chiến lược.")

    symbol = st.selectbox("Mã chứng khoán", ["XAUUSD", "SPY", "QQQ", "VNINDEX", "BTCUSD"])
    cash = st.number_input("Số dư demo", min_value=1000.0, value=100000.0, step=1000.0)
    units = st.number_input("Số lượng đơn vị", min_value=1, value=10, step=1)
    side = st.radio("Hướng", ["Mua", "Bán"])

    if st.button("Tạo vị thế demo"):
        st.success(f"Đã tạo vị thế demo: {side} {units} đơn vị {symbol} với vốn {cash:,.2f}")

    st.subheader("Portfolio Overview")
    st.dataframe(
        [
            {"Symbol": symbol, "Side": side, "Qty": units, "PnL": "+0.00%"},
            {"Symbol": "Gold", "Side": "Mua", "Qty": 2, "PnL": "+1.20%"},
        ]
    )
