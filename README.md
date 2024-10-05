## 目次
### 1.カメラから瞳孔径を計測する

## 本文
### 1.カメラから瞳孔径を計測する
### 2.Apple Watchを使って心拍数を計測する
### 3.サーバ同期をする

<1> infraredCamera.pyを実行します。

```sh
python infraredCamera.py
```

Intel RealSense D435をUSB接続して実行してください。

赤外線カメラ起動しない場合はescキーもしくはcontrol + Cを実行して終了させた後にUSBを差し直してください。

### 2.Apple Watchを使って心拍数を計測する

<1> Xcodeを起動して Create New Project > watchOSタブのAPPを選択してNext > Product NameはHeartRateを記入しBundle IdentiferはWatch APP with New Companion iOS Appを選択してNext

<2> GitのContentView.swiftをコピーしてXCodeのHeartRate/HeartRate/ContentViewに貼り付ける。

    続いてGitのWatchContentView.swiftをコピーしてXCodeのHeartRate/HeartRate Watch APP/ContentViewに貼り付ける。

<3> HealthKitを利用可能にするためHeartRate(プロジェクトフォルダ)を選択してTARGETSにHeartRateを設定する。

    infoタブを開きkeyの任意の場所で右クリックをしてAdd Rowを選択する。

    Add Rowするとプルダウンが表示されるので、Privacy - Health Share Usage Description、Privacy - Health Update Usage Description、Privacy - Health Records Usage Descriptionの3つを追加する。

    追加したkeyのValueのところにfor use healthkitと入力(文字はなんでも良いですが、文字数と文字形式に制限があります)

    <img width="1283" alt="スクリーンショット 2024-10-05 23 46 33" src="https://github.com/user-attachments/assets/7bfc9948-c614-4071-b1ff-3430082f5fbf">

    Package Dependenciesに関しては余計なこと(結果的に不必要だったもの)をしただけなので気にしないでください。

<4> macとiPhoneをUSB接続して上部のデバイスを自身のiPhoneに変更します。

<img width="564" alt="スクリーンショット 2024-10-05 23 51 12" src="https://github.com/user-attachments/assets/82e79ba1-ec32-4409-bc90-6ac434bf0950">

<5> XCodeの左上に再生ボタンがあるので押します

<6> iPhone側でHeartRateからのHealthKit利用を許可します。

<7> Apple Watchのstart workoutボタンを押せば計測が開始されます。

### 3.サーバ同期をする

現在コーディング中です。

出来上がり次第、更新します。
