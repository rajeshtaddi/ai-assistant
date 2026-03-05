from langchain_core.tools import tool
import requests

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url).json()

        if "results" not in geo_response:
            return "City not found"

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather = requests.get(weather_url).json()["current_weather"]

        return f"{city}: {weather['temperature']}°C, Wind {weather['windspeed']} km/h"

    except Exception as e:
        return f"Weather error: {str(e)}"