import csv
import re
from datetime import datetime
from kanjiconv import KanjiConv

# UniDic for accurate reading, and full-width space separator
kanji_conv = KanjiConv(separator="　", use_unidic=True)

def clear_diff():
    # Load staff name to ID mapping
    staff_map = {}
    with open('../data/staff_list.csv', encoding='utf-8') as staff_file:
        reader = csv.DictReader(staff_file)
        for row in reader:
            name = row['name'].replace('　', '').replace(' ', '')
            staff_map[name] = row['value']

    # Open input/output CSVs
    with open('../data/outfile.csv', encoding='utf-8') as infile, \
         open('../data/clear_diff.csv', 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read & write header
        header = next(reader)
        new_header = [
            'staff_id', 'date', 'start_hour', 'start_minute',
            'total_hour', 'total_minute',
            'surname', 'givenname'
        ] + header[3:]
        writer.writerow(new_header)

        for row in reader:
            # Staff name → staff_id
            staff_name = row[0].replace('　', '').replace(' ', '')
            staff_id = staff_map.get(staff_name, staff_name)

            # Parse datetime
            dt = row[1]
            date = dt[:8]
            start_hour = dt[8:10]
            start_minute = dt[10:12]

            # Calculate duration
            start_time = datetime.strptime(dt[8:12], "%H%M")
            end_time = datetime.strptime(dt[12:16], "%H%M")
            diff = end_time - start_time
            total_minutes = diff.seconds // 60
            hours = total_minutes // 60
            minutes = total_minutes % 60

            # Zero-padded
            total_hour = hours * 60
            total_minute = f"{minutes:02}"

            # Convert name to katakana
            client_name = row[2]
            katakana_full = kanji_conv.to_katakana(client_name)
            katakana_full = re.sub(r"キゴウ　*", "", katakana_full)  # remove '記号'

            # Split into surname + given name
            parts = katakana_full.split("　")
            surname = parts[0] if len(parts) > 0 else ""
            givenname = "".join(parts[1:]) if len(parts) > 1 else ""

            # Final output
            new_row = [
                staff_id, date, start_hour, start_minute,
                total_hour, total_minute,
                surname, givenname
            ] + row[3:]
            writer.writerow(new_row)

    print("✅ clear_diff.csv written with formatted durations and katakana names.")
