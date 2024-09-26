import cv2
import time
import numpy as np

# カメラ設定
cap = cv2.VideoCapture(0)

while True:
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
    
    '''
    ### 左目の検出及び矩形の描画
    # カスケード型の識別器
    eye_cascade = cv2.CascadeClassifier('haarcascade_left_eye.xml')
    # 目を検出
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    # 検出した目の描画
    for (x, y, w, h) in eyes:
        cv2.rectangle(median, (x, y), (x+w, y+h), (0, 0, 0), 2)
    '''
    
    '''
    ##### ドライバが首を振った際に見失ってしまうためボツ
    ### 目の位置をより大きく移したいためカメラの視界を1/2にリサイズ
    height, width = median.shape[:2]
    cropped_frame = median[height // 4: (height*3) // 4, width //4: (width*3) // 4]
    resized_frame = cv2.resize(cropped_frame, (width, height))
    '''
    
    '''
    ##### 誤検知多数のため保留
    ### ハフ円検出により虹彩を検出し表示する
    circles = cv2.HoughCircles(equalized, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=50, param2=30, minRadius=20, maxRadius=50)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # 円の描画
        for circle in circles[0, :]:
            cv2.circle(median, (circle[0], circle[1]), circle[2], (0, 0, 0), 5)
            cv2.circle(median, (circle[0], circle[1]), 2, (0, 0, 0), 3)
    '''
    
    ### 瞳孔の画素数を推定するために線を引いてみる
    #cv2.line(median, (200,50), (250,50), (0,0,0), 20)
    #cv2.line(median, (200,100), (400,100), (0,0,0), 20)
    
    # メディアンフィルタしたものを表示します
    cv2.imshow('median', median)
    
    '''
    ### カメラ画像デモ
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
