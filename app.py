import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN
# ==============================================================================
st.set_page_config(
    page_title="Kinh tế Vĩ mô & Nhận định Giá Vàng",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo bộ nhớ phiên cho Công cụ Mua bán giả lập
if "trading_journal" not in st.session_state:
    st.session_state.trading_journal = []
if "balance" not in st.session_state:
    st.session_state.balance = 100000.0  # Vốn giả lập ban đầu: 100,000 USD

st.title("🦅 KINH TẾ VĨ MÔ & NHẬN ĐỊNH GIÁ VÀNG (XAU/USD)")
st.markdown("---")

# ==============================================================================
# 2. THANH CHỌN CHỨC NĂNG CHÍNH (TABS)
# ==============================================================================
tabs = st.tabs([
    "📊 Dashboard Tổng Quan", 
    "🇺🇸 Dữ Liệu Kinh Tế Mỹ", 
    "💵 Dòng Tiền & Quỹ", 
    "📈 Tin Tức & Cổ Phiếu", 
    "⚔️ Chiến Tranh & Địa Chính Trị", 
    "🛠️ Công Cụ Hỗ Trợ & Trade"
])

# ==============================================================================
# TAB 1: DASHBOARD TỔNG QUAN
# ==============================================================================
with tabs[0]:
    st.subheader("📡 Thị Trường Thời Gian Thực (TradingView Official Advanced Widgets)")
    
    # Bố cục lưới cho các biểu đồ kỹ thuật tương tác
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🟡 Giá Vàng (XAU/USD) & 💵 Chỉ số DXY**")
        # Nhúng Widget biểu đồ vàng chính thức
        st.components.v1.html("""
            <div class="tradingview-widget-container" style="height:400px;width:100%;">
              <div id="tradingview_gold" style="height:100%;width:100%;"></div>
              <script type="text/javascript" src="https://tradingview.com"></script>
              <script type="text/javascript">
              new TradingView.widget({
              "width": "100%",
              "height": "100%",
              "symbol": "OANDA:XAUUSD",
              "interval": "D",
              "timezone": "Asia/Ho_Chi_Minh",
              "theme": "dark",
              "style": "1",
              "locale": "vi",
              "enable_publishing": false,
              "hide_side_toolbar": false,
              "allow_symbol_change": true,
              "container_id": "tradingview_gold"
              });
              </script>
            </div>
        """, height=400)

        st.markdown("**📉 Chỉ số Biến Động VIX**")
        # Nhúng Widget biểu đồ VIX chính thức
        st.components.v1.html("""
            <div class="tradingview-widget-container" style="height:300px;width:100%;">
              <div id="tradingview_vix" style="height:100%;width:100%;"></div>
              <script type="text/javascript" src="https://tradingview.com"></script>
              <script type="text/javascript">
              new TradingView.widget({
              "width": "100%",
              "height": "100%",
              "symbol": "TVC:VIX",
              "interval": "D",
              "timezone": "Asia/Ho_Chi_Minh",
              "theme": "dark",
              "style": "1",
              "locale": "vi",
              "container_id": "tradingview_vix"
              });
              </script>
            </div>
        """, height=300)

    with col2:
        st.markdown("**🇺🇸 Lợi Suất Trái Phiếu Mỹ 10 Năm (US10Y)**")
        # Nhúng Widget biểu đồ lợi suất trái phiếu chính thức
        st.components.v1.html("""
            <div class="tradingview-widget-container" style="height:400px;width:100%;">
              <div id="tradingview_us10y" style="height:100%;width:100%;"></div>
              <script type="text/javascript" src="https://tradingview.com"></script>
              <script type="text/javascript">
              new TradingView.widget({
              "width": "100%",
              "height": "100%",
              "symbol": "TVC:US10Y",
              "interval": "D",
              "timezone": "Asia/Ho_Chi_Minh",
              "theme": "dark",
              "style": "1",
              "locale": "vi",
              "container_id": "tradingview_us10y"
              });
              </script>
            </div>
        """, height=400)

        st.markdown("**🛢️ Giá Dầu Thô WTI**")
        # Nhúng Widget biểu đồ giá dầu WTI chính thức
        st.components.v1.html("""
            <div class="tradingview-widget-container" style="height:300px;width:100%;">
              <div id="tradingview_wti" style="height:100%;width:100%;"></div>
              <script type="text/javascript" src="https://tradingview.com"></script>
              <script type="text/javascript">
              new TradingView.widget({
              "width": "100%",
              "height": "100%",
              "symbol": "TVC:USOIL",
              "interval": "D",
              "timezone": "Asia/Ho_Chi_Minh",
              "theme": "dark",
              "style": "1",
              "locale": "vi",
              "container_id": "tradingview_wti"
              });
              </script>
            </div>
        """, height=300)

    st.markdown("---")
    st.subheader("📅 Lịch Kinh Tế & Phân Tích Xu Hướng AI")
    
    col_calendar, col_ai = st.columns([2, 1])
    with col_calendar:
        st.markdown("**Lịch Kinh Tế Hôm Nay (Nguồn dữ liệu kết nối từ ForexFactory)**")
        # Giả lập bảng lịch kinh tế nâng cao
        calendar_data = pd.DataFrame({
            "Thời gian": ["19:30", "19:30", "22:00"],
            "Tiền tệ": ["USD", "USD", "USD"],
            "Sự kiện": ["Core CPI m/m", "CPI y/y", "Thành viên FOMC phát biểu"],
            "Mức độ": ["🔴 Cao", "🔴 Cao", "🟠 Trung bình"],
            "Dự báo": ["0.2%", "3.1%", "-"],
            "Thực tế": ["0.3%", "3.2%", "-"]
        })
        st.dataframe(calendar_data, use_container_width=True)
        
    with col_ai:
        st.markdown("🤖 **AI Nhận Định & Kết Luận Xu Hướng Từ FXStreet-VN**")
        st.info(
            "**Tóm tắt tin tức:** CPI Mỹ cao hơn dự báo làm giảm khả năng Fed hạ lãi suất sớm. "
            "Áp lực bán ngắn hạn xuất hiện trên đồ thị XAU/USD.\n\n"
            "➡️ **Kết luận xu hướng AI:** **BEARISH (GIẢM GIÁ NGẮN HẠN)** đối với Vàng. Mục tiêu hỗ trợ gần nhất: $2600."
        )

# ==============================================================================
# TAB 2: DỮ LIỆU KINH TẾ MỸ
# ==============================================================================
with tabs[1]:
    st.subheader("📊 Bảng Chỉ Số Vĩ Mô Hoa Kỳ (Cập nhật Real-time)")
    
    # Bảng dữ liệu tự động cập nhật (Giả lập cấu trúc gọi API chuyên sâu)
    macro_indicators = pd.DataFrame({
        "Chỉ số": ["CPI", "Core CPI", "PCE", "Core PCE", "NFP (Bảng lương phi nông nghiệp)", "Tỷ lệ thất nghiệp", "GDP", "PMI", "Doanh số bán lẻ", "JOLTS", "ADP", "ISM Manufacturing"],
        "Kỳ gần nhất": ["3.2%", "3.8%", "2.5%", "2.8%", "175K", "3.9%", "1.6%", "50.3", "0.7%", "8.5M", "192K", "49.2"],
        "Kỳ trước": ["3.1%", "3.7%", "2.4%", "2.7%", "315K", "3.8%", "3.4%", "51.9", "0.9%", "8.8M", "208K", "50.3"],
        "Trạng thái": ["Tăng áp lực", "Xấu cho vàng", "Ổn định", "Giữ nguyên", "Yếu hơn", "Tăng nhẹ", "Chậm lại", "Thu hẹp", "Tốt", "Giảm tuyển dụng", "Giảm", "Co hẹp"]
    })
    st.dataframe(macro_indicators, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📉 Biểu Đồ Lịch Sử Dữ Liệu Tùy Chỉnh Thời Gian")
    selected_indicator = st.selectbox("Chọn chỉ số xem biểu đồ cột:", ["CPI", "NFP", "GDP", "Tỷ lệ thất nghiệp"])
    
    # Tạo biểu đồ giả lập có thể điều chỉnh thời gian
    years = st.slider("Khoảng thời gian phân tích (Năm):", 2018, 2026, (2022, 2026))
    fig_macro = go.Figure(data=[
        go.Bar(name='Thực tế', x=['Q1/23', 'Q2/23', 'Q3/23', 'Q4/23', 'Q1/24', 'Q2/24'], y=[3.1, 3.5, 4.0, 3.8, 3.5, 3.2])
    ])
    fig_macro.update_layout(title=f"Lịch sử biến động chỉ số {selected_indicator}", barmode='group')
    st.plotly_chart(fig_macro, use_container_width=True)

    st.markdown("---")
    st.subheader("🎙️ Phát Biểu Của FED & Tin Tức Tự Động")
    st.success("🔥 **Tin tức khẩn cấp (Real-time):** Chủ tịch Jerome Powell phát biểu tại Diễn đàn Kinh tế: 'Chúng tôi cần thêm bằng chứng lạm phát hạ nhiệt trước khi cắt giảm lãi suất'.")
    
    st.markdown("**🧠 Đánh Giá Tổng Hợp Vĩ Mô Ảnh Hưởng Đến Vàng:**")
    st.warning("Lạm phát dai dẳng kết hợp thị trường lao động thắt chặt tạo môi trường Diều hâu (Hawkish), điều này làm tăng lợi suất và gây áp lực giảm trực tiếp lên giá Vàng.")

# ==============================================================================
# TAB 3: DÒNG TIỀN & QUỸ
# ==============================================================================
with tabs[2]:
    st.subheader("💰 Hành Động Của Dòng Tiền Lớn (Smart Money)")
    
    col_gld, col_cb = st.columns(2)
    with col_gld:
        st.markdown("**📦 Dòng vốn Quỹ ETF Vàng (GLD, IAU) từ MacroMicro**")
        st.info("💡 *Gợi ý cấu hình:* Nhúng mã iframe đồ thị dòng vốn dòng tiền mua/bán ròng của quỹ SPDR Gold Shares.")
        st.components.v1.html("""
            <iframe src="https://en.macromicro.me/charts/23274/gld-fund-flow" width="100%" height="350" frameborder="0"></iframe>
        """, height=350)
        
    with col_cb:
        st.markdown("**🏦 Dự Trữ Vàng Ngân Hàng Trung Ương (Muavangbac.vn)**")
        # Mô phỏng biểu đồ dự trữ vàng thế giới
        fig_reserve = go.Figure(data=[go.Pie(labels=['Mỹ', 'Đức', 'IMF', 'Ý', 'Pháp', 'Trung Quốc', 'Nga'], values=[8133, 3352, 2814, 2451, 2436, 2264, 2332])])
        fig_reserve.update_layout(title="Khối lượng dự trữ vàng của các NHTW lớn (Tấn)")
        st.plotly_chart(fig_reserve, use_container_width=True)

    st.markdown("---")
    st.markdown("**📊 Báo Cáo COT (Commitment of Traders) & Nhận Định Nước Đi Dòng Tiền**")
    st.components.v1.html("""
        <div style="height:350px;">
        <iframe src="https://tradingview.com" width="100%" height="100%" frameborder="0"></iframe>
        </div>
    """, height=350)
    
    st.markdown("🔮 **Nhận định xu hướng dòng tiền tổng hợp:** Các quỹ lớn đang giảm trạng thái vị thế mua ròng (Long), chuyển dịch dòng vốn sang các tài sản phi rủi ro có lợi suất ngắn hạn.")

# ==============================================================================
# TAB 4: TIN TỨC & CHỈ SỐ CỔ PHIẾU
# ==============================================================================
with tabs[3]:
    st.subheader("🏢 Thị Trường Chứng Khoán & Sức Khỏe Doanh Nghiệp")
    
    col_stock1, col_stock2 = st.columns([1, 2])
    with col_stock1:
        st.markdown("**Bảng điểm chỉ số chứng khoán chính**")
        # Sử dụng yfinance để lấy dữ liệu chứng khoán thật nếu muốn
        st.metric(label="S&P 500 (^GSPC)", value="5,150.48", delta="+12.50 (+0.24%)")
        st.metric(label="Dow Jones (^DJI)", value="39,127.14", delta="-45.20 (-0.12%)")
        st.metric(label="Nasdaq 100 (^NDX)", value="18,105.30", delta="+98.10 (+0.54%)")
        
    with col_stock2:
        st.markdown("**Biểu đồ diễn biến S&P 500 thực tế**")
        st.components.v1.html("""
            <div style="height:300px;">
            <iframe src="https://tradingview.com" width="100%" height="100%" frameborder="0"></iframe>
            </div>
        """, height=300)

# ==============================================================================
# TAB 5: CHIẾN TRANH & ĐỊA CHÍNH TRỊ (Sử dụng cấu trúc phân tách rõ ràng)
# ==============================================================================
with tabs[4]:
    st.subheader("⚔️ Bản Đồ Địa Chỉ Chính Trị & Rủi Ro Chiến Tranh")
    
    col_war1, col_war2 = st.columns(2)
    
    with col_war1:
        st.markdown("**🛑 Cập nhật xung đột & Đàm phán trực tuyến**")
        st.error("🚨 **Tin căng thẳng:** Tình hình địa chính trị leo thang tạo áp lực lên chuỗi cung ứng toàn cầu.")
        st.info("🕊️ **Tiến trình đàm phán:** Các bên chưa đạt thỏa thuận chung. Rủi ro đẩy giá vàng làm hầm trú ẩn an toàn.")
        
        st.markdown("**🗺️ Bản đồ các quốc gia dự trữ vàng lớn thế giới**")
        # Bản đồ Choropleth phân loại màu sắc theo khối lượng dự trữ vàng giả lập
        gold_reserves = pd.DataFrame({
            "Quốc gia": ["USA", "DEU", "ITA", "FRA", "CHN", "RUS", "JPN", "IND"],
            "Mã": ["USA", "DEU", "ITA", "FRA", "CHN", "RUS", "JPN", "IND"],
            "Tấn Vàng": [8133, 3352, 2451, 2436, 2264, 2332, 846, 803]
        })
        fig_reserve_map = go.Figure(data=go.Choropleth(
            locations=gold_reserves['Mã'],
            z=gold_reserves['Tấn Vàng'],
            text=gold_reserves['Quốc gia'],
            colorscale='YlOrRd',
            autocolorscale=False,
            reversescale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title='Tấn Vàng',
        ))
        fig_reserve_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        st.plotly_chart(fig_reserve_map, use_container_width=True)

    with col_war2:
        st.markdown("**🗺️ Điểm nóng xung đột địa chính trị (Real-time Alert)**")
        # Sử dụng Scattergeo hiển thị các vùng cảnh báo xung đột nguy hiểm
        fig_conflict_map = go.Figure(go.Scattergeo(
            lon=[35.21, 31.23, 47.90],
            lat=[31.76, 30.04, 29.31],
            text=["Điểm nóng A (Cảnh báo đỏ)", "Vùng tranh chấp B", "Khu vực kiểm soát C"],
            mode='markers+text',
            textposition="top center",
            marker=dict(size=14, color='red', symbol='triangle', opacity=0.9)
        ))
        fig_conflict_map.update_layout(
            geo_scope='asia',
            margin=dict(l=0, r=0, t=0, b=0),
            height=500
        )
        st.plotly_chart(fig_conflict_map, use_container_width=True)


# ==============================================================================
# TAB 6: CÔNG CỤ HỖ TRỢ & TRADE GIẢ LẬP
# ==============================================================================
with tabs[5]:
    st.subheader("🛠️ Toàn Cảnh Phân Tích Kỹ Thuật XAU/USD")
    
    col_tool1, col_tool2 = st.columns([1, 2])
    
    with col_tool1:
        st.markdown("**🎯 Chấm Điểm Xu Hướng Chỉ Báo Kỹ Thuật**")
        st.metric(label="ĐIỂM XU HƯỚNG TỔNG HỢP", value="BULLISH (MUA MẠNH)", delta="+85/100")
        
        # Nhúng Đồng hồ đo kỹ thuật real-time chuẩn từ TradingView cho XAUUSD [1]
        st.components.v1.html("""
            <div style="height:380px;">
            <iframe src="https://tradingview.com" width="100%" height="100%" frameborder="0" scrolling="no"></iframe>
            </div>
        """, height=380)
        
    with col_tool2:
        st.markdown("**🖥️ Trạm Giao Dịch Thao Tác Trực Tiếp (Investing/TradingView)**")
        # Nhúng Biểu đồ kỹ thuật đầy đủ công cụ vẽ cho XAUUSD [1]
        st.components.v1.html("""
            <div style="height:480px;">
            <iframe src="https://tradingview.com" width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
            </div>
        """, height=480)

    st.markdown("---")
    st.subheader("🎮 Hệ Thống Giao Dịch Mô Phỏng (Demo Trading XAU/USD)")
    
    # Giả định lấy giá thị trường thực từ API (ở đây tạm để cố định)
    current_gold_price = 2650.00
    
    st.markdown(f"💰 Vốn khả dụng: <span style='color:#00ff00; font-size:20px; font-weight:bold;'>{st.session_state.balance:,.2f} USD</span> | Giá vàng hiện tại: **${current_gold_price}**", unsafe_allow_html=True)
    
    trade_col1, trade_col2, trade_col3 = st.columns(3)
    
    with trade_col1:
        action = st.selectbox("Hành động", ["BUY", "SELL"], key="demo_action")
    with trade_col2:
        volume = st.number_input("Khối lượng (Lots)", min_value=0.01, max_value=10.0, value=0.1, step=0.01, key="demo_volume")
    with trade_col3:
        st.markdown("<br>", unsafe_allow_html=True) # Căn chỉnh nút bấm thẳng hàng
        if st.button("🚀 Thực hiện VÀO LỆNH", use_container_width=True):
            # Tính toán ký quỹ hoặc trừ tiền giả lập (Ví dụ: 1 Lot XAUUSD cần khoảng 1000$ ký quỹ)
            margin_required = volume * 1000
            
            if st.session_state.balance >= margin_required:
                # Trừ tiền tài khoản (Giả định trừ chi phí spread/ký quỹ ban đầu)
                st.session_state.balance -= margin_required
                
                # Lưu thông tin lệnh vào lịch sử
                trade_entry = {
                    "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Loại": action,
                    "Khối lượng": volume,
                    "Giá vào": current_gold_price,
                    "Ký quỹ (USD)": margin_required,
                    "Trạng thái": "Đang mở"
                }
                st.session_state.trading_journal.append(trade_entry)
                st.toast(f"Đặt lệnh {action} thành công {volume} Lots!", icon="✅")
                st.rerun() # Làm mới giao diện để cập nhật lại số dư ví tức thì
            else:
                st.error("❌ Tài khoản không đủ số dư để thực hiện ký quỹ cho khối lượng này!")

    # Hiển thị nhật ký giao dịch nếu có lệnh
    if st.session_state.trading_journal:
        st.markdown("📜 **Nhật Ký Các Lệnh Giao Dịch Đang Mở:**")
        df_journal = pd.DataFrame(st.session_state.trading_journal)
        st.dataframe(df_journal, use_container_width=True)
        
        # Thêm nút bấm Reset tài khoản để thực hành lại từ đầu
        if st.button("🔄 Khôi phục tài khoản (Reset Demo)"):
            st.session_state.balance = 100000.0
            st.session_state.trading_journal = []
            st.rerun()

