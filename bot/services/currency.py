import aiohttp

async def is_valid_currency(currency_code: str) -> bool:
    url = f"https://api.exchangerate-api.com/v4/latest/{currency_code.upper()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.status == 200