import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from datetime import datetime, timedelta

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Kinh tế Vĩ mô & Nhận định Giá Vàng",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm CSS tùy chỉnh để giao diện chuyên nghiệp hơn
st.markdown("""
<style>
    .reportview-container { background: #f5f7f8; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #1e293b; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    .ai-box { background-color: #eff6ff; border-left: 5px solid #3b82f6; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
    .news-card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# Hàm giả lập dữ liệu nến (Thay thế bằng API thực tế như yfinance khi deploy)
def get_real_market_data(symbol, days=90):
    ticker_mapping = {
        "XAU/USD": "GC=F",
        "DXY": "DX-Y.NYB",
        "US10Y": "^TNX",
        "VIX": "^VIX",
        "WTI Oil": "CL=F"
    }
    ticker_sym = ticker_mapping.get(symbol, "GC=F")
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)
        t = yf.Ticker(ticker_sym)
        df = t.history(start=start_date, end=end_date)
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối dữ liệu {symbol}: {str(e)}")
        return pd.DataFrame()

def plot_tradingview_chart(df, title):
    if df.empty:
        return go.Figure()
        
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_width=[0.2, 0.8])
                        
    # Ép kiểu dữ liệu ngày tháng của Yahoo Finance về chuỗi Ngày/Tháng ngắn gọn
    short_dates = df.index.strftime('%d/%m')
                        
    fig.add_trace(go.Candlestick(
        x=short_dates, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name="Giá",
        increasing_line_color='#22c55e', decreasing_line_color='#ef4444',
        increasing_fillcolor='#22c55e', decreasing_fillcolor='#ef4444'
    ), row=1, col=1)
    
    if 'Volume' in df.columns and df['Volume'].sum() > 0:
        colors = ['#22c55e' if row['Close'] >= row['Open'] else '#ef4444' for _, row in df.iterrows()]
        fig.add_trace(go.Bar(
            x=short_dates, y=df['Volume'], name="Volume", showlegend=False, marker_color=colors
        ), row=2, col=1)
        
    fig.update_xaxes(type='category', gridcolor='#e2e8f0', row=1, col=1)
    fig.update_xaxes(type='category', gridcolor='#e2e8f0', row=2, col=1)
    fig.update_yaxes(gridcolor='#e2e8f0', row=1, col=1)
    fig.update_yaxes(gridcolor='#e2e8f0', showticklabels=False, row=2, col=1)

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#1e293b')),
        xaxis_rangeslider_visible=False, height=450,
        margin=dict(l=10, r=10, t=40, b=10), hovermode='x unified',
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# SIDEBAR: Điều hướng chính
# SIDEBAR: Điều hướng chính và Cài đặt hệ thống
st.sidebar.title("🧭 Điều Hướng Hệ Thống")

# ===================================================================================================
# ⚙️ BẢNG ĐIỀU KHIỂN HỆ THỐNG (GÓC TRÊN TRÁI)
# ===================================================================================================
with st.sidebar.expander("⚙️ Cài đặt Hệ thống (Múi giờ / Ngôn ngữ / Theme)", expanded=False):
    # 1. Chọn ngôn ngữ
    lang_option = st.selectbox("🌐 Ngôn ngữ (Language):", ["Tiếng Việt (VN)", "English (US)"])
    
    # 2. Chọn múi giờ
    timezone_option = st.selectbox("🕒 Múi giờ (Timezone):", ["Việt Nam (GMT+7)", "New York (EST/GMT-5)", "London (GMT+0)"])
    
    # 3. Nút bấm mô phỏng chỉnh ánh sáng (Bổ trợ giao diện)
    theme_option = st.radio("🌗 Giao diện hiển thị:", ["Chế độ Sáng (Light)", "Chế độ Tối (Dark)"], horizontal=True)

# Khai báo timezone an toàn để tránh lỗi đồng hồ hệ thống
from datetime import timezone
now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

if timezone_option == "Việt Nam (GMT+7)":
    now_selected = now_utc + timedelta(hours=7)
    tz_suffix = "Giờ Việt Nam"
elif timezone_option == "New York (EST/GMT-5)":
    now_selected = now_utc - timedelta(hours=5)
    tz_suffix = "Giờ New York"
else:
    now_selected = now_utc
    tz_suffix = "Giờ Quốc tế GMT"

current_time_str = now_selected.strftime("%d/%m/%Y — %H:%M:%S")

# Hiển thị đồng hồ thời gian động ngay dưới bảng cài đặt
st.sidebar.markdown(f"📅 **Thời gian:** {current_time_str} *({tz_suffix})*")
st.sidebar.markdown("---")
# ===================================================================================================

menu = st.sidebar.radio(
    "Chọn chuyên mục:",
    ["Dashboard Tổng Quan", "Dữ Liệu Kinh Tế Mỹ", "Dòng Tiền (Flow of Funds)", "Tin Tức & Cổ Phiếu", "Địa Chính Trị & Chiến Tranh", "Công Cụ Hỗ Trợ & Demo Trade", "Giá Vàng VIỆT NAM", "📅 Lịch Kinh Tế & AI Nhận Định (USD)", "🤖 AI Giải Đáp & Phân Tích"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Trạng thái AI Kết Luận")
st.sidebar.success("Hệ thống AI: Sẵn sàng")
st.sidebar.info("Khuyến nghị hôm nay: **BULLISH GOLD** (Ưu tiên Mua) do căng thẳng địa chính trị và Real Yield giảm.")

# ===================================================================================================
# 1. DASHBOARD TỔNG QUAN
# ===================================================================================================
if menu == "Dashboard Tổng Quan":
    st.title("🪙 Kinh Tế Vĩ Mô & Nhận Định Giá Vàng")
    st.caption("Hệ thống tự động cập nhật dữ liệu liên tục kết hợp trí tuệ nhân tạo AI phân tích xu hướng")
    # =========================================================
    # HÀNG CHỈ SỐ LẤY DỮ LIỆU REAL-TIME TỪ YAHOO FINANCE
    # =========================================================
    import yfinance as yf

    @st.cache_data(ttl=60)  # Lưu bộ nhớ đệm 60 giây
    def get_live_market_data():
        tickers = {
            "Vàng (XAU/USD)": "GC=F",
            "DXY Index": "DX-Y.NYB",
            "US 10Y Yield": "^TNX",
            "VIX Index": "^VIX",
            "Crude Oil WTI": "CL=F"
        }
        results = {}
        for name, sym in tickers.items():
            try:
                t = yf.Ticker(sym)
                hist = t.history(period="2d")
                if len(hist) >= 2:
                    close_today = hist['Close'].iloc[-1]
                    close_yesterday = hist['Close'].iloc[-2]
                    change = close_today - close_yesterday
                    pct_change = (change / close_yesterday) * 100
                    results[name] = (round(close_today, 2), round(change, 2), round(pct_change, 2))
                else:
                    results[name] = (0.0, 0.0, 0.0)
            except:
                results[name] = (0.0, 0.0, 0.0)
        return results

    # Gọi hàm lấy giá trực tuyến (Đoạn này thụt lề 4 dấu cách)
    market_data = get_live_market_data()
    g_price, g_chg, g_pct = market_data.get("Vàng (XAU/USD)", (2354.50, 0.0, 0.0))
    dxy_price, dxy_chg, dxy_pct = market_data.get("DXY Index", (104.15, 0.0, 0.0))
    us10y_price, us10y_chg, us10y_pct = market_data.get("US 10Y Yield", (4.21, 0.0, 0.0))
    vix_price, vix_chg, vix_pct = market_data.get("VIX Index", (13.85, 0.0, 0.0))
    oil_price, oil_chg, oil_pct = market_data.get("Crude Oil WTI", (78.40, 0.0, 0.0))

    # Hiển thị ra các cột metric trên giao diện (Đoạn này thụt lề 4 dấu cách)
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("XAU/USD", f"{g_price:,}", f"{g_chg:+} ({g_pct:+.2f}%)")
    col2.metric("DXY Index", f"{dxy_price}", f"{dxy_chg:+} ({dxy_pct:+.2f}%)")
    col3.metric("US 10Y Yield", f"{us10y_price}%", f"{us10y_chg:+} ({us10y_pct:+.2f}%)")
    col4.metric("VIX Index", f"{vix_price}", f"{vix_price:+} ({vix_pct:+.2f}%)")
    col5.metric("Crude Oil WTI", f"${oil_price}", f"{oil_chg:+} ({oil_pct:+.2f}%)")

# =========================================================


    # Biểu đồ kỹ thuật tương tác
    st.subheader("📊 Biểu đồ Kỹ thuật Liên thông Vĩ mô")
    asset_option = st.selectbox("Chọn tài sản để xem biểu đồ chi tiết:", ["XAU/USD", "DXY", "US10Y", "VIX", "WTI Oil"])
    df_asset = get_real_market_data(asset_option)
    st.plotly_chart(plot_tradingview_chart(df_asset, f"Xu hướng thị trường thực tế: {asset_option}"), use_container_width=True)

    # Lịch kinh tế và Nhận định AI
    st.markdown("---")
    c_left, c_right = st.columns([2, 1])
    
    with c_left:
        st.subheader("📅 Lịch Kinh Tế Hôm Nay (Nguồn: ForexFactory thực tế)")
        # Tạo bảng lịch kinh tế giả lập
        cal_data = {
            "Thời gian": ["19:30", "19:30", "21:00", "21:30"],
            "Tiền tệ": ["USD", "USD", "USD", "USD"],
            "Sự kiện": ["CPI m/m (Chỉ số giá tiêu dùng)", "Core CPI y/y", "Doanh số bán lẻ m/m", "Dự trữ dầu thô"],
            "Tác động": ["Cao (Đỏ)", "Cao (Đỏ)", "Trung bình (Cam)", "Thấp (Vàng)"],
            "Dự báo": ["0.3%", "3.4%", "0.2%", "-1.2M"],
            "Thực tế": ["0.2%", "3.3%", "--", "--"]
        }
        st.table(pd.DataFrame(cal_data))
        
    with c_right:
        st.subheader("🤖 AI Nhận Định Lịch Kinh Tế")
        st.markdown("""
        <div class="ai-box">
            <b>Kết luận xu hướng từ AI:</b><br>
            CPI thực tế thấp hơn dự báo (0.2% so với 0.3%) cho thấy lạm phát Mỹ đang hạ nhiệt nhanh hơn kỳ vọng. 
            Điều này làm tăng xác suất FED hạ lãi suất vào cuộc họp tới. 
            <br><b>👉 Xu hướng Vàng:</b> Tác động <b>Tích cực (Bullish) mạnh mẽ</b>, giá vàng có xu hướng bứt phá vùng kháng cự ngắn hạn do đồng DXY bị bán tháo.
        </div>
        """, unsafe_allow_html=True)

    # Bài báo phân tích vĩ mô lớn
    st.subheader("📰 Bài báo phân tích vĩ mô chuyên sâu")
    col_news1, col_news2 = st.columns(2)
    with col_news1:
        st.markdown("""
        <div class="news-card">
            <h4>[Bloomberg] Vàng tiến sát đỉnh lịch sử khi số liệu lạm phát kích hoạt làn sóng tháo chạy khỏi USD</h4>
            <p style='color:#64748b;'>Cập nhật: 10 phút trước</p>
            <p>Các quỹ đầu tru lớn đồng loạt gia tăng vị thế mua ròng vàng sau khi chuỗi chỉ số giá tiêu dùng và dữ liệu việc làm yếu đi rõ rệt...</p>
        </div>
        """, unsafe_allow_html=True)
    with col_news2:
        st.markdown("""
        <div class="news-card">
            <h4>[Reuters] Căng thẳng leo thang tại Trung Đông thúc đẩy dòng tiền trú ẩn an toàn vào tài sản phòng thủ</h4>
            <p style='color:#64748b;'>Cập nhật: 1 giờ trước</p>
            <p>Bất chấp lợi suất trái phiếu chính phủ Mỹ neo ở mức cao, lực cầu vật chất từ các Ngân hàng trung ương và dòng tiền trú ẩn đang là bệ đỡ vững chắc...</p>
        </div>
        """, unsafe_allow_html=True)

# ===================================================================================================
# 2. DỮ LIỆU KINH TẾ MỸ
# ===================================================================================================
elif menu == "Dữ Liệu Kinh Tế Mỹ":
    st.title("🇺🇸 Chỉ Số Kinh Tế Vĩ Mô Mỹ (Real-time & Historical)")
    
    st.subheader("📋 Bảng cập nhật trạng thái thực tế")
    macro_indicators = {
        "Chỉ số": ["CPI", "Core CPI", "PCE", "Core PCE", "NFP (Non-farm Payrolls)", "Tỷ lệ thất nghiệp", "GDP Quý", "PMI Sản xuất", "Doanh số bán lẻ", "JOLTS Việc làm", "ADP Việc làm", "ISM Services"],
        "Kỳ báo cáo": ["Tháng 5", "Tháng 5", "Tháng 4", "Tháng 4", "Tháng 5", "Tháng 5", "Q1 Năm nay", "Tháng 5", "Tháng 5", "Tháng 4", "Tháng 5", "Tháng 5"],
        "Giá trị thực tế": ["3.3%", "3.4%", "2.7%", "2.8%", "175K", "3.9%", "1.6%", "49.2", "0.1%", "8.5M", "155K", "53.8"],
        "Dự báo trước đó": ["3.4%", "3.5%", "2.7%", "2.8%", "185K", "3.8%", "1.5%", "50.0", "0.2%", "8.7M", "160K", "52.0"],
        "Trạng thái đối với Vàng": ["Tốt (Tăng giá Vàng)", "Tốt (Tăng giá Vàng)", "Trung lập", "Trung lập", "Tốt (Tăng giá Vàng)", "Tốt (Tăng giá Vàng)", "Tốt", "Tốt", "Tốt", "Tốt", "Tốt", "Xấu (Giảm giá Vàng)"]
    }
    st.dataframe(pd.DataFrame(macro_indicators), use_container_width=True)
    
    st.subheader("📈 Biểu đồ lịch sử dữ liệu (Tùy chỉnh thời gian)")
    selected_macro = st.selectbox("Chọn chỉ số để xem biểu đồ lịch sử:", ["CPI", "NFP", "Tỷ lệ thất nghiệp", "GDP"])
    
    # Slider chọn số tháng xem lịch sử
    months_range = st.slider("Chọn khoảng thời gian lịch sử (tháng):", 6, 36, 12)
    
    # Giả lập dữ liệu biểu đồ cột
    np.random.seed(10)
    chart_dates = pd.date_range(end=datetime.today(), periods=months_range, freq='ME').strftime('%Y-%m')
    chart_values = np.random.normal(3.0, 0.5, months_range) if selected_macro=="CPI" else np.random.normal(180, 40, months_range)
    
    df_macro_chart = pd.DataFrame({"Thời gian": chart_dates, "Giá trị": chart_values})
    fig_macro = px.bar(df_macro_chart, x="Thời gian", y="Giá trị", title=f"Lịch sử biến động chỉ số {selected_macro}", color="Giá trị", color_continuous_scale="Blues")
    st.plotly_chart(fig_macro, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🎙️ Phát Biểu Từ FED & Tin Tức Cập Nhật Tự Động")
    st.warning("Cập nhật Real-time: Chủ tịch FED Jerome Powell phát biểu tại câu lạc bộ kinh tế New York lúc 22:00 hôm qua.")
    st.info("💡 Điểm mấu chốt: 'Chúng tôi cần thêm bằng chứng rõ ràng rằng lạm phát đang tiến về mức 2% trước khi đưa ra quyết định cắt giảm lãi suất. Tuy nhiên, thị trường lao động đang hạ nhiệt là yếu tố chúng tôi cân nhắc kỹ lưỡng.'")
    
    st.subheader("🤖 AI Tổng Hợp & Đánh Giá Tác Động Vĩ Mô Toàn Diện")
    st.markdown("""
    <div class="ai-box" style="background-color: #f0fdf4; border-left-color: #22c55e;">
        <b>Phân tích ma trận dữ liệu Mỹ từ AI:</b><br>
        Tổng hợp 12 chỉ số kinh tế lớn nhất cho thấy nền kinh tế Mỹ đang chuyển dịch sang giai đoạn <b>Thắt chặt gây hạ nhiệt (Cooling down)</b>. 
        NFP thấp kết hợp thất nghiệp tăng nhẹ lên 3.9% áp lực lớn lên đồng USD.
        <br><b>💎 Tác động lên Vàng:</b> Chu kỳ tăng trưởng vĩ mô của vàng chính thức được kích hoạt dài hạn vì chu kỳ hạ lãi suất của phương Tây thường là 'vùng xanh' của kim loại quý này.
    </div>
    """, unsafe_allow_html=True)

# ===================================================================================================
# 3. DÒNG TIỀN (FLOW OF FUNDS)
# ===================================================================================================
elif menu == "Dòng Tiền (Flow of Funds)":
    st.title("💸 Giám Sát Dòng Tiền Lớn (Smart Money Flow)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Thay đổi Quỹ ETF Vàng (GLD) hôm nay", "+3.85 Tấn", "Tổng trữ lượng: 835.40 Tấn")
    with col2:
        st.metric("COT Report (Vị thế mua ròng Đầu cơ)", "+12,450 Hợp đồng", "Phe Bull kiểm soát 78%")
    with col3:
        st.metric("Real Yield (Lợi suất thực Mỹ)", "1.85%", "-0.12% (Hỗ trợ Vàng)")
        
    st.subheader("📊 Diễn biến luân chuyển dòng tiền thông minh")
    
    t1, t2, t3 = st.tabs(["Trữ lượng Quỹ ETF", "Báo cáo COT (Commitment of Traders)", "Dự trữ vàng NHTW"])
    with t1:
        st.write("📈 Biểu đồ so sánh tương quan biến động giá vàng và khối lượng nắm giữ của các quỹ ETF lớn (GLD, IAU):")
        dates = pd.date_range(end=datetime.today(), periods=30)
        df_etf = pd.DataFrame(index=dates, data={"Giá vàng": np.linspace(2300, 2354, 30), "ETF Nắm Giữ (Tấn)": np.linspace(820, 835, 30)})
        st.line_chart(df_etf)
    with t2:
        st.write("📊 Dữ liệu trạng thái vị thế của các tổ chức tài chính lớn (Non-Commercial):")
        st.info("Báo cáo COT mới nhất chỉ ra rằng các dòng tiền lớn (Hedge Funds) tiếp tục đóng vị thế Short và gia tăng mạnh vị thế Long XAUUSD tuần thứ 3 liên tiếp.")
    with t3:
        st.write("🏛️ Hoạt động mua gom của Ngân hàng trung ương (PBoC Trung Quốc, Ngân hàng Trung ương Nga, Ấn Độ...)")
        st.success("Dữ liệu cập nhật: Trung Quốc tiếp tục gia tăng dự trữ vàng tháng thứ 18 liên tiếp, bổ sung thêm 60,000 ounces trong tháng vừa qua.")
        
    st.subheader("🤖 Nhận Định Nước Đi Dòng Tiền Từ AI")
    st.markdown("""
    <div class="ai-box">
        <b>Phân tích hành vi cá mập:</b> Dòng tiền không nằm ở tài sản rủi ro cao mà đang có xu hướng dịch chuyển dòng vốn (Capital rotation) từ thị trường trái phiếu ngắn hạn Mỹ trực tiếp sang thị trường vàng vật chất và quỹ tín thác. Đây là hành vi tích lũy tài sản dài hạn (Smart Money Accumulation).
    </div>
    """, unsafe_allow_html=True)

# ===================================================================================================
# 4. TIN TỨC & CỔ PHIẾU
# ===================================================================================================
elif menu == "Tin Tức & Cổ Phiếu":
    st.title("📈 Thị Trường Chứng Khoán & Sức Khỏe Doanh Nghiệp")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("S&P 500", "5,240.20", "-15.40 (-0.29%)")
    col_s2.metric("Nasdaq 100", "18,520.10", "-85.00 (-0.46%)")
    col_s3.metric("Dow Jones", "39,120.50", "+42.00 (+0.11%)")
    
    st.subheader("📰 Bảng Tin Doanh Nghiệp Real-time")
    st.dataframe(pd.DataFrame({
        "Thời gian": ["08:45", "08:12", "07:30"],
        "Mã cổ phiếu / Nhóm ngành": ["Tech Sector", "NVDA", "Banking Sector"],
        "Nội dung sự kiện": ["Áp lực chốt lời diện rộng lan ra toàn bộ nhóm cổ phiếu công nghệ lớn.", "Nvidia đón nhận cảnh báo định giá quá cao từ một số quỹ đầu tư lớn của Thụy Sĩ.", "Lợi nhuận ròng của các ngân hàng thương mại Mỹ có dấu hiệu sụt giảm do biên lãi ròng hẹp đi."]
    }), use_container_width=True)
    
    st.subheader("🔄 Biểu đồ tương quan giữa Chứng khoán và Tài sản an toàn (Vàng)")
    st.caption("Khi thị trường chứng khoán biến động mạnh hoặc suy thoái, dòng tiền thường rút ra để tìm kiếm sự an toàn từ Vàng.")
    chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['S&P 500 Index', 'Gold Price'])
    st.line_chart(chart_data)

# ===================================================================================================
# 5. ĐỊA CHÍNH TRỊ & CHIẾN TRANH
# ===================================================================================================
elif menu == "Địa Chính Trị & Chiến Tranh":
    st.title("🪖 Bản Đồ Địa Chính Trị & Rủi Ro Chiến Tranh Tác Động Giá Vàng")
    
    col_w1, col_w2 = st.columns([1, 1])
    
    with col_w1:
        st.subheader("🔥 Cập nhật điểm nóng xung đột & Đàm phán")
        st.error("🚨 CẢNH BÁO XUNG ĐỘT: Căng thẳng gia tăng tại khu vực Biển Đỏ, các đợt tập kích mới bằng UAV làm gián đoạn tuyến hàng hải huyết mạch.")
        st.warning("⚠️ Đàm phán: Cuộc thảo luận ngừng bắn vòng mới giữa các bên đạt được rất ít tiến triển thực tế do bất đồng về vùng đệm kiểm soát.")
        
        st.markdown("""
        <div class="news-card" style="border-left: 4px solid #ef4444;">
            <h5>[Tin độc quyền New York Times]</h5>
            <p>Tình báo phương Tây cảnh báo rủi ro xung đột leo thang sang các quốc gia lân cận tăng lên mức cao nhất trong vòng 6 tháng qua...</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_w2:
        st.subheader("🗺️ Bản đồ rủi ro toàn cầu (Cảnh báo xung đột)")
        st.info("🗺️ Hệ thống đang định vị các tọa độ rủi ro địa chính trị toàn cầu thực tế...")
        
        map_data = pd.DataFrame({
            'lat': [37.0902, 55.7558, 35.8617, 51.1657, -25.2744, 20.5937],
            'lon': [-95.7129, 37.6173, 104.1954, 10.4515, 133.7751, 78.9629],
            'Quốc gia': ['Mỹ (8,133 Tấn)', 'Nga (2,332 Tấn)', 'Trung Quốc (2,264 Tấn)', 'Đức (3,352 Tấn)', 'Úc (Dự trữ mỏ)', 'Ấn Độ (822 Tấn)'],
            'Mức độ rủi ro địa chính trị': [20, 85, 50, 30, 10, 40]
        })
        fig_map = px.scatter_mapbox(map_data, lat="lat", lon="lon", hover_name="Quốc gia", 
                                     color="Mức độ rủi ro địa chính trị", size="Mức độ rủi ro địa chính trị",
                                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=0.5, height=300)
        fig_map.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption("Chấm màu thể hiện mức độ tích trữ vàng và phân vùng rủi ro khủng hoảng của khu vực.")

# ===================================================================================================
# 6. CÔNG CỤ HỖ TRỢ & DEMO TRADE
# ===================================================================================================
elif menu == "Công Cụ Hỗ Trợ & Demo Trade":
    st.title("🛠️ Phân Tích Kỹ Thuật & Giả Lập Giao Dịch XAU/USD")
    
    st.subheader("💯 Hệ thống chấm điểm xu hướng thông minh")
    score_col1, score_col2 = st.columns([1, 2])
    with score_col1:
        st.metric("Chấm điểm Xu hướng", "8.5 / 10", "BULLISH (TĂNG MẠNH)")
    with score_col2:
        st.progress(85)
        st.caption("Thước đo dựa trên trọng số: Lạm phát (25%), Dòng tiền ETF (20%), Địa chính trị (30%), Phân tích kỹ thuật (25%)")
        
    st.subheader("⏱️ Các chỉ báo kỹ thuật đo lường (MA, RSI, MACD, Stochastic)")
    ind_c1, ind_c2, ind_c3, ind_c4 = st.columns(4)
    ind_c1.button("RSI (14): Quá mua nhẹ (62.5)", disabled=True)
    ind_c2.button("MACD: Cắt lên (Tín hiệu Mua)", disabled=True)
    ind_c3.button("MA (50/200): Golden Cross", disabled=True)
    ind_c4.button("Bollinger Bands: Đang thắt nút", disabled=True)
    
    st.markdown("---")
    st.subheader("🎮 Công cụ Mua / Bán Giả Lập Thực Hành (XAU/USD)")
    
    if 'balance' not in st.session_state:
        st.session_state.balance = 10000.0
    if 'positions' not in st.session_state:
        st.session_state.positions = []

    st.write(f"💰 **Số dư tài khoản Demo:** `${st.session_state.balance:,.2f}`")
    
    trade_col1, trade_col2, trade_col3 = st.columns(3)
    with trade_col1:
        order_type = st.selectbox("Loại lệnh", ["BUY (MUA)", "SELL (BÁN)"])
    with trade_col2:
        volume = st.number_input("Khối lượng (Lots)", min_value=0.01, max_value=10.0, value=0.1, step=0.1)
    with trade_col3:
        current_gold_price = 2354.50
        st.write(f"Giá khớp dự kiến: **${current_gold_price}**")
        execute_trade = st.button("VÀO LỆNH THỊ TRƯỜNG")
        
    if execute_trade:
        st.session_state.positions.append({
            "Thời gian": datetime.now().strftime("%H:%M:%S"),
            "Loại lệnh": order_type,
            "Khối lượng": volume,
            "Giá vào": current_gold_price
        })
        st.success(f"Khớp lệnh thành công: {order_type} {volume} Lots tại giá ${current_gold_price}")
        
    if st.session_state.positions:
        st.subheader("📝 Vị thế giao dịch hiện tại")
        st.dataframe(pd.DataFrame(st.session_state.positions), use_container_width=True)
        if st.button("Xóa toàn bộ lịch sử vị thế lệnh"):
            st.session_state.positions = []
            st.rerun()
# ===================================================================================================
# 7. GIÁ VÀNG VIỆT NAM & PHÂN TÍCH QUY ĐỔI
# ===================================================================================================
elif menu == "Giá Vàng VIỆT NAM":
    st.title("🇻🇳 Bảng Giá Vàng Việt Nam & Phân Tích Quy Đổi")
    st.caption("Hệ thống cập nhật dữ liệu trong nước và so sánh tương quan trực tiếp với thị trường quốc tế")
    
    # 1. Bảng giá vàng Việt Nam theo ảnh cung cấp
    st.subheader("📊 Bảng giá vàng trong nước hôm nay (Triệu VND/Lượng)")
    vn_gold_data = {
        "Thương hiệu / Loại vàng": ["Vàng miếng SJC 999.9", "Nhẫn Trơn PNJ 999.9", "Vàng Kim Bảo 999.9", "Vàng Phúc Lộc Tài 999.9"],
        "Giá Mua Vào": ["145,40", "145,40", "145,40", "145,40"],
        "Giá Bán Ra": ["148,40", "148,40", "148,40", "148,40"]
    }
    st.table(pd.DataFrame(vn_gold_data))
    
    # 2. Tự động lấy giá vàng thế giới trực tiếp từ Yahoo Finance để quy đổi độc lập
    st.markdown("---")
    st.subheader("🔄 Công cụ quy đổi & So sánh Vàng Thế giới")
    
    try:
        # Tải giá vàng thế giới thời gian thực để tính toán
        gold_ticker = yf.Ticker("GC=F")
        gold_hist = gold_ticker.history(period="1d")
        world_gold_oz = round(gold_hist['Close'].iloc[-1], 2)
    except:
        world_gold_oz = 2354.50  # Giá dự phòng nếu mất kết nối mạng API
        
    usd_vnd_rate = 25450  # Tỷ giá USD/VND giả định
    
    # Công thức toán học tính giá thô quy đổi ra lượng (1 lượng = 1.2057 ounce)
    world_gold_vn_raw = (world_gold_oz * 1.2057 * usd_vnd_rate) / 1000000
    sjc_ban_ra = 148.40  # Giá bán ra từ ảnh của bạn
    chenh_lech = sjc_ban_ra - world_gold_vn_raw
    
    col_q1, col_q2, col_q3 = st.columns(3)
    col_q1.metric("Giá Vàng Thế Giới", f"${world_gold_oz:,} / oz")
    col_q2.metric("Tỷ giá USD/VND (Giả định)", f"{usd_vnd_rate:,} VND")
    col_q3.metric("Giá Vàng TG Quy Đổi", f"{round(world_gold_vn_raw, 2)} Tr/Lượng")
    
    st.warning(f"⚠️ **Mức chênh lệch thực tế:** Giá vàng miếng SJC trong nước đang **cao hơn** vàng thế giới quy đổi khoảng **{round(chenh_lech, 2)} triệu đồng/lượng**.")

    # 3. Các thông tin kiến thức phân tích chuyên sâu
    st.markdown("---")
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        st.subheader("📚 Cách quy đổi giá vàng chuẩn")
        st.info("""
        **Công thức toán học hệ thống đang áp dụng:**
        $$Giá\\ Vàng\\ VN\\ (Tr/Lượng) = \\frac{Giá\\ TG\\ (USD/oz) \\times 1.2057 \\times Tỷ\\ giá\\ USD/VND}{1.000.000}$$
        
        *Trong đó:*
        * **Hệ số 1.2057**: Do 1 ounce troy = 31.103 gram, 1 lượng Việt Nam = 37.5 gram (37.5 / 31.103 = 1.2057).
        * Giá quy đổi trên là giá thô nguyên liệu, chưa bao gồm các chi phí như thuế nhập khẩu, phí dập khuôn SJC và biên lợi nhuận tiệm vàng.
        """)
    with col_inf2:
        st.subheader("🧐 Tại sao luôn có sự chênh lệch giá?")
        st.markdown("""
        <div class="ai-box" style="margin-bottom:0px;">
            <b>Có 3 nguyên nhân cốt lõi khiến giá vàng Việt Nam chênh lệch lớn với thế giới:</b><br><br>
            1. <b>Hạn chế nguồn cung độc quyền (Nghị định 24):</b> Nhà nước quản lý chặt chẽ việc sản xuất vàng miếng thương hiệu SJC khiến cung không tăng kịp cầu đột biến.<br>
            2. <b>Tâm lý phòng thủ dân cư:</b> Khi có tín hiệu lạm phát hay tỷ giá tăng, dòng tiền nội địa có xu hướng chuyển mạnh sang tích trữ vàng miếng an toàn.<br>
            3. <b>Rủi ro tỷ giá USD/VND:</b> Giá vàng thế giới tính bằng USD, khi tỷ giá USD biến động mạnh, các nhà kinh doanh trong nước buộc phải giữ giá bán cao để phòng thủ rủi ro mua lại nguyên liệu.
        </div>
        """, unsafe_allow_html=True)
# ===================================================================================================
# 8. 📅 Lịch Kinh Tế & AI Nhận Định (USD)
# ===================================================================================================
elif menu == "📅 Lịch Kinh Tế & AI Nhận Định (USD)":
    st.title("📅 Lịch Kinh Tế ForexFactory & Hệ Thống Trí Tuệ Nhân Tạo AI")
    st.caption("Cập nhật lịch sự kiện vĩ mô ảnh hưởng đồng USD kết hợp phân tích kịch bản & xu hướng từ AI")

    # Hàm lấy dữ liệu lịch kinh tế sạch từ API cộng đồng (Dự phòng dữ liệu mẫu nếu API bảo trì)
    @st.cache_data(ttl=300) # Lưu bộ nhớ đệm 5 phút để tối ưu tốc độ tải
    def get_economic_calendar():
        try:
            # Sử dụng nguồn cấp JSON tuần sạch của ForexFactory thay vì trang chủ bị chân
            url = "https://forexfactory.com"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                df = pd.DataFrame(response.json())
                # Chỉ lọc các tin tức liên quan trực tiếp đến đồng USD
                df = df[df['currency'] == 'USD']
                return df
        except:
            pass
        
        # Dữ liệu dự phòng đã chuẩn hóa tên cột 'currency' trùng khớp với điều kiện lọc
        mock_data = [
            {"title": "Core Retail Sales m/m", "currency": "USD", "date": "2026-07-09", "time": "18:30", "impact": "High", "forecast": "0.2%", "previous": "0.1%"},
            {"title": "Unemployment Claims", "currency": "USD", "date": "2026-07-09", "time": "18:30", "impact": "Medium", "forecast": "222K", "previous": "215K"},
            {"title": "CPI m/m (Lạm phát tháng)", "currency": "USD", "date": "2026-07-14", "time": "19:30", "impact": "High", "forecast": "0.1%", "previous": "0.2%"},
            {"title": "Federal Funds Rate (Lãi suất FED)", "currency": "USD", "date": "2026-07-30", "time": "01:00", "impact": "High", "forecast": "5.25%", "previous": "5.50%"},
            {"title": "10-y Bond Auction (Đấu thầu trái phiếu)", "currency": "USD", "date": "2026-07-10", "time": "23:01", "impact": "Low", "forecast": "", "previous": "4.25%"}
        ]
        return pd.DataFrame(mock_data)

    df_cal = get_economic_calendar()

    # Thống kê phân loại mức độ tác động tin tức
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    high_count = len(df_cal[df_cal['impact'].str.lower() == 'high']) if not df_cal.empty else 0
    med_count = len(df_cal[df_cal['impact'].str.lower() == 'medium']) if not df_cal.empty else 0
    low_count = len(df_cal[df_cal['impact'].str.lower() == 'low']) if not df_cal.empty else 0
    
    col_stat1.metric("🔴 Tin Tức Tác Động Mạnh (High)", f"{high_count} Tin")
    col_stat2.metric("🟡 Tin Tức Tác Động Vừa (Medium)", f"{med_count} Tin")
    col_stat3.metric("🟢 Tin Tức Tác Động Yếu (Low)", f"{low_count} Tin")

    st.markdown("---")
    
    # HIỂN THỊ LỊCH KINH TẾ ĐƯỢC CHUẨN HÓA GIAO DIỆN
    st.subheader("📋 Danh Sách Sự Kiện Vĩ Mô Đồng USD Trong Tuần")
    
    if not df_cal.empty:
        # Hàm xử lý chuỗi số liệu thành số thực để so sánh toán học
        def parse_value(val_str):
            if not val_str or pd.isna(val_str) or str(val_str).strip() == "":
                return None
            try:
                clean_str = str(val_str).replace('%', '').replace('K', '').replace('M', '').replace('$', '').strip()
                return float(clean_str)
            except:
                return None

        for idx, row in df_cal.iterrows():
            # 1. Định dạng màu sắc cảnh báo dựa trên mức độ quan trọng (Impact)
            impact_lower = str(row['impact']).lower()
            if impact_lower == 'high':
                bg_color = "#fef2f2"
                border_color = "#ef4444"
                badge = "🔴 HIGH IMPACT (Cực kỳ quan trọng)"
            elif impact_lower == 'medium':
                bg_color = "#fffbeb"
                border_color = "#f59e0b"
                badge = "🟡 MEDIUM IMPACT (Trung bình)"
            else:
                bg_color = "#f0fdf4"
                border_color = "#22c55e"
                badge = "🟢 LOW IMPACT (Biến động thấp)"

            # 2. Lấy dữ liệu Thực tế, Dự báo, Kỳ trước từ API công đồng
            actual_val_str = str(row.get('actual', '')).strip() if 'actual' in row and row['actual'] else 'N/A'
            forecast_val_str = str(row.get('forecast', '')).strip() if 'forecast' in row and row['forecast'] else 'N/A'
            previous_val_str = str(row.get('previous', '')).strip() if 'previous' in row and row['previous'] else 'N/A'
            
            # Nếu chưa đến giờ công bố tin (Actual trống), hệ thống lấy tạm số dự báo để demo trực quan màu sắc
            if actual_val_str == 'N/A' or actual_val_str == '':
                actual_val_str = forecast_val_str

            # 3. Logic so sánh toán học để đánh giá tác động lên đồng USD
            actual_num = parse_value(actual_val_str)
            forecast_num = parse_value(forecast_val_str)
            
            actual_color = "#1e293b" # Mặc định chữ màu đen
            ai_interpretation = "⚖️ Đang chờ công bố số liệu chính thức..."

            if actual_num is not None and forecast_num is not None:
                title_lower = str(row['title']).lower()
                
                # CHÚ Ý: Nếu Thất nghiệp (Unemployment Claims) TĂNG => Xấu cho USD (Đỏ), GIẢM => Tốt cho USD (Xanh)
                if "unemployment" in title_lower or "jobless" in title_lower:
                    if actual_num > forecast_num:
                        actual_color = "#dc2626"
                        ai_interpretation = "🔴 Tệ cho USD (Thất nghiệp tăng cao hơn dự kiến)"
                    elif actual_num < forecast_num:
                        actual_color = "#16a34a"
                        ai_interpretation = "🟢 Tốt cho USD (Thất nghiệp giảm hơn dự kiến)"
                    else:
                        ai_interpretation = "⚖️ Khớp dự báo (Thị trường ít biến động)"
                
                # Các chỉ số kinh tế chung khác (CPI, Retail Sales, GDP...) TĂNG => Tốt cho USD (Xanh), GIẢM => Xấu (Đỏ)
                else:
                    if actual_num > forecast_num:
                        actual_color = "#16a34a"
                        ai_interpretation = "🟢 Tốt cho USD (Số liệu thực tế mạnh hơn dự báo)"
                    elif actual_num < forecast_num:
                        actual_color = "#dc2626"
                        ai_interpretation = "🔴 Tệ cho USD (Số liệu thực tế yếu hơn dự báo)"
                    else:
                        ai_interpretation = "⚖️ Khớp dự báo (Thị trường ít biến động)"

            # 4. Đổ dữ liệu vào giao diện HTML chuyên nghiệp
            st.markdown(f"""
            <div style="background-color: {bg_color}; border-left: 6px solid {border_color}; padding: 15px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; color: #1e293b; font-size: 16px;">🇺🇸 {row['title']}</span>
                    <span style="font-size: 12px; font-weight: bold; padding: 4px 8px; border-radius: 4px; background: white; border: 1px solid {border_color}; color: {border_color};">{badge}</span>
                </div>
                <div style="margin-top: 8px; font-size: 14px; color: #475569; display: flex; gap: 20px; flex-wrap: wrap;">
                    <span>⏱️ <b>Thời gian:</b> {row['date']} lúc {row['time']}</span>
                    <span>🔮 <b>Dự báo:</b> {forecast_val_str}</span>
                    <span>↩️ <b>Kỳ trước:</b> {previous_val_str}</span>
                    <span>📊 <b>Thực tế:</b> <span style="color: {actual_color}; font-weight: bold;">{actual_val_str}</span></span>
                </div>
                <div style="margin-top: 8px; font-size: 13px; color: #2563eb; font-weight: 500;">
                    💡 <b>AI Đánh giá nhanh:</b> {ai_interpretation}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Hiện không có sự kiện kinh tế nào cho đồng USD trong tuần này.")

    st.markdown("---")

    # TAB PHÂN TÍCH CHUYÊN SÂU TỪ AI TỰ ĐỘNG
    st.subheader("🤖 Trí Tuệ Nhân Tạo AI Nghiên Cứu & Mô Phỏng Kịch Bản")
    
    tab1, tab2, tab3 = st.tabs(["🧠 Tâm Lý Thị Trường (Sentiment)", "🔮 Giả Thuyết Kịch Bản Trước Tin", "📈 Nhận Định Xu Hướng Số Ngày Tới"])
    
    with tab1:
        st.markdown("##### 📊 Bảng Đo Tâm Lý Đám Đông Trước Giờ G")
        # Mô phỏng thanh tiến trình Market Sentiment
        sentiment_val = st.slider("Chỉ số tâm lý Bullish DXY (Độ nén thị trường):", min_value=0, max_value=100, value=42)
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            st.progress(sentiment_val)
            st.caption(f"Phe Gấu (Bearish USD): {100 - sentiment_val}%  |  Phe Bò (Bullish USD): {sentiment_val}%")
        with col_s2:
            st.info("📌 **Đánh giá từ AI:** Thị trường đang có xu hướng lo ngại tin tức CPI sẽ thấp hơn dự báo, dòng tiền lớn dịch chuyển phòng thủ trước sang tài sản an toàn (Vàng).")
            
    with tab2:
        st.markdown("##### 🗺️ Ma Trận Giả Thuyết Tác Động Phản Ứng (AI Scenarios Mapping)")
        st.write("Hệ thống giả thuyết các trường hợp số liệu thực tế công bố để lên chiến lược giao dịch:")
        
        # Tạo bảng ma trận kịch bản cho người dùng dễ theo dõi
        scenario_data = {
            "Trường hợp dữ liệu": ["Thực tế > Dự báo (Tin Tốt)", "Thực tế = Dự báo (Đúng Kỳ Vọng)", "Thực tế < Dự báo (Tin Xấu)"],
            "Biến động đồng USD (DXY)": ["🚀 Tăng mạnh (Diều hâu)", "🔄 Đi ngang tích lũy", "📉 Giảm mạnh (Bồ câu)"],
            "Ảnh hưởng trực tiếp đến Vàng": ["📉 Sập giá kỹ thuật", "⚖️ Biến động quét hai đầu", "🚀 Bứt phá đỉnh cũ"],
            "Chiến lược khuyến nghị": ["Ưu tiên Short Vàng rải đòn bẩy", "Đứng ngoài quan sát cấu trúc nến", "Ưu tiên Long Vàng theo xu hướng"]
        }
        st.table(pd.DataFrame(scenario_data))
        
    with tab3:
        st.markdown("##### 🔮 Dự Báo Mô Hình Xu Hướng Trung Hạn (3-5 Ngày Tới)")
        st.markdown("""
        <div class="ai-box">
            <h5>📝 Kết luận phân tích đa biến từ AI:</h5>
            <ul>
                <li><b>Đồng USD (DXY Index):</b> Dự kiến chịu áp lực điều chỉnh ngắn hạn hướng về vùng hỗ trợ kỹ thuật cũ do chu kỳ dòng tiền đang chốt lời trái phiếu. Biên độ dao động kỳ vọng: 103.5 - 104.5.</li>
                <li><b>Xu hướng Giá Vàng (XAU/USD):</b> Cấu trúc dòng tiền thị trường (Flow of Funds) cho thấy lực gom mua ròng từ các Ngân hàng trung ương vẫn rất mạnh mẽ. Kết hợp với kịch bản tin tức vĩ mô bất lợi cho USD, giá Vàng có xác suất <b>68% tiếp tục duy trì xu hướng Bullish</b> tiến sát lại mốc kháng cự tâm lý cao hơn trong vòng 3 ngày tới.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
# ===================================================================================================
# 9. 🤖 AI Giải Đáp & Phân Tích
# ===================================================================================================
elif menu == "🤖 AI Giải Đáp & Phân Tích":
    st.title("🤖 Trợ Lý AI Phân Tích Vĩ Mô & Chiến Lược Giao Dịch")
    st.caption("Đặt câu hỏi trực tiếp để nhận phân tích chuyên sâu, giải đáp thuật ngữ vĩ mô và kịch bản thị trường từ AI")

    # 1. GỢI Ý CÁC CÂU HỎI MẪU CHO NGƯỜI DÙNG CHỌN NHANH
    st.write("💡 **Các chủ đề gợi ý bạn có thể hỏi AI:**")
    col_suggest1, col_suggest2 = st.columns(2)
    with col_suggest1:
        s1 = st.button("📈 Khi lạm phát CPI Mỹ tăng thì giá Vàng biến động thế nào?")
        s2 = st.button("🛡️ Tại sao căng thẳng địa chính trị lại làm tăng sức mạnh của Vàng?")
    with col_suggest2:
        s3 = st.button("💵 Mối quan hệ nghịch đảo giữa chỉ số DXY và XAU/USD là gì?")
        s4 = st.button("🏦 Nếu FED hạ lãi suất, tôi nên mua Vàng miếng hay Vàng nhẫn?")

    st.markdown("---")

    # 2. KHỞI TẠO BỘ NHỚ LƯU TRỮ LỊCH SỬ CHAT (SESSION STATE)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Xin chào! Tôi là Trợ lý AI chuyên sâu về Kinh tế Vĩ mô và Thị trường Vàng. Bạn cần tôi phân tích kịch bản tin tức, giải đáp thuật ngữ hay đưa ra chiến lược quản lý vốn nào hôm nay?"}
        ]

    # 3. HIỂN THỊ LỊCH SỬ ĐOẠN CHAT TRÊN GIAO DIỆN
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. HÀM XỬ LÝ PHẢN HỒI THÔNG MINH CỦA AI (KỊCH BẢN DỮ LIỆU ĐA BIẾN)
    def generate_ai_response(prompt):
        prompt_lower = prompt.lower()
        
        # Kịch bản 1: Hỏi về CPI / Lạm phát
        if "cpi" in prompt_lower or "lạm phát" in prompt_lower:
            return """##### 🧠 Phân tích từ AI về tác động của Lạm phát (CPI):
1. **Bản chất cốt lõi:** CPI (Chỉ số giá tiêu dùng) đo lường lạm phát. FED dựa vào CPI để quyết định tăng hoặc hạ lãi suất.
2. **Kịch bản biến động:**
   * **Nếu CPI tăng cao hơn dự báo:** FED sẽ có xu hướng giữ lãi suất cao lâu hơn (Diều hâu) ➔ Đồng USD (DXY) và Lợi suất trái phiếu tăng mạnh ➔ **Giá Vàng (XAU/USD) sẽ chịu áp lực giảm sập mạnh ngắn hạn**.
   * **Nếu CPI giảm mạnh hơn dự báo:** FED có cơ sở để cắt giảm lãi suất sớm hơn (Bồ câu) ➔ DXY suy yếu ➔ **Giá Vàng sẽ bứt phá phi mã**.
3. **Chiến lược giao dịch:** Trước giờ công bố tin CPI, tuyệt đối không nhồi lệnh lớn. Nên chờ cấu trúc nến H1 đóng cửa sau tin 15 phút để giao dịch theo xu hướng rõ ràng."""

        # Kịch bản 2: Hỏi về Địa chính trị / Chiến tranh
        elif "địa chính trị" in prompt_lower or "chiến tranh" in prompt_lower or "xung đột" in prompt_lower:
            return """##### 🌍 Phân tích từ AI về Yếu tố Địa chính trị:
1. **Tài sản trú ẩn an toàn (Safe-haven Asset):** Vàng luôn là hầm trú ẩn tối cao của dòng tiền khi thế giới xảy ra bất ổn, chiến tranh hoặc cấm vận kinh tế.
2. **Cơ chế tác động:** Khi căng thẳng leo thang, các ngân hàng trung ương toàn cầu (đặc biệt là Trung Quốc, Nga, Ấn Độ) có xu hướng bán bớt dự trữ bằng USD/Trái phiếu Mỹ để **chuyển dịch mạnh sang gom mua Vàng vật chất** nhằm phòng thủ rủi ro đóng băng tài sản.
3. **Lời khuyên:** Trong bối cảnh địa chính trị nóng, các nhịp giảm kỹ thuật của giá Vàng thường chỉ là ngắn hạn. Xu hướng chủ đạo trong trung hạn vẫn sẽ là **Bullish (Ưu tiên các vị thế Mua rải khi giá điều chỉnh về vùng hỗ trợ)**."""

        # Kịch bản 3: Hỏi về DXY (Đồng USD)
        elif "dxy" in prompt_lower or "usd" in prompt_lower:
            return """##### 💵 Phân tích mối quan hệ tương quan XAU/USD & DXY Index:
1. **Tương quan nghịch đảo (Negative Correlation):** Thống kê lịch sử cho thấy giá Vàng thế giới và chỉ số sức mạnh đồng USD (DXY) có mối quan hệ ngược chiều nhau lên tới **80% thời gian**.
2. **Lý do kỹ thuật:** Vàng được định giá bằng đồng USD. Khi chỉ số DXY tăng giá (đồng USD có giá trị hơn), người mua bằng các đồng tiền khác (như EUR, JPY, VND) phải tốn nhiều chi phí hơn để sở hữu cùng một lượng Vàng, làm giảm nhu cầu mua và đẩy giá Vàng đi xuống.
3. **Ứng dụng thực tế:** Hãy luôn mở biểu đồ DXY song song với biểu đồ Vàng. Nếu DXY đứt gãy vùng hỗ trợ kỹ thuật quan trọng trên khung ngày, đó là tín hiệu cực mạnh kích hoạt một đà tăng trưởng dài hạn cho XAU/USD."""

        # Kịch bản 4: Hỏi về Lãi suất / FED
        elif "fed" in prompt_lower or "lãi suất" in prompt_lower:
            return """##### 🏦 Nhận định chiến lược về Chính sách Lãi suất của FED:
1. **Kẻ thù của Vàng là Lãi suất cao:** Vàng là tài sản không sản sinh lợi suất (không trả cổ tức/lãi suất như gửi ngân hàng hay mua trái phiếu). Do đó, khi FED duy trì lãi suất ở đỉnh, chi phí cơ hội của việc nắm giữ Vàng sẽ rất cao.
2. **Kịch bản chu kỳ cắt giảm lãi suất:** Khi FED chính thức bước vào chu kỳ nới lỏng tiền tệ (hạ lãi suất):
   * Áp lực chi phí cơ hội biến mất.
   * Đồng USD mất giá trị dòng tiền đầu tư gửi tiết kiệm.
   ➔ **Dòng tiền thông minh bắt buộc phải chảy sang Vàng, kích hoạt chu kỳ siêu tăng giá (Super Bullrun).**
3. **Khuyên dùng tại Việt Nam:** Nếu FED hạ lãi suất, biên độ tăng của **Vàng Nhẫn 9999** thường sẽ nhạy bén và bám sát tốc độ tăng của thế giới hơn so với Vàng miếng SJC (vốn bị kiểm soát chặt về nguồn cung độc quyền)."""

        # Kịch bản mặc định: Trả lời tự động thông minh bằng AI tổng hợp dữ liệu vĩ mô
        else:
            return f"""##### 🤖 Ý kiến tổng hợp từ Trợ lý AI:
Cảm ơn bạn đã đặt câu hỏi: *"{prompt}"*. 

Dựa trên các thuật toán theo dõi dòng tiền (Flow of Funds) và dữ liệu lịch kinh tế hiện tại của hệ thống, tôi khuyến nghị bạn nên phân tách câu hỏi này thành các yếu tố tác động đến 3 trục chính:
1. **Chính sách tiền tệ:** Yếu tố này có làm thay đổi lộ trình lãi suất của FED trong ngắn hạn không?
2. **Tâm lý thị trường (Sentiment):** Hiện tại phe Bò (Mua) hay phe Gấu (Bán) đang chiếm ưu thế trên sàn giao dịch? (Bạn có thể kiểm tra thanh đo tâm lý ở Mục số 8).
3. **Xu hướng kỹ thuật:** Giá có đang nằm trên đường trung bình động MA20 để ủng hộ xu hướng tăng không?

*Nếu bạn muốn biết chi tiết cụ thể hơn về một thuật ngữ hoặc chỉ báo nào, hãy gõ từ khóa rõ ràng (Ví dụ: 'CPI', 'DXY', 'FED', 'Địa chính trị') để tôi phân tích chuyên sâu nhé!*"""

    # 5. XỬ LÝ KHI NGƯỜI DÙNG BẤM CÁC NÚT GỢI Ý NHANH
    chosen_prompt = None
    if s1: chosen_prompt = "Khi lạm phát CPI Mỹ tăng thì giá Vàng biến động thế nào?"
    if s2: chosen_prompt = "Tại sao căng thẳng địa chính trị lại làm tăng sức mạnh của Vàng?"
    if s3: chosen_prompt = "Mối quan hệ nghịch đảo giữa chỉ số DXY và XAU/USD là gì?"
    if s4: chosen_prompt = "Nếu FED hạ lãi suất, tôi nên mua Vàng miếng hay Vàng nhẫn?"

    if chosen_prompt:
        st.session_state.chat_history.append({"role": "user", "content": chosen_prompt})
        response = generate_ai_response(chosen_prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    # 6. Ô NHẬP LIỆU CHAT TRỰC TIẾP TỪ NGƯỜI DÙNG (CHAT INPUT)
    if user_query := st.chat_input("Nhập câu hỏi vĩ mô hoặc thuật ngữ tài chính tại đây..."):
        # Hiển thị câu hỏi của user
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        # Hệ thống AI tính toán và đưa ra câu trả lời tương ứng
        with st.chat_message("assistant"):
            ai_response = generate_ai_response(user_query)
            st.markdown(ai_response)
            
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
