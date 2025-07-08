import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from login import login
from add_schedule import add_schedule

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 50)

print("▶ Step 1: Logging in to Sattou...")
login(driver, wait)

print("▶ Step 2: Adding schedule...")
# --- Step 1: Read the CSV ---
with open("../data/clear_diff.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        add_schedule(driver, wait, row)

time.sleep(10)

print("✅ All steps completed successfully.")
