import mariadb
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

### ポアンカレプロットを描画する関数
def plot_poincare(rri):
    # RRI の数を取得
    n = len(rri)

    # x, y 軸のデータを作成
    x = rri[:-1]  # RRI[n] を x 軸に
    y = rri[1:]   # RRI[n+1] を y 軸に

    # ポアンカレプロットの描画
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=10)  # 散布図を描く
    plt.title("Poincaré Plot")
    plt.xlabel("RRI(n)")
    plt.ylabel("RRI(n+1)")
    plt.plot([min(x), max(x)], [min(x), max(x)], color='red', linestyle='--')  # y = x の直線
    plt.grid()
    plt.axis('equal')  # アスペクト比を等しく保つ
    plt.show()

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

### RRIを100行取得して返す関数
def fetch_data():
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='std_db'
        )
        cur = con.cursor()
        
        # テーブルからデータ取得(準備の開始時刻を記入)
        insert_query = '''
        SELECT RRI FROM std_table
        WHERE time >= '2024-10-31 03:16:30'
        ORDER BY time ASC LIMIT 100
        '''
        # クエリ実行
        cur.execute(insert_query)
        
        data = cur.fetchall()
        
        # コネクションの終了
        cur.close()
        con.close()
        
        return data
    
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

# ポアンカレプロットの描画
plot_poincare(fetch_data())
# L/Tの算出
print(calculate_axes(fetch_data()))
