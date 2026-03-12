import os
import json

REPLAYS_DIR = "replays/secondwave"
KEYWORD = "reflect"

def search_keyword_in_replays(directory, keyword):
    keyword = keyword.lower()
    matches = []

    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(directory, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            log = data.get("log", "").lower()

            if keyword in log:
                matches.append(filename)

        except Exception as e:
            print(f"Erreur avec {filename}: {e}")

    return matches


if __name__ == "__main__":
    results = search_keyword_in_replays(REPLAYS_DIR, KEYWORD)

    print(f"\nFichiers contenant '{KEYWORD}':")
    for r in results:
        print("-", r)

    print(f"\nTotal: {len(results)} fichiers")
