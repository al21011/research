'''
### 瞳の生体情報を用いた集中力の推定機能の実装
    1.30秒間落ち着いた状態で真っ直ぐ前を向いてもらいDBに書き込みを行う。
    2.準備用の関数を実行して基準値を設定する
    DBにはtime, heartRate, pupil, position, blinkの順でカラムが用意されている
    0.00-2.00の間で算出し、エラーは3.00とする
'''

import mariadb
import numpy as np
import statistics
import time
import keyboard
import random

# 準備用の関数により得られた値を記入
pupil_m = 20
position_m = 24
blink_m = 2

### リストの最頻値あるいは中央値を返す
def mode_or_median(eye_list) -> int:
    try:
        ans = statistics.mode(eye_list)
    except statistics.StatisticsError:
        ans = int(np.median(eye_list))
    return ans

### 運転開始前の準備
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

### 2つの値の差を返す
def cul_dif(cnt, m) -> int:
    return int(m/3) - cnt

### 運転開始後
def cul_estimation() -> int:
    # 各項目の重みを設定(計1になるように)
    pupil_w = 0.5
    position_w = 0.2
    blink_w = 0.3
    
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='bio-db'
        )
        cur = con.cursor()
        
        # テーブルからデータ取得(実験の開始時刻を記入)
        insert_query = '''
        SELECT pupil, position, blink FROM bio_table
        WHERE time >= '2024-10-24 03:40:20'
        ORDER BY time DESC LIMIT 10
        '''
        # クエリ実行
        cur.execute(insert_query)
        
        # データの取得(新しい順に格納されることに注意)
        data = cur.fetchall()
        
        # コネクションの終了
        cur.close()
        con.close()
        
        if not data:
            return 3.00
        else:
            # 各カラムについてリストに格納
            pupil_list = [row[0] for row in data]
            position_list = [row[1] for row in data]
            blink_list = [row[2] for row in data]
            
            # 非集中時、過集中時の秒数を記録
            decentralized = sum(1 for x in pupil_list if x < (pupil_m-2))
            hyperfocus = sum(1 for x in pupil_list if x > (pupil_m+2))
            if decentralized > hyperfocus:
                pupil_cnt = decentralized
            elif decentralized < hyperfocus:
                pupil_cnt = hyperfocus
            else:
                pupil_cnt = int(pupil_m / 3)
            # 脇見回数を記録
            position_cnt = sum(1 for x in position_list if x != 1)
            # 瞬き回数を記録
            blink_cnt = blink_list.count(1)
            
            # 基準値との差を算出する
            pupil_dif = cul_dif(pupil_cnt, pupil_m) * (-1)
            position_dif = cul_dif(position_cnt, position_m)
            blink_dif = cul_dif(blink_cnt, blink_m)
            
            # 重みを考慮して集中具合を算出(0:非集中　1:適切　2:過集中)
            concentrate_value = 1.00 + ((pupil_dif * pupil_w) + (position_dif * position_w) + (blink_dif * blink_w)) * 3 / 10
            if concentrate_value < 0.00:
                concentrate_value = 0.00
            elif concentrate_value > 2.00:
                concentrate_value = 2.00
            
            return round(concentrate_value, 2)
    
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

# ランダムな値を返す(予測機能実装用の関数)
def random_value(min_value, max_value):
    return random.uniform(min_value, max_value)

# 準備段階で使用する
# print(mariadb_fetch())

# 運転開始後に実行する
while True:
    print(cul_estimation())
    time.sleep(1)

    # escキーで終了
    if keyboard.is_pressed('esc'):
        print('Loop terminated by user')
        break
