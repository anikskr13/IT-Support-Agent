import os
import uuid
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schema_models import ChatRequest, ChatResponse
from agent import agent
from data import EXISTING_TICKETS

app = FastAPI(title="IT Support Agent — Veridian Corp")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pre-load existing ticket queue from data.py ───────────────────────────────
def _status_to_decision(status: str) -> str:
    s = status.lower()
    if "resolved" in s or "rejected" in s or "approved" in s:
        return "resolved"
    return "escalated"

tickets_store = [
    {
        "ticket_id": t["id"],
        "employee_name": t["employee"],
        "employee_email": "",
        "issue_summary": t["issue"],
        "kb_used": None,
        "decision": _status_to_decision(t["status"]),
        "resolution": t["status"],
        "timestamp": "2026-09-18 (pre-existing)"
    }
    for t in EXISTING_TICKETS
]

# ── Session memory: session_id → conversation history ────────────────────────
session_memory: dict = {}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ── Health check endpoint ───────────────────────────────────────────────────
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "IT Support Agent — Veridian Corp"}


# ── Chat endpoint ─────────────────────────────────────────────────────────────
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    # Retrieve or init conversation history
    history = session_memory.get(session_id, [])
    history.append({"role": "user", "content": request.message})

    result = agent.invoke({
        "message": request.message,
        "employee_name": request.employee_name,
        "employee_email": request.employee_email,
        "issue_summary": "",
        "kb_used": None,
        "decision": "",
        "response": "",
        "ticket": None,
        "conversation_history": history
    })

    # Save agent response to history
    history.append({"role": "agent", "content": result["response"]})
    session_memory[session_id] = history

    # Only store ticket if one was created (not for follow_up)
    if result.get("ticket"):
        tickets_store.append(result["ticket"])

    return ChatResponse(
        response=result["response"],
        kb_used=result["kb_used"],
        decision=result["decision"],
        ticket=result.get("ticket"),
        session_id=session_id
    )


# ── Tickets endpoint ──────────────────────────────────────────────────────────
@app.get("/tickets")
def get_tickets():
    return {"tickets": tickets_store}


# ── Serve Frontend SPA (Production / Unified Single Service) ─────────────────
FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))

if os.path.exists(FRONTEND_DIST):
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    def serve_root():
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        # Don't intercept API paths or docs
        if full_path in ("docs", "redoc", "openapi.json", "chat", "tickets", "api/health"):
            return None
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
else:
    @app.get("/")
    def root():
        return {"status": "IT Support Agent backend running. Frontend not built."}