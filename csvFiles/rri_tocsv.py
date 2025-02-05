import mariadb
import csv
import statistics
import numpy as np
from sklearn.decomposition import PCA
from datetime import datetime

### 計測データを取得
def fetch_rri_data():
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
        SELECT Time, rri FROM data_table
        WHERE pupil IS NOT NULL AND position IS NOT NULL AND blink IS NOT NULL
        AND ((Time BETWEEN '2025-01-11 16:17:32' AND '2025-01-11 16:20:07')
        OR (Time BETWEEN '2025-01-11 16:22:11' AND '2025-01-11 16:29:02')
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

### 緊張感推定値を返す
def tension_value(current_rri) -> float:
    # L/Tを計算
    L_T = (calculate_axes(current_rri))
    # print(L_T)
    # 推定値算出
    tension = (L_T - 1) * 2.0 / 3.0
    if tension < 0.0:
        tension = 0.0
    elif 2.0 < tension:
        tension = 2.0
    return tension  

def write_to_csv(data):
    with open("csvFiles/rri_value.csv", mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "L_T"])
        
    for i in range(100, len(data)+1):
        current_rri = [item[1] for item in data[:i]]
        L_T = tension_value(current_rri)
        
        latest_time = data[i-1][0]
        with open("csvFiles/rri_value.csv", mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([latest_time, L_T])

data = fetch_rri_data()
write_to_csv(data)
print("書き込みが完了しました")

    
