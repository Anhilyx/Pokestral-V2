import pandas as pd

df = pd.read_csv("stats/complete_dataset.csv")

# traiter chaque match séparément
for match_id, match in df.groupby("match_id"):

    moves_p1 = {}

    # ───── récupérer les moves du match ─────

    for _, row in match.iterrows():

        slot = row["active_p1"]

        if pd.notna(slot):
            pokemon = row[f"pokemon_p1{slot}"]

            if pokemon not in moves_p1:
                moves_p1[pokemon] = set()

            for i in range(1,5):
                move = row[f"active_p1_move{i}"]
                if move != "none":
                    moves_p1[pokemon].add(move)

    # convertir en listes de 4 moves
    for p in moves_p1:
        moves = list(moves_p1[p])[:4]
        moves += ["none"] * (4 - len(moves))
        moves_p1[p] = moves

    # ───── appliquer les moves sur les lignes du match ─────

    for idx, row in match.iterrows():

        slot = row["active_p1"]

        if pd.notna(slot):
            pokemon = row[f"pokemon_p1{slot}"]

            if pokemon in moves_p1:
                moves = moves_p1[pokemon]

                for i in range(4):
                    df.at[idx, f"active_p1_move{i+1}"] = moves[i]

# sauvegarde
df.to_csv("stats/complete_dataset.csv", index=False)