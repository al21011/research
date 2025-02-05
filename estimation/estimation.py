### 心電センサ及び赤外線カメラを同時に実行して推定値をデータベースに書き込む
import databaseFunc as db
import serial
import time
import numpy as np
import statistics
import cv2
from datetime import datetime

# 推定値算出時の基準値から外れた値の影響度
est_w = 0.1
pupil_m = 20
position_m = 15
blink_m = 9

# 閾値の設定
tension_low = 0.4
tension_high = 0.80
concentration_low = 0.5
concentration_high = 1.40

### 集中力推定値を返す
def concentration_value() -> float:
    # 各項目の重みを設定
    pupil_w = 0.30
    position_w = 0.10
    blink_w = 0.10
    
    data = db.fetch_eye_data()
    if not data:
        return 1.00
    else:
        # 各カラムについてリストに格納
        pupil_list = [row[0] for row in data if row[0] is not None]
        position_list = [row[1] for row in data if row[1] is not None]
        blink_list = [row[2] for row in data if row[2] is not None]
        
        # 非集中時、過集中時の秒数を記録
        decentralized = sum(1 for x in pupil_list if x < pupil_m)
        hyperfocus = sum(1 for x in pupil_list if x > pupil_m)
        pupil_cnt = 0
        if decentralized >= hyperfocus:
            pupil_cnt = decentralized * -1
        else:
            pupil_cnt = hyperfocus
        # 脇見回数を記録
        position_cnt = sum(1 for x in position_list if x != 1)
        # 瞬き回数を記録
        blink_cnt = blink_list.count(1)
        
        # 基準値との差を算出する
        position_dif = position_m - position_cnt
        blink_dif = blink_m - blink_cnt
        
        # 重みを考慮して集中具合を算出(0:非集中　1:適切　2:過集中)
        concentration = 1.00 + ((pupil_cnt * pupil_w) + (position_dif * position_w) + (blink_dif * blink_w)) * est_w
        if concentration < 0.00:
            concentration = 0.00
        elif concentration > 2.00:
            concentration = 2.00
        
        # print(statistics.median(pupil_list), position_cnt, blink_cnt)
        
        # 算出値をデータベースに書き込む
        return concentration

### 緊張感推定値を返す
def tension_value() -> float:
    # L/Tを計算
    L_T = (db.calculate_axes(db.fetch_rri()))
    # print(L_T)
    # 推定値算出
    tension = (L_T - 1) * 2.0 / 3.0
    if tension < 0.0:
        tension = 0.0
    elif 2.0 < tension:
        tension = 2.0
    return tension  

# 毎秒処理を行う
last_time = time.time()
while True:
    current_time = time.time()
    if current_time - last_time >= 1:
        last_time = current_time
        # 記録する時間
        Time = time.strftime('%Y-%m-%d %H:%M:%S')
        # 緊張感及び集中力推定値の算出
        tension = tension_value()
        concentration = concentration_value()
        # 推定値をcsvファイルに書き込み
        db.csv_estimation(Time, tension, concentration)
        print(Time)
        # 緊張感推定結果
        tension_state = 'appropriate'
        if tension < tension_low:
            tension_state = 'low'
        if tension > tension_high:
            tension_state = 'high'
        # 集中力推定結果
        concentration_state = 'appropriate'
        if concentration < concentration_low:
            concentration_state = 'low'
        if concentration > concentration_high:
            concentration_state = 'high'
        # 推定結果記録
        db.write_estimation(Time, tension_state, concentration_state)
        
