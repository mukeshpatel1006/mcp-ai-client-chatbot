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

**Complete Flow **

User
  │
  ▼
Streamlit
  │
  ▼
Groq
  │
  ▼
Determine required MCP tool
  │
  ▼
LangChain MCP Adapter
  │
  ├─────────────── Calculator
  │
  ├─────────────── Expense
  │
  └─────────────── Manim
  │
  ▼
MCP Server
  │
  ▼
Tool Execution
  │
  ▼
Tool Result
  │
  ▼
Groq
  │
  ▼
Final Response
  │
  ▼
Streamlit
