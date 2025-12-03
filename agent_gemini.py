from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import Tool
from google.api_core.exceptions import ResourceExhausted
# Load environment variables
load_dotenv()
# 1️.Create LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 2️. Create a PromptTemplate
prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
You are a helpful AI assistant. Explain the topic below in simple, easy-to-understand language:

Topic: {topic}
"""
)

# 3️. Create a Chain (LLM + Prompt)

chain = LLMChain(llm=llm, prompt=prompt)

# 4️. Generate response with error handling

topic = "LangChain in simple words"
result = chain.run({"topic": topic})
print("LLM Output via Chain:\n", result)

# Week 2
# 1. Define a simple tool
def greet(name: str):
    return f"Hello {name}, welcome to your Gemini Agent!"

greet_tool = Tool(
    name="greet",
    func=greet,
    description="Greets a user by name"
)

# 2 .Test the tool
test_name = "Bhavya"
tool_output = greet_tool.run(test_name)
print("\n - Tool Output:", tool_output)

# 3. Optional: Interactive Console
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": user_input}
    ]
    response = llm.invoke(messages)
    print("Agent:", response.content)