import os
import json
import math
import statistics

# Файлы
profiles_file = "logs/players_nicknames.json"
stats_file = "logs/total_stats.json"
weapons_file = "logs/player_weapon_stats.json"
kills_folder = "logs/matches_kills"
output_file = "logs/teams.json"

# Бонус за любимое оружие
weapon_bonuses = {
    "AWP": 0.2,
    "SSG 08": 0.1,
    "AK-47": 0.1,
    "M4A4": 0.1,
    "M4A1-S": 0.1
}

# Игнорируем всякие неизвестные "Unknown weapon"
ignore_weapons = {"Unknown weapon 171", "Unknown weapon 174", "Unknown weapon 175", "Unknown weapon 180", "Unknown weapon 181"}

# Загрузка данных
with open(profiles_file, "r", encoding="utf-8") as f:
    profiles = json.load(f)

with open(stats_file, "r", encoding="utf-8") as f:
    stats = json.load(f)

with open(weapons_file, "r", encoding="utf-8") as f:
    weapons = json.load(f)

# Сбор убийств/смертей по матчам для стабильности
player_kills = {}
player_deaths = {}

for filename in os.listdir(kills_folder):
    if filename.startswith("match_kills_") and filename.endswith(".json"):
        with open(os.path.join(kills_folder, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
            kills = data.get("kills", [])
            round_stats = {}

            for kill in kills:
                killer_id = str(kill["killerId"])
                victim_id = str(kill["victimId"])

                if killer_id not in round_stats:
                    round_stats[killer_id] = {"kills": 0, "deaths": 0}
                if victim_id not in round_stats:
                    round_stats[victim_id] = {"kills": 0, "deaths": 0}

                round_stats[killer_id]["kills"] += 1
                round_stats[victim_id]["deaths"] += 1

            for player_id, stats_data in round_stats.items():
                if player_id not in player_kills:
                    player_kills[player_id] = []
                    player_deaths[player_id] = []
                player_kills[player_id].append(stats_data["kills"])
                player_deaths[player_id].append(stats_data["deaths"])

# Расчёт total_score для игроков
players_scores = {}

for player_id, stat in stats.items():
    player_id = str(player_id)

    if player_id not in profiles:
        continue  # Нет профиля - пропускаем

    kills = stat.get("Kills", 0)
    deaths = stat.get("Deaths", 1)  # чтобы не делить на 0
    kd = kills / deaths
    adr = stat.get("ADR", 0)
    hs_percent = stat.get("HS%", 0) / 100

    skill_score = (kd * 0.4) + (adr / 100 * 0.3) + (hs_percent * 0.3)

    profile = profiles[player_id]
    manual = profile.get("Manual", {})

    serious = manual.get("serious", 0)
    calls = manual.get("calls", 0)
    communication = manual.get("communication", 0)
    teamplay = manual.get("teamplay", 0)
    toxicity = manual.get("toxicity", 0)

    mental_score = (serious * 0.3) + (calls * 0.25) + (communication * 0.25) + (teamplay * 0.2) - (toxicity * 0.5)

    # Оружейный бонус
    weapon_bonus = 0
    player_weapon_data = weapons.get(player_id, {})
    if player_weapon_data:
        top_weapon = max(
            (w for w in player_weapon_data.items() if w[0] not in ignore_weapons),
            key=lambda x: x[1],
            default=(None, 0)
        )[0]
        if top_weapon in weapon_bonuses:
            weapon_bonus = weapon_bonuses[top_weapon]

    # Стабильность
    if player_id in player_kills and len(player_kills[player_id]) >= 2:
        kills_std = statistics.stdev(player_kills[player_id])
        deaths_std = statistics.stdev(player_deaths[player_id])
        stability_score = 1 / (1 + kills_std + deaths_std)
    else:
        stability_score = 0.5  # если мало данных

    total_score = skill_score + mental_score + weapon_bonus + stability_score

    players_scores[player_id] = {
        "nickname": profile.get("Fastcup Nickname", f"Player {player_id}"),
        "score": total_score
    }

# Сортировка по рейтингу
sorted_players = sorted(players_scores.items(), key=lambda x: x[1]["score"], reverse=True)

# Формируем команды
team_A = []
team_B = []
bench = []

for i, (player_id, info) in enumerate(sorted_players):
    if i < 10:
        if i % 2 == 0:
            team_A.append(info["nickname"])
        else:
            team_B.append(info["nickname"])
    else:
        bench.append(info["nickname"])

# Вывод результатов
teams = {
    "Team A": team_A,
    "Team B": team_B,
    "Bench": bench
}

os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(teams, f, indent=2, ensure_ascii=False)

print(f"✅ Команды сформированы и сохранены в {output_file}")
