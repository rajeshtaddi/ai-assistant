from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("tools-server")

@mcp.tool()
async def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=j1"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()

    temp = data["current_condition"][0]["temp_C"]
    desc = data["current_condition"][0]["weatherDesc"][0]["value"]

    return f"The weather in {city} is {temp}°C with {desc}."


if __name__ == "__main__":
    mcp.run()