from flask import Flask, request, jsonify

app = Flask(__name__)
# データを保存するためのリスト
data_store = []

# POSTリクエストを受け取ってデータを保存するエンドポイント
@app.route('/write', methods=['POST'])
def write_data():
    data = request.json
    data_store.append(data)
    return jsonify({"message": "Data written Successfully", "data": data}), 200

# 保存されたデータを確認するエンドポイント
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_store), 200

if __name__ == '__main__':
    app.run(debug=True)
