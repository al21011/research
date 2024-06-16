from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ChromeDriverのセットアップ
options = Options()
options.headless = True  # ブラウザを非表示にする
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ウェブページを開く
url = "https://app.hyperate.io/0181"
driver.get(url)

# ページが完全に読み込まれるのを待つための遅延
driver.implicitly_wait(10)

# 心拍数データを含む要素を探す
heart_rate_element = driver.find_element(By.CLASS_NAME, 'heartrate')

# 心拍数データを取得して表示
heart_rate = heart_rate_element.text
print("心拍数データ：", heart_rate)

# ブラウザを閉じる
driver.quit()




'''
# ライブラリ
import requests
# 解析ライブラリ
from bs4 import BeautifulSoup

# ウェブページurl
r = requests.get("https://app.hyperate.io/0181")
# タイプ
result = r.text
# BeautifulSoupタイプに変換
bs = BeautifulSoup(result, 'html.parser')
print("データ：")
# class属性を使って値を取得します
data1 = bs.find_all(class_='heartrate')
# ループ出力
for i in data1:
    print(i.text)
'''
