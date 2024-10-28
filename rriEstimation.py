'''
### 心電センサを用いた集中力の推定機能の実装
    1.
    2.準備用の関数を実行して基準値を
    DBにはtime, heartRate, RRI, position, blinkの順でカラムが用意されている
    0.00-2.00の間で算出し、エラーは3.00とする
'''

import matplotlib.pyplot as plt
import numpy as np

### RRIデータからポアンカレプロットを描画する関数
def plot_poincare(rri):
    # RRIデータから次のRRI間隔とその前のRR間隔を取得
    rri_n = rri[:-1]
    rri_n1 = rri[1:]
    
    # プロットの作成
    plt.figure(figsize=(6, 6))
    plt.scatter(rri_n, rri_n1, color='blue', alpha=0.5, edgecolor='k', s=20)
    
    # 軸の設定
    plt.xlabel("RRI(n) [ms]")
    plt.ylabel("RRI(n+1) [ms]")
    plt.title("Poincare Plot")
    plt.axline((0, 0), slope=1, color="red", linestyle="--")
    
    # 軸の範囲をRRIの範囲に合わせる
    min_rri = min(min(rri_n), min(rri_n1))
    max_rri = max(max(rri_n), max(rri_n1))
    plt.xlim(min_rri - 50, max_rri + 50)
    plt.ylim(min_rri - 50, max_rri + 50)
    
    plt.grid(True)
    plt.show()
    
    return np.array(rri_n), np.array(rri_n1)
    
### 最大距離の算出
def max_distances(rri_n, rri_n1):
    # 各点の並行成分と垂直成分を計算
    parallel_components = (rri_n + rri_n1) / np.sqrt(2)
    perpendicular_components = (rri_n1 - rri_n) / np.sqrt(2)
    
    # 並行成分の最大距離
    L = np.max(parallel_components) - np.min(parallel_components)
    
    # 垂直成分の最大距離
    T = np.max(perpendicular_components) - np.min(perpendicular_components)
    
    return L, T

# RRIの例データ（単位はms）
rri_data = [800, 810, 790, 830, 820, 850, 800, 790, 770, 760, 780]
rri_n, rri_n1 = plot_poincare(rri_data)
L, T = max_distances(rri_n, rri_n1)
    