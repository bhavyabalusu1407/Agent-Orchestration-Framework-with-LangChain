#Week 8: Frontend UI for Multi-Agent Workflow

import streamlit as st
import requests
# Config
API_URL = "http://127.0.0.1:8000"  # Your FastAPI backend

st.set_page_config(page_title="Multi-Agent Workflow UI", page_icon="🤖", layout="centered")
st.title("Multi-Agent Orchestration Dashboard ")

st.markdown("""
This UI allows you to:
- Run full workflows
- Run individual agents
- View agent memory
- Reset memory
- View workflow logs
""")

# Sidebar Navigation
menu = ["Run Full Workflow", "Run Single Agent", "Agent Memory", "Reset Memory", "Workflow Logs"]
choice = st.sidebar.selectbox("Choose Action", menu)

# 1. Run Full Workflow
if choice == "Run Full Workflow":
    st.subheader("Run Full Workflow: Research → Summarize → Compose Email")
    topic = st.text_input("Topic for Research", "LangChain Multi-Agent Systems")
    recipient = st.text_input("Recipient Email", "mentor@example.com")
    if st.button("Run Workflow"):
        payload = {"topic": topic, "recipient": recipient}
        response = requests.post(f"{API_URL}/workflow/run", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success(f"Workflow Completed! ID: {data['workflow_id']}")
            st.write("**Steps Executed:**", data["steps_executed"])
            st.write("**Generated Email:**")
            st.code(f"Subject: {data['email_generated']['subject']}\n\n{data['email_generated']['body']}")
        else:
            st.error("Workflow failed. Check backend.")

# 2. Run Single Agent
elif choice == "Run Single Agent":
    st.subheader("Run Single Agent")
    agent_name = st.selectbox("Select Agent", ["research", "summarizer", "email"])
    input_text = st.text_area("Input Data")
    if st.button("Run Agent"):
        payload = {"agent_name": agent_name, "input": input_text}
        response = requests.post(f"{API_URL}/agent/run", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success(f"Agent Output:")
            st.code(data["output"])
        else:
            st.error("Agent execution failed.")

# 3. View Agent Memory
elif choice == "Agent Memory":
    st.subheader("View Agent Memory")
    agent_name = st.selectbox("Select Agent", ["research_agent", "summarizer_agent", "email_agent"])
    if st.button("Show Memory"):
        response = requests.get(f"{API_URL}/memory/{agent_name}")
        if response.status_code == 200:
            data = response.json()
            st.write(f"Memory for {agent_name}:")
            for i, item in enumerate(data["memory"], 1):
                st.write(f"{i}. {item}")
        else:
            st.error("Failed to fetch memory.")

# 4. Reset Memory
elif choice == "Reset Memory":
    st.subheader("Reset All Agent Memory")
    if st.button("Reset Memory"):
        response = requests.post(f"{API_URL}/memory/reset")
        if response.status_code == 200:
            st.success("All agent memory reset successfully!")
        else:
            st.error("Memory reset failed.")

# 5. View Workflow Logs
elif choice == "Workflow Logs":
    st.subheader("View Workflow Logs")
    workflow_id = st.text_input("Enter Workflow ID")
    if st.button("Get Logs"):
        response = requests.get(f"{API_URL}/logs/{workflow_id}")
        if response.status_code == 200:
            data = response.json()
            st.write(f"Workflow ID: {workflow_id}")
            st.write("Steps Executed:")
            for step in data.get("logs", []):
                st.write(f"- {step}")
        else:
            st.error("Failed to fetch workflow logs.")
