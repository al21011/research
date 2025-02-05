import mariadb
import csv

### 計測データを取得
def fetch_eye_data():
    try:
        # アクセスするサーバおよびデータベース設定
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()

        # テーブルからデータ取得(最新100行を取得)
        insert_query = f'''
        SELECT * FROM data_table
        WHERE pupil IS NOT NULL AND position IS NOT NULL AND blink IS NOT NULL
        AND ((Time BETWEEN '2024-12-11 11:48:10' AND '2024-12-11 11:50:40')
        OR (Time BETWEEN '2024-12-11 11:53:38' AND '2024-12-11 11:55:48')
        OR (Time BETWEEN '2025-01-11 16:30:43' AND '2025-01-11 16:32:45')
        OR (Time BETWEEN '2025-01-11 16:37:09' AND '2025-01-11 16:39:27'))
        ORDER BY Time DESC
        '''
        # クエリ実行
        cur.execute(insert_query)
        
        # データの取得
        data = cur.fetchall()
        data.reverse()
               
        # コネクションの終了
        cur.close()
        con.close()
        
        return data
    
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

data = fetch_eye_data()
with open("csvFiles/data_value.csv", mode='w') as file:
    writer = csv.writer(file)
    writer.writerows(data)
print("書き込みが完了しました")
    
