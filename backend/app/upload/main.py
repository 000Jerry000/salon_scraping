import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

def upload(driver):
    driver.get("https://salonboard.com/login/")

    # Step 4: Login
    userId = "CD53764"
    password = "@filament09-1"

    driver.find_element(By.CSS_SELECTOR, 'input[name="userId"]').send_keys(userId)
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".common-CNCcommon__primaryBtn.loginBtnSize").click()

    print("✅ Loggin OK")

    # Step 5: Click "Today’s Schedule"
    try:
        today_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mod_btn_102")))
        today_button.click()
        print("✅ [本日のスケジュール] ボタンをクリックしました。")

        time.sleep(3)

    except Exception as e:
        print("❌ [本日のスケジュール] ボタンが見つかりませんでした:", e)

    try:
        todo_inner = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".scheduleToDoInner")))
        todo_inner.click()
        print("-- ✅ Clicked .scheduleToDoInner --")

        # Then click the rest button (class: .mod_btn_11)
        rest_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mod_btn_11")))
        rest_button.click()
        print("-- ✅ Clicked .mod_btn_11 button --")

    except Exception as e:
        print("❌ 要素が見つかりませんでした:", e)

    time.sleep(10)

upload(driver)