import csv

def read_csv(filepath):
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        return [row for row in csv.reader(f) if len(row) >= 2]

def compare_rows(a_file, b_file, output_file='../data/outfile.csv'):
    a_data = read_csv(a_file)
    b_data = read_csv(b_file)

    different_rows = []

    for a_row in a_data:
        a_1st = a_row[0].strip()
        a_2nd = a_row[1].strip()

        match_found = False
        mismatch_found = False

        for b_row in b_data:
            if len(b_row) < 5:
                continue
            b_3rd = b_row[3].strip().replace('　','')
            b_5th = f"{b_row[6].strip()}{b_row[7].strip()}{b_row[8].strip()}"

            if a_1st == b_3rd:
                if a_2nd == b_5th:
                    match_found = True
                    break
                else:
                    mismatch_found = True
            else:
                mismatch_found = True


        # If no match found but mismatch exists, treat as different
        if mismatch_found and not match_found:
            different_rows.append(a_row)

    # Output result
    if different_rows:
        with open(output_file, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(different_rows)
        print(f"✅ 差分 {len(different_rows)} 件を出力しました: {output_file}")
    else:
        print("✅ すべての行が一致しています。")
