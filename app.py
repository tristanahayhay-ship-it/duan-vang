import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import requests

# 1. CẤU HÌNH TRANG CHUẨN
st.set_page_config(page_title="Hệ thống Vĩ mô & Liên thị trường XAU/USD", layout="wide", initial_sidebar_state="expanded")
st.title("🦅 HỆ THỐNG PHÂN TÍCH VĨ MÔ TOÀN CẢNH & GIAO DỊCH VÀNG")
st.markdown("---")

# 2. CẤU HÌNH API & BẢO MẬT
FINNHUB_API_KEY = st.secrets.get("FINNHUB_API_KEY", "d96keq1r01qr77dkrm4g")

# 3. KHỞI TẠO DỮ LIỆU ĐỘNG (SESSION STATE) ĐỂ TRÁNH MẤT DỮ LIỆU KHI LÀM MỚI TRANG
if "macro_history" not in st.session_state:
    st.session_state.macro_history = pd.DataFrame([
        {"Chỉ báo": "CPI", "Kỳ": "Tháng 05/2026", "Thực tế": 3.2, "Dự báo": 3.1, "Kỳ trước": 3.4, "Tác động": "Tốt cho USD / Xấu cho Vàng"},
        {"Chỉ báo": "CPI", "Kỳ": "Tháng 04/2026", "Thực tế": 3.4, "Dự báo": 3.4, "Kỳ trước": 3.5, "Tác động": "Trung lập"},
        {"Chỉ báo": "NFP", "Kỳ": "Tháng 05/2026", "Thực tế": 175.0, "Dự báo": 185.0, "Kỳ trước": 210.0, "Tác động": "Xấu cho USD / Tốt cho Vàng"},
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
    
    for label, ticker in assets.items():
        price, change, fig = get_market_data_with_chart(ticker, label)
        c_metric, c_chart = st.columns(2)
        with c_metric:
            suffix = "%" if "10Y" in label else ""
            prefix = "" if "10Y" in label or "DXY" in label or "VIX" in label else "$"
            st.metric(label=label, value=f"{prefix}{price:,.2f}{suffix}", delta=f"{change:.2f}%")
        with c_chart:
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True, key=f"chart_{ticker}")
        st.markdown("<hr style='margin:0.5em 0px;'>", unsafe_allow_html=True)

    st.subheader("📅 Lịch kinh tế tiêu điểm hôm nay")
    mock_calendar = pd.DataFrame({
        "Thời gian": ["19:30", "19:30", "21:00"], 
        "Quốc gia": ["USD", "USD", "USD"],
        "Sự kiện kinh tế": ["Core CPI m/m (Chỉ số lạm phát lõi)", "Yêu cầu trợ cấp thất nghiệp lần đầu", "Doanh số bán nhà xây mới"],
        "Dự báo": ["0.3%", "215K", "680K"], 
        "Thực tế": ["⏱️ Chờ công bố", "⏱️ Chờ công bố", "⏱️ Chờ công bố"], 
        "Tác động dự kiến": ["🔴 Biến động mạnh", "🟡 Biến động vừa", "🟢 Biến động thấp"]
    })
    st.dataframe(mock_calendar, use_container_width=True, hide_index=True)
    
    st.subheader("💡 Phân tích vĩ mô ngắn hạn & Kết luận xu hướng")
    st.info("**Nhận định:** DXY đang tích lũy, lợi suất 10Y hạ nhiệt hỗ trợ đà tăng của Vàng. Chiến lược phiên: **Canh Mua (Bullish) khi giá điều chỉnh kỹ thuật.**")

# ==========================================
# MODULE 2: DỮ LIỆU KINH TẾ MỸ
# ==========================================
elif module == "🇺🇸 Dữ Liệu Kinh Tế Mỹ":
    st.header("🇺🇸 Bộ Cơ Sở Dữ Liệu Kinh Tế Vĩ Mô Mỹ")
    
    macro_indicators = ["CPI", "Core CPI", "PCE", "Core PCE", "NFP", "Tỷ lệ thất nghiệp", "GDP", "PMI", "Doanh số bán lẻ", "JOLTS", "ADP", "ISM Manufacturing/Services"]
    selected_ind = st.selectbox("🎯 Chọn chỉ số vĩ mô để theo dõi chu kỳ:", macro_indicators)
    
    filtered_df = st.session_state.macro_history[st.session_state.macro_history["Chỉ báo"] == selected_ind]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"📊 Bảng dữ liệu lịch sử: {selected_ind}")
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.warning("Chưa có dữ liệu cho chỉ số này. Hãy cập nhật ở biểu mẫu phía dưới.")
            
    with col2:
        st.subheader("📈 Biểu đồ diễn biến chu kỳ")
        if not filtered_df.empty:
            fig_macro = px.bar(filtered_df, x="Kỳ", y="Thực tế", text_auto=True, title=f"Giá trị thực tế qua các kỳ - {selected_ind}", color_discrete_sequence=['#1f77b4'])
            st.plotly_chart(fig_macro, use_container_width=True)
        else:
            st.info("Biểu đồ sẽ hiển thị khi có dữ liệu.")

    st.markdown("---")
    st.subheader("📥 Cập nhật số liệu mới")
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
    * **[Báo cáo từ Chủ tịch Fed]:** Lộ trình điều chỉnh lãi suất sẽ phụ thuộc hoàn toàn vào tốc độ hạ nhiệt ổn định của lạm phát.
    * **[Nhận định ảnh hưởng]:** Tuyên bố mang tính trung lập, làm giảm rủi ro thắt chặt đột ngột, giữ vững tâm lý kỳ vọng tăng trưởng trung hạn cho thị trường Vàng.
    """)

# ==========================================
# MODULE 3: DÒNG TIỀN & VỊ THẾ VỐN
# ==========================================
elif module == "💸 Dòng Tiền & Vị Thế Vốn":
    st.header("💸 Phân Tích Luân Chuyển Dòng Tiền Toàn Cầu")
    
    # SỬA LỖI GỐC: Điền chính xác mảng số liệu mẫu cho "Vị thế Long COT (Hợp đồng)"
    df_flow = pd.DataFrame({
        "Ngày": ["02/07", "03/07", "04/07", "07/07", "08/07"],
        "Quỹ ETF GLD (Tấn)": [828.4, 829.1, 831.5, 830.2, 834.8],
        "Dự trữ Ngân hàng TW (Triệu Oz)": [39.1, 39.1, 39.2, 39.2, 39.4],
        "Vị thế Long COT (Hợp đồng)": [250000, 252000, 248000, 255000, 260000],
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
    st.success("**Kết luận dòng vốn:** Khối lượng nắm giữ từ các quỹ ETF gia tăng đồng thuận với các lệnh Long ròng trên báo cáo COT. Vòng luân chuyển dòng tiền cho thấy trạng thái tích trữ phòng thủ rõ rệt.")

# ==========================================
# MODULE 4: TIN TỨC & CỔ PHIẾU
# ==========================================
elif module == "📈 Tin Tức & Cổ Phiếu":
    st.header("📈 Tình Hình Doanh Nghiệp & Thị Trường Chứng Khoán")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏢 Sức khỏe tài chính các Doanh nghiệp lớn")
        st.markdown("""
        * **Nhóm Công nghệ lớn (Mag 7):** Doanh thu ổn định nhưng tốc độ tăng trưởng có phần chững lại, dòng tiền ngắn hạn có xu hướng dịch chuyển tìm kiếm biên an toàn.
        * **Doanh nghiệp Khai thác Vàng (NEM, GOLD):** Hưởng lợi biên lợi nhuận ròng tăng vọt do duy trì được nền giá sản phẩm neo ở mức cao lịch sử.
        """)
    with col2:
        st.subheader("📰 Tin tức thị trường chứng khoán")
        st.warning("Chỉ số S&P 500 gặp áp lực điều chỉnh kỹ thuật nhẹ tại các mốc kháng cự cũ khi tâm lý lo ngại rủi ro hạ cánh mềm quay trở lại.")

# ==========================================
# MODULE 5: TIN TỨC CHIẾN TRANH
# ==========================================
elif module == "🪖 Tin Tức Chiến Tranh":
st.header("🪖 Bản Tin Địa Chính Trị & Rủi Ro Xung Đột")
col1, col2 = st.columns(2)
with col1:
st.subheader("📰 Cập nhật tình hình các chiến sự & Đàm phán")
st.error("Căng thẳng khu vực Trung Đông: Tiến trình đàm phán tạm thời đi vào bế bẽ, nguy cơ rủi ro chuỗi cung ứng logistics đẩy cao tâm lý phòng vệ.")
st.info("Cấm vận kinh tế: Các lệnh hạn chế thương mại mới đối với nhóm nguyên liệu thô tiếp tục tạo áp lực lên chuỗi cung ứng hàng hóa toàn cầu.")
with col2:
st.subheader("🗺 Bản đồ các vùng cảnh báo rủi ro xung đột cao")
conflict_data = pd.DataFrame({
'Khu vực': ['Trung Đông', 'Đông Âu', 'Biển Đông'],
'Vĩ độ': [29.0, 48.0, 15.0],
'Kinh độ': [47.0, 31.0, 115.0],
'Mức độ rủi ro': ['🔴 Nguy cấp', '🔴 Rủi ro cao', '🟡 Cảnh báo']
})
fig_map = px.scatter_geo(
conflict_data, lat='Vĩ độ', lon='Kinh độ', hover_name='Khu vực',
text='Khu vực', size_max=15, title="Các tọa điểm nóng địa chính trị toàn cầu",
projection="natural earth"
)
fig_map.update_layout(template="plotly_dark")
st.plotly_chart(fig_map, use_container_width=True)
==========================================
MODULE 6: CÔNG CỤ HỖ TRỢ GIAO DỊCH
==========================================
elif module == "🛠 Công Cụ Hỗ Trợ Giao Dịch":
st.header("🛠 Hệ Thống Chấm Điểm Kỹ Thuật & Nhật Ký Chiến Thuật")
st.subheader("🎯 1. Các chỉ báo kỹ thuật đo lường chính (Khung D1)")
c1, c2, c3 = st.columns(3)
c1.metric("RSI (14)", "62.5", "Xu hướng Mua chiếm ưu thế")
c2.metric("MACD Histogram", "+14.2", "Động lượng Tăng mạnh")
c3.metric("Đường trung bình MA200", "$2,310", "Nằm trên cấu trúc tăng dài hạn")
st.subheader("🧮 2. Chấm điểm áp lực xu hướng tổng hợp từ Vĩ mô")
score = st.slider("Thang điểm áp lực (1: Cực kỳ hỗ trợ Vàng - 10: Áp lực giảm giá mạnh)", 1, 10, 3)
if score <= 4:
st.success("🟢 KẾT LUẬN XU HƯỚNG: BULLISH (Chiến lược: Chỉ canh Mua / Buy Only)")
elif score >= 7:
st.error("🔴 KẾT LUẬN XU HƯỚNG: BEARISH (Chiến lược: Chỉ canh Bán / Sell Only)")
else:
st.warning("🟡 KẾT LUẬN XU HƯỚNG: SIDEWAYS (Thị trường tích lũy biên độ)")
st.markdown("---")
st.subheader("📝 3. Nhật ký giao dịch chiến thuật & Nhận định cá nhân")
with st.form("journal_form", clear_on_submit=True):
col_j1, col_j2 = st.columns(2)
with col_j1:
action = st.selectbox("Hành động lệnh:", ["BUY", "SELL", "STANDBY"])
price_entry = st.number_input("Mức giá entry dự kiến:", value=0.0)
with col_j2:
notes = st.text_area("Ghi chú phân tích kỹ thuật và quản lý vốn:")
if st.form_submit_button("💾 Lưu chiến thuật vào nhật ký"):
entry = {
"Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M"),
"Lệnh": action, "Mức giá": price_entry, "Ghi chú": notes
}
st.session_state.journal.append(entry)
st.toast("Đã đồng bộ nhật ký giao dịch!", icon="📝")
if st.session_state.journal:
st.markdown("### 📚 Lịch sử nhật ký giao dịch trong phiên")
st.dataframe(pd.DataFrame(st.session_state.journal), use_container_width=True)
