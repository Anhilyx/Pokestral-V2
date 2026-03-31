import pandas as pd

# 🔹 Fichiers
INPUT_DATASET = "../IA_switch_move/complete_dataset_2.csv"
PKMN_DATASET = "../IA_switch_move/pkmn.csv"
OUTPUT_DATASET = "../IA_switch_move/complete_dataset.csv"

# 🔹 Chargement
df = pd.read_csv(INPUT_DATASET)
pkmn = pd.read_csv(PKMN_DATASET)

# 🔹 Nettoyage colonnes
df.columns = df.columns.str.strip()
pkmn.columns = pkmn.columns.str.strip()

# =========================================================
# 🔥 POKEMON DATA CLEAN
# =========================================================

pkmn = pkmn[[
    "Pokemon Name",
    "Health Stat",
    "Attack Stat",
    "Defense Stat",
    "Special Attack Stat",
    "Special Defense Stat",
    "Speed Stat"
]]

pkmn = pkmn.rename(columns={
    "Pokemon Name": "name",
    "Health Stat": "hp_stat",
    "Attack Stat": "atk_stat",
    "Defense Stat": "def_stat",
    "Special Attack Stat": "spa_stat",
    "Special Defense Stat": "spd_stat",
    "Speed Stat": "spe_stat"
})

# 🔥 nettoyage noms
pkmn["name"] = (
    pkmn["name"]
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.strip()
)

# =========================================================
# 🔥 EXTRACTION DU POKEMON ACTIF
# =========================================================

def get_active_pokemon(row, player):
    letter = row.get(f"active_{player}")

    # 🔥 gestion NaN
    if pd.isna(letter):
        return None

    letter = str(letter).strip()

    col = f"pokemon_{player}{letter}"

    # 🔥 sécurité colonne
    if col not in row.index:
        return None

    return row[col]

df["active_p1_name"] = df.apply(lambda row: get_active_pokemon(row, "p1"), axis=1)
df["active_p2_name"] = df.apply(lambda row: get_active_pokemon(row, "p2"), axis=1)

# 🔥 nettoyage noms actifs
df["active_p1_name"] = (
    df["active_p1_name"]
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.strip()
)

df["active_p2_name"] = (
    df["active_p2_name"]
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.strip()
)

# =========================================================
# 🔥 MERGE STATS
# =========================================================

all_missing_names = set()

for col in ["active_p1_name", "active_p2_name"]:
    print(f"Processing {col}...")

    stats = pkmn.copy()

    stats = stats.rename(columns={
        "hp_stat": f"{col}_hp_stat",
        "atk_stat": f"{col}_atk_stat",
        "def_stat": f"{col}_def_stat",
        "spa_stat": f"{col}_spa_stat",
        "spd_stat": f"{col}_spd_stat",
        "spe_stat": f"{col}_spe_stat"
    })

    df = df.merge(
        stats,
        how="left",
        left_on=col,
        right_on="name"
    )

    # 🔍 noms manquants
    missing_mask = df[f"{col}_hp_stat"].isna()
    missing_names = df.loc[missing_mask, col].dropna().unique()

    all_missing_names.update(missing_names)

    df = df.drop(columns=["name"])

# =========================================================
# 🔥 GESTION DES NaN
# =========================================================

for col in ["active_p1_name", "active_p2_name"]:
    stat_cols = [
        f"{col}_hp_stat",
        f"{col}_atk_stat",
        f"{col}_def_stat",
        f"{col}_spa_stat",
        f"{col}_spd_stat",
        f"{col}_spe_stat"
    ]

    # 🔥 si pas de Pokémon actif → 0
    df.loc[df[col].isna(), stat_cols] = 0

    # 🔥 sinon remplir NaN restants
    df[stat_cols] = df[stat_cols].fillna(0)

# =========================================================
# 🔍 DEBUG
# =========================================================

print("\n==============================")
print("NOMS NON TROUVÉS DANS pkmn.csv")
print("==============================")

print(f"Nombre de noms uniques problématiques : {len(all_missing_names)}")

if len(all_missing_names) > 0:
    print("\nListe des noms :")
    for name in sorted(all_missing_names):
        print(name)

# =========================================================
# 💾 SAVE
# =========================================================

df.to_csv(OUTPUT_DATASET, index=False)

print("\n✅ Dataset sauvegardé :", OUTPUT_DATASET)