# Week 1: LLM Basics using LangChain

from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

# 1. Create LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. Create Prompt Template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
You are a helpful AI assistant.
Explain the following topic in simple, easy-to-understand language.

Topic: {topic}
"""
)

# 3. Create Chain (LLM + Prompt)
chain = LLMChain(llm=llm, prompt=prompt)

# 4. Run the chain
topic = "LangChain in simple words"
result = chain.run({"topic": topic})

print("Week 1 Output:\n", result)
