import aiohttp

async def get_currency_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("rates", {})
            return {}