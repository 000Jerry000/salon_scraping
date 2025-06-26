# ============================================================================================================================
# ||                                                     Create plan                                                        ||
# ============================================================================================================================


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

def login():
    source_file = "../../config.csv"

    # フォームページにアクセス
    driver.get("https://salonboard.com/login/")
    time.sleep(1)

    with open(source_file, 'r', encoding="utf-8", errors="ignore") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        userId = reader[0][1]
        password = reader[0][2]

    # 氏名入力（姓と名の間は半角スペース）
    name_input = driver.find_element(By.NAME, "userId")
    name_input.send_keys(userId)
    name_input = driver.find_element(By.NAME, "password")
    name_input.send_keys(password)

    # 検索ボタンをクリック（JS関数呼び出し型）
    driver.find_element(By.CSS_SELECTOR, 'div.loginBtnWrap a').click()

    # 検索結果を待つ（必要なら待機を増やす）
    time.sleep(1)

login()

driver.quit()
print("---------------------------------- ✅ Login Successfully ---------------------------------")