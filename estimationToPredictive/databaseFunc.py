'''
データベース関連の関数をまとめてあるファイル
1.std_db    心電データ
2.bio-db    瞳関連データ
3.est_db    集中力・緊張感推定値
'''

import mariadb
import statistics
import numpy as np

# データベースに書き込む時刻などの変数(実験時に確認してから動作させること)
start_rri = '2024-10-31 03:16:30'   # 心電データを取得する開始時刻

start_eye = '2024-10-31 03:16:30'   # 瞳関連データを取得する開始時刻
limit_eye = 30                      # 瞳関連データを取得する行数(準備段階)
# limit_bio = 5                       # 瞳関連データを取得する行数(実験時)

### rri_tableに書き込みを行う
def write_rri_table(Time, rri):
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()

        # テーブルにデータ挿入
        insert_query = '''
        INSERT INTO rri_table (Time, rri, tension)
        VALUES (%s, %s, %s)
        '''
        # クエリ実行
        cur.execute(insert_query, (Time, rri, None))
            
        # コミットして行が更新されたか確認
        con.commit()
            
        # コネクションの終了
        con.close()
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

### rri_tableの最新100行を取得する
def fetch_rri_table() -> float:
    try:
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
        SELECT RRI FROM rri_table
        WHERE Time >= '{start_rri}'
        ORDER BY Time DESC LIMIT 100
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

### eye_tableから読み取る
def fetch_eye_table() -> int:
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()
        
        # テーブルからデータ取得(実験前に行う計測の開始時刻を記入)
        insert_query = f'''
        SELECT pupil, position, blink FROM eye_table
        WHERE Time >= '{start_eye}'
        ORDER BY Time ASC LIMIT {limit_eye}
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
        
### eye_tableとrri_tableの結合を行う
def join_est_table():
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()

        # テーブルにデータ挿入
        insert_query = '''
        INSERT INTO est_table (Time, concentration, tenstion)
        SELECT e.Time, e.concentration, r.tension
        FROM eye_table e
        JOIN rri_table r ON e.Time = r.Time
        WHERE e.concentration IS NOT NULL;
        '''
        # クエリ実行
        cur.execute(insert_query)
            
        # コミットして行が更新されたか確認
        con.commit()
            
        # コネクションの終了
        cur.close()
        con.close()
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

### est_tableから5行読み取りを行う
def fetch_est_table() -> float:
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()
        
        # テーブルからデータ取得(最新100行を取得)
        insert_query = '''
        SELECT * FROM est_table
        ORDER BY Time DESC LIMIT 5
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
