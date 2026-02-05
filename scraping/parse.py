import json
import os
from collections import Counter

replays_folder = "replays/gen9ou"
output_folder = "stats"
os.makedirs(output_folder, exist_ok=True)

pokemon_counter = Counter()

for filename in os.listdir(replays_folder):
    if filename.endswith(".json"):
        filepath = os.path.join(replays_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

            log_lines = data.get("log", "").split("\n")
            replay_pokemon = []

            # Pour chaque joueur
            for player_index in [1, 2]:
                player_pokemon = []
                for line in log_lines:
                    if line.startswith(f"|poke|p{player_index}|"):
                        parts = line.split("|")
                        if len(parts) >= 4:
                            poke_name = parts[3].split(",")[0].strip()
                            player_pokemon.append(poke_name)
                replay_pokemon.extend(player_pokemon)  # on ajoute tous les Pokémon du joueur

            # On incrémente le compteur global avec tous les Pokémon de ce replay
            pokemon_counter.update(replay_pokemon)

# Sauvegarde dans un JSON
output_path = os.path.join(output_folder, "pokemon_counts.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(pokemon_counter, f, indent=4, ensure_ascii=False)

print("Analyse terminée !")