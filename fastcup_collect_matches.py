# fastcup_collect_matches.py
import asyncio
from playwright.async_api import async_playwright
import json
import os
from config import cookie_string, user_id

profile_url = f"https://cs2.fastcup.net/id{user_id}/matches"

async def main():
    if not os.path.exists('logs'):
        os.makedirs('logs')

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

        await page.goto(profile_url)
        await asyncio.sleep(5)

        matches = await page.evaluate('''() => {
            const matches = [];
            document.querySelectorAll('[href^="/matches/"]').forEach(el => {
                const href = el.getAttribute('href');
                const matchId = href.match(/\/matches\/(\d+)/);
                if (matchId) {
                    matches.push(parseInt(matchId[1]));
                }
            });
            return [...new Set(matches)];
        }''')

        print(f"✅ Найдено матчей: {len(matches)}")

        with open("logs/matches_from_profile.json", "w", encoding="utf-8") as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)

        print("✅ ID матчей сохранены в logs/matches_from_profile.json")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
