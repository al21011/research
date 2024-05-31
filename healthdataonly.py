'''
容量を軽くしたxmlファイルをcsvファイルに変換するためのソースコードです
python healthDataOnly.py ****.xml
csvファイルに変換したいxmlファイルのパスを入力してください
なお、extractionXml.pyにて容量削減したxmlファイルを使用してください
'''

import sys
import re

# 入出力のファイル名
srcFile = sys.argv[1]
dstFile = "xmlDataFile/HeartRate.csv"

# xmlファイルから必要なデータのみ抽出する
sFile = open(srcFile, "r")
dLine = ""
while True:
    sLine = sFile.readline()
    if sLine:
        print(re.split('name:|creationDate="|startDate="|endDate="|value="|"|,'))
    else:
        break

sFile.close()

dFile = open(dstFile, "w")
# csvファイルのヘッダ
dFile.write("deviceName,creationDate,startDate,endDate,value")

dFile.close()
