import requests
import json

url = "https://hasura.fastcup.net/v1/graphql"

headers = {
    "Content-Type": "application/json",
    "origin": "https://cs2.fastcup.net",
    "referer": "https://cs2.fastcup.net/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "cookie": "_ym_uid=173206126248818616; _ym_d=1732061262; sid=13852041.gkzgHx5JIKrRJPdG5pKm44fleZ9EMMtpxKf8Y2S1vO0; intercom-device-id-z5hvtvqq=b8b71486-40a7-4d30-a400-ea52395d0622; _gid=GA1.2.1057375111.1745677944; so=true; _ym_isad=1; _ga=GA1.2.1319435234.1732061261; _ga_FQFZB52Q62=GS1.2.1745931208.16.1.1745931215.53.0.0; intercom-session-z5hvtvqq=dHBOVWxRNTJqaEZVMVBqNlhHTjdreERRUFZaaHAyVGZwVnZpZzlYcm93MGZFYlhTTHhMc05KOE5JYmVKa3VEbUZMeU9TVkEvTDhLenVBSXp0cWpBQ3ZPQ1BlcllraTdLL1ZRcVBlVWQ5OHc9LS1CUmlhMVhaL3BmTkJvV0g0RnYzSTd3PT0=--fbf365aeeb1f3e4f461d47df06f8aefe893b021d; _ga_WNB3BQ8WVD=GS1.1.1745933474.23.0.1745933474.0.0.0; cf_clearance=.PnEdz2nt6sYhwJQPJNm5uVMMMxsCyqMgEaETu1Ej1Q-1745933474-1.2.1.1-0XL1xZtune9Hm29.p6HPnmQ1Y9LzKz_lO_5mBMaqpQaioYl5GwRi7egCvzjJsgWViU.ubTMz9E6YHSNSEreQJ24KTxJInt_OEgxyvM5cgdwaaMwrmDXfk4178hdT8prubbBF98GuzTtj9QeakJXYkFO8THW3K3Hj14BlN0nE8IdFyULmfE.2UKX0axTfIhqg5Q._paI6UqmZpaSYEnWnVty7U5arXsR_mSqQenXbeXLAi6DsMUAPVIpz8bRaFKP7OuLEGd8.VekAVhufcEwyeyUasRMxxQq4r._FL3ZGUQgmqrvQU8nHVB9boMYbyDRAKWgwYY8CvT0kqiQhY6CQAYCsqMzZhB98c6au_bd2vi4"
}

match_id = 17395452  # <-- сюда ID матча

payload = {
    "operationName": "__GetMatchKills",
    "variables": {
        "matchId": match_id
    },
    "query": """
    query __GetMatchKills($matchId: Int!, $userId: Int) {
      kills: match_kills(
        where: {
          match_id: {_eq: $matchId},
          _or: [
            {killer_id: {_eq: $userId}},
            {victim_id: {_eq: $userId}},
            {assistant_id: {_eq: $userId}}
          ]
        },
        order_by: {created_at: asc}
      ) {
        roundId: round_id
        createdAt: created_at
        killerId: killer_id
        victimId: victim_id
        assistantId: assistant_id
        isTeamkill: is_teamkill
      }
    }
    """
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    with open("kills_output.txt", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ Данные сохранены в kills_output.txt")
else:
    print(f"❌ Ошибка запроса: {response.status_code}")