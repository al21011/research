'''
ポアンカレプロットによる緊張感推定
準備: std_dbから最新100行を取得してポアンカレプロットによる数値を算出して変数に格納する
'''
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import mariadb
from sklearn.decomposition import PCA

poincare_value = 2.3438        # 準備段階で算出した値

Threshold = 600   #心電の閾値(Arduinoのシリアルプロッタから確認すると吉)
Timeout = 0.3   #1度目のピークから次のピークまでのタイムアウト

last_cross_time = None  # 前回閾値を超えた時刻
prev_RRI_time = None  # 前回のRRI計測時刻

rri_record = 0.0

### RRIを計算する(未取得：0)
def Calc_RRI(val_decoded):
    global last_cross_time, prev_RRI_time
    global rri_record
    current_time = time.time()  # 現在の時間を取得
    
    if val_decoded > Threshold:# 閾値を超えたか
        if last_cross_time is None or (current_time - last_cross_time > Timeout):# 次のピークまでの時間
            if prev_RRI_time is not None:
                
                RRI = current_time - prev_RRI_time  # RRIを算出
                # print('{:.5f}'.format(RRI), end=' , ')
                rri_record = round(RRI, 4)
                
                HR = 60/RRI  #瞬間心拍数を算出
                # print('{:.5f}'.format(HR))
            
            # 時刻を更新
            prev_RRI_time = current_time
            last_cross_time = current_time

### RRIを時間と共にDBのカラムへ書き込む
def writeRRI(Time, RRI):
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='std_db'
        )
        cur = con.cursor()

        # テーブルにデータ挿入
        insert_query = '''
        INSERT INTO std_table (Time, RRI)
        VALUES (%s, %s)
        '''
        # クエリ実行
        cur.execute(insert_query, (Time, RRI))
            
        # コミットして行が更新されたか確認
        con.commit()
            
        # コネクションの終了
        con.close()
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

### RRIを最新100行取得する
def rri_fetch():
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='std_db'
        )
        cur = con.cursor()
        
        # テーブルからデータ取得(最新100行を取得)
        insert_query = '''
        SELECT RRI FROM std_table
        WHERE Time >= '2024-10-31 03:16:30'
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

ser = serial.Serial('/dev/cu.usbmodem1101', 9600) # ここのポート番号を変更
ser.readline()

# 毎秒処理を行う
last_time = time.time()
while True:
    # RRIを計算する
    val_arduino = ser.readline()
    val_decoded = int(repr(val_arduino.decode())[1:-5])
    Calc_RRI(val_decoded)
    
    if rri_record > 0.0:
        # RRIを毎秒書き込む
        current_time = time.time()
        if current_time - last_time >= 1:
            writeRRI(time.strftime('%Y-%m-%d %H:%M:%S'), rri_record)
            last_time = current_time
            # L/Tを再計算
            L_T = (calculate_axes(rri_fetch()))
            print(L_T)
            # 推定値算出
            print((L_T - 1) * 2 / 3)
    
ser.close()
