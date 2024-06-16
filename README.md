## 目次
### 1.apple watchで計測したxmlファイルを心拍数のみを抽出してcsvファイルにする場合
### 2.intel realsense d435を用いてまばたき検出を行う
### 3.Intel RealSense D435を用いてまばたき検出と瞳孔径計測を行う

## 本文
### 1.apple watchで計測したxmlファイルを心拍数のみを抽出してcsvファイルにする場合

<1> extractionXml.pyによってxmlファイルを心拍数のみ抽出して書き直します

    python extractionXml.py ****.xml

　　ここで****.xmlは容量を減らしたいxmlファイルのパスを入力してください

<2> 書き直したxmlファイルをcsvファイルに変換します

    python healthDataOnly.py ****.xml

　　ここで****.xmlは先ほどと同じくファイルのパスです


### 2.intel realsense d435を用いてまばたき検出を行う

<1> 以下のコードをコマンドプロンプトで入力して必要なファイルをインストールしてください

    pip install pyrealsense2
    pip install numpy
    pip install opencv-python

たびたびエラーが起こるのでその場合はインストール方法をブラウザ検索するなどしてください

<2> eye_blink_only.pyを実行してください

    python d435/eye_blink_only.py

### 3.Intel RealSense D435を用いてまばたき検出と瞳孔径計測を行う

<1> 以下のURLからshape_predictor_68_face_landmarks.dat.bz2をダウンロードしてください

[こちら](http://dlib.net/files/)

解凍して得られるdatファイルはd435内にコピーしてください

<2> eye_size.pyを実行してください

    python d435/eye_size.py
