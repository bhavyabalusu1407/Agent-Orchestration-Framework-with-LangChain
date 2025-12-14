
# Week 4: Tool Reasoning + Prompting + Error Handling

from dotenv import load_dotenv
import os
import random

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

#  Load environment variables

load_dotenv()

#  1: Define Tools


# Calculator Tool
def calculator(expression: str):
    try:
        result = eval(expression)  # demo purpose only
        return f"Result: {result}"
    except Exception:
        return "Calculator Error: Invalid expression."

# Weather Tool with simulated API failure
def weather(city: str):
    if random.random() < 0.2:
        return f"Weather API Error: Unable to fetch weather for {city}."
    return f"Current temperature in {city} is {random.randint(15, 30)}°C"

calculator_tool = Tool(
    name="calculator",
    func=calculator,
    description="Use this tool for mathematical calculations like '12*5'."
)

weather_tool = Tool(
    name="weather",
    func=weather,
    description="Use this tool to get the current temperature of a city."
)

tools = [calculator_tool, weather_tool]


#  2: System Prompt 

SYSTEM_PROMPT = """
You are a tool-using AI agent. Follow these rules strictly:

1. Use the CALCULATOR tool for any math-related query.
2. Use the WEATHER tool for any weather-related query.
3. If the user asks for both math and weather, use both tools.
4. If a tool returns an error, apologize and provide a helpful response.
5. Clearly explain the final answer to the user.
"""

#  3: Initialize LLM

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    api_key=os.getenv("GOOGLE_API_KEY")
)


# 4: Create Agent

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    system_message=SYSTEM_PROMPT
)

# 5: Run Agent

print("Week 4 Tools-enabled LangChain Agent is ready!")
print("Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break

    try:
        response = agent.run(query)
    except Exception as e:
        response = f"Agent Error: {str(e)}"

    print("Agent:", response)
