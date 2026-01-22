import os
import json
from collections import defaultdict
import csv

# --- CONFIG ---
REPLAYS_DIR = "replays/gen9ou"  # dossier contenant les JSON
OUTPUT_DIR = "stats_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- STRUCTURES DE DONNEES ---
stats = {
    "games_played": defaultdict(int),
    "wins": defaultdict(int),
    "vs": defaultdict(lambda: defaultdict(lambda: [0, 0])),   # wins / games
    "with": defaultdict(lambda: defaultdict(lambda: [0, 0])),
    "moves": defaultdict(lambda: defaultdict(lambda: [0, 0])),
    "tera_used": defaultdict(lambda: [0, 0]),  # used / present
    "status": defaultdict(lambda: [0, 0])      # affected / present
}

# --- FONCTION DE PARSING D'UN REPLAY ---
def process_replay(data):
    log = data["log"].split("\n")

    teams = {"p1": set(), "p2": set()}
    moves_used = defaultdict(set)
    tera = set()
    status = set()
    winner = None

    for line in log:
        if line.startswith("|player|"):
            _, side, name, *_ = line.split("|")

        elif line.startswith("|poke|"):
            _, side, poke = line.split("|")[1:4]
            poke = poke.split(",")[0]
            teams[side].add(poke)

        elif line.startswith("|move|"):
            parts = line.split("|")
            if len(parts) < 4:
                continue
            pokemon = parts[2].split(": ")[-1]
            move = parts[3]
            moves_used[pokemon].add(move)

        elif line.startswith("|-terastallize|"):
            pokemon = line.split("|")[2].split(": ")[-1]
            tera.add(pokemon)

        elif line.startswith("|-status|"):
            pokemon = line.split("|")[2].split(": ")[-1]
            status.add(pokemon)

        elif line.startswith("|win|"):
            winner = line.split("|")[2]

    return teams, winner, moves_used, tera, status

# --- FONCTION POUR METTRE A JOUR LES STATS ---
def update_stats(teams, winner, moves_used, tera, status):
    sides = ["p1", "p2"]
    # Chaque Pokémon joue
    for side in sides:
        for poke in teams[side]:
            stats["games_played"][poke] += 1
            if poke in winner_team(teams, winner):
                stats["wins"][poke] += 1
            # Tera
            stats["tera_used"][poke][1] += 1
            if poke in tera:
                stats["tera_used"][poke][0] += 1
            # Status
            stats["status"][poke][1] += 1
            if poke in status:
                stats["status"][poke][0] += 1
            # Moves
            for move in moves_used.get(poke, []):
                stats["moves"][poke][move][1] += 1
                if poke in winner_team(teams, winner):
                    stats["moves"][poke][move][0] += 1
        # Winrate vs chaque Pokémon adverse
        opp = "p2" if side == "p1" else "p1"
        for poke in teams[side]:
            for opp_poke in teams[opp]:
                stats["vs"][poke][opp_poke][1] += 1
                if poke in winner_team(teams, winner):
                    stats["vs"][poke][opp_poke][0] += 1
        # Winrate avec coéquipier
        for poke in teams[side]:
            for teammate in teams[side]:
                if poke != teammate:
                    stats["with"][poke][teammate][1] += 1
                    if poke in winner_team(teams, winner):
                        stats["with"][poke][teammate][0] += 1

# --- AIDE : renvoie l'équipe gagnante ---
def winner_team(teams, winner_name):
    for side, pokes in teams.items():
        if winner_name in [winner_name, ""]:
            if winner_name in teams[side] or winner_name == "":
                return teams[side]
    # fallback
    for side, pokes in teams.items():
        if winner_name in teams[side]:
            return teams[side]
    # si nom non reconnu, prend p1
    return teams["p1"]

# --- PARSING DE TOUS LES REPLAYS ---
files = [f for f in os.listdir(REPLAYS_DIR) if f.endswith(".json")]
for i, filename in enumerate(files, 1):
    with open(os.path.join(REPLAYS_DIR, filename), encoding="utf-8") as f:
        data = json.load(f)
    teams, winner, moves_used, tera, status = process_replay(data)
    update_stats(teams, winner, moves_used, tera, status)
    if i % 100 == 0:
        print(f"✅ {i}/{len(files)} replays traités")

print("🎉 Parsing terminé")

# --- FONCTION POUR EXPORTER EN CSV ---
def export_csv(d, filename):
    with open(os.path.join(OUTPUT_DIR, filename), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for key, val in d.items():
            if isinstance(val, dict) or isinstance(val, defaultdict):
                for subkey, subval in val.items():
                    if isinstance(subval, list):
                        writer.writerow([key, subkey] + subval)
                    else:
                        writer.writerow([key, subkey, subval])
            elif isinstance(val, list):
                writer.writerow([key] + val)
            else:
                writer.writerow([key, val])

# --- EXPORT DES STATISTIQUES ---
export_csv(stats["games_played"], "games_played.csv")
export_csv(stats["wins"], "wins.csv")
export_csv(stats["vs"], "vs.csv")
export_csv(stats["with"], "with.csv")
export_csv(stats["moves"], "moves.csv")
export_csv(stats["tera_used"], "tera_used.csv")
export_csv(stats["status"], "status.csv")

print(f"✅ Toutes les stats exportées dans {OUTPUT_DIR}")
