import csv
from bs4 import BeautifulSoup

def parse_schedule(html_code, output_csv):
    """
    Parses an HTML schedule file to extract booking information and saves it to a CSV file.

    Args:
        html_code (str): The HTML string of the schedule.
        output_csv (str): The path to the output CSV file.
    """
    soup = BeautifulSoup(html_code, 'html.parser')

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
            # datetime_str = f"{booking_date} {time_span.get_text(strip=True)}" if time_span else "N/A"
            if time_span:
                raw_time = time_span.get_text(strip=True)  # e.g., "13:00-14:00"
                start_time, end_time = raw_time.split('-')  # Split into "13:00" and "14:00"
                datetime_str = f"{booking_date}{start_time}{end_time}" \
                    .replace('-', '') \
                    .replace(':', '') \
                    .replace(' ', '')
            else:
                datetime_str = "N/A"
            
            text_span = bar.select_one('.text')
            full_text = ""
            if text_span:
                # Use a separator to handle <br> tags gracefully
                full_text = text_span.get_text(separator=' ', strip=True)

            parts = full_text.split('／')
            client_name = parts[0].strip() if parts else "N/A"
            note = parts[1].strip() if len(parts) > 1 else ''
            place = parts[2].strip() if len(parts) > 2 else ''

            schedule_data.append({
                'name': staff_name,
                'datetime': datetime_str,
                'client_name': client_name,
                'note': note,
                # 'place': place,  
                # 'book_id': book_id
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

    await page.wait_for_timeout(500)    # 少し待機
    # ------------------------------------------------------
    html_element = await page.query_selector('div.sc_wrapper')
    html_code = await html_element.inner_html()
    csv_file = "sattou_schedule.csv"
    parse_schedule(html_code, csv_file)

    print(f"✅ データをCSVに保存しました: {csv_file}")