import csv

def read_csv(filepath):
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        return [row for row in reader if len(row) >= 4]

def compare_and_export_diff(sattou_file, board_file, output_file):
    sattou_data = read_csv(sattou_file)
    board_data = read_csv(board_file)

    max_len = max(len(sattou_data), len(board_data))
    differences = []

    print("📊 差分比較を開始します...")

    for i in range(max_len):
        row1 = sattou_data[i] if i < len(sattou_data) else [''] * 4
        row2 = board_data[i] if i < len(board_data) else [''] * 9

        val1_1st = row1[0].strip()
        val1_2nd = row1[1].strip()

        val2_4th = row2[3].strip().replace('　', '')
        val2_7th = f"{row2[6].strip()}{row2[7].strip()}{row2[8].strip()}"

        if val1_1st != val2_4th or val1_2nd != val2_7th:
            print(f"\n❌ 差分あり (Row {i+1}):")
            print(f"  sattou.csv → 1st: {val1_1st}, 2nd: {val1_2nd}")
            print(f"  board.csv → 4th: {val2_4th}, 7th: {val2_7th}")
            differences.append(row1)  # Save the mismatched row from sattou

    # Export mismatched rows to new CSV
    if differences:
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(differences)
        print(f"\n✅ 差分データを保存しました: {output_file}")
    else:
        print("\n✅ 差分はありませんでした。")

# Run comparison
compare_and_export_diff(
    'sattou_schedule.csv',
    './output.csv',
    'sattou_diff_output.csv'
)
