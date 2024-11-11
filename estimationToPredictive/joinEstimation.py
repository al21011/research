'''
集中力・緊張感を時刻で同期して結合する
'''
import eyeEstimation as eyeEst
import time

# 毎秒処理
last_time = time.time()
while True:
    current_time = time.time()
    if current_time - last_time >= 1:
        # 集中力推定値の書き込みと推定値の結合
        eyeEst.write_estimation()
        last_time = current_time
