import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def add_schedule(driver, wait, wait50, row):
    try:
        time.sleep(0.1)
        todo_inner = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".scheduleToDoInner")))
        # Create ActionChains object
        actions = ActionChains(driver)

        # Move to the element, offset by 100px from the left (x-axis), and 10px from the top (y-axis)
        actions.move_to_element_with_offset(todo_inner, 100, 10).click().perform()
        print("-- ✅ Clicked スケジュールバンド --")

    except Exception as e:
        print("❌ 'todo_inner' 要素が見つかりませんでした")

    for _ in range(2):
        try:
            rest_button = driver.find_element(By.CSS_SELECTOR, ".mod_btn_11")
            rest_button.click()
            print("-- ✅ Clicked '予約登録' button --")
            break
        except Exception:
            time.sleep(0.5)
    try:
        # --- Step 2: Get values from CSV ---
        date = row["date"]
        start_hour = row["start_hour"].zfill(2)     
        start_minute = row["start_minute"].zfill(2) 
        total_hour_min = row["total_hour"]  
        total_minute = row["total_minute"]    
        staff_id = row["staff_id"]  
        surname = row["surname"]
        givenname = row["givenname"]

        # --- Step 3: Set form values ---
        # --- Set date ---
        driver.execute_script(f"document.getElementById('rsvDate').value = '{date}';")
        # Set Hour
        hour_select =  wait.until(EC.presence_of_element_located((By.ID, "jsiRsvHour")))
        Select(hour_select).select_by_value(start_hour)

        # Set Minute
        
        minute_select = wait.until(EC.presence_of_element_located((By.ID, "jsiRsvMinute")))
        Select(minute_select).select_by_value(start_minute)

        # 時間（分単位）を select で選択
        wait.until(EC.presence_of_element_located((By.ID, "jsiRsvTermHour")))
        Select(driver.find_element("id", "jsiRsvTermHour")).select_by_value(total_hour_min)

        # 分を select で選択
        wait.until(EC.presence_of_element_located((By.ID, "jsiRsvTermMinute")))
        Select(driver.find_element("id", "jsiRsvTermMinute")).select_by_value(total_minute)

        # --- Set staff ID ---
        staff_select = Select(driver.find_element("name", "staffIdList"))
        staff_select.select_by_value(staff_id)
        
        # Set client name (if applicable)
        wait.until(EC.presence_of_element_located((By.ID, "nmSeiKana")))
        driver.find_element("id", "nmSeiKana").send_keys(surname)
        # driver.find_element("id", "nmMeiKana").send_keys(givenname)


        driver.find_element(By.ID, "regist").click()
        time.sleep(3)
        alert = driver.switch_to.alert
        alert.accept()  # 「OK」をクリック
        print("✅ アラートでOKをクリックしました。")

        try:
            ok_button = wait50.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.mod_btn_116.mb5.mr10.columnBlock.fr.accept")
            ))
            ok_button.click()
            print("✅ OKボタンをクリックしました。")
        except TimeoutException:
            print("⚠️ OKボタンが表示されませんでした（スキップします）")
            
        print(f"✅ Inserted: {surname} {givenname} {start_hour}:{start_minute}")
        time.sleep(5)

    except Exception as e:
        print("❌ 要素が見つかりませんでした1:", e)
