import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import requests

# ==========================================
# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN TẠP CHÍ
# ==========================================
st.set_page_config(
    page_title="Tạp Chí Liên Thị Trường & Giao Dịch XAU/USD", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Khởi tạo bộ nhớ phiên để lưu trữ dữ liệu người dùng nhập
if "macro_user_data" not in st.session_state:
    st.session_state.macro_user_data = []
if "trading_journal" not in st.session_state:
    st.session_state.trading_journal = []

# API Key NewsAPI dùng chung để quét tin tức toàn cầu
NEWS_API_KEY = "a6886e01a8ef4df6b09ee63f03b22cf9"

# Hàm quét tin tức tự động theo từ khóa chuyên ngành
@st.cache_data(ttl=600)
def fetch_magazine_news(query, max_results=4):
    url = f"https://newsapi.org{query}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("articles", [])[:max_results]
    except Exception:
        pass
    return []

# Hàm vẽ thẻ bài báo chuẩn giao diện tạp chí chuyên nghiệp
def render_magazine_card(art, card_type="info"):
    with st.container(border=True):
        if art.get("urlToImage"):
            st.image(art["urlToImage"], use_container_width=True)
        
        # Phân loại màu tiêu đề theo tính chất tin tức
        if card_type == "error":
            st.markdown(f"### 🔴 [{art['title']}]({art['url']})")
        elif card_type == "success":
            st.markdown(f"### 🟢 [{art['title']}]({art['url']})")
        else:
            st.markdown(f"### 🌐 [{art['title']}]({art['url']})")
            
        st.caption(f"✍️ *Nguồn: {art['source']['name']} | Xuất bản: {art['publishedAt'][:10]}*")
        desc = art.get("description", "")
        if desc:
            st.write(desc[:200] + "..." if len(desc) > 200 else desc)
        st.markdown(f"[👉 Đọc bài phân tích gốc trên {art['source']['name']}]({art['url']})")

# Hàm lấy giá và vẽ biểu đồ đường liên thị trường
@st.cache_data(ttl=300)
def get_market_data_with_chart(ticker_symbol, name):
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period="1mo")
        if df.empty:
            df = ticker.history(period="7d")
            
        if not df.empty:
            current = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2] if len(df) >= 2 else current
            change = ((current - prev) / prev) * 100 if current != prev else 0.0
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Close'], mode='lines', 
                line=dict(color='#FFD700' if "Vàng" in name else '#1f77b4', width=2.5)
            ))
            fig.update_layout(
                margin=dict(l=10, r=10, t=10, b=10), height=140,
                xaxis=dict(visible=False), yaxis=dict(visible=True), template="plotly_dark"
            )
            return current, change, fig
    except Exception:
        pass
    # Giá dự phòng nền nếu API nghẽn mạch cục bộ
    fallback_prices = {"GC=F": 2350.5, "DX-Y.NYB": 104.2, "^TNX": 4.25, "^VIX": 13.4, "CL=F": 78.3}
    return fallback_prices.get(ticker_symbol, 0.0), 0.0, None

# ==========================================
# 2. THANH ĐIỀU HƯỚNG SIDEBAR
# ==========================================
st.sidebar.title("🦅 TẠP CHÍ VĨ MÔ XAU/USD")
st.sidebar.markdown("*Hệ thống quét dữ liệu phân tích tự động*")
st.sidebar.markdown("---")
module = st.sidebar.radio(
    "CHỌN KHÔNG GIAN PHÂN TÍCH:",
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
    st.header("📊 Dashboard Diễn Biến Liên Thị Trường Hàng Ngày")
    st.markdown("---")
    
    assets = {
        "Giá vàng thế giới (XAU/USD)": "GC=F",
        "Chỉ số Sức mạnh Đô la (DXY)": "DX-Y.NYB",
        "Lợi suất Trái phiếu Mỹ 10Y": "^TNX",
        "Chỉ số Biến động Sợ hãi VIX": "^VIX",
        "Giá Năng lượng Dầu Thô WTI": "CL=F"
    }
    
    for label, ticker in assets.items():
        price, change, fig = get_market_data_with_chart(ticker, label)
        c_metric, c_chart = st.columns([1, 2])
        with c_metric:
            suffix = "%" if "10Y" in label else ""
            prefix = "" if "10Y" in label or "DXY" in label or "VIX" in label else "$"
            st.metric(label=label, value=f"{prefix}{price:,.2f}{suffix}", delta=f"{change:.2f}%")
        with c_chart:
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True, key=f"dash_{ticker}")
        st.markdown("<hr style='margin:0.3em 0px;'>", unsafe_allow_html=True)

    st.subheader("💡 Tiêu Điểm Báo Chí: Phân Tích Xu Hướng Vàng")
    dash_news = fetch_magazine_news("gold+price+trend+forecast", max_results=2)
    if dash_news:
        c1, c2 = st.columns(2)
        for idx, art in enumerate(dash_news):
            with c1 if idx == 0 else c2:
                render_magazine_card(art, card_type="success")

# ==========================================
# MODULE 2: DỮ LIỆU KINH TẾ MỸ
# ==========================================
elif module == "🇺🇸 Dữ Liệu Kinh Tế Mỹ":
    st.header("🇺🇸 Trung Tâm Dữ Liệu Kinh Tế Vĩ Mô Hoa Kỳ")
    st.markdown("---")
    
    macro_indicators = ["CPI", "PCE", "NFP", "GDP", "PMI", "Unemployment Rate", "Retail Sales"]
    selected_ind = st.selectbox("🎯 Chọn chỉ số vĩ mô để phân tích chu kỳ:", macro_indicators)
    
    # Ứng dụng tự động quét các bài phân tích chuyên sâu về chỉ số kinh tế được chọn
    st.subheader(f"📊 Các bài nghiên cứu & Phân tích chuyên sâu về chỉ số {selected_ind}")
    macro_news = fetch_magazine_news(f"US+economy+{selected_ind}+fed", max_results=2)
    
    if macro_news:
        col1, col2 = st.columns(2)
        for idx, art in enumerate(macro_news):
            with col1 if idx == 0 else col2:
                render_magazine_card(art)
                
    st.markdown("---")
    st.subheader("📝 Bảng theo dõi và Đánh giá tác động số liệu")
    with st.form("macro_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            period = st.text_input("Kỳ công bố (Ví dụ: Tháng 07/2026)")
            act_val = st.number_input("Giá trị Thực tế (Actual)", value=0.0)
        with c2:
            fore_val = st.number_input("Giá trị Dự báo (Forecast)", value=0.0)
            prev_val = st.number_input("Giá trị Kỳ trước (Previous)", value=0.0)
        with c3:
            impact = st.selectbox("Đánh giá tác động", ["Tốt cho USD / Áp lực lên Vàng", "Xấu cho USD / Hỗ trợ đà tăng Vàng", "Trung lập"])
            
        if st.form_submit_button("💾 Đồng bộ số liệu vào hệ thống"):
            st.session_state.macro_user_data.append({
                "Chỉ báo": selected_ind, "Kỳ": period, "Thực tế": act_val, 
                "Dự báo": fore_val, "Kỳ trước": prev_val, "Tác động": impact
            })
            st.success("Đã ghi nhận dữ liệu đánh giá vĩ mô!")

    if st.session_state.macro_user_data:
        st.dataframe(pd.DataFrame(st.session_state.macro_user_data), use_container_width=True, hide_index=True)

# ==========================================
# MODULE 3: DÒNG TIỀN & VỊ THẾ VỐN
# ==========================================
elif module == "💸 Dòng Tiền & Vị Thế Vốn":
    st.header("💸 Báo Cáo Luân Chuyển Dòng Vốn & Vị Thế Các Quỹ Lớn")
    st.markdown("---")
    
    # Quét tin tức về dòng tiền của các quỹ ETF lớn như GLD, IAU hoặc trạng thái mua ròng của Ngân hàng Trung ương
    st.subheader("📰 Góc Nhìn Tạp Chí: Động thái mua ròng Vàng toàn cầu")
    flow_news = fetch_magazine_news("gold+ETF+GLD+central+bank+reserve", max_results=2)
    
    if flow_news:
        c1, c2 = st.columns(2)
        for idx, art in enumerate(flow_news):
            with c1 if idx == 0 else c2:
                render_magazine_card(art, card_type="info")
                
    st.markdown("---")
    st.subheader("📈 Đồ thị biến động Lợi suất thực tế và Vị thế ròng")
    df_flow = pd.DataFrame({
        "Tuần": ["Tuần 1", "Tuần 2", "Tuần 3", "Tuần 4", "Tuần 5"],
        "Dự trữ ETF Vàng (Tấn)": [828.4, 829.1, 831.5, 830.2, 834.8],
        "Lợi suất thực Real Yield (%)": [2.01, 1.98, 1.95, 1.96, 1.91]
    })
    
    view_metric = st.selectbox("Chọn chỉ số dòng vốn để vẽ mô hình trực quan:", ["Dự trữ ETF Vàng (Tấn)", "Lợi suất thực Real Yield (%)"])
    fig_flow = px.line(df_flow, x="Tuần", y=view_metric, markers=True, color_discrete_sequence=['#FFD700'])
    st.plotly_chart(fig_flow, use_container_width=True)

# ==========================================
# MODULE 4: TIN TỨC & CỔ PHIẾU
# ==========================================
elif module == "📈 Tin Tức & Cổ Phiếu":
    st.header("📈 Tin Tức Doanh Nghiệp & Sức Khỏe Thị Trường Chứng Khoán")
    st.markdown("---")
    
    stock_news = fetch_magazine_news("S&P500+earnings+stocks+market", max_results=4)
    if stock_news:
        col_n1, col_n2 = st.columns(2)
        for idx, art in enumerate(stock_news):
            target_col = col_n1 if idx % 2 == 0 else col_n2
            with target_col:
                render_magazine_card(art)
    else:
        st.info("Đang đồng bộ dòng tin tức chứng khoán quốc tế...")

# ==========================================
# MODULE 5: TIN TỨC CHIẾN TRANH
# ==========================================
elif module == "🪖 Tin Tức Chiến Tranh":
    st.header("🪖 Bản Tin Địa Chính Trị & Rủi Ro Xung Đột Vũ Trang")
    st.markdown("---")
    
    c1, c2 = st.columns([1.3, 1])
    with c1:
    st.subheader("🔴 Nhật ký khủng hoảng địa chính trị ảnh hưởng đến tài sản trú ẩn")
    war_news = fetch_magazine_news("geopolitics+conflict+war+sanctions", max_results=3)
    if war_news:
        for art in war_news:
            render_magazine_card(art, card_type="error")
            st.markdown("", unsafe_allow_html=True)
    else:
        st.warning("Đang kết nối cổng thông tấn quốc tế để lấy dòng sự kiện xung đột...")
            
    with c2:
        st.subheader("🗺️ Bản đồ các vùng cảnh báo rủi ro cao")
        conflict_data = pd.DataFrame({
            'Khu vực': ['Trung Đông', 'Đông Âu', 'Biển Đông'],
            'Vĩ độ': [29.0, 48.0, 15.0], 
            'Kinh độ': [47.0, 31.0, 115.0],
            'Mức độ rủi ro': ['🔴 Nguy cấp', '🔴 Rủi ro cao', '🟡 Cảnh báo']
        })
        fig_map = px.scatter_geo(
            conflict_data, lat='Vĩ độ', lon='Kinh độ', hover_name='Khu vực',
            text='Khu vực', size_max=15, projection="natural earth"
        )
        fig_map.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# MODULE 6: CÔNG CỤ HỖ TRỢ GIAO DỊCH
# ==========================================
elif module == "🛠️ Công Cụ Hỗ Trợ Giao Dịch":
    st.header("🛠️ Hệ Thống Nhật Ký Chiến Thuật & Quản Lý Vốn")
    st.markdown("---")
    
    # Ứng dụng tự động quét các bài viết hướng dẫn mẹo phân tích kỹ thuật của các chuyên gia hàng đầu
    st.subheader("🧠 Góc Học Tập: Chiến lược phân tích kỹ thuật từ các chuyên gia")
    tech_news = fetch_magazine_news("gold+technical+analysis+strategy", max_results=2)
    if tech_news:
        col1, col2 = st.columns(2)
        for idx, art in enumerate(tech_news):
            with col1 if idx == 0 else col2:
                render_magazine_card(art)
                
    st.markdown("---")
    st.subheader("📝 Ghi chép nhật ký chiến thuật và quản lý vốn cá nhân")
    with st.form("journal_form", clear_on_submit=True):
        col_j1, col_j2 = st.columns(2)
        with col_j1:
            action = st.selectbox("Hành động lệnh:", ["BUY", "SELL", "STANDBY"])
            price_entry = st.number_input("Mức giá Entry dự kiến:", value=0.0)
        with col_j2:
            notes = st.text_area("Ghi chú phân tích cấu trúc thị trường:")
            
        if st.form_submit_button("💾 Lưu nhận định cá nhân"):
            st.session_state.trading_journal.append({
                "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Lệnh": action, 
                "Mức giá": price_entry, 
                "Ghi chú": notes
            })
            st.toast("Đã lưu nhận định vào phiên làm việc!", icon="📝")
            
    if st.session_state.trading_journal:
        st.markdown("### 📚 Lịch sử ghi chép nhật ký trong phiên")
        st.dataframe(pd.DataFrame(st.session_state.trading_journal), use_container_width=True, hide_index=True)

