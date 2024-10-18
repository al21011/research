## 目次
### 1.データベースのテーブルを確認する方法
### 2.integration_testブランチ関連

## 本文
### 1.データベースのテーブルを確認する方法

<1> Macbookのターミナルを開いてさくらサーバに入ります。

```sh
ssh selab@(IPアドレス)
```

<2>MariaDBコンテナに入ります。

```sh
docker exec -it bio-container bash
```

<3>rootユーザでコンテナ内のmariadbにアクセスします。

```sh
mariadb -u root -p
```

<4>データベースを選択します。

```sh
USE bio-db;
```

ここからはSQL文でテーブル内を参照したり、削除したり、挿入したり好きなようにできます。<br>
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

### 2.integration_testブランチ関連
以下のコマンドを打つと更新が反映されます。<br>
(addの.はファイル名を指定することもできます)

```sh
git add .
git commit -m "コメント"
git push origin integration_test
```

pushで弾かれる場合(リモートとローカルのブランチ履歴が違うと発生します)<br>
以下のコードを実行して下さい。多くの場合はこちらでpushを行えるようになります。

```sh
git pull origin integration_test
```

実行に少し時間がかかることがあります。また、ターミナルが遷移してしまった場合は:q!を入力してEnterキーを押すと解決します。

実行が済んだらpushを改めて行います。

```sh
git push origin integration_test
```
