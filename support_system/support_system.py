import time
import mariadb
from playsound import playsound
from typing import Tuple

def fetch_est_latest_data() -> Tuple[str, str]:
    try:
        # アクセスするサーバおよびデータベース設定
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()

        # 特定の時刻のデータを取得(デバッグ用)
        query = '''
        SELECT tension, concentration
        FROM est_table
        ORDER BY Time DESC LIMIT 1
        '''
        
        # クエリ実行
        cur.execute(query)
        
        # データの取得
        result = cur.fetchone()
        
        # コネクションの終了
        cur.close()
        con.close()

        if result:
            tensionType, concentrationType = result  # データをそれぞれの変数に格納
            return tensionType, concentrationType
        else:
            raise ValueError("No data found for the given timestamp.")

    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# 音声の再生
def play_audio(file_name):
    print(f"Playing {file_name}")
    playsound(file_name)

while True:
    # 最新データの取得
    try:
        tensionType, concentrationType = fetch_est_latest_data()
        concentrationType = concentrationType.lower()
        tensionType = tensionType.lower()
    except ValueError as e:
        print(e)
        continue
    except Exception as e:
        print(f"Unexpected error: {e}")
        continue

    # Truffic situation(今回は1と2の2パターンの用意)
    try:
        Tsituation = int(input("Enter Tsituation (1 or 2): "))
        if Tsituation not in [1, 2]:
            print("Please enter 1 or 2.")
            continue
    except ValueError:
        print("Please enter 1 or 2.")
        continue

    # 心的状態(Mtype)の場合分け
    if tensionType == "low" or (tensionType == "appropriate" and concentrationType == "low"):
        Mtype = 1
    elif tensionType == "high":
        Mtype = 2
    elif tensionType == "appropriate" and concentrationType == "appropriate":
        Mtype = 3
    elif tensionType == "appropriate" and concentrationType == "high":
        Mtype = 4
    else:
        print("Invalid tensionType or concentrationType values. Try again.")
        continue

    # 心的状態による音声の再生
    if Tsituation == 1:
        if Mtype == 1:
            print("非緊張非集中型")
            play_audio("guide1.mp3")
        elif Mtype == 2:
            print("過緊張型")
            play_audio("guide2.mp3")
        elif Mtype == 3:
            print("適切型")
            play_audio("guide3.mp3")
        elif Mtype == 4:
            print("過集中型")
            play_audio("guide4.mp3")
    elif Tsituation == 2:
        if Mtype == 1:
            print("非緊張非集中型")
            play_audio("guide5.mp3")
        elif Mtype == 2:
            print("過緊張型")
            play_audio("guide6.mp3")
        elif Mtype == 3:
            print("適切型")
            play_audio("guide7.mp3")
        elif Mtype == 4:
            print("過集中型")
            play_audio("guide8.mp3")

    time.sleep(1)
    