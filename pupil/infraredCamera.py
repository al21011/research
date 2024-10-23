import cv2
import numpy as np
import mariadb
import time
from datetime import datetime
import asyncio

# カメラ設定
cap = cv2.VideoCapture(0)

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

### サーバ内のデータベースに書き込む処理
def mariadb_transactions(time, pupil, position, blink) -> None:
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='bio-db'
        )
        cur = con.cursor()
        
        # テーブルにデータ挿入
        insert_query = '''
        INSERT INTO bio_table (time, pupil, position, blink)
        VALUES (%s, %s, %s, %s)
        '''
        # クエリ実行
        cur.execute(insert_query, (time, pupil, position, blink))
        
        # コネクションの終了
        con.commit()
        con.close()
        print(f'{time}')
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()
    
### リストの中央値を返す
def cal_median(list):
    sorted_list = sorted(list)
    n = len(sorted_list)
    return sorted_list[n // 2]

### スレッド処理用1秒待機
def call_periodically():
    time.sleep(1)

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
                mariadb_transactions(
                    now_time,
                    int(cal_median(pupil)),
                    int(cal_median(position)),
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
