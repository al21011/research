import cv2

# カメラ設定
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.imshow('camera', frame)

    key = cv2.waitKey(10)
    if key == 27:
        break

# メモリ解放
cap.release()
cv2.destroyAllWindows()
