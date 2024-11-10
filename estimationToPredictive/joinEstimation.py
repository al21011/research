'''
瞳情報と心電データを時刻で同期して書き込む
'''
import estimationToPredictive.eyeEstimation as eyeEst
import estimationToPredictive.rriEstimation as rriEst
import keyboard
import time
import mariadb
import asyncio

### サーバに書き込みを行う
def est_write(eye, rri):
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()
        
        # テーブルにデータ挿入
        insert_query = '''
        INSERT INTO bio_table (Time, eye, rri)
        VALUES (%s, %s, %s)
        '''
        # クエリ実行
        cur.execute(insert_query, (time, pupil, position, blink))
        
        # コネクションの終了
        con.commit()
        con.close()
        print(f'{time}')
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

# 瞳情報を計測して書き込む
async def eye_task():
    print("Task 1 started")
    await asyncio.sleep(2)  # 2秒待機（非同期）
    print("Task 1 finished")
    
    while True:
        print(eyeEst.cul_estimation())
        time.sleep(1)

        # escキーで終了
        if keyboard.is_pressed('esc'):
            print('Loop terminated by user')
            break
    return "Result of Task 1"

# 心電データを計測して書き込む
async def rri_task():
    print("Task 2 started")
    await asyncio.sleep(1)  # 1秒待機（非同期）
    print("Task 2 finished")
    return "Result of Task 2"

async def main():
    # 1秒ごとにeye, rriを実行して書き込みを行う
    
    while True:
        # タスクを同時に実行
        results = await asyncio.gather(eye_task(), rri_task())
        print("All tasks completed")
        print(results)
        
            # escキーで終了
        if keyboard.is_pressed('esc'):
            print('Loop terminated by user')
            break

# 非同期関数を実行
asyncio.run(main())
