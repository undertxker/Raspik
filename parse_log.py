import json
import re
from collections import defaultdict

# 1. Загружаем лог
with open('log.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("Файл log.txt загружен")
print(f"Размер файла: {len(text)} символов")

# 2. Ищем ВСЕ JSON-блоки в тексте
json_blocks = re.findall(r'\{.*?\}', text, re.DOTALL)

kills_data = []
damages_data = []
shots_data = []
clutches_data = []

# 3. Проверяем каждый блок
for block in json_blocks:
    try:
        data = json.loads(block)
        if 'data' in data:
            if 'kills' in data['data']:
                kills_data = data['data']['kills']
            if 'damages' in data['data']:
                damages_data = data['data']['damages']
            if 'shots' in data['data']:
                shots_data = data['data']['shots']
            if 'clutches' in data['data']:
                clutches_data = data['data']['clutches']
    except Exception:
        continue

print(f"Убийств найдено: {len(kills_data)}")
print(f"Уронов найдено: {len(damages_data)}")
print(f"Выстрелов найдено: {len(shots_data)}")
print(f"Клатчей найдено: {len(clutches_data)}")

# 4. Создаём базу для подсчёта статистики
players = defaultdict(lambda: {
    "kills": 0,
    "deaths": 0,
    "hs": 0,
    "adr_sum": 0,
    "damage_events": 0,
    "shots": 0,
    "hits": 0,
    "clutches_attempted": defaultdict(int),
    "clutches_won": defaultdict(int),
    "weapons": defaultdict(lambda: {"kills": 0, "hs": 0, "shots": 0, "hits": 0})
})

# 5. Обработка убийств
for kill in kills_data:
    killer = kill['killerId']
    victim = kill['victimId']
    weapon = kill['weaponId']
    headshot = kill['headshot']

    players[killer]['kills'] += 1
    players[killer]['weapons'][weapon]['kills'] += 1

    if headshot:
        players[killer]['hs'] += 1
        players[killer]['weapons'][weapon]['hs'] += 1

    players[victim]['deaths'] += 1

# 6. Обработка урона
for damage in damages_data:
    attacker = damage['attackerId']
    value = damage['damage']

    players[attacker]['adr_sum'] += value
    players[attacker]['damage_events'] += 1

# 7. Обработка стрельбы
for shot in shots_data:
    shooter = shot['userId']
    weapon = shot['weaponId']
    shots = shot['shots']
    hits = shot['hits']

    players[shooter]['shots'] += shots
    players[shooter]['hits'] += hits

    players[shooter]['weapons'][weapon]['shots'] += shots
    players[shooter]['weapons'][weapon]['hits'] += hits

# 8. Обработка клатчей
for clutch in clutches_data:
    user = clutch['userId']
    amount = clutch['amount']
    success = clutch['success']

    players[user]['clutches_attempted'][amount] += 1
    if success:
        players[user]['clutches_won'][amount] += 1

# 9. Вывод результата
for user_id, stats in players.items():
    total_kills = stats['kills']
    total_deaths = stats['deaths']
    hs_percent = round(stats['hs'] / total_kills * 100, 1) if total_kills else 0
    adr = round(stats['adr_sum'] / stats['damage_events'], 1) if stats['damage_events'] else 0
    accuracy = round(stats['hits'] / stats['shots'] * 100, 1) if stats['shots'] else 0

    print(f"\nИгрок {user_id}: 🎯")
    print(f" Kills: {total_kills}, Deaths: {total_deaths}, HS%: {hs_percent}%, ADR: {adr}")
    print(f" Точность стрельбы: {accuracy}%")

    print(" Клатчи:")
    for amount, tries in stats['clutches_attempted'].items():
        wins = stats['clutches_won'].get(amount, 0)
        print(f"  1v{amount}: {wins} побед из {tries} попыток")

    print(" Оружие:")
    for weapon_id, weapon_stats in stats['weapons'].items():
        weapon_accuracy = round(weapon_stats['hits'] / weapon_stats['shots'] * 100, 1) if weapon_stats['shots'] else 0
        print(f"  Оружие {weapon_id}: {weapon_stats['kills']} фрагов, {weapon_stats['hs']} HS, {weapon_accuracy}% точности")

    print("-"*50)