import pandas as pd

def filter_rows_by_time(csv_file, start_time, end_time):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file, header=None, names=["datetime", "value1", "value2"])

    # datetime列を日時型に変換
    df["datetime"] = pd.to_datetime(df["datetime"])

    # 指定した時間範囲でフィルタリング
    filtered_df = df[(df["datetime"] >= start_time) & (df["datetime"] <= end_time)]

    # フィルタリング結果をプリント
    print(filtered_df)

# 入力CSVファイルのパス
csv_file = "csvFiles/est_value.csv"

# 時間範囲を指定
start_time = "2025-01-11 10:52:52"
end_time = "2025-01-11 10:55:59"

filter_rows_by_time(csv_file, start_time, end_time)
