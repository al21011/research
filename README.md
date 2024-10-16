## 目次
### データベースのテーブルを確認する方法

## 本文
### データベースのテーブルを確認する方法

<1> Macbookのターミナルを開いてさくらサーバに入ります。

```sh
ssh selab@(IPアドレス)
```

MariaDBコンテナに入ります。

```sh
docker exec -it bio-container bash
```

rootユーザでコンテナ内のmariadbにアクセスします。

```sh
mariadb -u root -p
```

データベースを選択します。

```sh
USE bio-db;
```

SQLでテーブル内を参照したり、削除したり、挿入したり好きなようにできます。<br>
以下は全テーブルを参照する例です。

```sh
SELECT * FROM bio_table;
```

他にもいくつか使いそうなものの例を上げておきます。<br>
・テーブルのカラムを確認する

```sh
DESCRIBE bio_table;
```

・テーブルの特定のデータを消去する(双方の許可がある、もしくは不要なことが自明な場合に使いましょう)<br>
なお、WHEREはSELECT * FROMの時など色々な場面で使えます。

```sh
DElETE FROM bio_table WHERE heartRate >= 30;
```

