from bs4 import BeautifulSoup
import csv

# 最大10秒（10000ミリ秒）待機して、要素が表示されるまで待つ

async def getting_schedule(page, human_wait):
    await page.wait_for_selector('#todayReserve', timeout=100000)

    # その後にクリックなどの処理を続けられる
    print("✅ ログインを通過しました。")

    await human_wait()
    # 要素が表示されるまで待機（念のため）
    await page.wait_for_selector('#todayReserve')

    # 人間らしく、少し待ってからクリック
    await page.hover('#todayReserve')   # マウスを乗せる（自然な動き）
    await page.wait_for_timeout(500)    # 少し待機
    await page.click('#todayReserve')   # クリック

    # Wait for the page to update (choose a selector that appears after the click)
    await page.wait_for_selector('select#stylistId')  # or another unique selector

    # Get the HTML of the whole page
    html = await page.content()

    soup = BeautifulSoup(html, 'html.parser')
    options = soup.select('select#stylistId option')

    staff_list = []
    for option in options:
        value = option.get('value').strip()
        name = option.get_text(strip=True)
        if value:  # skip "すべてのスタッフ"
            staff_list.append([value, name])

    # Write to CSV
    with open('staff_list.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['value', 'name'])  # header
        writer.writerows(staff_list)

    print("✅ staff_list.csv has been created.")

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
