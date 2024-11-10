'''
瞳関連データから推定値を算出して書き込む
30秒間落ち着いた状態で真っ直ぐ前を向いてもらいDBに書き込みを行う。
準備用の関数を実行して基準値を設定する
0.00-2.00の間で算出し、エラーは3.00とする
'''

import culFunc
import databaseFunc as db

# 推定値算出時の基準値から外れた値の影響度
est_w = 0.3

# 準備用の関数により得られた値を記入
pupil_m = 20
position_m = 24
blink_m = 2

### 集中力推定値算出
def cul_estimation() -> float:
    # 各項目の重みを設定(計1になるように)
    pupil_w = 0.5
    position_w = 0.2
    blink_w = 0.3
    
    data = db.fetch_bio_db()
    if not data:
        return 3.00
    else:
        # 各カラムについてリストに格納
        pupil_list = [row[0] for row in data]
        position_list = [row[1] for row in data]
        blink_list = [row[2] for row in data]
        
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
        concentrate_value = 1.00 + ((pupil_cnt * pupil_w) + (position_dif * position_w) + (blink_dif * blink_w)) * est_w
        if concentrate_value < 0.00:
            concentrate_value = 0.00
        elif concentrate_value > 2.00:
            concentrate_value = 2.00
        
        return round(concentrate_value, 2)

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
    # print(cul_estimation())
    time.sleep(1)

    # escキーで終了
    if keyboard.is_pressed('esc'):
        print('Loop terminated by user')
        break
'''

# 準備段階で使用
print(ref_value())
