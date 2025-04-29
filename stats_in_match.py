import json
import os
from collections import defaultdict

# Пути
MATCHES_FILE = "logs/matches_from_profile.json"
KILLS_FOLDER = "logs/matches_kills"
DAMAGES_FOLDER = "logs/matches_damages"
OUTPUT_FILE = "logs/total_stats.json"

# Функция для загрузки данных одного матча
def load_match_stats(match_id):
    kills_path = os.path.join(KILLS_FOLDER, f"match_kills_{match_id}.json")
    damages_path = os.path.join(DAMAGES_FOLDER, f"match_damage_{match_id}.json")

    if not os.path.exists(kills_path) or not os.path.exists(damages_path):
        print(f"⚠️ Файлы для матча {match_id} не найдены, пропускаю.")
        return None, None

    with open(kills_path, "r", encoding="utf-8") as f:
        kills = json.load(f)["kills"]
    with open(damages_path, "r", encoding="utf-8") as f:
        damages = json.load(f)["damages"]

    return kills, damages

# Функция для расчета статистики по одному матчу
def calculate_match_stats(kills, damages, match_id):
    stats = defaultdict(lambda: {
        "kills": 0,
        "deaths": 0,
        "assists": 0,
        "total_damage": 0,
        "rounds": set(),
        "matches": set(),
        "hs_kills": 0,
        "oneshot_kills": 0,
        "noscope_kills": 0,
        "airshot_kills": 0,
        "wallbang_kills": 0,
    })

    for kill in kills:
        killer = kill["killerId"]
        victim = kill["victimId"]
        assistant = kill.get("assistantId")
        round_id = kill["roundId"]

        stats[killer]["kills"] += 1
        stats[killer]["matches"].add(match_id)
        stats[victim]["deaths"] += 1
        stats[victim]["matches"].add(match_id)

        if assistant:
            stats[assistant]["assists"] += 1
            stats[assistant]["matches"].add(match_id)

        if kill["isHeadshot"]:
            stats[killer]["hs_kills"] += 1
        if kill["isWallbang"]:
            stats[killer]["wallbang_kills"] += 1
        if kill["isOneshot"]:
            stats[killer]["oneshot_kills"] += 1
        if kill["isAirshot"]:
            stats[killer]["airshot_kills"] += 1
        if kill["isNoscope"]:
            stats[killer]["noscope_kills"] += 1

        stats[killer]["rounds"].add(round_id)
        stats[victim]["rounds"].add(round_id)

    for dmg in damages:
        inflictor = dmg["inflictorId"]
        stats[inflictor]["total_damage"] += dmg["damageReal"]
        stats[inflictor]["rounds"].add(dmg["roundId"])
        stats[inflictor]["matches"].add(match_id)

    return stats

# Основной сбор всей статистики
def main():
    if not os.path.exists("logs"):
        print("❌ Папка logs не найдена!")
        return

    with open(MATCHES_FILE, "r", encoding="utf-8") as f:
        matches = json.load(f)

    total_stats = defaultdict(lambda: {
        "kills": 0,
        "deaths": 0,
        "assists": 0,
        "total_damage": 0,
        "rounds": set(),
        "matches": set(),
        "hs_kills": 0,
        "oneshot_kills": 0,
        "noscope_kills": 0,
        "airshot_kills": 0,
        "wallbang_kills": 0,
    })

    for match_id in matches:
        kills, damages = load_match_stats(match_id)
        if kills is None or damages is None:
            continue

        match_stats = calculate_match_stats(kills, damages, match_id)

        for player_id, m in match_stats.items():
            for key in ["kills", "deaths", "assists", "total_damage", "hs_kills", "oneshot_kills", "noscope_kills", "airshot_kills", "wallbang_kills"]:
                total_stats[player_id][key] += m[key]
            total_stats[player_id]["rounds"].update(m["rounds"])
            total_stats[player_id]["matches"].update(m["matches"])

    # Финальная обработка
    final_stats = {}
    for player_id, s in total_stats.items():
        rounds_count = len(s["rounds"]) if s["rounds"] else 1
        adr = round(s["total_damage"] / rounds_count, 1)
        kd = round(s["kills"] / s["deaths"], 2) if s["deaths"] else float('inf')
        hs_percent = round((s["hs_kills"] / s["kills"])*100, 1) if s["kills"] else 0.0
        matches_played = len(s["matches"])

        final_stats[player_id] = {
            "Kills": s["kills"],
            "Deaths": s["deaths"],
            "Assists": s["assists"],
            "+/-": s["kills"] - s["deaths"],
            "K/D": kd,
            "ADR": adr,
            "HS%": hs_percent,
            "Oneshots": s["oneshot_kills"],
            "Noscope": s["noscope_kills"],
            "Airshots": s["airshot_kills"],
            "Wallbangs": s["wallbang_kills"],
            "Matches": matches_played
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_stats, f, indent=2, ensure_ascii=False)

    print(f"✅ Общая статистика сохранена в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()