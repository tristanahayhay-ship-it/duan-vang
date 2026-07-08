
// 1. Nhúng Biểu đồ Nến Tương tác TradingView cho Vàng (XAUUSD) và Đô la (DXY)
document.addEventListener("DOMContentLoaded", function() {
    new TradingView.widget({
        "width": "100%",
        "height": "100%",
        "symbol": "FX_IDC:XAUUSD",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "vi",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_gold"
    });

    new TradingView.widget({
        "width": "100%",
        "height": "100%",
        "symbol": "CAPITALCOM:DXY",
        "interval": "D",
        "theme": "dark",
        "style": "1",
        "locale": "vi",
        "container_id": "tradingview_dxy"
    });

    // Gọi dữ liệu từ Backend khi trang tải xong
    fetchMacroData();
    fetchAIDecision();
    initConflictMap();
});

// 2. Lấy dữ liệu bảng chỉ số kinh tế Mỹ từ Backend API
async function fetchMacroData() {
    try {
        const response = await fetch('http://127.0.0');
        const data = await response.json();
        const tbody = document.getElementById('macro-table-body');
        tbody.innerHTML = ""; // Xóa dữ liệu cũ

        for (const [key, item] of Object.entries(data)) {
            tbody.innerHTML += `
                <tr class="hover:bg-gray-700/50 transition">
                    <td class="p-3 font-semibold text-gray-300">${key.replace('_', ' ')}</td>
                    <td class="p-3 text-amber-400 font-bold">${item.value}</td>
                    <td class="p-3 text-xs ${item.status.includes('Bullish') ? 'text-green-400' : 'text-red-400'}">${item.status}</td>
                </tr>
            `;
        }
    } catch (error) {
        console.error("Không thể kết nối API Backend dữ liệu vĩ mô.", error);
    }
}

// 3. Lấy dữ liệu Kết luận Toàn cảnh từ Trí tuệ Nhân tạo AI
async function fetchAIDecision() {
    try {
        const response = await fetch('http://127.0.0');
        const data = await response.json();
        document.getElementById('ai-trend').innerText = `${data.trend} (${data.sentiment_score}/100)`;
        document.getElementById('ai-desc').innerText = data.explanation;
    } catch (error) {
        console.error("Lỗi gọi AI nhận định.", error);
    }
}

// 4. Khởi tạo Bản đồ Xung đột và Dự trữ Vàng sử dụng Leaflet
function initConflictMap() {
    // Tọa độ trung tâm bản đồ thế giới
    var map = L.map('map').setView([20.0, 0.0], 2);
    L.tileLayer('https://{s}://{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Điểm nóng xung đột mẫu
    var middleEast = L.circle([31.5, 34.8], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 500000
    }).addTo(map).bindPopup('<b>Điểm nóng Địa chính trị Trung Đông</b><br>Tình trạng: Căng thẳng cao độ (Hỗ trợ giá Vàng tăng)');
}

// 5. Logic Công cụ mua bán giả lập (Demo Trading) cơ bản
function executeDemoOrder(type) {
    const lot = document.getElementById('trade-volume').value;
    const statusBox = document.getElementById('order-status');
    statusBox.className = type === 'BUY' ? 'text-green-400 font-bold' : 'text-red-400 font-bold';
    statusBox.innerText = `Đã mở trạng thái ${type} ${lot} lot XAUUSD thành công tại giá thị trường thực!`;
}
