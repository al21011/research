import serial
import time

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
                print('{:.5f}'.format(RRI), end=' , ')
                
                HR = 60/RRI  #瞬間心拍数を算出
                print('{:.5f}'.format(HR))
            
            # 時刻を更新
            prev_RRI_time = current_time
            last_cross_time = current_time

ser = serial.Serial('/dev/cu.usbmodem1101', 9600) # ここのポート番号を変更
ser.readline()
while True:
  val_arduino = ser.readline()
  val_decoded = int(repr(val_arduino.decode())[1:-5])
  Calc_RRI(val_decoded)
  
ser.close()