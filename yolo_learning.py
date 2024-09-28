'''
パラメータなど、YOLOの使い方についての説明
Train(学習用データセット):全データセットの大部分を占める
    epochs:何回学習を行うか imgsz:入力画像のサイズ 
Valid(検証用データセット):モデルの性能評価に使われる
Test(テスト用データセット):モデルの最終評価に使われる
'''

import cv2
from roboflow import Roboflow
from ultralytics import YOLO

'''
### APIキーを利用してYOLOの学習データをダウンロード
rf = Roboflow(api_key="S4bGxsxcJ6Xg9zuZTy3T")
project = rf.workspace("s11").project("iris-and-pupil-detection")
version = project.version(1)
dataset = version.download("yolov8")
'''

'''
# 入力画像のサイズを調べる
img = cv2.imread('Iris-and-pupil-detection-1/valid/images/kelvinr4_bmp_jpg.rf.7d1572d059f3313c678b0f6e231ad2be.jpg')
print(img.shape)
'''

'''
### ダウンロードしたYOLOの学習データを用いてモデルを作成
model = YOLO('yolov8n.pt')
# epochs:学習を繰り返す回数 imgsz:入力画像のサイズ
results = model.train(data='Iris-and-pupil-detection-1/data.yaml', epochs=3, imgsz=640, device='mps')             
'''


### 作成したモデルを用いて実際に動かす(画像)
model = YOLO('runs/detect/train/weights/last.pt')
model.predict('test.png', save=True, conf=0.1)


