'''
瞳関連データから推定値を算出する
30秒間落ち着いた状態で真っ直ぐ前を向いてもらいDBに書き込みを行う。
準備用の関数を実行して基準値を設定する
0.00-2.00の間で算出し、エラーは3.00とする
'''

import databaseFunc as db
import statistics
import numpy as np

# 推定値算出時の基準値から外れた値の影響度
est_w = 0.5

# 準備用の関数により得られた値を記入
pupil_m = 16
position_m = 16
blink_m = 25

def mode_or_median(eye_list) -> int:
    try:
        ans = statistics.mode(eye_list)
    except statistics.StatisticsError:
        ans = int(np.median(eye_list))
    return ans

# 準備段階で被験者の基準値を計測する
def ref_value():
    data = db.fetch_eye_data()
    if not data:
        pupil_med, position_cnt, blink_cnt = 0, 0, 0
    else:
        # 各カラムについてリストに格納
        pupil_list = [row[0] for row in data]
        position_list = [row[1] for row in data]
        blink_list = [row[2] for row in data]
        
        pupil_med = mode_or_median(pupil_list)
        # 脇見回数を記録
        position_cnt = sum(1 for x in position_list if x != 1)
        # 瞬き回数を記録
        blink_cnt = blink_list.count(1)
        
    return pupil_med, position_cnt, blink_cnt

# 準備段階で使用
print(ref_value())
