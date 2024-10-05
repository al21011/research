## 目次
### 1.カメラから瞳孔径を計測する

## 本文
### 1.カメラから瞳孔径を計測する
### 2.Apple Watchを使って心拍数を計測する

<1> infraredCamera.pyを実行します。

    python infraredCamera.py
   
    Intel RealSense D435をUSB接続して実行してください。

　　赤外線カメラ起動しない場合はescキーもしくはcontrol + Cを実行して終了させた後にUSBを差し直してください。

### 2.Apple Watchを使って心拍数を計測する

<1> 以下のコードをコマンドプロンプトで入力して必要なファイルをインストールしてください

   pip install pyrealsense2
    pip install numpy
    pip install opencv-python

たびたびエラーが起こるのでその場合はインストール方法をブラウザ検索するなどしてください

<2> eye_blink_only.pyを実行してください

    python d435/eye_blink_only.py

### 3.Intel RealSense D435を用いてまばたき検出と瞳孔径計測を行う

<1> eye_size.pyを実行してください

    python d435/eye_size.py

<datファイルでエラーが起こった場合>

以下のURLからshape_predictor_68_face_landmarks.dat.bz2をダウンロードしてください

[こちら](http://dlib.net/files/)

解凍して得られるdatファイルはd435内にコピーしてください