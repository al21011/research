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
dstFile = 'dataFile/HeartRate.csv'

# xmlファイルから必要なデータのみ抽出する
sFile = open(srcFile, "r")
dList = []
while True:
    sLine = sFile.readline()
    # workoutで計測したデータを除外しています
    if sLine[1] == '<':
        list1 = re.split('name:|creationDate="|startDate="|endDate="|value="|">|"|,', sLine)[20]
        # list1 = re.sub(r'\W', '', list1).replace(' +0900', '')
        list2 = re.split('name:|creationDate="|startDate="|endDate="|value="|">|"|,', sLine)[24]
        dList.append([list1, list2])
    else:
        break
    dList.sort()
sFile.close()

# csvファイルへ書き込み
dFile = open(dstFile, 'w')
# ヘッダ
dFile.write('date,value')
cnt = 0
for listIdx in dList:
    for idx in listIdx:
        if(cnt%2 == 0):
            dFile.write('\n')
        else:
            dFile.write(',')
        dFile.write(idx)
        cnt += 1

dFile.close()
