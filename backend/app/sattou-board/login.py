# ============================================================================================================================
# ||                                                    Login to Sattou                                                     ||
# ============================================================================================================================


import time
from selenium.webdriver.common.by import By

def login(driver):
    driver.get("https://sv1.sattou.net/filament/")

    # Step 4: Login
    userId = "hpbtest"
    password = "sattouhpb"

    driver.find_element(By.CSS_SELECTOR, 'input[name="login_id"]').send_keys(userId)
    driver.find_element(By.CSS_SELECTOR, 'input[name="pw"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    time.sleep(3)
    print("---------------------------------- ✅ Login to sattou Successfully ---------------------------------")
