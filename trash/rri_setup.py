'''
検証を行う前の準備段階でRRIをDBに書き込む処理
100行以上書き込むまで行う
'''

import serial
import mariadb
import time

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
                print('{:.5f}'.format(RRI), end=' , ')
                rri_record = round(RRI, 4)
                
                HR = 60/RRI  #瞬間心拍数を算出
                print('{:.5f}'.format(HR))
            
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

ser = serial.Serial('/dev/cu.usbmodem1101', 9600) # ここのポート番号を変更
ser.readline()

# 毎秒RRIを取得してDBに書き込む
last_time = time.time()
cnt = 0
while True:
    val_arduino = ser.readline()
    val_decoded = int(repr(val_arduino.decode())[1:-5])
    Calc_RRI(val_decoded)

    current_time = time.time()
    if current_time - last_time >= 1:
        writeRRI(time.strftime('%Y-%m-%d %H:%M:%S'), rri_record)
        cnt += 1
        last_time = current_time
    
    # 100行で処理を終了させる
    if cnt >= 110:
        print('100行以上書き込み終了')
        break
  
ser.close()
