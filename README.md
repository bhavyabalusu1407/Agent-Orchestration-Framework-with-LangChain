# Agent-Orchestration Framework with LangChain

## Project Overview
This project demonstrates a multi-agent orchestration framework built using LangChain, FastAPI, and Streamlit.  
The system simulates intelligent, collaborative agents that can plan tasks, invoke tools, manage memory, and work together to automate multi-step workflows.

The project is developed week-wise (Week 1 to Week 8) following Agile methodology and milestone-based deliverables.

---

## Key Features

- Multi-agent collaboration: Research Agent, Summarizer Agent, Email Agent  
- Tool integration: Calculator, Mock APIs  
- Individual and shared memory management  
- REST API backend using FastAPI  
- Frontend UI using Streamlit  
- Workflow logging and evaluation feedback  
- Agile documentation and testing artifacts  

---

## Project Structure
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── .env.example
├── doc/
│ ├── Agile_Documentation.xlsx
│ ├── Sample_Defect_tracker.xlsx
| ├── Sample_Unit_Test_Plan.xlsx
├── src/
│ ├── week1.py
│ ├── week2.py
│ ├── week3.py
│ ├── week4.py
│ ├── week5.py
│ ├── week6.py
│ ├── week7.py # FastAPI Backend
│ └── week8.py # Streamlit Frontend
└── venv/


---

## Milestones Overview

### Milestone 1 (Weeks 1–2): Environment Setup & Basic Agent
- LangChain setup
- Prompt templates and LLM chains
- Console-based agent interaction

### Milestone 2 (Weeks 3–4): Tool Integration
- Calculator and mock APIs
- Tool invocation via agents
- Error handling

### Milestone 3 (Weeks 5–6): Multi-Agent Orchestration & Memory
- Research, Summarizer, Email agents
- Agent communication
- Individual and shared memory

### Milestone 4 (Weeks 7–8): Workflow Automation & UI
- Full workflow: Research → Summarize → Compose Email
- FastAPI backend with REST endpoints
- Streamlit frontend UI
- Logs, feedback, memory inspection

---

## How to Run the Project

1️⃣ Create and Activate Virtual Environment

bash
python -m venv venv
venv\Scripts\activate

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run FastAPI Backend (Week 7)

uvicorn src.week7:app --reload


Open API Docs: http://127.0.0.1:8000/docs

4️⃣ Run Streamlit Frontend (Week 8)

streamlit run src/week8.py


Open UI: http://localhost:8501


API Endpoints (Week 7)

| Method | Endpoint               | Description              |
| ------ | ---------------------- | ------------------------ |
| GET    | `/health`              | Health check             |
| POST   | `/agent/run`           | Run single agent         |
| POST   | `/workflow/run`        | Run full workflow        |
| POST   | `/workflow/step`       | Run workflow step        |
| GET    | `/memory/{agent_name}` | Get agent memory         |
| POST   | `/memory/reset`        | Reset all agent memory   |
| POST   | `/tools/test`          | Test tools               |
| GET    | `/agents`              | List available agents    |
| GET    | `/tools`               | List available tools     |
| POST   | `/evaluation/feedback` | Submit workflow feedback |
| GET    | `/logs/{workflow_id}`  | Get workflow logs        |


Run Single Agent
{
  "agent_name": "research",
  "input": "LangChain multi-agent systems"
}



Run Workflow

{
  "topic": "LangChain multi-agent systems",
  "recipient": "mentor@example.com"
}


Deployment

This project is currently demonstrated via:

Local Backend API: http://127.0.0.1:8000

Local Frontend UI: http://localhost:8501

Live Deployment: https://agent-orchestration-framework-with-beige.vercel.app/


Testing & Evaluation

Manual testing using Swagger UI

Workflow logs verified via /logs/{workflow_id}

Agent memory verified via /memory/{agent_name}

Feedback captured using /evaluation/feedback endpoint


Documentation Included

✅ Agile Documentation
✅ Unit Testing & Defect Tracker
✅ README File
✅ MIT License

License

This project is licensed under the MIT License.
See the LICENSE file for details.


Author

Bhavya Balusu