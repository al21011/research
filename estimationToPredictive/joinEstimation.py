'''
瞳情報と心電データを時刻で同期して書き込む
'''
import eyeEstimation as eyeEst
import rriEstimation as rriEst
import keyboard
import time
import mariadb
import asyncio

def main():
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


### コピペ
import multiprocessing
import subprocess

def run_script(script):
    # スクリプトを実行
    subprocess.run(['python', script])

scripts = ['script1.py', 'script2.py', 'script3.py']
processes = []

# 各スクリプトをプロセスで実行
for script in scripts:
    process = multiprocessing.Process(target=run_script, args=(script,))
    processes.append(process)
    process.start()

# 全てのプロセスが終了するのを待つ
for process in processes:
    process.join()

print("全てのスクリプトが終了しました。")

