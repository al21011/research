## 目次
### 1.apple watchで計測したxmlファイルを心拍数のみを抽出してcsvファイルにする場合
### 2.intel realsense d435をpythonで起動する

# 本文
### 1.apple watchで計測したxmlファイルを心拍数のみを抽出してcsvファイルにする場合

<1> extractionXml.pyによってxmlファイルを心拍数のみ抽出して書き直します

> python extractionXml.py ****.xml

ここで****.xmlは容量を減らしたいxmlファイルのパスを入力してください

<2> 書き直したxmlファイルをcsvファイルに変換します

> python healthDataOnly.py ****.xml

ここで****.xmlは先ほどと同じくファイルのパスです


### 2.intel realsense d435をpythonで起動する

<事前準備> pyrealsense2をinstallする必要があります(pythonのバージョンが最新だとできません)

> pip install pyrealsense2 (もしくは python -m pip install pyrealsense2)

<1> display.pyを実行する

> python display.py

まだ全然いじれていないのでただ表示するだけです...

以下のURLからダウンロード
http://dlib.net/files/