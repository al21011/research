'''
ヘルスケアから書き出したxmlファイルが重いので心拍数のみのファイルに書き換えるソースコードです
python extractionXml.py ****.xml
を実行すると****.xmlファイル内の必要なデータのみを残して削除します
なお、コマンドライン引数のxmlファイル名はパスを入力してください
'''

import sys

# 対象ファイルのパス
fileName = sys.argv[1]
# 必要なデータのRecode type名
recodeType = r'"HKQuantityTypeIdentifierHeartRate"'

# Recode type名を含む行の抽出
f = open(fileName, "r")
newData = ""
while True:
    line = f.readline()
    if line:
        if recodeType in line:
            newData += line
    else:
        break
f.close()

# 抽出したデータをファイルへ書き込み
f = open(fileName, "w")
f.write(newData)
f.close()
