import cv2
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

    ### テンプレートマッチング
    # テンプレート画像
    temp = cv2.imread('ok/eye0001.png')

    # 正規化相互相関演算
    result = cv2.matchTemplate(median, temp, cv2.TM_CCOEFF_NORMED)

    # 類似度の閾値
    threshold = 0.8

    match_y, match_x = np.where(result >= threshold)

    h, w = temp.shape[:2]

    for x, y in zip(match_x, match_y):
        cv2.rectangle(median, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
    cv2.imshow('template_matting', median)    
    
    # escキーでカメラを止める
    key = cv2.waitKey(10)
    if key == 27:
        break
    
# メモリ解放
cap.release()
cv2.destroyAllWindows()

