'''
緊張感・集中力の推定機能の実装
DBにはtime, heartRate, pupil, eyeX, eyeY, blinkの順でカラムが用意されている
'''

import mariadb
import random

### データベースから情報取得
def mariadb_fetch() -> None:
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
        SELECT * FROM bio_table
        '''
        # クエリ実行
        cur.execute(insert_query)
        
        # データの取得
        rows = cur.fetchall()
        
        # データの表示
        for row in rows:
            print(row)
            
        # コネクションの終了
        con.commit()
        con.close()
        
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()

# ランダムな値を返す
def random_value(min_value, max_value):
    return random.uniform(min_value, max_value)

mariadb_fetch()
