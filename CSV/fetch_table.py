import mariadb
import csv

def fetch_rri_table() -> float:
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

        # テーブルからデータ取得
        insert_query = f'''
        SELECT e.Time, e.pupil, e.position, e.blink, r.rri FROM eye_table e LEFT JOIN rri_table r ON e.Time = r.Time
        WHERE e.Time >= '2024-12-11 00:00:00';
        '''
        # クエリ実行
        cur.execute(insert_query)
        
        # データの取得
        data = cur.fetchall()
               
        # コネクションの終了
        cur.close()
        con.close()
        
        return data
    
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

csv_file = 'est.csv'
# 書き込む処理
with open(csv_file, mode='w') as file:
    writer = csv.writer(file)
    writer.writerows(fetch_rri_table())
    