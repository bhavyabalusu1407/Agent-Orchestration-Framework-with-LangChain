# WEEK 5: Multi-Agent Orchestration with Individual Memory
# Roles: Research Agent, Summarizer Agent
# Memory: ConversationBufferMemory (per agent)

from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool

# 1. Load Environment Variables
load_dotenv()

# 2. Initialize LLM 
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 3. Define Tools

def research_tool(topic: str) -> str:
    return f"Research on '{topic}': definition, background, applications, and challenges."

def summarize_tool(text: str) -> str:
    return f"Summary: {text[:200]}..."

research_tool_langchain = Tool(
    name="research_tool",
    func=research_tool,
    description="Use this tool to research a topic and return key insights."
)

summarize_tool_langchain = Tool(
    name="summarize_tool",
    func=summarize_tool,
    description="Use this tool to summarize research content."
)

# 4. Individual Memories 

research_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

summary_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
# 5. Create Agents

research_agent = initialize_agent(
    tools=[research_tool_langchain],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=research_memory,
    verbose=True
)

summarizer_agent = initialize_agent(
    tools=[summarize_tool_langchain],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=summary_memory,
    verbose=True
)

# 6. Orchestrator (Agent Communication)

def run_pipeline(user_query: str):
    print("\n--- Research Agent ---")
    research_output = research_agent.run(
        f"Research the topic and give key points: {user_query}"
    )

    print("\n--- Summarizer Agent ---")
    summary_output = summarizer_agent.run(
        f"Summarize the following content:\n{research_output}"
    )

    return research_output, summary_output

# 7. Run Application

if __name__ == "__main__":
    print("Multi-Agent System Ready")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Enter topic: ")
        if query.lower() == "exit":
            break

        research, summary = run_pipeline(query)

        print("\n===== FINAL OUTPUT =====")
        print("Research Output:\n", research)
        print("\nSummary Output:\n", summary)
        print("========================\n")
