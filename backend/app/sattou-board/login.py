# ============================================================================================================================
# ||                                                    Login to Sattou                                                     ||
# ============================================================================================================================


async def login(page, human_wait):

    userId = "hpbtest"
    password = "sattouhpb"

    # Step 1: Go to the login page
    await page.goto("https://sv1.sattou.net/filament/")

    # ユーザーID欄にフォーカスし、人間っぽく入力
    await page.focus('input[name="login_id"]')
    await human_wait()
    await page.fill('input[name="login_id"]', '')
    await human_wait()
    await page.type('input[name="login_id"]', userId, delay=120)

    # パスワード欄にフォーカスし、クリアしてゆっくり入力
    await page.focus('input[name="pw"]')
    await human_wait()
    await page.fill('input[name="pw"]', '')
    await human_wait()
    await page.type('input[name="pw"]', password, delay=130)

    # 少し間を置いてログインボタンクリック
    await human_wait(500, 300)
    await page.click('input[type="submit"]')

    # ログイン後に人間らしい確認待機
    await human_wait(2000, 1000)
    print("---------------------------------- ✅ Login to sattou Successfully ---------------------------------")

