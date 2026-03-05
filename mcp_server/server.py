from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("tools-server")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather of a city."""

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo = requests.get(geo_url).json()

        if "results" not in geo:
            return "City not found"

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather = requests.get(weather_url).json()

        temp = weather["current_weather"]["temperature"]
        wind = weather["current_weather"]["windspeed"]

        return f"{city}: {temp}°C, Wind {wind} km/h"

    except Exception as e:
        return f"Weather error: {str(e)}"


if __name__ == "__main__":
    mcp.run()