'''
ポアンカレプロットによる緊張感推定
準備: std_dbから最新100行を取得してポアンカレプロットによる数値を算出して変数に格納する
'''
import culFunc
import databaseFunc as db
import serial
import time
import numpy as np

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
            db.write_rri_table(time.strftime('%Y-%m-%d %H:%M:%S'), rri_record)
            last_time = current_time
            
            if len(db.fetch_rri_table()) < 100:
                tension = None
            else:
                # L/Tを再計算 
                L_T = (culFunc.calculate_axes(db.fetch_rri_table()))
                print(L_T)
                # 推定値算出
                tension = (L_T - 1) * 2.0 / 3.0
                if tension < 0.0:
                    tension = 0.0
                elif 2.0 < tension:
                    tension = 2.0
                print(tension)
            db.update_rri_table(time.strftime('%Y-%m-%d %H:%M:%S'), tension)

ser.close()
