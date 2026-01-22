import requests
import time
import os

FORMAT = "gen9ou"
RATING = 1300  # (optionnel)
SLEEP = 0.5  # sec entre requêtes
MAX_REPLAYS = 3000  # ← nombre de matchs voulus


BASE_SEARCH = "https://replay.pokemonshowdown.com/search.json"
BASE_REPLAY = "https://replay.pokemonshowdown.com"

output_dir = "replays"
os.makedirs(output_dir, exist_ok=True)

def get_replays_page(page):
    params = {
        "format": FORMAT,
        "rating": RATING,
        "page": page
    }
    r = requests.get(BASE_SEARCH, params=params)
    r.raise_for_status()
    return r.json()

def save_replay(replay_id):
    url = f"{BASE_REPLAY}/{replay_id}.json"
    r = requests.get(url)
    if r.status_code == 200:
        with open(f"{output_dir}/{replay_id}.json", "w", encoding="utf-8") as f:
            f.write(r.text)
        return True
    return False

def main():
    page = 1
    total = 0

    while total < MAX_REPLAYS:
        print(f"📄 Page {page}...")
        data = get_replays_page(page)
        if not data:
            print("👉 Fin des résultats.")
            break

        for item in data:
            if total >= MAX_REPLAYS:
                break

            replay_id = item["id"]
            if save_replay(replay_id):
                total += 1
                print(f"✔ {replay_id} ({total}/{MAX_REPLAYS})")

            time.sleep(SLEEP)

        page += 1
        time.sleep(SLEEP)

    print(f"\n🎉 Total replays téléchargés: {total}")

if __name__ == "__main__":
    main()
