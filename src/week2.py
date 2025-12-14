# Week 2: Tool Basics using LangChain

from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool

# Load environment variables
load_dotenv()

# Create LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 1. Define a simple tool
def greet(name: str):
    return f"Hello {name}, welcome to your Gemini Agent!"

greet_tool = Tool(
    name="greet",
    func=greet,
    description="Greets a user by name"
)

# 2. Test the tool
test_name = "Bhavya"
tool_output = greet_tool.run(test_name)
print("Week 2 Tool Output:", tool_output)

# 3. Optional: Interactive LLM chat 
print("\nType 'exit' to quit")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = llm.invoke(user_input)
    print("LLM:", response.content)
