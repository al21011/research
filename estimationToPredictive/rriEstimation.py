'''
### 心電センサを用いた集中力の推定機能の実装
    1.
    2.準備用の関数を実行して基準値を
    DBにはtime, heartRate, RRI, position, blinkの順でカラムが用意されている
    0.00-2.00の間で算出し、エラーは3.00とする
'''
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import mariadb

Threshold = 600   #心電の閾値(Arduinoのシリアルプロッタから確認すると吉)
Timeout = 0.3   #1度目のピークから次のピークまでのタイムアウト

last_cross_time = None  # 前回閾値を超えた時刻
prev_RRI_time = None  # 前回のRRI計測時刻

def Calc_RRI(val_decoded):
    global last_cross_time, prev_RRI_time
    current_time = time.time()  # 現在の時間を取得
    
    if val_decoded > Threshold:# 閾値を超えたか
        if last_cross_time is None or (current_time - last_cross_time > Timeout):# 次のピークまでの時間
            if prev_RRI_time is not None:
                
                RRI = current_time - prev_RRI_time  # RRIを算出
                
                HR = 60/RRI  #瞬間心拍数を算出
                
                return RRI, HR
            
            # 時刻を更新
            prev_RRI_time = current_time
            last_cross_time = current_time
    return 0, 0

### データベースへの時間による同期及び書き込み
def mariadb_fetch() -> int:
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='bio-db'
        )
        cur = con.cursor()
        
        # テーブルからデータ取得(実験前に行う計測の開始時刻を記入)
        insert_query = '''
        SELECT pupil, position, blink FROM bio_table
        WHERE time >= '2024-10-24 03:34:05'
        ORDER BY time ASC LIMIT 30
        '''
        # クエリ実行
        cur.execute(insert_query)
        
        # データの取得
        data = cur.fetchall()
        
        # コネクションの終了
        cur.close()
        con.close()
        
        # 各カラムについてリストに格納
        pupil_list = [row[0] for row in data]
        position_list = [row[1] for row in data]
        blink_list = [row[2] for row in data]
        
        return mode_or_median(pupil_list), position_list.count(1), blink_list.count(1)
        
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

### RRIデータからポアンカレプロットを描画する関数
def plot_poincare(rri):
    # RRIデータから次のRRI間隔とその前のRR間隔を取得
    rri_n = rri[:-1]
    rri_n1 = rri[1:]
    
    # プロットの作成
    plt.figure(figsize=(6, 6))
    plt.scatter(rri_n, rri_n1, color='blue', alpha=0.5, edgecolor='k', s=20)
    
    # 軸の設定
    plt.xlabel("RRI(n) [ms]")
    plt.ylabel("RRI(n+1) [ms]")
    plt.title("Poincare Plot")
    plt.axline((0, 0), slope=1, color="red", linestyle="--")
    
    # 軸の範囲をRRIの範囲に合わせる
    min_rri = min(min(rri_n), min(rri_n1))
    max_rri = max(max(rri_n), max(rri_n1))
    plt.xlim(min_rri - 50, max_rri + 50)
    plt.ylim(min_rri - 50, max_rri + 50)
    
    plt.grid(True)
    plt.show()
    
    return np.array(rri_n), np.array(rri_n1)
    
### 最大距離の算出
def max_distances(rri_n, rri_n1):
    # 各点の並行成分と垂直成分を計算
    parallel_components = (rri_n + rri_n1) / np.sqrt(2)
    perpendicular_components = (rri_n1 - rri_n) / np.sqrt(2)
    
    # 並行成分の最大距離
    L = np.max(parallel_components) - np.min(parallel_components)
    
    # 垂直成分の最大距離
    T = np.max(perpendicular_components) - np.min(perpendicular_components)
    
    return L, T

ser = serial.Serial('/dev/cu.usbmodem1101', 9600) # ここのポート番号を変更
ser.readline()
while True:
  val_arduino = ser.readline()
  val_decoded = int(repr(val_arduino.decode())[1:-5])
  RRI, HR = Calc_RRI(val_decoded)
  
# RRIの例データ（単位はms）
rri_data = [800, 810, 790, 830, 820, 850, 800, 790, 770, 760, 780]
rri_n, rri_n1 = plot_poincare(rri_data)
L, T = max_distances(rri_n, rri_n1)

ser.close()   