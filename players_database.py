import json
import os

# Данные игроков
players_data = {
    "1107287": {"Fastcup Nickname": "w1rtu0zZz", "Discord Tag": "w1rtu50"},
    "559900": {"Fastcup Nickname": "Geniputhe", "Discord Tag": "_riprep"},
    "876603": {"Fastcup Nickname": "gde moy aurabot?", "Discord Tag": "no_yawn"},
    "2034593": {"Fastcup Nickname": "unlucky on mid", "Discord Tag": "undertxker"},
    "2916809": {"Fastcup Nickname": "nichi buchi", "Discord Tag": "huujin"},
    "553599": {"Fastcup Nickname": "dreis'no'rs", "Discord Tag": "dreisnors"},
    "582898": {"Fastcup Nickname": "indigo kid", "Discord Tag": ""},
    "735548": {"Fastcup Nickname": "Pale_R1der", "Discord Tag": ""},
    "730844": {"Fastcup Nickname": "Sunsey killer", "Discord Tag": "sunseyy"},
    "553601": {"Fastcup Nickname": "Korotiwka", "Discord Tag": "korotiwka"},
    "557377": {"Fastcup Nickname": "profmars", "Discord Tag": "profmars"},
    "772037": {"Fastcup Nickname": "haski gungerbrod", "Discord Tag": "golovolomka"},
    "925446": {"Fastcup Nickname": "ZHORA KOZUBENKO", "Discord Tag": ""},
    "554594": {"Fastcup Nickname": "SLAB_KARAGACHA", "Discord Tag": ""},
    "1125631": {"Fastcup Nickname": "Hellwist", "Discord Tag": "malmwist"},
    "566587": {"Fastcup Nickname": "Angry_Lobster", "Discord Tag": "angry_lobster"}
}

# Путь для сохранения
OUTPUT_FILE = "logs/players_nicknames.json"

# Убедимся, что папка logs существует
os.makedirs("logs", exist_ok=True)

# Сохранение данных
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(players_data, f, indent=2, ensure_ascii=False)

print(f"✅ База данных игроков сохранена в {OUTPUT_FILE}")
