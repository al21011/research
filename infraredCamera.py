import cv2
import numpy as np

# カメラ設定
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # グレースケール変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ヒストグラム均一化
    equalized = cv2.equalizeHist(gray)
    # オープニング処理
    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(equalized, cv2.MORPH_OPEN, kernel)
    median = cv2.medianBlur(opening, 5)
    
    """
    # 単純なカメラ表示
    cv2.imshow('camera', frame)
    """
    # ヒストグラム均一化したものを表示
    cv2.imshow('histgram', equalized)
    """
    # オープニング処理したものを表示
    cv2.imshow('opening', opening)
    """
    # メディアンフィルタしたものを表示
    cv2.imshow('medianFilter', median)
    
    key = cv2.waitKey(10)
    if key == 27:
        break

# メモリ解放
cap.release()
cv2.destroyAllWindows()
