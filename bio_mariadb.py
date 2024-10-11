import mariadb
from datetime import datetime

def test_mariadb_transactions() -> None:
    try:
        con = mariadb.connect(
            host='160.16.210.86',
            port=3307,
            user='root',
            password='selab',
            database='bio-db'
        )
        cur = con.cursor()
        
        # 挿入するデータ
        time = datetime.now()
        heartRate = 0
        pupil = 12
        eyeX = 30
        eyeY = 40
        blink = False
        
        # テーブルにデータ挿入
        insert_query = '''
        INSERT INTO bio_table (time, pupil, eyeX, eyeY, blink)
        VALUES (%s, %s, %s, %s, %s)
        '''
        # クエリ実行
        cur.execute(insert_query, (time, pupil, eyeX, eyeY, blink))
        
        print('Connection Succeeded!')
        # コネクションの終了
        con.commit()
        con.close()
    except Exception as e:
        print(f'Error commiting transaction: {e}')
        con.rollback()
        
test_mariadb_transactions()

'''
# MariaDBサーバーに接続
connection = mysql.connector.connect(
    host='160.16.210.86',
    port=3307,
    user='root',
    database='bio-db',
    password='selab'
)
print("Connected to MariaDB")

# カーソルを作成
cursor = connection.cursor()


# データ挿入
cursor.execute("INSERT INTO bio_table VALUES ('test', 'test', '', '', '')")
connection.commit()
print("Data inserted")

# データ読み込み
cursor.execute("SELECT * FROM bio_table")
records = cursor.fetchall()
print("Data from bio_table:", records)


cursor.close()
connection.close()
print("Connection closed")
'''
