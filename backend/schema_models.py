from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class ChatRequest(BaseModel):
    message: str
    employee_name: str
    employee_email: str
    session_id: Optional[str] = None

class TicketModel(BaseModel):
    ticket_id: str = ""
    employee_name: str
    employee_email: str
    issue_summary: str
    kb_used: Optional[str] = None
    decision: str  # "resolved" or "escalated"
    resolution: str
    timestamp: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        if not self.ticket_id:
            self.ticket_id = f"TK-{str(uuid.uuid4())[:6].upper()}"
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ChatResponse(BaseModel):
    response: str
    kb_used: Optional[str] = None
    decision: str  # "resolved", "escalated", "follow_up"
    ticket: Optional[TicketModel] = None
    session_id: str