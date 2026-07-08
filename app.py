import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app) # Cho phép Frontend kết nối tới Backend

# Cấu hình API Keys (Cần điền vào file .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

@app.route('/api/macro-data', methods=['GET'])
def get_macro_data():
    """API lấy dữ liệu kinh tế Mỹ (CPI, NFP, Unemployment Rate, GDP...)"""
    # Trong thực tế, bạn sẽ gọi tới AlphaVantage hoặc Fred API. 
    # Dưới đây là dữ liệu mẫu mô phỏng dữ liệu thời gian thực cập nhật.
    sample_data = {
        "CPI": {"value": "3.1%", "status": "Bearish for Gold"},
        "Core_CPI": {"value": "3.8%", "status": "Neutral"},
        "NFP": {"value": "175K", "status": "Bullish for Gold"},
        "Unemployment_Rate": {"value": "3.9%", "status": "Bullish for Gold"},
        "GDP": {"value": "2.5%", "status": "Bearish for Gold"},
        "PMI": {"value": "49.2", "status": "Bullish for Gold"}
    }
    return jsonify(sample_data)

@app.route('/api/ai-analysis', methods=['GET'])
def get_ai_analysis():
    """AI tổng hợp tin tức từ ForexFactory, Chiến tranh, Dòng tiền để nhận định giá Vàng"""
    # Logic gọi OpenAI GPT-4 để phân tích toàn cảnh vĩ mô
    # Ở đây giả lập kết quả trả về từ AI sau khi quét dữ liệu hệ thống
    ai_response = {
        "sentiment_score": 75, # 75/100 Điểm Bullish
        "trend": "BULLISH (Tăng giá)",
        "explanation": "Lợi suất trái phiếu Mỹ 10Y đang giảm mạnh kết hợp với rủi ro địa chính trị leo thang tại Trung Đông làm tăng nhu cầu trú ẩn an toàn vào Vàng. Chỉ số DXY suy yếu hỗ trợ trực tiếp cho XAU/USD hướng tới mốc kháng cự tiếp theo.",
        "cot_report": "Các quỹ lớn (Large Speculators) tiếp tục gia tăng vị thế vị thế Mua ròng (Net Long)."
    }
    return jsonify(ai_response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


