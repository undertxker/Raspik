import requests
import json
import os

# Твоя кука (очень важна)
cookie = "_ym_uid=173206126248818616; _ym_d=1732061262; sid=13852041.gkzgHx5JIKrRJPdG5pKm44fleZ9EMMtpxKf8Y2S1vO0; intercom-device-id-z5hvtvqq=b8b71486-40a7-4d30-a400-ea52395d0622; _gid=GA1.2.1057375111.1745677944; _ym_isad=1; so=true; intercom-session-z5hvtvqq=K3lId29nMVNUL1EvNEJSSXhTNmhyaUg4bGJ3OGpNZ2VVK3ZYKzkvb3FSWEZraTJra25vQ2dHUytxUC8zcTZ6Q0dlcWFyNCt5ZlhXclI4eEUyUEhxclFtNkpvays2N3FyT3RjYUU0Q3g4U1E9LS1qNXdFcW9CYVg0WE1Bc1lxS2V4VW13PT0=--0128cfa7e59c1451337bda059822c8e541ad7994; _ga_FQFZB52Q62=GS1.2.1745873270.15.1.1745873770.58.0.0; _ga_WNB3BQ8WVD=GS1.1.1745873270.21.1.1745874026.0.0.0; _ga=GA1.2.1319435234.1732061261; _gat_UA-138348631-1=1; cf_clearance=B8hURq7qM79b758in33HD_IyNkc84I4fPCZWY9TkNJg-1745874027-1.2.1.1-80VUYCYnNAtB2qtgCAvukHE4bNcYLb1mhD8R8vdO_TMWdLVdch0lbm.WQJtPzdm1Ag.7l2.tBWAzeecQ9plQ6PfIm8mdIZZzAvTolr.Hh93z9QBxOYjfJlkR93UQ_5.WI_u7cCxOCp2nb30q7zZYZ50phu.66hdDKkO0FPZfnhYVQnWrgJDzAIbZcC8WczE7C6A7z7B1FCVDum0VkPlJbu3ZfoIaEYS80gbORho3wXK3hCPkj2vs8hP2L3jWLu4mQSRlUjjeEw.uSQUT6tGLzDCLzWSJ5FVVvSF_SXnmDuPWF_iRvWw_HPvkCwRxTI8Mmx9hFhwStFacAzbcfztW3Of5rfgg1sWcRB1_U9MGp0w"
match_ids = [
    17395452,
    17283520,
    # другие id
]

headers = {
    "Content-Type": "application/json",
    "origin": "https://cs2.fastcup.net",
    "referer": "https://cs2.fastcup.net/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "cookie": cookie,
}

url = "https://hasura.fastcup.net/v1/graphql"

if not os.path.exists('logs'):
    os.makedirs('logs')

for match_id in match_ids:
    print(f"🔎 Работаем с матчем {match_id}...")

    payload = {
        "operationName": "__GetMatchKills",
        "variables": {
            "matchId": match_id,
            "userId": None  # <-- Ключевая фиксация
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
                roundId
                createdAt
                killerId
                victimId
                assistantId
                isTeamkill
              }
            }
        """
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and "kills" in data["data"]:
            with open(f"logs/match_{match_id}.json", "w", encoding="utf-8") as f:
                json.dump(data["data"], f, indent=2, ensure_ascii=False)
            print(f"✅ Матч {match_id} сохранён!\n")
        else:
            print(f"⚠️ Нет данных по убийствам для матча {match_id}.\n")
    else:
        print(f"❌ Ошибка HTTP {response.status_code} для матча {match_id}.\n")



