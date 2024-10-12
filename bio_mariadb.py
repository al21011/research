'''
さくらサーバ内でPOSTを行うためのコードです。
さくらサーバselabディレクトリのbio_mariadb.pyコードにコピペするものです。
'''

from flask import Flask, request, jsonify
import MySQLdb
from datetime import datetime

app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    heartRate = data.get('heartRate')
    time = data.get('time')
    print(time, heartRate)
    # SwiftUIのDate型からPythonのdatetime型への変換
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')

    # データベースに接続してデータを挿入
    con = MySQLdb.connect(
        host='localhost',
        user='root',
        password='selab',
        database='bio-db'
    )
    cur = con.cursor()
    
    # SQLクエリと実行
    query = '''
    UPDATE bio_table
    SET heartRate = %s
    WHERE time = %s
    '''
    cur.execute(query, (heartRate, time))
    # コミット
    con.commit()
    # 終了処理
    cur.close()
    con.close()
    
    return jsonify({'message': 'User added successfully'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# swiftuiからpythonにてdatetimeへ変換する
# swift_time = datetime.strptime(swift_time_string, '%Y-%m-%dT%H:%M:%S')
