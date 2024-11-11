'''
瞳関連データから推定値を算出する
30秒間落ち着いた状態で真っ直ぐ前を向いてもらいDBに書き込みを行う。
準備用の関数を実行して基準値を設定する
0.00-2.00の間で算出し、エラーは3.00とする
'''

import culFunc
import databaseFunc as db
import time
import statistics

# 推定値算出時の基準値から外れた値の影響度
est_w = 0.3

# 準備用の関数により得られた値を記入
pupil_m = 20
position_m = 14
blink_m = 20

### 集中力推定値を書き込む
def write_estimation() -> float:
    # 各項目の重みを設定
    pupil_w = 0.30
    position_w = 0.20
    blink_w = 0.10
    
    data = db.fetch_eye_table()
    if not data:
        return 3.00
    else:
        # 各カラムについてリストに格納
        Time_list = [row[0] for row in data]
        pupil_list = [row[1] for row in data]
        position_list = [row[2] for row in data]
        blink_list = [row[3] for row in data]
        
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
        
        print(statistics.median(pupil_list), position_cnt, blink_cnt)
        
        # 算出値をデータベースに書き込む
        db.update_eye_table(Time_list[0], concentration)

# 準備段階で被験者の基準値を計測する
def ref_value():
    data = db.fetch_eye_table()
    if not data:
        pupil_med, position_cnt, blink_cnt = 0, 0, 0
    else:
        # 各カラムについてリストに格納
        pupil_list = [row[0] for row in data]
        position_list = [row[1] for row in data]
        blink_list = [row[2] for row in data]
        
        pupil_med = culFunc.mode_or_median(pupil_list)
        # 脇見回数を記録
        position_cnt = sum(1 for x in position_list if x != 1)
        # 瞬き回数を記録
        blink_cnt = blink_list.count(1)
        
    return pupil_med, position_cnt, blink_cnt


'''
# デバッグ
while True:
    # 推定値の確認
    # print(write_estimation())
    time.sleep(1)

    # escキーで終了
    if keyboard.is_pressed('esc'):
        print('Loop terminated by user')
        break
'''

# 準備段階で使用
# print(ref_value())

# 推定値の書き込みを実行
# 毎秒処理を行う
last_time = time.time()
while True:
    current_time = time.time()
    if current_time - last_time >= 1:
        write_estimation()
        last_time = current_time
