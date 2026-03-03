import httpx

async def get_weather(city: str):
    url = f"http://wttr.in/{city}?format=3"

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            verify=False   # ⭐ VERY IMPORTANT
        ) as client:
            response = await client.get(url)
            return response.text

    except Exception as e:
        return f"Weather error: {str(e)}"