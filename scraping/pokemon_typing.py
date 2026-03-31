import pandas as pd
import json

df = pd.read_csv("../IA_switch_move/complete_dataset.csv")

with open("stats/pokemon.json", "r", encoding="utf-8") as f:
    types_data = json.load(f)

pokemon_cols = [
    "pokemon_p1A", "pokemon_p1B", "pokemon_p1C", "pokemon_p1D", "pokemon_p1E", "pokemon_p1F",
    "pokemon_p2A", "pokemon_p2B", "pokemon_p2C", "pokemon_p2D", "pokemon_p2E", "pokemon_p2F"
]


def get_types(pokemon):
    if pd.isna(pokemon):
        return "-", "-"

    types = types_data.get(pokemon)

    if types is None:
        return "-", "-"

    if len(types) == 1:
        return types[0], "-"

    return types[0], types[1]


for col in pokemon_cols:
    type1_col = f"type_1_{col.split('pokemon_')[1]}"
    type2_col = f"type_2_{col.split('pokemon_')[1]}"

    types = df[col].apply(get_types)

    df[type1_col] = types.apply(lambda x: x[0])
    df[type2_col] = types.apply(lambda x: x[1])

    col_index = df.columns.get_loc(col)

    cols = list(df.columns)
    cols.insert(col_index + 1, cols.pop(cols.index(type1_col)))
    cols.insert(col_index + 2, cols.pop(cols.index(type2_col)))

    df = df[cols]

df.to_csv("../IA_switch_move/complete_dataset.csv", index=False)

print("Dataset généré : complete_dataset.csv")