import os
import json
import asyncio
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient


load_dotenv()

st.set_page_config(
    page_title="AI MCP Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI MCP Assistant")
st.caption("Groq + MCP + Calculator + Expenses + Manim")


SERVER_DIR = r"C:\Users\Mukesh Patel\Desktop\MCP-MATH-SERVER"

SERVER_PYTHON = os.path.join(
    SERVER_DIR,
    ".venv",
    "Scripts",
    "python.exe"
)

MAIN_SERVER = os.path.join(
    SERVER_DIR,
    "main.py"
)

MANIM_SERVER = os.path.join(
    SERVER_DIR,
    "manim_server.py"
)

OUTPUT_DIR = os.path.join(
    SERVER_DIR,
    "manim_output"
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in .env")
    st.stop()

if not os.path.isfile(SERVER_PYTHON):
    st.error(f"Python not found:\n{SERVER_PYTHON}")
    st.stop()

if not os.path.isfile(MAIN_SERVER):
    st.error(f"main.py not found:\n{MAIN_SERVER}")
    st.stop()

if not os.path.isfile(MANIM_SERVER):
    st.error(f"manim_server.py not found:\n{MANIM_SERVER}")
    st.stop()

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


SERVERS = {

    "math-expense": {
        "transport": "stdio",
        "command": SERVER_PYTHON,
        "args": [
            MAIN_SERVER
        ]
    },

    "expense-remote": {
        "transport": "streamable_http",
        "url": "https://splendid-gold-dingo.fastmcp.app/mcp"
    },

    "manim": {
        "transport": "stdio",
        "command": SERVER_PYTHON,
        "args": [
            MANIM_SERVER
        ],
        "env": {
            "MANIM_EXECUTABLE": os.path.join(
                SERVER_DIR,
                ".venv",
                "Scripts",
                "manim.exe"
            )
        }
    }
}


SYSTEM_PROMPT = """
You are an AI assistant connected to MCP servers.

You can perform calculations, manage expenses, and create Manim animations.

For arithmetic questions, use the available calculator tools.

For adding an expense, use add_expense.

For viewing expenses, use list_expenses.

For expense summaries, use summarize.

For a rotating triangle animation, use create_rotating_triangle.

For a rotating square animation, use create_square_animation.

For both animations, use create_both_animations if available.

For generated video information, use list_generated_videos if available.

When an animation tool returns status success and a video_path,
tell the user that the video was successfully generated.

Never claim a video was generated if the tool returns an error.

Always use an MCP tool when an appropriate tool is available.

Do not unnecessarily describe internal tool execution.
"""


@st.cache_resource
def initialize_mcp():

    async def load():

        client = MultiServerMCPClient(
            SERVERS
        )

        tools = await client.get_tools()

        return client, tools

    return asyncio.run(
        load()
    )


try:

    mcp_client, tools = initialize_mcp()

except Exception as error:

    st.error(
        "MCP connection failed."
    )

    st.exception(
        error
    )

    st.stop()


tool_map = {
    tool.name: tool
    for tool in tools
}


with st.sidebar:

    st.header(
        "🔧 MCP Tools"
    )

    st.write(
        f"Total tools: {len(tools)}"
    )

    for index, tool in enumerate(
        tools,
        start=1
    ):

        st.success(
            f"{index}. {tool.name}"
        )


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)


llm_with_tools = llm.bind_tools(
    tools
)


if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        content = message.get(
            "content",
            ""
        )

        if content:

            st.markdown(
                content
            )

        videos = message.get(
            "videos",
            []
        )

        for video in videos:

            if os.path.isfile(video):

                st.video(
                    video
                )


def parse_tool_result(result):

    if isinstance(
        result,
        dict
    ):

        return result

    if isinstance(
        result,
        list
    ):

        for item in result:

            if isinstance(
                item,
                dict
            ):

                text = item.get(
                    "text"
                )

                if text:

                    try:

                        return json.loads(
                            text
                        )

                    except Exception:

                        pass

        return {
            "status": "success",
            "raw": result
        }

    if isinstance(
        result,
        str
    ):

        try:

            return json.loads(
                result
            )

        except Exception:

            return {
                "status": "success",
                "message": result
            }

    return {
        "status": "success",
        "raw": str(result)
    }


def find_videos(data):

    videos = []

    if isinstance(
        data,
        dict
    ):

        video_path = data.get(
            "video_path"
        )

        if isinstance(
            video_path,
            str
        ):

            videos.append(
                video_path
            )

        video_paths = data.get(
            "video_paths"
        )

        if isinstance(
            video_paths,
            list
        ):

            videos.extend(
                video_paths
            )

        for value in data.values():

            if isinstance(
                value,
                (dict, list)
            ):

                videos.extend(
                    find_videos(
                        value
                    )
                )

    elif isinstance(
        data,
        list
    ):

        for item in data:

            videos.extend(
                find_videos(
                    item
                )
            )

    final_paths = []

    for path in videos:

        if not isinstance(
            path,
            str
        ):

            continue

        path = path.strip(
            "\"'"
        )

        if not os.path.isabs(
            path
        ):

            path = os.path.join(
                SERVER_DIR,
                path
            )

        path = os.path.normpath(
            path
        )

        if path not in final_paths:

            final_paths.append(
                path
            )

    return final_paths


async def execute_tool(
    tool_name,
    tool_args
):

    if tool_name not in tool_map:

        return {
            "status": "error",
            "message":
                f"Tool not found: {tool_name}"
        }

    return await tool_map[
        tool_name
    ].ainvoke(
        tool_args
    )


async def process_message(
    user_text
):

    messages = [

        SystemMessage(
            content=SYSTEM_PROMPT
        ),

        HumanMessage(
            content=user_text
        )

    ]

    response = await (
        llm_with_tools.ainvoke(
            messages
        )
    )

    if not response.tool_calls:

        return {
            "content":
                response.content or "",
            "videos": []
        }

    messages.append(
        response
    )

    videos = []

    for tool_call in response.tool_calls:

        tool_name = tool_call[
            "name"
        ]

        tool_args = (
            tool_call.get(
                "args"
            ) or {}
        )

        tool_id = tool_call[
            "id"
        ]

        try:

            result = await execute_tool(
                tool_name,
                tool_args
            )

            print(
                "MCP TOOL:",
                tool_name
            )

            print(
                "MCP ARGUMENTS:",
                tool_args
            )

            print(
                "MCP RESULT:",
                result
            )

            result_data = parse_tool_result(
                result
            )

        except Exception as error:

            result_data = {
                "status": "error",
                "message": str(error)
            }

        videos.extend(
            find_videos(
                result_data
            )
        )

        messages.append(
            ToolMessage(
                tool_call_id=tool_id,
                content=json.dumps(
                    result_data,
                    default=str
                )
            )
        )

    final_response = await (
        llm.ainvoke(
            messages
        )
    )

    return {
        "content":
            final_response.content or "",

        "videos":
            list(
                dict.fromkeys(
                    videos
                )
            )
    }


user_text = st.chat_input(
    "Ask anything..."
)


if user_text:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_text,
            "videos": []
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_text
        )

    with st.chat_message(
        "assistant"
    ):

        try:

            with st.spinner(
                "Thinking..."
            ):

                result = asyncio.run(
                    process_message(
                        user_text
                    )
                )

            content = result.get(
                "content",
                ""
            )

            if content:

                st.markdown(
                    content
                )

            videos = result.get(
                "videos",
                []
            )

            displayed_videos = []

            for video_path in videos:

                if os.path.isfile(
                    video_path
                ):

                    st.success(
                        "🎬 Video generated successfully!"
                    )

                    st.video(
                        video_path
                    )

                    with open(
                        video_path,
                        "rb"
                    ) as video_file:

                        st.download_button(
                            label="⬇️ Download video",
                            data=video_file.read(),
                            file_name=os.path.basename(
                                video_path
                            ),
                            mime="video/mp4"
                        )

                    displayed_videos.append(
                        video_path
                    )

                else:

                    st.warning(
                        "Video path returned but file was not found."
                    )

                    st.code(
                        video_path
                    )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": content,
                    "videos": displayed_videos
                }
            )

        except Exception as error:

            st.error(
                "❌ Error"
            )

            st.exception(
                error
            )