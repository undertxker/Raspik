import json
from collections import defaultdict

# Загружаем файл
with open('kills_output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Проверяем правильность данных
if 'data' not in data or 'kills' not in data['data']:
    print("❌ Нет данных об убийствах в файле.")
    exit()

kills = data['data']['kills']

# Статистика по игрокам
stats = defaultdict(lambda: {
    'kills': 0,
    'deaths': 0,
    'assists': 0,
    'teamkills': 0
})

# Обрабатываем все события
for kill in kills:
    killer_id = kill.get('killerId')
    victim_id = kill.get('victimId')
    assistant_id = kill.get('assistantId')
    is_teamkill = kill.get('isTeamkill', False)

    if killer_id:
        stats[killer_id]['kills'] += 1
        if is_teamkill:
            stats[killer_id]['teamkills'] += 1

    if victim_id:
        stats[victim_id]['deaths'] += 1

    if assistant_id:
        stats[assistant_id]['assists'] += 1

# Сохраняем в текстовый файл
with open('player_stats.txt', 'w', encoding='utf-8') as f:
    for player_id, s in stats.items():
        deaths = s['deaths'] if s['deaths'] != 0 else 1  # Чтобы не делить на ноль
        kda = (s['kills'] + s['assists']) / deaths
        teamkill_rate = (s['teamkills'] / s['kills']) * 100 if s['kills'] > 0 else 0

        f.write(f"Игрок {player_id}:\n")
        f.write(f"  Убийств: {s['kills']}\n")
        f.write(f"  Смертей: {s['deaths']}\n")
        f.write(f"  Ассистов: {s['assists']}\n")
        f.write(f"  Тимкилов: {s['teamkills']}\n")
        f.write(f"  KDA: {kda:.2f}\n")
        f.write(f"  Тимкил-рейтинг: {teamkill_rate:.2f}%\n")
        f.write("-" * 40 + "\n")

print("✅ Статистика сохранена в player_stats.txt")
