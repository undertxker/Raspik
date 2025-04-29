import os
import json

# Маппинг weaponId -> Название оружия
weapon_id_to_name = {
    110: "Glock-18",
    111: "P2000",
    112: "USP-S",
    113: "Dual Berettas",
    114: "P250",
    116: "Five-SeveN",
    117: "CZ75-Auto",
    118: "Tec-9",
    119: "Desert Eagle",
    120: "R8 Revolver",
    121: "Nova",
    122: "XM1014",
    123: "Sawed-Off",
    124: "MAG-7",
    125: "MP9",
    126: "MAC-10",
    127: "MP7",
    128: "UMP-45",
    129: "P90",
    130: "PP-Bizon",
    131: "FAMAS",
    132: "Galil AR",
    133: "M4A4",
    134: "M4A1-S",
    135: "AK-47",
    136: "SG 553",
    137: "AUG",
    138: "SSG 08",
    139: "AWP",
    140: "G3SG1",
    141: "SCAR-20",
    142: "Negev",
    143: "M249",
    144: "Zeus x27",
    145: "Knife",
}

# ID оружий, которые нужно игнорировать
ignored_weapon_ids = {
    146,  # HE Grenade
    147,  # Flashbang
    148,  # Smoke Grenade
    149,  # Molotov
    150,  # Decoy Grenade
    151,  # Incendiary Grenade
    152,  # C4
    153,  # Taser
    154,  # Kevlar Vest
    155,  # Kevlar + Helmet
    156,  # Defuse Kit
    157,  # Rescue Kit
}

kills_folder = "logs/matches_kills"
output_file = "logs/player_weapon_stats.json"

player_weapons = {}

for filename in os.listdir(kills_folder):
    if filename.startswith("match_kills_") and filename.endswith(".json"):
        with open(os.path.join(kills_folder, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
            kills = data.get("kills", [])
            for kill in kills:
                killer_id = str(kill["killerId"])
                weapon_id = kill["weaponId"]

                if weapon_id in ignored_weapon_ids:
                    continue  # Пропускаем ненужное

                weapon_name = weapon_id_to_name.get(weapon_id, f"Unknown weapon {weapon_id}")

                if killer_id not in player_weapons:
                    player_weapons[killer_id] = {}

                if weapon_name not in player_weapons[killer_id]:
                    player_weapons[killer_id][weapon_name] = 0

                player_weapons[killer_id][weapon_name] += 1

# Сохраняем результат
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(player_weapons, f, indent=2, ensure_ascii=False)

print(f"✅ Статистика по оружию сохранена в {output_file}")
