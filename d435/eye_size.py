import pyrealsense2 as rs
import numpy as np
import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance

def calc_ear(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    eye_ear = (A + B) / (2.0 * C)
    return round(eye_ear, 3)

def eye_marker(face_mat, position):
    for i, ((x, y)) in enumerate(position):
        cv2.circle(face_mat, (x, y), 1, (255, 255, 255), -1)
        cv2.putText(face_mat, str(i), (x + 2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

# RealSenseカメラの設定
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# カスケード分類器の読み込み
cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
parts_detector = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


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

    # 以下引用
        tick = cv2.getTickCount()

        if len(faces) == 1:
            x, y, w, h = faces[0, :]
            cv2.rectangle(color_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            face_gray = gray[y :(y + h), x :(x + w)]
            scale = 480 / h
            face_gray_resized = cv2.resize(face_gray, dsize=None, fx=scale, fy=scale)

            face = dlib.rectangle(0, 0, face_gray_resized.shape[1], face_gray_resized.shape[0])
            face_parts = parts_detector(face_gray_resized, face)
            face_parts = face_utils.shape_to_np(face_parts)

            left_eye = face_parts[42:48]
            eye_marker(face_gray_resized, left_eye)

            left_eye_ear = calc_ear(left_eye)
            cv2.putText(color_image, "LEFT eye EAR:{} ".format(left_eye_ear), 
                (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, cv2.LINE_AA)

            right_eye = face_parts[36:42]
            eye_marker(face_gray_resized, right_eye)

            right_eye_ear = calc_ear(right_eye)
            cv2.putText(color_image, "RIGHT eye EAR:{} ".format(round(right_eye_ear, 3)), 
                (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, cv2.LINE_AA)

            if (left_eye_ear + right_eye_ear) < 0.55:
                cv2.putText(color_image,"Sleepy eyes. Wake up!",
                    (10,180), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3, 1)

            cv2.imshow('frame_resize', face_gray_resized)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - tick)
        cv2.putText(color_image, "FPS:{} ".format(int(fps)), 
            (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('frame', color_image)
        if cv2.waitKey(1) == 27:
            break  # esc to quit

finally:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()
