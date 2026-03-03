from langchain_ollama import ChatOllama
from services.weather_tool import get_weather

llm = ChatOllama(model="phi")

async def chat_with_ai(message: str):

    message_lower = message.lower()

    # 🔥 Weather detection
    if "weather" in message_lower:
        if "in" in message_lower:
            city = message_lower.split("in")[-1].strip()
            return await get_weather(city)   # ✅ IMPORTANT
        else:
            return "Please specify a city."

    # Normal AI response
    response = await llm.ainvoke(message)
    return response.content