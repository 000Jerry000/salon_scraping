import csv
from bs4 import BeautifulSoup

def parse_schedule(html_file, output_csv):
    """
    Parses an HTML schedule file to extract booking information and saves it to a CSV file.

    Args:
        html_file (str): The path to the input HTML file.
        output_csv (str): The path to the output CSV file.
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    staff_elements = soup.select('.sc_data_scroll .timeline-title')
    timeline_elements = soup.select('.sc_main > .timeline')

    schedule_data = []

    for staff_el, timeline_el in zip(staff_elements, timeline_elements):
        # Extract staff name and booking date
        staff_name = staff_el.get_text(strip=True).split('[')[0].strip()
        booking_date = staff_el.get('data-book', '')

        # Find all booking/event bars for the staff member
        booking_bars = timeline_el.select('.sc_bar')

        for bar in booking_bars:
            book_id = bar.get('data-book_id', 'N/A')
            
            # Skip if it's not a client booking (like breaks or other events)
            if book_id == "0":
                continue

            time_span = bar.select_one('.time')
            datetime_str = f"{booking_date} {time_span.get_text(strip=True)}" if time_span else "N/A"
            
            text_span = bar.select_one('.text')
            full_text = ""
            if text_span:
                # Use a separator to handle <br> tags gracefully
                full_text = text_span.get_text(separator=' ', strip=True)

            parts = full_text.split('／')
            client_name = parts[0].strip() if parts else "N/A"
            note = ' '.join(p.strip() for p in parts[1:]) if len(parts) > 1 else ""
            
            schedule_data.append({
                'name': staff_name,
                'datetime': datetime_str,
                'client_name': client_name,
                'note': note,
                'place': '',  # 'place' is not available in the HTML
                'book_id': book_id
            })

    # Write data to CSV
    if schedule_data:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'datetime', 'client_name', 'note', 'place', 'book_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(schedule_data)
        print(f"✅ Successfully parsed the schedule and saved it to '{output_csv}'")
    else:
        print("Could not find any schedule data to parse.")

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
    html_code = await page.query_selector('div.sc_wrapper')
    csv_file = "booking_csv.csv"
    parse_schedule(html_code, csv_file)
    # # Wait for all booking elements to appear
    # await page.wait_for_selector('div.sc_bar.typeA')

    # # Select all booking blocks
    # booking_elements = await page.query_selector_all('div.sc_bar.typeA')
    # print("booking", booking_elements)
    # results = []

    # for booking in booking_elements:
    #     # Get time (e.g., 11:00-12:00)
    #     time_el = await booking.query_selector('.time')
    #     time = await time_el.inner_text() if time_el else ''

    #     # Get text block and parse it
    #     text_el = await booking.query_selector('.text')
    #     full_text = await text_el.inner_text() if text_el else ''
    #     parts = full_text.split('／')
        
    #     client_name = parts[0].strip() if len(parts) > 0 else ''
    #     note = parts[1].strip() if len(parts) > 1 else ''
    #     place = parts[2].strip() if len(parts) > 2 else ''

    #     # Get booking ID
    #     book_id = await booking.get_attribute('data-book_id')

    #     # Save one booking's data
    #     results.append({
    #         'time': time,
    #         'name': client_name,
    #         'note': note,
    #         'place': place,
    #         'book_id': book_id
    #     })

    # # ✅ Output all results
    # # for i, r in enumerate(results, 1):
    # #     print(f"[{i}] 時間: {r['time']} | 名前: {r['name']} | メモ: {r['note']} | 場所: {r['place']} | 予約ID: {r['book_id']}")
    # # Save results to CSV
    # output_file = 'booking_schedule.csv'
    # with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.DictWriter(file, fieldnames=['time', 'client_name', 'note', 'place', 'book_id'])
    #     writer.writeheader()
    #     writer.writerows(results)

    print(f"✅ データをCSVに保存しました: {csv_file}")