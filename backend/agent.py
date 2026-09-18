import os
from dotenv import load_dotenv
from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from kb import get_kb_as_text
from schema_models import TicketModel

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-20b",
    temperature=0
)

class AgentState(TypedDict):
    message: str
    employee_name: str
    employee_email: str
    issue_summary: str
    kb_used: Optional[str]
    decision: str
    response: str
    ticket: Optional[dict]
    conversation_history: List[dict]  # [{"role": "user"/"agent", "content": str}]

SYSTEM_PROMPT = f"""
You are an IT support agent for Veridian Corp.
You help employees resolve IT issues based strictly on the following knowledge base.
Do NOT invent any policy or information not present in the knowledge base.

KNOWLEDGE BASE:
{get_kb_as_text()}

ASSET MANAGEMENT POLICY (Critical — read carefully):
- All company hardware follows a STANDARD 4-YEAR refresh cycle from date of issue.
- KB-03 says laptops are eligible after 3 years OR hardware failure — but this means IT approval only.
- If the laptop is UNDER 4 years old: replacement ALSO requires Finance sign-off in addition to IT approval.
- If the laptop is 4 years or older: IT approval alone is sufficient, no Finance sign-off needed.
- Always tell the employee whether Finance sign-off is required based on the laptop age.

ESCALATION RULES — you MUST escalate (do not resolve yourself) when:
- Employee requests admin or elevated server access
- Security incident is reported (phishing, malware, unauthorized access)
- Request is completely vague and you cannot determine the issue
- Issue is outside IT scope (e.g. expense tool access — that is Finance)
- Any request that has no matching KB article

FOLLOW-UP RULES — ask ONE clarifying question when:
- You need one key piece of info to decide RESOLVED vs ESCALATED
- E.g. laptop issue: ask if it's a verified hardware failure or just won't charge
- E.g. expense tool: ask if their account already exists in the system
- E.g. printer: ask for the asset tag if they haven't provided it
- E.g. screen flickering: ask if the issue is consistent or intermittent
- Do NOT ask follow-up if the issue is already clear enough to decide

RESOLUTION RULES — you CAN resolve when:
- Issue clearly matches a KB article
- Resolution is straightforward (e.g. tell them to use self-service portal, guest wifi kiosk)
- No approval or elevated access is needed

Always cite which KB article you used (e.g. KB-01, KB-07).
"""

def format_history(history: List[dict]) -> str:
    """Format conversation history for prompt context (exclude current message)."""
    if not history or len(history) <= 1:
        return "No prior conversation."
    prior = history[:-1]  # exclude the current user message
    lines = []
    for msg in prior:
        role = "Employee" if msg["role"] == "user" else "Agent"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)

def understand_issue(state: AgentState) -> AgentState:
    # Only include EMPLOYEE messages from history (not agent questions/responses)
    history = state.get("conversation_history", [])
    employee_msgs = [m["content"] for m in history if m["role"] == "user"]
    employee_context = "\n".join(f"- {msg}" for msg in employee_msgs[:-1]) if len(employee_msgs) > 1 else "No prior messages."

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""
        Employee: {state['employee_name']}
        Current message: {state['message']}
        Previous employee statements:
        {employee_context}

        Summarize the complete IT issue based ONLY on what the EMPLOYEE has said.
        Include ALL factual details the employee has provided across all their messages.
        Do NOT include agent questions or responses in the summary.
        Example: "Laptop is 3.5 years old, completely dead with no lights. Employee says technician confirmed dead motherboard."
        Reply with ONLY the issue summary, nothing else.
        """)
    ]
    result = llm.invoke(messages)
    state['issue_summary'] = result.content.strip()
    return state

def match_policy(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""
        Issue: {state['issue_summary']}

        Which KB article applies to this issue?
        Reply with ONLY a valid KB article ID in the exact format KB-XX (e.g. KB-01, KB-03).
        If no KB article applies, reply with exactly: NONE
        Do NOT reply with questions, sentences, or anything other than the KB ID or NONE.
        """)
    ]
    result = llm.invoke(messages)
    kb = result.content.strip()
    # Safety: if response is not a valid KB ID or NONE, default to NONE
    import re
    if not re.match(r'^KB-\d{2}$', kb) and kb != 'NONE':
        kb = 'NONE'
    state['kb_used'] = kb
    return state

def decide_and_respond(state: AgentState) -> AgentState:
    history_text = format_history(state.get("conversation_history", []))
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""
        Employee: {state['employee_name']}
        Issue summary (complete picture): {state['issue_summary']}
        KB Article: {state['kb_used']}
        Prior conversation:
        {history_text}

        CRITICAL RULES BEFORE DECIDING:
        - Read the FULL conversation history above carefully.
        - If a question was already asked and the employee has answered it, do NOT ask it again.
        - If the employee said "I don't know", "not sure", or cannot answer → do NOT ask again. ESCALATE immediately so IT can investigate.
        - Count the number of agent messages in the history. If there are already 2 or more agent responses, you MUST make a FINAL decision (RESOLVED or ESCALATED) right now — no more FOLLOW_UP allowed.
        - If the issue summary already contains enough information to decide, make the decision NOW.
        - Only choose FOLLOW_UP on the FIRST response if one specific key piece of info is missing.

        Based on the KB article, escalation rules, and follow-up rules:
        1. Decide: RESOLVED, ESCALATED, or FOLLOW_UP?
           - FOLLOW_UP: ONLY if a key unanswered question still remains
           - RESOLVED: if issue clearly maps to KB and can be resolved
           - ESCALATED: if issue requires human intervention per escalation rules
        2. Write a professional response to the employee.
        3. If FOLLOW_UP: ask exactly one NEW clarifying question not already asked.
        4. If RESOLVED: explain the resolution steps based on the KB article.
        5. If ESCALATED: explain why and say a human agent will follow up.

        Reply in this exact format:
        DECISION: resolved OR escalated OR follow_up
        RESPONSE: your response to the employee here
        """)
    ]
    result = llm.invoke(messages)
    content = result.content.strip()

    lines = content.split('\n')
    decision_line = next((l for l in lines if l.startswith('DECISION:')), 'DECISION: escalated')

    # Capture full multi-line response after RESPONSE:
    response_idx = next((i for i, l in enumerate(lines) if l.startswith('RESPONSE:')), None)
    if response_idx is not None:
        first_line = lines[response_idx].replace('RESPONSE:', '').strip()
        remaining = '\n'.join(lines[response_idx + 1:]).strip()
        full_response = (first_line + '\n' + remaining).strip()
    else:
        full_response = 'Your request has been escalated.'

    state['decision'] = decision_line.replace('DECISION:', '').strip().lower()
    state['response'] = full_response
    return state

def create_ticket(state: AgentState) -> AgentState:
    # Only create a ticket for resolved or escalated — not for follow_up
    if state['decision'] in ('resolved', 'escalated'):
        ticket = TicketModel(
            employee_name=state['employee_name'],
            employee_email=state['employee_email'],
            issue_summary=state['issue_summary'],
            kb_used=state['kb_used'],
            decision=state['decision'],
            resolution=state['response']
        )
        state['ticket'] = ticket.model_dump()
    else:
        state['ticket'] = None
    return state

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("understand_issue", understand_issue)
    graph.add_node("match_policy", match_policy)
    graph.add_node("decide_and_respond", decide_and_respond)
    graph.add_node("create_ticket", create_ticket)

    graph.set_entry_point("understand_issue")
    graph.add_edge("understand_issue", "match_policy")
    graph.add_edge("match_policy", "decide_and_respond")
    graph.add_edge("decide_and_respond", "create_ticket")
    graph.add_edge("create_ticket", END)

    return graph.compile()

agent = build_graph()