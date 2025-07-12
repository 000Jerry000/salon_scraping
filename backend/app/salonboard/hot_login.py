import requests
import csv
import re
from get_token import token_generation

token, _ = token_generation()

def hot_login():
    # Config values
    API_URL = "https://sattou.net"
    BRAND_DIR = "filament"

    params = {
        "param1": 2,
    }

    url = f"{API_URL}/{BRAND_DIR}/api/v1/hotLogin"

    headers = {
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        result = response.json()

        return result

    except Exception as e:
        print("Error:", e)
        return False

def save_to_csv(data, filename="../salon-data/hotpepper_login.csv"):
    if not data:
        print("No data to write.")
        return

    # extract the list of dicts
    records = data.get("data", [])

    if not records:
        print("No records in response.")
        return

    # Collect all unique keys across all records
    all_keys = set()
    for rec in records:
        all_keys.update(rec.keys())

    # Sort keys for neatness
    all_keys = sorted(all_keys)

    # Function to extract shop number from csv_path
    def extract_shop_num(row):
        path = row.get("csv_path", "")
        match = re.search(r"shop(\d+)", path)
        return int(match.group(1)) if match else float('inf')

    # Sort records by shop number
    records_sorted = sorted(records, key=extract_shop_num)

    # Write CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        for row in records_sorted:
            writer.writerow(row)

    print(f"CSV file saved as: {filename}")

if __name__ == "__main__":
    response = hot_login()
    if response and response.get("status") == 200:
        save_to_csv(response)
        print("実行結果: True")
    else:
        print("実行結果: False")