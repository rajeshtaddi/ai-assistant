from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from services.weather_tool import get_weather

# LLM
llm = ChatOllama(model="phi")

# tools list
tools = [get_weather]

# bind tools to model
llm_with_tools = llm.bind_tools(tools)


async def chat_with_ai(message: str):

    # send user message
    response = await llm_with_tools.ainvoke(
        [HumanMessage(content=message)]
    )

    # if AI wants to call tool
    if response.tool_calls:

        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        if tool_name == "get_weather":
            result = await get_weather(**tool_args)
            return result

    return response.content