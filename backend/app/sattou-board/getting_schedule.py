# 最大10秒（10000ミリ秒）待機して、要素が表示されるまで待つ

async def getting_schedule(page, human_wait):
    # その後にクリックなどの処理を続けられる
    print("✅ ログインを通過しました。")

    await page.wait_for_load_state('networkidle')

    # try:
    #     await page.wait_for_selector('li.nav1 a', timeout=10000)
    #     await page.hover('li.nav1 a')   # マウスを乗せる（自然な動き）
    #     await page.wait_for_timeout(500)    # 少し待機
    #     await page.click('li.nav1 a')
    # except Exception as e:
    #     print("❌ li.nav1 a が見つかりません:", e)

    # まず fromdate と todate は str にしておく（.type() や evaluate 用）
    await page.wait_for_timeout(500)    # 少し待機
    await page.click('#datepicker')   # クリック
# ------------------------------------------------------
    # Wait for all booking elements to appear
    await page.wait_for_selector('div.sc_bar.typeA')

    # Select all booking blocks
    booking_elements = await page.query_selector_all('div.sc_bar.typeA')
    print("booking", booking_elements)
    results = []

    for booking in booking_elements:
        # Get time (e.g., 11:00-12:00)
        time_el = await booking.query_selector('.time')
        time = await time_el.inner_text() if time_el else ''

        # Get text block and parse it
        text_el = await booking.query_selector('.text')
        full_text = await text_el.inner_text() if text_el else ''
        parts = full_text.split('／')
        
        name = parts[0].strip() if len(parts) > 0 else ''
        note = parts[1].strip() if len(parts) > 1 else ''
        place = parts[2].strip() if len(parts) > 2 else ''

        # Get booking ID
        book_id = await booking.get_attribute('data-book_id')

        # Save one booking's data
        results.append({
            'time': time,
            'name': name,
            'note': note,
            'place': place,
            'book_id': book_id
        })

    # ✅ Output all results
    for i, r in enumerate(results, 1):
        print(f"[{i}] 時間: {r['time']} | 名前: {r['name']} | メモ: {r['note']} | 場所: {r['place']} | 予約ID: {r['book_id']}")
