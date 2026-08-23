import asyncio
import json

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

SERVERS = {
    "manim-server": {
        "transport": "stdio",
        "command": r"C:\Users\Mukesh Patel\Desktop\MCP-MATH-SERVER\.venv\Scripts\python.exe",
        "args": [
            r"C:\Users\Mukesh Patel\Desktop\MCP-MATH-SERVER\manim_server.py"
        ]
    },

    "expense": {
        "transport": "streamable_http",
        "url": "https://splendid-gold-dingo.fastmcp.app/mcp"
    },

    "manim-server": {
        "transport": "stdio",
        "command": r"C:\Users\Mukesh Patel\Desktop\MCP-MATH-SERVER\.venv\Scripts\python.exe",
        "args": [
            r"C:\Users\Mukesh Patel\Desktop\MCP-MATH-SERVER\manim_server.py"
        ],
        "env": {
            "MANIM_EXECUTABLE": "manim"
        }
    }
}


async def main():

    print("Connecting to MCP servers...")

    client = MultiServerMCPClient(SERVERS)

    tools = await client.get_tools()

    named_tools = {
        tool.name: tool
        for tool in tools
    }

    print("\n========================================")
    print("ALL AVAILABLE MCP TOOLS")
    print("========================================")

    for index, tool in enumerate(tools, start=1):
        print(f"{index}. {tool.name}")

    print("========================================")
    print(f"Total tools: {len(tools)}")
    print("========================================")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    llm_with_tools = llm.bind_tools(tools)

    prompt = HumanMessage(
    content="Create a rotating triangle animation using the Manim tool."
)

    response = await llm_with_tools.ainvoke([prompt])

    print("\n========================================")
    print("LLM RESPONSE")
    print("========================================")
    print(response.content)

    if not response.tool_calls:
        print("\nNo MCP tool was called.")
        return

    tool_messages = []

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call.get("args") or {}
        tool_call_id = tool_call["id"]

        print("\n----------------------------------------")
        print(f"Calling tool: {tool_name}")
        print(f"Arguments: {tool_args}")
        print("----------------------------------------")

        if tool_name not in named_tools:
            print(f"Tool not found: {tool_name}")
            continue

        result = await named_tools[tool_name].ainvoke(
            tool_args
        )

        print("\nTool result:")
        print(result)

        tool_messages.append(
            ToolMessage(
                tool_call_id=tool_call_id,
                content=json.dumps(
                    result,
                    default=str
                )
            )
        )

    final_response = await llm_with_tools.ainvoke(
        [
            prompt,
            response,
            *tool_messages
        ]
    )

    print("\n========================================")
    print("FINAL RESPONSE")
    print("========================================")
    print(final_response.content)


if __name__ == "__main__":
    asyncio.run(main())