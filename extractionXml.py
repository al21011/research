'''
ヘルスケアから書き出したxmlファイルが重いので心拍数のみのファイルに書き換えるソースコードです
'''

# 対象ファイルのパス
fileName = "xmlDataFile/export5_28.xml"
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
