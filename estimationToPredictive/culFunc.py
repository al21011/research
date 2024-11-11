'''
代表値などの計算を行う関数を集めたファイル
'''

import statistics
import numpy as np
from sklearn.decomposition import PCA

### リストの最頻値あるいは中央値を返す
def mode_or_median(eye_list) -> int:
    try:
        ans = statistics.mode(eye_list)
    except statistics.StatisticsError:
        ans = int(np.median(eye_list))
    return ans

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
