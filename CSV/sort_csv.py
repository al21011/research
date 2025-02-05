import sys
import csv
import datetime

filename = 'est.csv'
with open(filename, encoding='utf8', newline='') as f:
    reader = csv.reader(f)
    l = [row for row in reader]

    # リストlの１行目から最終行までを対象とし（スライス）、得点順にソートした新たなリストsortを生成
    sort = sorted(l[1:], reverse=True, key=lambda x:datetime(x[0]))

    # 出力 
    writer = csv.writer(sys.stdout)  # CSVファイルの内容を標準出力に出力
    writer.writerow(l[0])
    writer.writerows(sort)
    