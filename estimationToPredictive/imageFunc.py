'''
瞳関連データ取得時に使う関数
'''

import cv2

### リストの中央値を返す
def cal_median(list):
    sorted_list = sorted(list)
    n = len(sorted_list)
    return sorted_list[n // 2]

### Pタイル法による2値化処理
def p_tile(img_gray, per):
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