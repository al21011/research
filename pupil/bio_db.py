'''
データベース関連の関数をまとめてあるファイル
bio-db    瞳関連データを記録する
'''

import mariadb

### サーバ内のデータベースに書き込む処理
def write_bio_db(time, pupil, position, blink) -> None:
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='est_db'
        )
        cur = con.cursor()
        
        # テーブルにデータ挿入
        insert_query = '''
        INSERT INTO eye_table (time, pupil, position, blink, concentration)
        VALUES (%s, %s, %s, %s, %s)
        '''
        # クエリ実行
        cur.execute(insert_query, (time, pupil, position, blink, None))
        
        # コネクションの終了
        con.commit()
        con.close()
        print(f'{time}')
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()
