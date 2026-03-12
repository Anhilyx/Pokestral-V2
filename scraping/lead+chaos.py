import json

# Fichiers
chaos_file = "stats/chaos-gen9ou-1825.json"
lead_file = "stats/lead-gen9ou-1825.json"
output_file = "stats/chaos-gen9ou-1825-with-leads.json"

# Charger les deux JSON
with open(chaos_file, "r", encoding="utf-8") as f:
    chaos_data = json.load(f)

with open(lead_file, "r", encoding="utf-8") as f:
    lead_data = json.load(f)

# Ajouter Lead Usage % dans chaque Pokémon du JSON chaos
for pokemon_name in chaos_data["data"]:
    chaos_data["data"][pokemon_name]["Lead Usage %"] = lead_data.get(pokemon_name, 0)

# Sauvegarder le JSON fusionné
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chaos_data, f, indent=4, ensure_ascii=False)

print(f"Fusion terminée ! Fichier créé : {output_file}")
