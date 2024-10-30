'''
RRIをDBに書き込む処理
'''

import serial
import mariadb
import time

Threshold = 600   #心電の閾値(Arduinoのシリアルプロッタから確認すると吉)
Timeout = 0.3   #1度目のピークから次のピークまでのタイムアウト

last_cross_time = None  # 前回閾値を超えた時刻
prev_RRI_time = None  # 前回のRRI計測時刻

### RRIを計算する(未取得：0)
def Calc_RRI(val_decoded):
    global last_cross_time, prev_RRI_time
    current_time = time.time()  # 現在の時間を取得
    
    if val_decoded > Threshold:# 閾値を超えたか
        if last_cross_time is None or (current_time - last_cross_time > Timeout):# 次のピークまでの時間
            if prev_RRI_time is not None:
                
                RRI = current_time - prev_RRI_time  # RRIを算出
                print('{:.5f}'.format(RRI), end=' , ')
                
                ## HR = 60/RRI  #瞬間心拍数を算出
                ## print('{:.5f}'.format(HR))
                
                return RRI
            
            # 時刻を更新
            prev_RRI_time = current_time
            last_cross_time = current_time
            
    return 0

### RRIをDBの時間が一致するカラムに書き込む
def writeRRI(time, RRI):
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='bio-db'
        )
        cur = con.cursor()

        # クエリ実行
        cur.execute('UPDATE bio_table SET RRI = ? WHERE time = ?', (time, RRI))
        if cur.rowcount > 0:
            print(f'{time}に{RRI}を挿入')
        else:
            time.sleep(0.5)
            cur.execute('UPDATE bio_table SSET RRI = ? WHERE time = ?', (time, RRI))
            
        # コネクションの終了
        con.commit()
        con.close()
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

ser = serial.Serial('/dev/cu.usbmodem1101', 9600) # ここのポート番号を変更
ser.readline()
while True:
  val_arduino = ser.readline()
  val_decoded = int(repr(val_arduino.decode())[1:-5])
  writeRRI(time.strftime('%Y-%m-%d %H:%M:%S'), Calc_RRI(val_decoded))
  
ser.close()