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
dstFile = "dataFile/HeartRate.csv"

# xmlファイルから必要なデータのみ抽出する
sFile = open(srcFile, "r")
dLine = ""
while True:
    sLine = sFile.readline()
    if sLine[1] == '<':
        dLine += (re.split('name:|creationDate="|startDate="|endDate="|value="|">|"|,', sLine)[9] + ",")
        # dLine += (re.split('name:|creationDate="|startDate="|endDate="|value="|">|"|,', sLine)[18] + ",")
        dLine += (re.split('name:|creationDate="|startDate="|endDate="|value="|">|"|,', sLine)[20] + ",")
        # dLine += (re.split('name:|creationDate="|startDate="|endDate="|value="|">|"|,', sLine)[22] + ",")
        dLine += (re.split('name:|creationDate="|startDate="|endDate="|value="|">|"|,', sLine)[24] + "\n")
    else:
        break
sFile.close()

# csvファイルへ書き込み
dFile = open(dstFile, "w")
# ヘッダ
dFile.write("deviceName,date,value\n")
dFile.write(dLine)
dFile.close()
