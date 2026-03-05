from langchain_core.tools import tool
import httpx

@tool
async def get_weather(city: str) -> str:
    """Get current weather of a city."""

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:

            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            geo_response = await client.get(geo_url)
            geo_data = geo_response.json()

            if "results" not in geo_data:
                return "City not found"

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = await client.get(weather_url)

            weather = weather_response.json()["current_weather"]

            return f"{city}: {weather['temperature']}°C, Wind {weather['windspeed']} km/h"

    except Exception as e:
        return f"Weather error: {str(e)}"