import json
import os

json_folder = "stats/indent"
output_folder = "stats/indent"
for filename in os.listdir(json_folder):
    os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(json_folder):
    if not filename.endswith(".json"):
        continue

    input_path = os.path.join(json_folder, filename)
    output_path = os.path.join(output_folder, filename)

    with open(input_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Erreur de lecture {filename}: {e}")
            continue

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"{filename} reformatté")
