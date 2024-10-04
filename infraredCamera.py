import cv2
import time
import numpy as np

# カメラ設定
cap = cv2.VideoCapture(0)


# 照明やメガネの有無などでムラがあるので保留
### Pタイル法による2値化処理
def p_tile_threshold(img_gray, per):
    img_hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
    # 画像で占める割合から画素数を計算
    all_pic = img_gray.shape[0] * img_gray.shape[1]
    pic_per = all_pic * per
    # Pタイル法による閾値計算
    p_tile_thr = 0
    pic_sum = 0
    for hist in img_hist:
        pic_sum += hist
        # 輝度の割合が定めた割合を超えた場合に終了
        if pic_sum > pic_per:
            break
        p_tile_thr += 1
    # Pタイル法を踏まえて2値化処理
    ret, img_thr = cv2.threshold(img_gray, p_tile_thr, 255, cv2.THRESH_BINARY)
    return img_thr


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
    
    ### 左目の検出及び矩形の描画
    # カスケード型の識別器
    eye_cascade = cv2.CascadeClassifier('haarcascade_left_eye.xml')
    # 目を検出
    eyes = eye_cascade.detectMultiScale(median, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    # 検出しなかった場合
    if len(eyes) == 0:
        cv2.putText(median, 'Blink...', (20,20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255))
    # 検出した目の描画
    for (x, y, w, h) in eyes:
        cv2.rectangle(median, (x, y), (x+w, y+h), (0, 0, 0), 2)
        # 目の領域を切り出す
        eye_region = median[y:y+h, x:x+w]
        # ノイズ軽減
        blurred_eye_region = cv2.GaussianBlur(eye_region, (9, 9), 2)
        
        
        # Pタイル法
        binary_frame = p_tile_threshold(blurred_eye_region, 0.01)
        
        
        '''
        # Cannyエッジ検出
        edges = cv2.Canny(blurred_eye_region, 50, 150)
        # CLAHE(適応的ヒストグラム平坦化)によるコントラスト強調 + 大津の2値化
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_image = clahe.apply(blurred_eye_region)
        ret, binary_frame = cv2.threshold(enhanced_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # 大津の二値化
        ret, binary_frame = cv2.threshold(blurred_eye_region, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # アダプティブ2値化
        binary_frame = cv2.adaptiveThreshold(blurred_eye_region, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        '''
        
        # ハフ円検出
        circles = cv2.HoughCircles(binary_frame, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=100, param2=10, minRadius=0, maxRadius=40)
        
        if circles is not None: 
            circles = np.round(circles[0, :]).astype("int")
            # 検出した円の描画
            for (cx, cy, r) in circles:
                cv2.circle(median, (x+cx, y+cy), r, (0,0,0), 2)
                cv2.circle(median, (x+cx, y+cy), 2, (0,0,0), 3)
                
                '''
                ### 検出した円内部のヒストグラム表示
                # マスク(円の内部を1,外部を0とする)作成
                mask = np.zeros_like(blurred_eye_region)
                cv2.circle(mask, (cx, cy), r, 255, thickness=-1)
                # 円内部に限定してヒストグラム計算
                masked_pixels = cv2.bitwise_and(blurred_eye_region, blurred_eye_region, mask=mask)
                hist = cv2.calcHist([masked_pixels], [0], mask, [256], [0, 256])
                # ヒストグラム表示
                plt.figure()
                plt.plot(hist)
                plt.title(f'Histgram for circle at ({cx}, {cy}) with radius {r}')
                plt.xlabel('Pixel Intensity')
                plt.ylabel('Number of Pixels')
                plt.show()
                '''
                
            print(f'瞳孔径： {circles[0][2]*2}')
            print(f'( {x+circles[0][0]} , {y+circles[0][1]} )')
        
            
        # 目の周りの2値化画像確認用
        cv2.imshow('pupil', binary_frame)
        cv2.moveWindow('pupil', 0, 50)
        

    ### カメラ画像デモ
    cv2.imshow('median', median)
    cv2.imshow('opening', opening)
    cv2.imshow('histgram', equalized)
    cv2.imshow('camera', frame)
    
    # escキーでカメラを止める
    key = cv2.waitKey(10)
    if key == 27:
        break

# メモリ解放
cap.release()
cv2.destroyAllWindows()
