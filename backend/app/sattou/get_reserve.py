import csv
import urllib.parse
from dotenv import load_dotenv
import os
from get_token import auth_token

load_dotenv()

def reserve(api_url, brand_dir, token, session):

    params = {
        'param1': 2,
        'book_id': 21,
        'url_id': 0,
        'book_shop_id': 0,
        'book_staff_id': 0,
        'book_date': 0,
        'menu2': 0,
        'customer_id': 0,
        'mail': 0,
        'tel': 0,
    }

    url = f"{api_url}{brand_dir}/api/v1/reserve?" + urllib.parse.urlencode(params)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("Arayy変換結果")
        print(data)

        return data.get("status") == 200
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False

def save_reserve_to_csv(response_data, csv_filename):
    """
    Save reservation data to CSV.
    """
    if response_data.get("status") != 200:
        print("Error: API did not return status 200.")
        return

    data = response_data.get("data", {})
    book_data = data.get("book_data", {})

    if not book_data:
        print("No booking data to save.")
        return

    # prepare CSV rows
    rows = []
    fieldnames = set()

    for book_id, booking in book_data.items():
        # base columns
        row = {
            "book_id": booking.get("book_id"),
            "shop_id": booking.get("shop_id"),
            "staff_id": booking.get("staff_id"),
            "date": booking.get("date"),
            "start_time": booking.get("start_time"),
            "end_time": booking.get("end_time"),
            "customer_id": booking.get("customer_id"),
            "user_name1": booking.get("user_name1"),
            "user_name2": booking.get("user_name2"),
            "customer_phone": booking.get("customer_phone"),
            "user_email": booking.get("user_email"),
            "status": booking.get("status"),
        }

        # include form_data as separate columns
        form_data = booking.get("form_data", [])
        for item in form_data:
            key = item.get("form_name")
            value = item.get("value1")
            if key:
                row[key] = value
                fieldnames.add(key)

        rows.append(row)

    # add base columns to fieldnames
    base_fields = [
        "book_id", "shop_id", "staff_id", "date", 
        "start_time", "end_time", "customer_id",
        "user_name1", "user_name2", "customer_phone", 
        "user_email", "status"
    ]
    fieldnames = base_fields + sorted(fieldnames)

    # write to CSV
    with open(csv_filename, mode="w", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print("-" * 30)
    print(f"Saved {len(rows)} rows to {csv_filename}")

if __name__ == "__main__":
    API_URL = os.getenv("API_URL")
    BRAND_DIR = os.getenv("BRAND_DIR")
    USER_NAME = os.getenv("USER_NAME")
    PASSWORD = os.getenv("PASSWORD")

    token, session = auth_token(API_URL, BRAND_DIR, USER_NAME, PASSWORD)

    shop_id = 2

    params = {
        'param1': 2,
        'book_id': 0,
        # 'book_id': 66087,
        'url_id': 0,
        'book_shop_id': shop_id,
        'book_staff_id': 0,
        'book_date': 0,
        'menu2': 0,
        'customer_id': 0,
        'mail': 0,
        'tel': 0,
    }

    url = f"{API_URL}{BRAND_DIR}/api/v1/reserve?" + urllib.parse.urlencode(params)
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = session.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    save_reserve_to_csv(data, f"../sattou-data/reserve_data_{shop_id}.csv")