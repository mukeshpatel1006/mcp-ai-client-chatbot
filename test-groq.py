import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found")
    raise SystemExit

print("✅ GROQ_API_KEY found")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=api_key
)

try:
    response = llm.invoke(
        "Say hello in one short sentence."
    )

    print("\n✅ Groq API is working!")
    print("Response:")
    print(response.content)

except Exception as e:
    print("\n❌ Groq API failed!")
    print(type(e).__name__)
    print(e)