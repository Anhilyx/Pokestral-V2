import json

with open("stats/chaos-gen9ou-1825.json", "r", encoding="utf-8") as f:
    data = json.load(f)

result = {}

for pokemon, infos in data["data"].items():
    if "Moves" in infos:
        sorted_moves = dict(
            sorted(infos["Moves"].items(), key=lambda x: x[1], reverse=True)
        )
        result[pokemon] = sorted_moves

with open("stats/pokemon_moves_sorted.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print("Fichier généré : pokemon_moves_sorted.json")