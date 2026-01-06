#Week 7: Backend API for Multi-Agent Workflow
from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from typing import Dict, List

app = FastAPI(title="Multi-Agent Orchestration API")

# In-memory storage 
agent_memory: Dict[str, List[str]] = {
    "research_agent": [],
    "summarizer_agent": [],
    "email_agent": []
}

workflow_logs: Dict[str, List[str]] = {}

tools = ["calculator", "mock_weather_api"]
agents = ["research_agent", "summarizer_agent", "email_agent"]

# Dummy Agent Implementation

def research_agent(topic: str) -> str:
    output = f"Research insights about {topic}. Covers concepts, use cases, and benefits."
    agent_memory["research_agent"].append(output)
    return output

def summarizer_agent(research_text: str) -> str:
    output = f"Summary: {research_text}"
    agent_memory["summarizer_agent"].append(output)
    return output

def email_agent(summary: str, recipient: str) -> Dict[str, str]:
    subject = "Overview of Research Topic"
    body = (
        f"Dear {recipient},\n\n"
        f"{summary}\n\n"
        "Best regards,\n"
        "AI Email Agent"
    )
    agent_memory["email_agent"].append(body)
    return {"subject": subject, "body": body}

# Request Models
class AgentRequest(BaseModel):
    agent_name: str
    input: str

class WorkflowRequest(BaseModel):
    topic: str
    recipient: str

class StepRequest(BaseModel):
    step: str
    data: str

class FeedbackRequest(BaseModel):
    workflow_id: str
    rating: int
    comments: str

# 1. Health Check
@app.get("/health")
def health():
    return {"status": "ok"}

# 2. Run Single Agent
@app.post("/agent/run")
def run_agent(request: AgentRequest):
    if request.agent_name == "research":
        output = research_agent(request.input)
    elif request.agent_name == "summarizer":
        output = summarizer_agent(request.input)
    elif request.agent_name == "email":
        output = email_agent(request.input, "User")
    else:
        return {"error": "Invalid agent name"}

    return {
        "agent": request.agent_name,
        "output": output
    }


# 3. Run Full Workflow
@app.post("/workflow/run")
def run_workflow(request: WorkflowRequest):
    workflow_id = str(uuid.uuid4())
    workflow_logs[workflow_id] = []

    research_output = research_agent(request.topic)
    workflow_logs[workflow_id].append("research_agent executed")

    summary_output = summarizer_agent(research_output)
    workflow_logs[workflow_id].append("summarizer_agent executed")

    email_output = email_agent(summary_output, request.recipient)
    workflow_logs[workflow_id].append("email_agent executed")

    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "steps_executed": agents,
        "email_generated": email_output
    }

# 4. Run Workflow Step
@app.post("/workflow/step")
def run_step(request: StepRequest):
    if request.step == "research":
        result = research_agent(request.data)
    elif request.step == "summarizer":
        result = summarizer_agent(request.data)
    else:
        return {"error": "Invalid workflow step"}

    return {
        "step": request.step,
        "result": result
    }

# 5. Get Agent Memory
@app.get("/memory/{agent_name}")
def get_memory(agent_name: str):
    return {
        "agent": agent_name,
        "memory": agent_memory.get(agent_name, [])
    }

# 6. Reset Memory
@app.post("/memory/reset")
def reset_memory():
    for agent in agent_memory:
        agent_memory[agent].clear()
    return {"message": "All agent memory reset successfully"}

# 7. Test Tools
@app.post("/tools/test")
def test_tools():
    return {
        "tool": "calculator",
        "input": "10 * 5",
        "output": 50
    }

# 8. Get Agents
@app.get("/agents")
def get_agents():
    return {"agents": agents
    }

# 9. Get Tools
@app.get("/tools")
def get_tools():
    return {"tools": tools}

# 10. Evaluation Feedback
@app.post("/evaluation/feedback")
def feedback(request: FeedbackRequest):
    return {
        "message": "Feedback recorded successfully",
        "data": request
    }

# 11. Workflow Logs
@app.get("/logs/{workflow_id}")
def get_logs(workflow_id: str):
    return {
        "workflow_id": workflow_id,
        "logs": workflow_logs.get(workflow_id, [])
    }
