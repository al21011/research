import csv

# 基準値
pupil_standard = 16
big_standard = 18
small_standard = 9
point_of_interest = 2   # 注視点
position_standard = 9
blink_standard = 27

# 重み
w1 = 3
w2 = 1
w3 = 1
t = 0.01    # 影響度

data = []

with open('csvFiles/concentration.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# 瞳孔径基準値:20,瞳孔径回数:21,6,視線の向き:2,瞬き:1
# 最新30行を取得して比較
for index in range(len(data) - 29):
    big_cnt, small_cnt, position_cnt, blink_cnt = 0, 0, 0, 0
    # 30行分カウントする
    for eye_data in data[index:index+9]:
        if int(eye_data[0]) > pupil_standard:
            big_cnt += 1
        elif int(eye_data[0]) < pupil_standard:
            small_cnt += 1
        if int(eye_data[1]) != point_of_interest:
            position_cnt += 1
        if int(eye_data[2]) == 1:
            blink_cnt += 1
        
    x1 = (big_cnt*3 - big_standard) - (small_cnt*3 - small_standard)
    x2 = position_cnt*3 - position_standard
    x3 = blink_cnt*3 - blink_standard

    concentration = 1.00 + (x1 * w1 - x2 * w2 - x3 * w3) * t

    print(concentration)
