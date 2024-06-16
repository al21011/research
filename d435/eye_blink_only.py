import pyrealsense2 as rs
import numpy as np
import cv2

# RealSenseカメラの設定
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# カスケード分類器の読み込み
cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

# RealSenseカメラのストリーミング開始
pipeline.start(config)

try:
    while True:
        # フレーム待ち
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # RGB画像の取得
        color_image = np.asanyarray(color_frame.get_data())

        # グレースケールに変換
        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        # 顔の検出
        faces = cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=3, minSize=(100, 100))

        for (x, y, w, h) in faces:
            # 顔を矩形で囲む
            cv2.rectangle(color_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # 顔の上半分を検出対象範囲とする
            eyes_gray = gray[y : y + int(h/2), x : x + w]
            eyes = eye_cascade.detectMultiScale(eyes_gray, scaleFactor=1.11, minNeighbors=3, minSize=(8, 8))

            for (ex, ey, ew, eh) in eyes:
                # 目を矩形で囲む
                cv2.rectangle(color_image, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 255, 0), 1)

            if len(eyes) == 0:
                # 目が閉じているときの警告を表示
                cv2.putText(color_image, "Blink!", (10, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2, cv2.LINE_AA)

        # 画像を表示
        cv2.imshow('RealSense', color_image)

        # キー入力を待機し、ESCキーでループを抜ける
        if cv2.waitKey(1) == 27:
            break

finally:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()
