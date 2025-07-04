import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv


from get_salon_schedul import get_salon_schedul
from convert_board_data import convert_board_data
from login import login
from getting_schedule import getting_schedule
from finding_diff import compare_rows

# Step 1: Set and clean download directory
download_dir = os.path.abspath("../downloads")
os.makedirs(download_dir, exist_ok=True)

# 🔥 Clean download folder
for filename in os.listdir(download_dir):
    file_path = os.path.join(download_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            import shutil
            shutil.rmtree(file_path)
    except Exception as e:
        print(f"⚠️ Failed to delete {file_path}. Reason: {e}")
print("✅ Download folder cleaned:", download_dir)

# Step 2: Configure Chrome to use the folder
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Step 3: Launch browser
driver = webdriver.Chrome(options=chrome_options)

print("▶ Step 0: Loggin to Salonboard...")
get_salon_schedul(driver, download_dir)

print("▶ Step 1: Converting salon board data...")
convert_board_data()

print("▶ Step 2: Logging in to Sattou...")
login(driver)

print("▶ Step 3: Getting schedule page...")
getting_schedule(driver)

print("▶ Step 4: Finding different row...")
compare_rows('../data/sattou_schedule.csv', '../data/board_data.csv')

print("✅ All steps completed successfully.")
