# 最大10秒（10000ミリ秒）待機して、要素が表示されるまで待つ

async def getting_schedule(page, human_wait):
    await page.wait_for_selector('#todayReserve', timeout=100000)

    # その後にクリックなどの処理を続けられる
    print("✅ ログインを通過しました。")
    # ログイン済みのページオブジェクトを再利用してアクセス
    # await page.goto("https://salonboard.com/KLP/reserve/reserveList/searchDate?date=20250628")

    await human_wait()
    # 要素が表示されるまで待機（念のため）
    await page.wait_for_selector('#todayReserve')

    # 人間らしく、少し待ってからクリック
    await page.hover('#todayReserve')   # マウスを乗せる（自然な動き）
    await page.wait_for_timeout(500)    # 少し待機
    await page.click('#todayReserve')   # クリック

    # まず fromdate と todate は str にしておく（.type() や evaluate 用）
    fromdate = "20250630"
    todate = "20250730"

    # hidden input が DOM に現れるまで待つ
    await page.wait_for_timeout(500)    # 少し待機
    await human_wait()
    await page.evaluate(f"""() => {{
        document.querySelector('#rsvDateFrom').value = '{fromdate}';
    }}""")

    await human_wait()
    await page.evaluate(f"""() => {{
        document.querySelector('#rsvDateTo').value = '{todate}';
    }}""")
    await human_wait(2000, 1000)
    await page.wait_for_timeout(500)
    await page.click('#search')
    await page.wait_for_timeout(1500)
    await page.click('#csvOutput')
    print("✅ Schedule page opened")
