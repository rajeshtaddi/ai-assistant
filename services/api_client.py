from services.weather_tool import get_weather
from langchain_ollama import ChatOllama

llm = ChatOllama(model="phi")

async def chat_with_ai(message: str):

    # 🔥 Step 1: Detect weather intent manually
    if "weather" in message.lower():
        city = message.lower().split("in")[-1].strip()
        weather = get_weather(city)
        return weather

    # 🔥 Step 2: Otherwise normal AI response
    response = await llm.ainvoke(message)
    return response.content