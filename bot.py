import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=False, чтобы видеть окно браузера
        context = await browser.new_context()
        page = await context.new_page()

        # Ловим только нужные ответы
        responses = []

        async def handle_response(response):
            if "hasura.fastcup.net/v1/graphql" in response.url:
                try:
                    json_data = await response.json()
                    responses.append(json_data)
                except Exception as e:
                    print("Ошибка парсинга ответа:", e)

        page.on("response", handle_response)

        # Переходим на страницу матча
        await page.goto("https://cs2.fastcup.net/matches/17395452/stats")

        # Ждем чтобы все запросы успели пройти
        await asyncio.sleep(7)  # можно увеличить если слабый интернет

        # Выводим все собранные ответы
        for idx, resp in enumerate(responses):
            print(f"\nОтвет #{idx + 1}:\n", resp)

        await browser.close()

asyncio.run(main())
