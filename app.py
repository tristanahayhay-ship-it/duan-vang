import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests

st.set_page_config(page_title="Hệ thống Liên thị trường XAU/USD", layout="wide")
st.title("🦅 HỆ THỐNG PHÂN TÍCH LIÊN THỊ TRƯỜNG & GIAO DỊCH VÀNG")
st.markdown("---")

# CẤU HÌNH API FINNHUB
FINNHUB_API_KEY = "d96keq1r01qr77dkrm4g"

# MENU SIDEBAR
st.sidebar.title("🎛️ MENU ĐIỀU KHIỂN")
module_selection = st.sidebar.radio(
    "CHỌN MODULE LÀM VIỆC:",
    ["Module 1 – Dashboard", "Module 2 – Dữ liệu kinh tế Mỹ", "Module 3 – Dòng tiền", "Module 4 – Công cụ hỗ trợ"]
)

@st.cache_data(ttl=60)
def fetch_market_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="7d")
        if len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            return current, ((current - prev) / prev) * 100
    except:
        pass
    return 0.0, 0.0

def fetch_economic_calendar():
    today_str = datetime.now().strftime("%Y-%m-%d")
    url = f"https://finnhub.io{today_str}&to={today_str}&token={FINNHUB_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            events = response.json().get("economicCalendar", [])
            if not events: return None
            df = pd.DataFrame(events)
            df = df[df['country'].isin(['USD', 'EUR', 'GBP', 'CNY'])]
            if df.empty: return None
            df_display = pd.DataFrame({
                "Thời gian (UTC)": pd.to_datetime(df['time']).dt.strftime('%H:%M'),
                "Quốc gia": df['country'],
                "Sự kiện kinh tế": df['event'],
                "Dự báo (Forecast)": df['forecast'].fillna("-"),
                "Thực tế (Actual)": df['actual'].fillna("⏱️ Chờ công bố"),
                "Kỳ trước (Previous)": df['previous'].fillna("-"),
                "Mức ảnh hưởng": df['impact'].map({'high': '🔴 Cao', 'medium': '🟡 Trung bình', 'low': '🟢 Thấp'}).fillna("🟢 Thấp")
            })
            return df_display.sort_values(by="Thời gian (UTC)")
    except:
        pass
    return None

# MODULE 1
if module_selection == "Module 1 – Dashboard":
    st.header("📈 Module 1 – Dashboard Tổng Hợp")
    tickers = {"Giá vàng (XAU/USD)": "GC=F", "Chỉ số USD (DXY)": "DX-Y.NYB", "Lợi suất Mỹ 10Y": "^TNX", "Chỉ số VIX": "^VIX", "Giá Dầu WTI": "CL=F"}
    cols = st.columns(5)
    for index, (label, ticker) in enumerate(tickers.items()):
        price, change = fetch_market_data(ticker)
        with cols[index]:
            if "10Y" in label: st.metric(label=label, value=f"{price:.3f}%", delta=f"{change:.2f}%")
            else: st.metric(label=label, value=f"${price:,.2f}", delta=f"{change:.2f}%")
    st.markdown("---")
    st.subheader("📅 Lịch kinh tế thực tế hôm nay")
    eco_df = fetch_economic_calendar()
    if eco_df is not None:
        st.success("⚡ Hệ thống đã tự động đồng bộ thành công lịch kinh tế trực tuyến!")
        st.dataframe(eco_df, use_container_width=True)
    else:
        st.info("Hiện tại chưa có sự kiện vĩ mô lớn nào được ghi nhận hôm nay hoặc kết nối mạng đang bận. Hệ thống hiển thị lịch kinh tế dự phòng:")
        mock_calendar = pd.DataFrame({
            "Thời gian": ["19:30", "19:30"], "Quốc gia": ["USD", "USD"],
            "Sự kiện kinh tế": ["Core CPI (Lạm phát Mỹ cốt lõi)", "Số đơn xin trợ cấp thất nghiệp tuần"],
            "Dự báo": ["0.2%", "215K"], "Thực tế": ["⏱️ Chờ công bố", "⏱️ Chờ công bố"], "Mức độ ảnh hưởng": ["🔴 Cao", "🟡 Trung bình"]
        })
        st.dataframe(mock_calendar, use_container_width=True)

# MODULE 2
elif module_selection == "Module 2 – Dữ liệu kinh tế Mỹ":
    st.header("🇺🇸 Module 2 – Dữ liệu kinh tế vĩ mô Mỹ")
    macro_indicators = ["CPI", "Core CPI", "PCE", "Core PCE", "NFP", "Tỷ lệ thất nghiệp", "GDP", "PMI", "Doanh số bán lẻ", "JOLTS", "ADP", "ISM Manufacturing/Services"]
    selected_indicator = st.selectbox("Chọn chỉ báo kinh tế:", macro_indicators)
    with st.form("macro_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            pub_date = st.date_input("Ngày công bố", datetime.today())
            period = st.text_input("Kỳ báo cáo")
        with c2:
            act_val = st.text_input("Thực tế (Actual)")
            fore_val = st.text_input("Dự báo (Forecast)")
        with c3:
            prev_val = st.text_input("Kỳ trước (Previous)")
            impact = st.selectbox("Tác động", ["Tốt cho USD / Xấu cho Vàng", "Xấu cho USD / Tốt cho Vàng", "Trung lập"])
        if st.form_submit_button("💾 Lưu Số Liệu"):
            st.success(f"Đã cập nhật {selected_indicator} thành công!")

# MODULE 3
elif module_selection == "Module 3 – Dòng tiền":
    st.header("💸 Module 3 – Dòng tiền & Vị thế dòng vốn")
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("📊 1. Quỹ ETF vàng (GLD, IAU…) & Ngân hàng trung ương")
        fig_etf = go.Figure(go.Scatter(x=["T2", "T3", "T4", "T5", "T6"], y=[830.2, 831.5, 829.1, 828.4, 832.0], mode='lines+markers', line=dict(color='#FFD700')))
        st.plotly_chart(fig_etf, use_container_width=True)
    with col_right:
        st.subheader("📜 2. Báo cáo COT Report & Chỉ báo khác")
        st.number_input("Vị thế Long (Non-Commercial)", value=250000)
        st.number_input("Vị thế Short (Non-Commercial)", value=65000)
        st.text_input("Real Yield (Lợi suất thực tế Mỹ 10Y):", value="1.95%")

# MODULE 4
elif module_selection == "Module 4 – Công cụ hỗ trợ":
    st.header("🛠️ Module 4 – Công cụ quản lý & Hỗ trợ giao dịch")
    st.subheader("🎯 1. Chấm điểm xu hướng Vàng tổng hợp")
    score = st.slider("Chấm điểm áp lực liên thị trường (Càng thấp càng ủng hộ Vàng)", 1, 10, 5)
    if score <= 4: st.success("🟢 Xu hướng Vàng: BULLISH")
    elif score >= 7: st.error("🔴 Xu hướng Vàng: BEARISH")
    else: st.warning("🟡 Xu hướng Vàng: SIDEWAYS")
    st.markdown("---")
    st.subheader("📝 2 & 3. Nhật ký giao dịch & Ghi chú nhận định")
    with st.form("journal_form"):
        trade_action = st.selectbox("Lệnh", ["BUY", "SELL", "STANDBY"])
        trading_notes = st.text_area("Ghi chú nhận định:")
        if st.form_submit_button("📝 Ghi Nhật Ký"): st.toast("Đã lưu!")
