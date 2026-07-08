
# 📈 Dự án Phân tích Kinh Tế Vĩ Mô & Nhận định Giá Vàng (XAU/USD)

Hệ thống bảng điều khiển toàn diện (All-in-one Dashboard) tích hợp dữ liệu kinh tế vĩ mô thời gian thực, biểu đồ kỹ thuật tương tác, bản đồ điểm nóng địa chính trị và mô hình kết luận xu hướng từ trí tuệ nhân tạo AI.

## ✨ Tính năng chính
- **Dashboard Đa tài sản:** Biểu đồ nến tương tác thời gian thực của XAUUSD, DXY, US10Y, VIX, WTI từ TradingView.
- **Bảng dữ liệu vĩ mô Mỹ:** Cập nhật tự động lịch trình CPI, NFP, GDP, FOMC...
- **Bản đồ trực quan toàn cầu:** Hiển thị điểm nóng chiến tranh và phân bố màu sắc lượng dự trữ vàng quốc gia.
- **Trí tuệ nhân tạo (AI Engine):** Tổng hợp tin tức từ ForexFactory, phân tích tác động vĩ mô và chấm điểm xu hướng Bullish/Bearish.
- **Trình giả lập Trading:** Cho phép mở lệnh Demo Mua/Bán trực quan trên biểu đồ XAUUSD thực tế.

## 🚀 Hướng dẫn cài đặt và Chạy hệ thống

### 1. Khởi động Backend (Python Server)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
*Lưu ý: Tạo file `.env` trong thư mục `backend` và điền khóa bí mật `OPENAI_API_KEY` của bạn.*

### 2. Khởi động Frontend
Bạn chỉ cần mở trực tiếp file `frontend/index.html` trên trình duyệt hoặc chạy thông qua tiện ích mở rộng Live Server của VS Code để trải nghiệm giao diện thời gian thực.
