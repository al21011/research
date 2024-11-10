import imageFunc
import bio_db as db
import cv2
import numpy as np
import mariadb
import time
from datetime import datetime

# カメラ設定
cap = cv2.VideoCapture(0)

# 変数
tmp_time = -1
blink_flag = 0

while True:
    # データベースに書き込む情報
    now_time = datetime.now()
    pupil, position = [], []
    
    ret, frame = cap.read()
    
    ### ノイズ除去
    # グレースケール変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ヒストグラム均一化
    equalized = cv2.equalizeHist(gray)
    # オープニング処理、メディアンフィルタによるノイズ除去
    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(equalized, cv2.MORPH_OPEN, kernel)
    median = cv2.medianBlur(opening, 5)
    
    ### 左目の検出及び矩形の描画
    # カスケード型の識別器
    eye_cascade = cv2.CascadeClassifier('pupil/haarcascade_left_eye.xml')
    # 目を検出
    eyes = eye_cascade.detectMultiScale(median, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    # 目の検出数は1つに絞る
    if len(eyes) >= 2:
        continue
    # 検出しなかった場合
    if len(eyes) == 0:
        cv2.putText(median, 'Blink...', (20,20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255))
        blink_flag = 1
    # 検出した目の描画
    for (x, y, w, h) in eyes:
        cv2.rectangle(median, (x, y), (x+w, y+h), (0, 0, 0), 2)
        # 目の領域を切り出す
        eye_region = median[y:y+h, x:x+w]
        # ノイズ軽減
        blurred_eye_region = cv2.GaussianBlur(eye_region, (9, 9), 2)
        
        # Pタイル法
        binary_frame = imageFunc.p_tile(blurred_eye_region, 0.01)
        
        # ハフ円検出
        circles = cv2.HoughCircles(binary_frame, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=100, param2=10, minRadius=0, maxRadius=40)
        
        if circles is not None: 
            circles = np.round(circles[0, :]).astype("int")
            # 検出した円の描画
            for (cx, cy, r) in circles:
                cv2.circle(median, (x+cx, y+cy), r, (0,0,0), 2)
                cv2.circle(median, (x+cx, y+cy), 2, (0,0,0), 3)
                
            # 取得データをリストに追加する
            pupil.append(circles[0][2]*2)
            if circles[0][0] < (7*w/18):
                position.append(0)
            elif circles[0][0] < (4*w/9):
                position.append(1)
            else:
                position.append(2)

            
            # データベースへ書き込み
            if (int(now_time.second) - tmp_time >= 1) or (int(now_time.second) - tmp_time < 0):
                db.write_bio_db(
                    now_time,
                    int(imageFunc.cal_median(pupil)),
                    int(imageFunc.cal_median(position)),
                    blink_flag
                )
                # 色々リセット
                pupil.clear()
                position.clear()
                blink_flag = 0
                tmp_time = int(now_time.second)
                time.sleep(0.05)
            
        '''
        # 目の周りの2値化画像確認用
        cv2.imshow('pupil', binary_frame)
        cv2.moveWindow('pupil', 0, 50)
        '''

    ### カメラ画像デモ
    cv2.imshow('median', median)
    '''
    cv2.imshow('opening', opening)
    cv2.imshow('histgram', equalized)
    cv2.imshow('camera', frame)
    '''
    
    # escキーでカメラを止める
    key = cv2.waitKey(10)
    if key == 27:
        break

# メモリ解放
cap.release()
cv2.destroyAllWindows()
