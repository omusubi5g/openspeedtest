from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime
import sqlite3
import threading

app = Flask(__name__)
CORS(app)

# SQLiteデータベースの初期化
def init_db():
    with sqlite3.connect('network_data.db') as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            timestamp TEXT,
            ip_address TEXT,
            download_speed REAL,
            upload_speed REAL,
            rtt REAL,
            jitter REAL
        )
        ''')

# データベースを初期化
init_db()
db_lock = threading.Lock()

# HTMLテンプレート
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ネットワーク測定データ</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .button {
            padding: 10px 20px;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
            margin-bottom: 20px;
        }
        .refresh-button {
            background-color: #4CAF50;
        }
        .clear-button {
            background-color: #f44336;
        }
        .button:hover {
            opacity: 0.9;
        }
        .button-container {
            margin-bottom: 20px;
        }
    </style>
    <script>
        function refreshTable() {
            location.reload();
        }
        
        function clearDatabase() {
            if (confirm('本当にデータベースをクリアしますか？')) {
                fetch('/', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                })
                .catch(error => {
                    alert('エラーが発生しました: ' + error);
                });
            }
        }
        
        // 30秒ごとに自動更新
        setInterval(refreshTable, 30000);
    </script>
</head>
<body>
    <h1>ネットワーク測定データ</h1>
    <div class="button-container">
        <button class="button refresh-button" onclick="refreshTable()">更新</button>
        <button class="button clear-button" onclick="clearDatabase()">データベースをクリア</button>
    </div>
    <table>
        <thead>
            <tr>
                <th>タイムスタンプ</th>
                <th>IPアドレス</th>
                <th>ダウンロード速度 [Mbps]</th>
                <th>アップロード速度 [Mbps]</th>
                <th>RTT [ms]</th>
                <th>Jitter [ms]</th>
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ "%.2f"|format(row[2]) }}</td>
                <td>{{ "%.2f"|format(row[3]) }}</td>
                <td>{{ "%.1f"|format(row[4]) }}</td>
                <td>{{ "%.1f"|format(row[5]) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
'''

@app.route('/')
def index():
    with db_lock:
        with sqlite3.connect('network_data.db') as conn:
            # 最新100件のデータを取得
            data = conn.execute('''
                SELECT timestamp, ip_address, download_speed, upload_speed, rtt, jitter 
                FROM measurements 
                ORDER BY timestamp DESC 
                LIMIT 100
            ''').fetchall()
    return render_template_string(HTML_TEMPLATE, data=data)

@app.route('/', methods=['POST'])
def receive_post():
    if request.method == 'POST':
        try:
            # フォームデータの取得
            data = request.form
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip_address = request.remote_addr
            
            # データの解析（アップロード速度のパラメータを'u'に修正）
            download_speed = float(data.get('d', 0))  # Mbps(DL)
            upload_speed = float(data.get('u', 0))    # Mbps(UL) - 'U'から'u'に変更
            rtt = float(data.get('p', 0))            # ms(RTT)
            jitter = float(data.get('j', 0))         # ms(jitter)
            
            print(f"受信データ: DL={download_speed}, UL={upload_speed}, RTT={rtt}, Jitter={jitter}")  # デバッグ用
            
            # データベースに保存
            with db_lock:
                with sqlite3.connect('network_data.db') as conn:
                    conn.execute('''
                        INSERT INTO measurements 
                        (timestamp, ip_address, download_speed, upload_speed, rtt, jitter)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (timestamp, ip_address, download_speed, upload_speed, rtt, jitter))
            
            return jsonify({
                "status": "success",
                "message": "データを保存しました"
            })
            
        except Exception as e:
            print(f"エラー発生: {str(e)}")  # デバッグ用
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400

@app.route('/', methods=['DELETE'])
def clear_database():
    try:
        with db_lock:
            with sqlite3.connect('network_data.db') as conn:
                conn.execute('DELETE FROM measurements')
        return jsonify({
            "status": "success",
            "message": "データベースをクリアしました"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
