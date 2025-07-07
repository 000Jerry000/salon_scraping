import os
import csv

def convert_board_data():

    data_dir = '../downloads'
    output_dir = '../data'
    output_filename = 'board_data.csv'

    # 🧾 Step 2: Find the only CSV file in board_file
    csv_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.csv')]

    if len(csv_files) != 1:
        print("⚠️ board_file フォルダ内に CSV ファイルが 1 つだけ存在する必要があります。")
    else:
        input_path = os.path.join(data_dir, csv_files[0])
        output_path = os.path.join(output_dir, output_filename)

        # Read Shift-JIS CSV
        with open(input_path, encoding='shift_jis', errors='ignore') as f:
            reader = csv.reader(f)
            data = list(reader)

        # Write as UTF-8-sig
        with open(output_path, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        print(f"✅ {csv_files[0]} を UTF-8 に変換し、{output_filename} として保存しました。")
