import aiohttp

async def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=%C+%t&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                return text.strip()
            return "Не удалось получить данные"