import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def login(driver, wait):
    driver.get("https://salonboard.com/login/")

    # Step 4: Login
    userId = "CD53764"
    password = "@filament09-1"

    driver.find_element(By.CSS_SELECTOR, 'input[name="userId"]').send_keys(userId)
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".common-CNCcommon__primaryBtn.loginBtnSize").click()

    print("✅ Loggin OK")

    try:
        today_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mod_btn_102")))
        today_button.click()
        print("✅ [本日のスケジュール] ボタンをクリックしました。")

        time.sleep(3)

    except Exception as e:
        print("❌ [本日のスケジュール] ボタンが見つかりませんでした:", e)
