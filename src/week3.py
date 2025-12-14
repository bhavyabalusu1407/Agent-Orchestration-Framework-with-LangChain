#Week3 Tools+Basic Integration

from dotenv import load_dotenv
import os
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

#  Load environment variables

load_dotenv()

#  1: Define Tools 

# Calculator tool
def calculator(expression: str):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception:
        return "Calculator Error: Invalid expression."

calculator_tool = Tool(
    name="calculator",
    func=calculator,
    description="Calculate math expressions like '23+45'."
)

# Weather tool 
def weather(city: str):
    return f"Current temperature in {city} is {random.randint(15, 30)}°C"

weather_tool = Tool(
    name="weather",
    func=weather,
    description="Get current temperature of a city."
)

tools = [calculator_tool, weather_tool]

#  2: Initialize LLM

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    api_key=os.getenv("GOOGLE_API_KEY")
)


# 3: Create Agent

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


#  4: Test Agent

print("Tools-enabled Agent is ready! Type 'exit' to quit.")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break

    response = agent.invoke({"input": query})
    print("Agent:", response["output"])
