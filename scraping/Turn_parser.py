import json
import csv
import os
from copy import deepcopy

SLOTS = ["A", "B", "C", "D", "E", "F"]
STATS = ["atk", "def", "spa", "spd", "spe", "accuracy", "evasion"]
HAZARDS = { "Stealth Rock", "Spikes", "Sticky Web", "Toxic Spikes"}
SCREENS = {"Reflect", "Light Screen", "Aurora Veil", "Safeguard", "Mist"}


def empty_pokemon():
    return {
        "name": None,
        "hp": 100,
        "status": "none",
        "alive": True,
        "boosts": {stat: 0 for stat in STATS},
        "moves": set()
    }

def normalize_name(raw_name):
    if raw_name is None:
        return None
    name = raw_name.split("|")[0]
    name = name.split(",")[0]
    name = name.replace("*", "").strip()
    return name

def init_state():
    return {
        "teams": {
            "p1": {slot: empty_pokemon() for slot in SLOTS},
            "p2": {slot: empty_pokemon() for slot in SLOTS}
        },
        "active": {
            "p1": None,
            "p2": None
        },
        "terrain": "none",
        "weather": "none",
        "trick_room": 0,
        "tailwind": {
            "p1": 0,
            "p2": 0
        },
        "hazards": {
            "p1": set(),
            "p2": set()
        },
        "screens": {
            "p1": set(),
            "p2": set()
        },
        "last_faint": None,
        "pending_choice_p1": "none"
    }

def parse_hp(hp_str):
    if "fnt" in hp_str:
        return 0
    return int(hp_str.split("/")[0])

def clamp_boost(value):
    return max(-6, min(6, value))

def parse_replay(json_data, output_csv):
    log_lines = json_data["log"].split("\n")

    state = init_state()
    snapshots = []

    slot_index = {"p1": 0, "p2": 0}
    name_to_slot = {"p1": {}, "p2": {}}

    current_turn = 0

    for line in log_lines:

        # ───── Team preview ─────
        if line.startswith("|poke|"):
            _, _, player, poke_raw = line.split("|", 3)
            poke_name = normalize_name(poke_raw)

            slot = SLOTS[slot_index[player]]
            slot_index[player] += 1

            state["teams"][player][slot]["name"] = poke_name
            name_to_slot[player][poke_name] = slot

        # ───── Turn marker ─────
        elif line.startswith("|turn|"):
            if current_turn > 0:
                snapshots.append(deepcopy(state))

            current_turn = int(line.split("|")[2])
            state["pending_choice_p1"] = "none"

        # ───── Switch ─────
        elif line.startswith("|switch|"):
            parts = line.split("|")
            position = parts[2]
            player = position[:2]

            poke_raw = parts[3]
            true_name = normalize_name(poke_raw)

            if true_name not in name_to_slot[player]:
                continue
            else:
                slot = name_to_slot[player][true_name]

            if player == "p1" and state["pending_choice_p1"] == "none":
                state["pending_choice_p1"] = f"switch:{slot}"

            state["active"][player] = slot

            hp = parse_hp(parts[4])
            state["teams"][player][slot]["hp"] = hp

            state["teams"][player][slot]["boosts"] = {stat: 0 for stat in STATS}

        # ───── Move used ─────
        elif line.startswith("|move|"):
            parts = line.split("|")
            position = parts[2].split(":")[0]
            player = position[:2]

            slot = state["active"][player]
            if slot is None:
                continue

            move_name = parts[3].strip()

            if move_name.lower() == "struggle":
                continue

            if player == "p1" and state["pending_choice_p1"] == "none":
                state["pending_choice_p1"] = f"move:{move_name}"

            moves = state["teams"][player][slot]["moves"]
            if len(moves) < 4:
                moves.add(move_name)

        # ───── Damage / Heal ─────
        elif line.startswith("|-damage|") or line.startswith("|-heal|"):
            parts = line.split("|")
            position = parts[2].split(":")[0]
            player = position[:2]

            slot = state["active"][player]
            if slot is None:
                continue

            hp = parse_hp(parts[3])
            state["teams"][player][slot]["hp"] = hp
            if hp == 0:
                state["teams"][player][slot]["alive"] = False

        # ───── Status ─────
        elif line.startswith("|-status|"):
            parts = line.split("|")
            position = parts[2].split(":")[0]
            player = position[:2]

            slot = state["active"][player]
            if slot is None:
                continue

            state["teams"][player][slot]["status"] = parts[3]

        # ───── Faint ─────
        elif line.startswith("|faint|"):
            parts = line.split("|")
            position = parts[2].split(":")[0]
            player = position[:2]

            slot = state["active"][player]
            if slot is None:
                continue

            mon = state["teams"][player][slot]
            mon["hp"] = 0
            mon["alive"] = False

            state["last_faint"] = player

            mon["boosts"] = {stat: 0 for stat in STATS}

        # ───── Boost ─────
        elif line.startswith("|-boost|"):
            parts = line.split("|")
            position = parts[2].split(":")[0]
            player = position[:2]

            slot = state["active"][player]
            if slot is None:
                continue

            stat = parts[3].lower()
            change = int(parts[4])

            if stat in state["teams"][player][slot]["boosts"]:
                state["teams"][player][slot]["boosts"][stat] = clamp_boost(
                    state["teams"][player][slot]["boosts"][stat] + change
                )

        # ───── Field start (Terrain / Trick Room) ─────
        elif line.startswith("|-fieldstart|"):
            parts = line.split("|")

            if "Trick Room" in line:
                state["trick_room"] = 1

            elif len(parts) > 2 and "move:" in parts[2]:
                terrain = parts[2].replace("move:", "").strip()
                state["terrain"] = terrain


        # ───── Field end (Terrain / Trick Room) ─────
        elif line.startswith("|-fieldend|"):
            if "Trick Room" in line:
                state["trick_room"] = 0
            else:
                state["terrain"] = "none"

        # ───── Weather ─────
        elif line.startswith("|-weather|"):
            parts = line.split("|")

            if len(parts) > 2:
                weather = parts[2].strip()
                state["weather"] = weather

        # ───── Side start ─────
        elif line.startswith("|-sidestart|"):
            parts = line.split("|")

            if len(parts) >= 3:
                side = parts[2]
                player = side[:2]

                raw = parts[3].strip() if len(parts) >= 4 else ""
                move = raw.replace("move:", "").strip()

                if move == "Tailwind":
                    state["tailwind"][player] = 1

                elif move in HAZARDS:
                    state["hazards"][player].add(move)

                elif move in SCREENS:
                    state["screens"][player].add(move)

        # ───── Side end ─────
        elif line.startswith("|-sideend|"):
            parts = line.split("|")

            if len(parts) >= 3:
                side = parts[2]
                player = side[:2]

                raw = parts[3].strip() if len(parts) >= 4 else ""
                condition = raw.replace("move:", "").strip()

                if condition == "Tailwind":
                    state["tailwind"][player] = 0

                elif condition in HAZARDS:
                    state["hazards"][player].discard(condition)

                elif condition in SCREENS:
                    state["screens"][player].discard(condition)

        # ───── Court change ─────
        elif line.startswith("|-swapsideconditions"):
            state["hazards"]["p1"], state["hazards"]["p2"] = (
                state["hazards"]["p2"],
                state["hazards"]["p1"],
            )

            state["tailwind"]["p1"], state["tailwind"]["p2"] = (
                state["tailwind"]["p2"],
                state["tailwind"]["p1"],
            )

            state["screens"]["p1"], state["screens"]["p2"] = (
                state["screens"]["p2"],
                state["screens"]["p1"],
            )

    if current_turn > 0:
        snapshots.append(deepcopy(state))

    # ───── Write CSV ─────
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        header = ["turn", "terrain", "weather", "trick_room", "tailwind_p1",
    "tailwind_p2", "hazards_p1", "hazards_p2", "screens_p1", "screens_p2",
    "active_p1", "active_p2", "choice_p1"]
        for p in ["p1", "p2"]:
            for s in SLOTS:
                header += [
                    f"pokemon_{p}{s}",
                    f"hp_{p}{s}",
                    f"status_{p}{s}"
                ]

            for stat in STATS:
                header.append(f"active_{p}_{stat}")

            for i in range(1, 5):
                header.append(f"active_{p}_move{i}")

        writer.writerow(header)

        for i, snap in enumerate(snapshots, start=1):
            row = [
                i, snap["terrain"], snap["weather"], snap["trick_room"],
                snap["tailwind"]["p1"], snap["tailwind"]["p2"],
                list(snap["hazards"]["p1"]), list(snap["hazards"]["p2"]),
                list(snap["screens"]["p1"]), list(snap["screens"]["p2"]),
                snap["active"]["p1"], snap["active"]["p2"], snap["pending_choice_p1"]
            ]

            for p in ["p1", "p2"]:
                for s in SLOTS:
                    mon = snap["teams"][p][s]
                    row += [mon["name"], mon["hp"], mon["status"]]

                active_slot = snap["active"][p]
                if active_slot is not None:
                    boosts = snap["teams"][p][active_slot]["boosts"]
                    row += [boosts[stat] for stat in STATS]

                    moves = list(snap["teams"][p][active_slot]["moves"])
                    moves += ["none"] * (4 - len(moves))
                    row += moves[:4]
                else:
                    row += [0 for _ in STATS]
                    row += ["none"] * 4

            writer.writerow(row)

# ───── Usage ─────
INPUT_DIR = "replays/secondwave"
OUTPUT_DIR = "stats/csv_debug"

os.makedirs(OUTPUT_DIR, exist_ok=True)

success = 0
failed = []

json_files = sorted(
    f for f in os.listdir(INPUT_DIR)
    if f.endswith(".json")
)

print(f"JSON trouvés : {len(json_files)}")

for filename in json_files:
    json_path = os.path.join(INPUT_DIR, filename)
    csv_name = filename.replace(".json", ".csv")
    csv_path = os.path.join(OUTPUT_DIR, csv_name)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        parse_replay(data, csv_path)
        success += 1

    except Exception as e:
        failed.append((filename, str(e)))

print("\n===== DEBUG REPORT =====")
print(f"CSV générés avec succès : {success}/{len(json_files)}")
print(f"Échecs                 : {len(failed)}")

if failed:
    print("\n❌ FICHIERS EN ERREUR :")
    for fname, err in failed:
        print(f"- {fname} → {err}")
