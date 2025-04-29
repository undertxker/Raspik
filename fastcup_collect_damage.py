# fastcup_collect_match_damages.py
import asyncio
from playwright.async_api import async_playwright
import json
import os
from config import cookie_string

async def collect_data_for_match(page, match_id):
    print(f"🔎 Парсю матч {match_id}...")

    await page.goto(f"https://cs2.fastcup.net/matches/{match_id}/stats")
    await asyncio.sleep(5)  # дать странице авторизоваться и подгрузить session/localStorage

    graphql_query = """
        return fetch("https://hasura.fastcup.net/v1/graphql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                operationName: "GetMatchDamages",
                variables: { matchId: MATCH_ID },
                query: `query GetMatchDamages($matchId: Int!) {
                    damages: match_damages(where: {match_id: {_eq: $matchId}}) {
                        roundId: round_id
                        inflictorId: inflictor_id
                        victimId: victim_id
                        weaponId: weapon_id
                        hitboxGroup: hitbox_group
                        damageReal: damage_real
                        damageNormalized: damage_normalized
                        hits
                        __typename
                    }
                }`
            })
        }).then(res => res.json());
    """

    try:
        data = await page.evaluate(f"""(MATCH_ID) => {{ {graphql_query} }}""", match_id)
    except Exception as e:
        print(f"❌ Ошибка при парсинге {match_id}: {e}")
        return None

    if not data or "data" not in data or "damages" not in data["data"]:
        print(f"⚠️ Нет данных по урону для матча {match_id}")
        return None

    return {
        "match_id": match_id,
        "damages": data["data"]["damages"]
    }


async def main():
    if not os.path.exists('logs/matches_damages'):
        os.makedirs('logs/matches_damages')

    with open("logs/matches_from_profile.json", "r", encoding="utf-8") as f:
        matches = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        await context.add_cookies([
            {
                "name": pair.split("=")[0],
                "value": pair.split("=")[1],
                "domain": ".fastcup.net",
                "path": "/",
                "httpOnly": False,
                "secure": True,
                "sameSite": "Lax"
            } for pair in cookie_string.split("; ")
        ])

        page = await context.new_page()

        for match_id in matches:
            try:
                match_data = await collect_data_for_match(page, match_id)
                if match_data:
                    with open(f"logs/matches_damages/match_damage_{match_id}.json", "w", encoding="utf-8") as f:
                        json.dump(match_data, f, indent=2, ensure_ascii=False)
                    print(f"✅ Матч {match_id} сохранён!")
                else:
                    print(f"⚠️ Нет данных для матча {match_id}")
            except Exception as e:
                print(f"❌ Ошибка при парсинге матча {match_id}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())