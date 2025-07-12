import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

def get_salon_schedul(driver, download_dir):
    driver.get("https://salonboard.com/login/")

    # Step 4: Login
    userId = "CD53764"
    password = "@filament09-1"

    driver.find_element(By.CSS_SELECTOR, 'input[name="userId"]').send_keys(userId)
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".common-CNCcommon__primaryBtn.loginBtnSize").click()

    print("✅ Login to Salonboard")

    # Step 5: Click "Today’s Schedule"
    try:
        wait = WebDriverWait(driver, 10)
        today_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#todayReserve")))
        today_button.click()
        print("✅ [今日の予約] ボタンをクリックしました。")

        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        start_tag = soup.find('input', {'id': 'rsvDateFrom'})
        start_tag['value'] = '20250710'

        end_tag = soup.find('input', {'id': 'rsvDateTo'})
        end_tag['value'] = '20250810'

        options = soup.select('select#stylistId option')

        staff_list = []
        for option in options:
            value = option.get('value').strip()
            name = option.get_text(strip=True)
            if value:  # skip "すべてのスタッフ"
                staff_list.append([value, name])

        # Write to CSV
        with open('../data/staff_list.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['value', 'name'])  # header
            writer.writerows(staff_list)

        print("✅ staff_list.csv has been created.")

        # Step 6: Click download CSV button
        driver.find_element(By.CSS_SELECTOR, "#csvOutput").click()
        print("-- ✅ Clicked download button --")

        # Step 7: Wait for file to download completely
        while True:
            files = os.listdir(download_dir)

            csv_ready = any(f.endswith(".csv") for f in files)
            crdownload_exists = any(f.endswith(".crdownload") for f in files)

            if csv_ready and not crdownload_exists:
                print("-- ✅ Download finished")
                break
            else:
                time.sleep(0.5)

        # Step 8: Wait a little extra time to ensure write is complete
        time.sleep(2)

        print("-- ✅ Download completed. Getting today schedule. --")

    except Exception as e:
        print("❌ ボタンが見つかりませんでした:", e)