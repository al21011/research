'''
データベース関連の関数をまとめてあるファイル
1.std_db    心電データ
2.bio-db    瞳関連データ
3.est_db    集中力・緊張感推定値
'''

import mariadb
import numpy as np
from datetime import datetime
import csv

# データベースに書き込む時刻などの変数(実験時に確認してから動作させること)
start_rri = '2024-12-02 10:31:00'   # 心電データを取得する開始時刻

### 瞳関連データを取得
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
        SELECT pupil, position, blink FROM data_table
        WHERE pupil IS NOT NULL AND position IS NOT NULL AND blink IS NOT NULL
        ORDER BY Time DESC LIMIT 30
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
        
### 心電データの最新100行を取得する
def fetch_rri() -> float:
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
        SELECT rri FROM data_table
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
 
### 心電データを書き込む
def write_rri(Time, rri_record):
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

        # テーブルにデータ挿入
        insert_query = '''
        INSERT INTO data_table
        (Time, rri) VALUES (%s, %s)
        '''
        # クエリ実行
        cur.execute(insert_query, (Time, rri_record))
            
        # コミットして行が更新されたか確認
        con.commit()
            
        # コネクションの終了
        cur.close()
        con.close()
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

### 緊張感推定値記録
def update_tension(Time, tension):
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

        # テーブルにデータ挿入
        insert_query = '''
        UPDATE data_table
        SET tension = %s
        WHERE Time = (SELECT MAX(Time) FROM data_table)
        '''
        # クエリ実行
        cur.execute(insert_query, (tension,))
            
        # コミットして行が更新されたか確認
        con.commit()
            
        # コネクションの終了
        cur.close()
        con.close()
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()  

def update_concentration(Time, concentration):
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

        # テーブルにデータ挿入
        insert_query = '''
        UPDATE data_table
        SET concentration = %s
        WHERE Time = (SELECT MAX(Time) FROM data_table)
        '''
        # クエリ実行
        cur.execute(insert_query, (concentration,))
            
        # コミットして行が更新されたか確認
        con.commit()
            
        # コネクションの終了
        cur.close()
        con.close()
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

### 推定値記録
def write_estimation(Time, tension, concentration):
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
        INSERT INTO est_table (Time, tension, concentration)
        VALUES (%s, %s, %s)
        '''
        # クエリ実行
        cur.execute(insert_query, (Time, tension, concentration))
        
        # コネクションの終了
        con.commit()
        con.close()
        print(f'{Time}')
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

### csvファイルに推定値を書き込む
def csv_estimation(Time, tension, concentration):
    with open("csvFiles/est_value.csv", mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([Time, tension, concentration])

import statistics
import numpy as np
from sklearn.decomposition import PCA

### リストの最頻値あるいは中央値を返す
def mode_or_median(eye_list) -> int:
    try:
        ans = statistics.mode(eye_list)
    except statistics.StatisticsError:
        ans = int(np.median(eye_list))
    return ans

### L/Tの計算
def calculate_axes(returns):
    # PCAを使用して主成分を計算
    pca = PCA(n_components=2)
    # データを整形
    data = np.column_stack((returns[:-1], returns[1:]))
    pca.fit(data)

    # 主成分ベクトル
    components = pca.components_
    # 分散
    explained_variance = pca.explained_variance_

    # 長軸と短軸の長さを取得
    L = 2 * np.sqrt(explained_variance[0])  # 長軸
    T = 2 * np.sqrt(explained_variance[1])  # 短軸
    
    return L/T
