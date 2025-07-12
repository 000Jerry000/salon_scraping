import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()

def get_csrf_token_and_cookies(api_url, brand_dir):
    """
    Mimics getCsrfTokenAndCookies() in PHP.
    - performs a GET to /login
    - extracts CSRF token and cookies
    """

    url = f"{api_url}{brand_dir}/login"
    session = requests.Session()
    resp = session.get(url)

    # Extract cookies as single header string
    cookies_str = "; ".join(
        [f"{k}={v}" for k, v in session.cookies.items()]
    )

    # Extract CSRF token from HTML response
    csrf_token = ""
    match = re.search(r'name="csrf_test_name"\s+value="(.*?)"', resp.text)
    if match:
        csrf_token = match.group(1)

    return {
        "csrf_token": csrf_token,
        "cookies": cookies_str,
        "session": session,
    }


def auth_token(api_url, brand_dir, username, password):
    """
    Mimics authToken() in PHP.
    """
    # Step 1 - get CSRF token + cookies
    candt = get_csrf_token_and_cookies(api_url, brand_dir)
    csrf_token = candt["csrf_token"]
    cookie_header = candt["cookies"]
    session = candt["session"]

    # Prepare POST data
    params = {
        "username": username,
        "password": password,
        "csrf_token": csrf_token
    }

    # The URL for authToken API
    url = f"{api_url}{brand_dir}/api/v1/authToken"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRF-TOKEN": csrf_token,
        "Cookie": cookie_header,
    }

    try:
        resp = session.post(url, headers=headers, data=params)
        resp.raise_for_status()
        data = resp.json()

        # print("Array変換結果")
        # print(data)

        if data.get("status") == 200:
            csrf_token = data["data"].get("csrf_token")
            token = data["data"].get("token")
            print("csrf_token - ", csrf_token)
            print("token - ", token)
            print("-" * 30)
            return token, session
        else:
            return None
    except requests.RequestException as e:
        print(f"エラーが発生しました: {e}")
        return None

def token_generation():

    # These would come from your config in PHP
    API_URL = os.getenv("API_URL")
    BRAND_DIR = os.getenv("BRAND_DIR")
    USER_NAME = os.getenv("USER_NAME")
    PASSWORD = os.getenv("PASSWORD")

    token, session = auth_token(API_URL, BRAND_DIR, USER_NAME, PASSWORD)

    # print("実行結果")
    # print(token)
    return token, session

if __name__ == "__main__":
    token_generation()