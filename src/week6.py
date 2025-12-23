
# WEEK 6: Shared Memory + Collaborative Reasoning
# Agents: Research Agent, Summarizer Agent
# Memory: Shared VectorStoreRetrieverMemory (FAISS)
from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.agents import initialize_agent, AgentType
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import FAISS
from langchain.tools import Tool

# 1. Load Environment Variables

load_dotenv()

# 2. Initialize Gemini LLM

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 3. Create SHARED VECTOR MEMORY (Week 6 Core)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vectorstore = FAISS.from_texts(
    texts=[],
    embedding=embeddings
)

shared_memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever()
)

# 4. Define Tools
def research_tool(topic: str) -> str:
    return (
        f"Research on '{topic}': "
        "definition, real-world applications, advantages, and limitations."
    )

def summarize_tool(text: str) -> str:
    return f"Summary: {text[:300]}..."

research_tool_langchain = Tool(
    name="research_tool",
    func=research_tool,
    description="Research a topic and return detailed insights."
)

summarize_tool_langchain = Tool(
    name="summarize_tool",
    func=summarize_tool,
    description="Summarize the provided research content."
)

# 5. Create Agents 
research_agent = initialize_agent(
    tools=[research_tool_langchain],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=shared_memory,
    verbose=True
)

summarizer_agent = initialize_agent(
    tools=[summarize_tool_langchain],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=shared_memory,
    verbose=True
)

# 6. Orchestrator Pipeline

def run_pipeline(user_query: str):
    print("\n Research Agent Phase")
    research_output = research_agent.invoke(
        {"input": f"Research the following topic thoroughly: {user_query}"}
    )["output"]

    # Store research result in shared memory
    shared_memory.save_context(
        {"input": user_query},
        {"output": research_output}
    )

    print("\n Summarizer Agent Phase")
    summary_output = summarizer_agent.invoke(
        {"input": f"Summarize the research below:\n{research_output}"}
    )["output"]

    return research_output, summary_output


# 7. Run Application
if __name__ == "__main__":
    print("  Shared-Memory Multi-Agent System Ready")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Enter research topic: ")

        if query.lower() == "exit":
            break

        try:
            research, summary = run_pipeline(query)

            print("\n========== FINAL OUTPUT ==========")
            print("Research Output:\n", research)
            print("\nSummary Output:\n", summary)
            print("=================================\n")

        except Exception as e:
            print(" Agent Error:", str(e))
