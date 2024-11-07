import csv
from sklearn.decomposition import PCA
import numpy as np

### L/Tの計算
def calculate_axes(returns):
    # PCAを使用して主成分を計算
    pca = PCA(n_components=2)
    # データを整形
    data = np.column_stack((returns[:-1], returns[1:]))
    pca.fit(data)

    # 主成分ベクトル
    components = pca.components_
    # 分散
    explained_variance = pca.explained_variance_

    # 長軸と短軸の長さを取得
    L = 2 * np.sqrt(explained_variance[0])  # 長軸
    T = 2 * np.sqrt(explained_variance[1])  # 短軸
    
    return L/T

### L/Tの計算(参考文献の提案手法のやり方)
# X座標を変える必要がありそうなので保留

### CSVファイルに書き込みを行う処理
def write_to_csv(L_T):
    filename = 'csvFiles/sleep_cal.csv'
    # CSVファイルに書き込み
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        # timeとRRIを行ごとに書き込む
        writer.writerow([L_T])

dataRRI = []

with open('csvFiles/sleep.csv', 'r') as file:
    # 初めに100行を取得
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        dataRRI.append(row[1])
        if i < 100:
            continue
        # L/Tの書き込み
        write_to_csv(calculate_axes(dataRRI))
    