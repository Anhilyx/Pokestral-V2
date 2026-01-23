import json
import os

replays_folder = "replays/gen9ou"  # Dossier contenant tes fichiers replay
pokemon_name = "Great Tusk"

files_with_pokemon = 0
files_in_both_teams = 0

for filename in os.listdir(replays_folder):
    if filename.endswith(".json"):
        filepath = os.path.join(replays_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            log_lines = data.get("log", "").split("\n")

            # Vérifier si le Pokémon apparaît dans p1 et p2
            in_p1 = any(
                line.startswith("|poke|p1|") and line.split("|")[3].split(",")[0].strip() == pokemon_name for line in
                log_lines)
            in_p2 = any(
                line.startswith("|poke|p2|") and line.split("|")[3].split(",")[0].strip() == pokemon_name for line in
                log_lines)

            if in_p1 or in_p2:
                files_with_pokemon += 1
                print(f"{pokemon_name} trouvé dans : {filename}")

            if in_p1 and in_p2:
                files_in_both_teams += 1
                print(f"{pokemon_name} présent dans les DEUX équipes dans : {filename}")

print(f"\n{pokemon_name} apparaît dans {files_with_pokemon} fichier(s).")
print(f"{pokemon_name} apparaît dans les deux équipes dans {files_in_both_teams} fichier(s).")
