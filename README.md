# 🤖 MCP AI Assistant — Groq + MCP + Manim + Expense Tracker

An AI-powered Streamlit chatbot that connects a Groq LLM with multiple MCP servers.

The system can perform mathematical calculations, manage expenses, generate Manim animations, display generated videos, and provide AI-powered responses through a Streamlit chat interface.

---

# 🚀 Project Overview

This project is divided into two separate repositories:

1. **MCP Server**
2. **AI Client / Streamlit Chatbot**

The MCP server provides the actual tools, while the client provides the AI chatbot interface.

## MCP Server Repository

```text
https://github.com/mukeshpatel1006/mcp-math-manim-server

https://github.com/mukeshpatel1006/mcp-ai-client-chatbot

                         ┌─────────────────────────┐
                         │          USER           │
                         │                         │
                         │ "50 divided by 8?"      │
                         │ "Add ₹500 food expense" │
                         │ "Create triangle"       │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     STREAMLIT CLIENT     │
                         │       client2.py         │
                         │                         │
                         │   Chat Interface        │
                         │   Video Player          │
                         │   Download Video        │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       GROQ LLM           │
                         │                          │
                         │   openai/gpt-oss-120b   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                   ┌────────────────────────────────────┐
                   │       LANGCHAIN MCP ADAPTER       │
                   │                                    │
                   │      MultiServerMCPClient          │
                   └───────────────┬────────────────────┘
                                   │
                     MCP STDIO     │
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
              ▼                                         ▼
┌───────────────────────────────┐       ┌──────────────────────────────┐
│     MCP MATH / EXPENSE        │       │       MCP MANIM SERVER       │
│          SERVER               │       │                              │
│                               │       │      manim_server.py         │
│          main.py              │       │                              │
└───────────────┬───────────────┘       └──────────────┬───────────────┘
                │                                      │
       ┌────────┼─────────┐                            ▼
       │        │         │                     ┌──────────────┐
       ▼        ▼         ▼                     │    MANIM     │
   Calculator Expenses  Summary                 │   Renderer   │
       │        │         │                     └──────┬───────┘
       │        │         │                            │
       │        │         │                            ▼
       │        │         │                     ┌──────────────┐
       │        │         │                     │  MP4 VIDEO   │
       │        │         │                     └──────┬───────┘
       │        │         │                            │
       └────────┴─────────┴────────────────────────────┘
                            │
                            ▼
                   ┌────────────────────┐
                   │   STREAMLIT UI     │
                   │                    │
                   │  🎬 Video Player   │
                   │  ⬇️ Download       │
                   └────────────────────┘

**Complete Flow **                   User
                   │
                   ▼
            Streamlit Chat
                   │
                   ▼
                Groq
                   │
                   ▼
      create_rotating_triangle
                   │
                   ▼
             MCP Protocol
                   │
                   ▼
         manim_server.py
                   │
                   ▼
                Manim
                   │
                   ▼
             Render MP4
                   │
                   ▼
          manim_output/videos
                   │
                   ▼
          Return video_path
                   │
                   ▼
             Streamlit
              │        │
              ▼        ▼
            Play    Download

Video Architecture

                  User
                   │
                   ▼
            Streamlit Chat
                   │
                   ▼
                Groq
                   │
                   ▼
      create_rotating_triangle
                   │
                   ▼
             MCP Protocol
                   │
                   ▼
         manim_server.py
                   │
                   ▼
                Manim
                   │
                   ▼
             Render MP4
                   │
                   ▼
          manim_output/videos
                   │
                   ▼
          Return video_path
                   │
                   ▼
             Streamlit
              │        │
              ▼        ▼
            Play    Download

🏠 Local Development Structure

C:\Users\Mukesh Patel\Desktop\
│
├── MCP-MATH-SERVER\
│   │
│   ├── main.py
│   ├── manim_server.py
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .venv\
│   │
│   └── manim_output\
│
└── youtube-mcp-client\
    │
    ├── client1.py
    ├── client2.py
    ├── pyproject.toml
    ├── uv.lock
    ├── .env
    └── .venv\
