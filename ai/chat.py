from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage



import os
from langchain_mcp_adapters.client import MultiServerMCPClient

llm = ChatOllama(model="qwen2.5:3b")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

client = MultiServerMCPClient(
    {
        "tools-server": {
            "command": "python",
            "args": [os.path.join(BASE_DIR, "mcp_server", "server.py")],
            "transport": "stdio",
        }
    }
)

llm_with_tools = None


async def initialize_tools():
    global llm_with_tools

    tools = await client.get_tools()   # ✅ MUST await
    llm_with_tools = llm.bind_tools(tools)


async def chat_with_ai(message: str):

    global llm_with_tools

    if llm_with_tools is None:
        await initialize_tools()

    response = await llm_with_tools.ainvoke(
        [HumanMessage(content=message)]
    )

    return response.content