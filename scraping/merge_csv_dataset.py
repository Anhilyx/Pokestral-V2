import csv
import os

INPUT_DIR = "stats/csv_debug"
OUTPUT_CSV = "stats/complete_dataset.csv"

csv_files = sorted(
    f for f in os.listdir(INPUT_DIR)
    if f.endswith(".csv")
)

print(f"CSV trouvés : {len(csv_files)}")

match_id = 1
total_rows = 0
header_written = False

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as out_f:
    writer = None

    for filename in csv_files:
        path = os.path.join(INPUT_DIR, filename)

        with open(path, "r", encoding="utf-8") as in_f:
            reader = csv.reader(in_f)
            header = next(reader)

            # ➜ Ajouter match_id + source_file au header
            if not header_written:
                writer = csv.writer(out_f)
                writer.writerow(["match_id", "source_file"] + header)
                header_written = True

            row_count = 0

            for row in reader:
                writer.writerow([match_id, filename] + row)
                row_count += 1

            if row_count > 0:
                total_rows += row_count
                print(f"✔ {filename} → {row_count} lignes")
                match_id += 1
            else:
                print(f"✘ {filename} → CSV vide ignoré")

print("\n===== DATASET FINAL =====")
print(f"Matches fusionnés : {match_id - 1}")
print(f"Lignes totales    : {total_rows}")
print(f"CSV final         : {OUTPUT_CSV}")