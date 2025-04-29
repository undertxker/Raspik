import asyncio
from playwright.async_api import async_playwright
import json
import os

cookie_string = "_ym_uid=173206126248818616; _ym_d=1732061262; sid=13852041.gkzgHx5JIKrRJPdG5pKm44fleZ9EMMtpxKf8Y2S1vO0; intercom-device-id-z5hvtvqq=b8b71486-40a7-4d30-a400-ea52395d0622; _gid=GA1.2.1057375111.1745677944; so=true; _ym_isad=1; _ga=GA1.2.1319435234.1732061261; _ga_FQFZB52Q62=GS1.2.1745931208.16.1.1745931215.53.0.0; intercom-session-z5hvtvqq=dHBOVWxRNTJqaEZVMVBqNlhHTjdreERRUFZaaHAyVGZwVnZpZzlYcm93MGZFYlhTTHhMc05KOE5JYmVKa3VEbUZMeU9TVkEvTDhLenVBSXp0cWpBQ3ZPQ1BlcllraTdLL1ZRcVBlVWQ5OHc9LS1CUmlhMVhaL3BmTkJvV0g0RnYzSTd3PT0=--fbf365aeeb1f3e4f461d47df06f8aefe893b021d; _ga_WNB3BQ8WVD=GS1.1.1745933474.23.0.1745933474.0.0.0; cf_clearance=.PnEdz2nt6sYhwJQPJNm5uVMMMxsCyqMgEaETu1Ej1Q-1745933474-1.2.1.1-0XL1xZtune9Hm29.p6HPnmQ1Y9LzKz_lO_5mBMaqpQaioYl5GwRi7egCvzjJsgWViU.ubTMz9E6YHSNSEreQJ24KTxJInt_OEgxyvM5cgdwaaMwrmDXfk4178hdT8prubbBF98GuzTtj9QeakJXYkFO8THW3K3Hj14BlN0nE8IdFyULmfE.2UKX0axTfIhqg5Q._paI6UqmZpaSYEnWnVty7U5arXsR_mSqQenXbeXLAi6DsMUAPVIpz8bRaFKP7OuLEGd8.VekAVhufcEwyeyUasRMxxQq4r._FL3ZGUQgmqrvQU8nHVB9boMYbyDRAKWgwYY8CvT0kqiQhY6CQAYCsqMzZhB98c6au_bd2vi4"

profile_url = "https://cs2.fastcup.net/id559900/matches"

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

        # Считываем матч ID из DOM страницы
        matches = await page.evaluate('''() => {
            const matches = [];
            document.querySelectorAll('[href^="/matches/"]').forEach(el => {
                const href = el.getAttribute('href');
                const matchId = href.match(/\/matches\/(\d+)/);
                if (matchId) {
                    matches.push(parseInt(matchId[1]));
                }
            });
            return matches;
        }''')

        print(f"✅ Найдено матчей: {len(matches)}")

        with open("logs/matches_from_profile.json", "w", encoding="utf-8") as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)

        print("✅ ID матчей сохранены в logs/matches_from_profile.json")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
