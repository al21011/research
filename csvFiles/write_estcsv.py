import csv
import mariadb

def insert_csv_to_mariadb(csv_file):
    try:
        # MariaDBへの接続
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()

        # データ挿入用クエリ
        query = f"INSERT INTO est_table (Time, tension, concentration) VALUES (%s, %s, %s)"

        # CSVファイルを開いてデータを読み込む
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)

            # 各行をデータベースに挿入
            for row in reader:
                if len(row) == 3:  # 各行が3つの値を持っていることを確認
                    cur.execute(query, row)

        # コミットして変更を確定
        con.commit()
        print("データが正常に挿入されました！")

    except mariadb.Error as e:
        print(f"エラーが発生しました: {e}")

    finally:
        # 接続を閉じる
        if cur:
            cur.close()
        if con:
            con.close()

# 実行例
if __name__ == "__main__":
    csv_file = "csvFiles/estimation.csv"  # 対象のCSVファイルを指定
    insert_csv_to_mariadb(csv_file)
