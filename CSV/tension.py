import csv
import numpy as np
from sklearn.decomposition import PCA

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

data = []

with open('csvFiles/tension.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

for index in range(len(data)):
    if index < 94:
        continue
    # L/Tを計算
    L_T = (calculate_axes(data[:index]))
    print(L_T)
    # 推定値算出

