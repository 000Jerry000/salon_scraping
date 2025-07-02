import csv

with open('../../board_data.csv', encoding='shift_jis', errors='ignore') as f:
    reader = csv.reader(f)
    data = list(reader)

with open('output.csv', mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("✅ 正常に読み書きしました")
