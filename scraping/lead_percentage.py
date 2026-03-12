import json
import re

lead_file = "stats/lead-gen9ou-1825.txt"
output_file = "stats/lead-gen9ou-1825.json"

lead_stats = {}

with open(lead_file, "r", encoding="utf-8") as f:
    for line in f:
        # On cherche n'importe où dans la ligne un | Rank | Pokemon | Usage %
        match = re.search(r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*([\d\.]+)%", line)
        if match:
            name = match.group(1).strip()   # nom du Pokémon
            usage_pct = float(match.group(2))  # Usage %
            lead_stats[name] = usage_pct

# Sauvegarder en JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(lead_stats, f, indent=4, ensure_ascii=False)

print(f"Conversion terminée ! {len(lead_stats)} Pokémon ajoutés dans {output_file}")
