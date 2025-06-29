# ============================================================================================================================
# ||                                                  Login in Salonboard                                                   ||
# ============================================================================================================================


async def login(page, human_wait):

    userId = "CD53764"
    password = "@filament09-1"

    # Step 1: Go to the login page
    await page.goto("https://salonboard.com/login/")

    # ユーザーID欄にフォーカスし、人間っぽく入力
    await page.focus('input[name="userId"]')
    await human_wait()
    await page.fill('input[name="userId"]', '')
    await human_wait()
    await page.type('input[name="userId"]', userId, delay=120)

    # パスワード欄にフォーカスし、クリアしてゆっくり入力
    await page.focus('input[name="password"]')
    await human_wait()
    await page.fill('input[name="password"]', '')
    await human_wait()
    await page.type('input[name="password"]', password, delay=130)

    # 少し間を置いてログインボタンクリック
    await human_wait(500, 300)
    await page.click('a.common-CNCcommon__primaryBtn.loginBtnSize')

    # ログイン後に人間らしい確認待機
    await human_wait(2000, 1000)
    print("---------------------------------- ✅ Login Successfully ---------------------------------")

