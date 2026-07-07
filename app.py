import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests

# 1. CẤU HÌNH TRANG CHUẨN
st.set_page_config(page_title="Hệ thống Vĩ mô & Liên thị trường XAU/USD", layout="wide", initial_sidebar_state="expanded")
st.title("🦅 HỆ THỐNG PHÂN TÍCH VĨ MÔ TOÀN CẢNH & GIAO DỊCH VÀNG")
st.markdown("---")

# 2. CẤU HÌNH API & BẢO MẬT
FINNHUB_API_KEY = st.secrets.get("FINNHUB_API_KEY", "d96keq1r01qr77dkrm4g")

# 3. KHỞI TẠO DỮ LIỆU ĐỘNG (SESSION STATE) ĐỂ TRÁNH MẤT DỮ LIỆU KHI LÀM MỚI TRANG
if "macro_history" not in st.session_state:
    # Khởi tạo dữ liệu lịch sử cho các chỉ số vĩ mô Mỹ (Mô phỏng chu kỳ 3 kỳ gần nhất)
    st.session_state.macro_history = pd.DataFrame([
        {"Chỉ báo": "CPI", "Kỳ": "Tháng 05/2026", "Thực tế": 3.2, "Dự báo": 3.1, "Kỳ trước": 3.4, "Tác động": "Tốt cho USD / Xấu cho Vàng"},
        {"Chỉ báo": "CPI", "Kỳ": "Tháng 04/2026", "Thực tế": 3.4, "Dự báo": 3.4, "Kỳ trước": 3.5, "Tác động": "Trung lập"},
        {"Chỉ báo": "NFP", "Kỳ": "Tháng 05/2026", "Thực tế": 175, "Dự báo": 185, "Kỳ trước": 210, "Tác động": "Xấu cho USD / Tốt cho Vàng"},
        {"Chỉ báo": "GDP", "Kỳ": "Q1/2026", "Thực tế": 1.6, "Dự báo": 2.0, "Kỳ trước": 3.4, "Tác động": "Xấu cho USD / Tốt cho Vàng"},
    ])

if "journal" not in st.session_state:
    st.session_state.journal = []

# 4. HÀM TẢI DỮ LIỆU THỊ TRƯỜNG & VẼ BIỂU ĐỒ 
@st.cache_data(ttl=300)
def get_market_data_with_chart(ticker_symbol, name, period="3mo"):
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period)
        if not df.empty:
            current = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            change = ((current - prev) / prev) * 100
            
            # Tạo biểu đồ đường thẳng thu nhỏ (Sparkline/Trend)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', line=dict(color='#FFD700' if "Vàng" in name else '#1f77b4', width=2)))
            fig.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=150,
                xaxis=dict(visible=False),
                yaxis=dict(visible=True),
                template="plotly_dark"
            )
            return current, change, fig
    except Exception:
        pass
    return 0.0, 0.0, None

# 5. MENU CHÍNH TẠI SIDEBAR
st.sidebar.title("🎛️ KHÔNG GIAN LÀM VIỆC")
module = st.sidebar.radio(
    "CHỌN MODULE PHÂN TÍCH:",
    [
        "📊 Dashboard Tổng Hợp",
        "🇺🇸 Dữ Liệu Kinh Tế Mỹ",
        "💸 Dòng Tiền & Vị Thế Vốn",
        "📈 Tin Tức & Cổ Phiếu",
        "🪖 Tin Tức Chiến Tranh",
        "🛠️ Công Cụ Hỗ Trợ Giao Dịch"
    ]
)

# ==========================================
# MODULE 1: DASHBOARD TỔNG HỢP
# ==========================================
if module == "📊 Dashboard Tổng Hợp":
    st.header("📊 Dashboard Theo Dõi Các Tài Sản Liên Thị Trường")
    
    assets = {
        "Giá vàng (XAU/USD)": "GC=F",
        "Chỉ số USD (DXY)": "DX-Y.NYB",
        "Lợi suất Mỹ 10Y": "^TNX",
        "Chỉ số Biến động VIX": "^VIX",
        "Giá Dầu Thô WTI": "CL=F"
    }
    
    # Hiển thị Metric kèm Biểu đồ mini cho từng tài sản
    for label, ticker in assets.items():
        price, change, fig = get_market_data_with_chart(ticker, label)
        c_metric, c_chart = st.columns([1, 2])
        with c_metric:
            suffix = "%" if "10Y" in label else ""
            prefix = "" if "10Y" in label or "DXY" in label or "VIX" in label else "$"
            st.metric(label=label, value=f"{prefix}{price:,.2f}{suffix}", delta=f"{change:.2f}%")
        with c_chart:
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True, key=f"chart_{ticker}")
        st.markdown("<hr style='margin:0.5em 0px;'>", unsafe_allow_html=True)

    st.subheader("📅 Lịch kinh tế tiêu điểm hôm nay")
    # Giao diện hiển thị lịch kinh tế mẫu chuyên nghiệp
    mock_calendar = pd.DataFrame({
        "Thời gian": ["19:30", "19:30", "21:00"], 
        "Quốc gia": ["USD", "USD", "USD"],
        "Sự kiện kinh tế": ["Core CPI m/m (Chỉ số lạm phát lõi)", "Yêu cầu trợ cấp thất nghiệp lần đầu", "Doanh số bán nhà xây mới"],
        "Dự báo": ["0.3%", "215K", "680K"], 
        "Thực tế": ["⏱️ 19:30 Công bố", "⏱️ 19:30 Công bố", "⏱️ 21:00 Công bố"], 
        "Tác động dự kiến": ["🔴 Biến động mạnh", "🟡 Biến động vừa", "🟢 Biến động thấp"]
    })
    st.dataframe(mock_calendar, use_container_width=True, hide_index=True)
    
    st.subheader("💡 Phân tích vĩ mô ngắn hạn & Kết luận xu hướng")
    st.info("**Nhận định:** DXY đang có dấu hiệu tích lũy quanh vùng 104.5 trong khi Lợi suất 10Y giảm nhẹ hỗ trợ cho giá Vàng giữ vững trên mốc tâm lý. Chiến lược chủ đạo trong phiên: **Ưu tiên canh Mua (Bullish) khi giá điều chỉnh kỹ thuật.**")

# ==========================================
# MODULE 2: DỮ LIỆU KINH TẾ MỸ
# ==========================================
elif module == "🇺🇸 Dữ Liệu Kinh Tế Mỹ":
    st.header("🇺🇸 Bộ Cơ Sở Dữ Liệu Kinh Tế Vĩ Mô Mỹ")
    
    macro_indicators = ["CPI", "Core CPI", "PCE", "Core PCE", "NFP", "Tỷ lệ thất nghiệp", "GDP", "PMI", "Doanh số bán lẻ", "JOLTS", "ADP", "ISM Manufacturing/Services"]
    selected_ind = st.selectbox("🎯 Chọn chỉ số vĩ mô để theo dõi chu kỳ:", macro_indicators)
    
    # Bộ lọc hiển thị lịch sử của chỉ số đã chọn
    filtered_df = st.session_state.macro_history[st.session_state.macro_history["Chỉ báo"] == selected_ind]
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader(f"📊 Bảng dữ liệu lịch sử: {selected_ind}")
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.warning("Chưa có dữ liệu nhập cho chỉ số này. Hãy điền form bên dưới để cập nhật tự động.")
            
    with col2:
        st.subheader("📈 Biểu đồ diễn biến chu kỳ")
        if not filtered_df.empty:
            fig_macro = px.bar(filtered_df, x="Kỳ", y="Thực tế", text_auto=True, title=f"Giá trị thực tế qua các kỳ - {selected_ind}", color_discrete_sequence=['#1f77b4'])
            st.plotly_chart(fig_macro, use_container_width=True)
        else:
            st.info("Biểu đồ sẽ hiển thị khi có dữ liệu.")

    st.markdown("---")
    st.subheader("📥 Cập nhật số liệu mới (Điền Form tự động vẽ lại biểu đồ)")
    with st.form("macro_entry", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            in_key = st.text_input("Kỳ báo cáo (Ví dụ: Tháng 06/2026)")
            in_act = st.number_input("Giá trị Thực tế (Actual)", value=0.0, step=0.1)
        with c2:
            in_fore = st.number_input("Giá trị Dự báo (Forecast)", value=0.0, step=0.1)
            in_prev = st.number_input("Giá trị Kỳ trước (Previous)", value=0.0, step=0.1)
        with c3:
            in_impact = st.selectbox("Tác động thực tế", ["Tốt cho USD / Xấu cho Vàng", "Xấu cho USD / Tốt cho Vàng", "Trung lập"])
            
        if st.form_submit_button("💾 Xác nhận và Đồng bộ biểu đồ"):
            new_row = {"Chỉ báo": selected_ind, "Kỳ": in_key, "Thực tế": in_act, "Dự báo": in_fore, "Kỳ trước": in_prev, "Tác động": in_impact}
            st.session_state.macro_history = pd.concat([st.session_state.macro_history, pd.DataFrame([new_row])], ignore_index=True)
            st.rerun()

    st.markdown("---")
    st.subheader("🎙️ Theo dõi các bài phát biểu quan trọng (Fed / Tổng thống)")
    st.markdown("""
    * **[Báo cáo từ Chủ tịch Fed]:** Phát biểu tại điều trần Quốc hội nhấn mạnh lộ trình lãi suất sẽ phụ thuộc hoàn toàn vào dữ liệu lạm phát hạ nhiệt bền vững.
    * **[Nhận định]:** Diễn biến này làm giảm kỳ vọng thắt chặt, tạo động lực tăng trưởng trung hạn cho dòng vốn dịch chuyển sang tài sản an toàn (Vàng).
    """)

# ==========================================
# MODULE 3: DÒNG TIỀN & VỊ THẾ VỐN
# ==========================================
elif module == "💸 Dòng Tiền & Vị Thế Vốn":
    st.header("💸 Phân Tích Luân Chuyển Dòng Tiền Toàn Cầu")
    
    # Giả lập dữ liệu dòng tiền theo ngày
    df_flow = pd.DataFrame({
        "Ngày": ["02/07", "03/07", "04/07", "07/07", "08/07"],
        "Quỹ ETF GLD (Tấn)": [828.4, 829.1, 831.5, 830.2, 834.8],
        "Dự trữ Ngân hàng TW (Triệu Oz)": [39.1, 39.1, 39.2, 39.2, 39.4],
        "Vị thế Long COT (Hợp đồng)": [245000, 248000, 250000, 252000, 258000],
        "Lợi suất thực Real Yield (%)": [2.01, 1.98, 1.95, 1.96, 1.91]
    })
    
    st.subheader("📊 Bảng theo dõi chỉ số dòng tiền cập nhật hàng ngày")
    st.dataframe(df_flow, use_container_width=True, hide_index=True)
    
    st.subheader("📈 Biểu đồ trực quan hóa động lực dòng vốn")
    metric_to_plot = st.selectbox("Chọn chỉ số dòng tiền để vẽ biểu đồ:", list(df_flow.columns[1:]))
    fig_flow = px.line(df_flow, x="Ngày", y=metric_to_plot, markers=True, title=f"Xu hướng thay đổi chỉ số: {metric_to_plot}", color_discrete_sequence=['#FFD700'])
    st.plotly_chart(fig_flow, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🎯 Phân tích hành động & Nước đi của dòng tiền")
    st.success("**Kết luận:** Các quỹ ETF lớn (GLD) liên tục mua ròng trong 2 phiên gần nhất kết hợp với báo cáo COT cho thấy phe mua lớn (Non-Commercial) đang tăng vị thế vị thế Long. Dòng tiền thông minh đang dịch chuyển khỏi tài sản rủi ro để chuẩn bị cho chu kỳ phòng thủ.")

# ==========================================
# MODULE 4: TIN TỨC & CỔ PHIẾU
# ==========================================
elif module == "📈 Tin Tức & Cổ Phiếu":
    st.header("📈 Tình Hình Doanh Nghiệp & Thị Trường Chứng Khoán")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏢 Sức khỏe tài chính các Doanh nghiệp lớn")
        st.markdown("""

