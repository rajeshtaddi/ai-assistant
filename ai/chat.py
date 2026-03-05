import os
import logging
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage

logging.basicConfig(level=logging.INFO)

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
TOOLS = []


async def initialize_tools():

    global llm_with_tools, TOOLS

    TOOLS = await client.get_tools()

    llm_with_tools = llm.bind_tools(TOOLS)


async def chat_with_ai(message: str):

    global llm_with_tools, TOOLS

    if llm_with_tools is None:
        await initialize_tools()

    response = await llm_with_tools.ainvoke(
        [HumanMessage(content=message)]
    )

    if response.tool_calls:

        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        print("Executing tool:", tool_name, tool_args)

        tool_map = {tool.name: tool for tool in TOOLS}

        result = await tool_map[tool_name].ainvoke(tool_args)

        final_response = await llm_with_tools.ainvoke([
            HumanMessage(content=message),
            response,
            ToolMessage(
                content=result,
                tool_call_id=tool_call_id
            )
        ])

        return final_response.content

    return response.content