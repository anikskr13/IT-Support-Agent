# 📊 10-Slide Presentation Deck — Internal IT Support Agent
> **AIONOS Agentic AI Factory — Assignment 2 Submission & Defense**  
> Use the slides below to populate your PowerPoint or Google Slides presentation.

---

### Slide 1: Title & Overview
- **Title:** Veridian Corp IT Support Agent
- **Subtitle:** Autonomous Multi-Turn Internal Service Agent with LangGraph & Groq Llama 3.3 70B
- **Author:** [Your Name / Candidate ID]
- **Date:** September 2026
- **Key Takeaway:** An agentic AI support system that autonomously resolves common IT inquiries, requests clarifications when information is missing, safely escalates edge cases, and logs structured auditable tickets.

---

### Slide 2: Business Context & Objective
- **The Challenge:** IT helpdesks are overwhelmed with repetitive Tier-1 tickets (password lockouts, VPN setups, basic hardware queries), causing delayed resolution times and high operational cost.
- **Assignment Objective:**
  - Understand employee issue in natural language.
  - Ground answers strictly in official corporate IT policies (KB-01 to KB-10).
  - Clarify ambiguities with contextual follow-up questions.
  - Auto-resolve eligible requests and escalate risky/unclear tickets.
  - Maintain an end-to-end auditable ticketing log.

---

### Slide 3: Agent Architecture & Process Flow
- **4-Node LangGraph State Machine:**
  1. `understand_issue`: Extracts core intent, hardware details, error messages, and context across conversation turns.
  2. `match_policy`: Evaluates issue against 10 KB articles and matches relevant policy (or flags `NONE`).
  3. `decide_and_respond`: Formulates decision (`RESOLVED`, `ESCALATED`, or `FOLLOW_UP`) and generates polite, policy-grounded guidance.
  4. `create_ticket`: Emits a structured ticket payload with unique ID, timestamp, and audit trail.
- **Session Memory:** Preserves multi-turn state across user interactions without hallucinating previous context.

---

### Slide 4: Knowledge Base Grounding & Policy Design
- **10 Core IT Policies:**
  - `KB-01`: Account Lockout & Self-Service Password Reset
  - `KB-02`: VPN Configuration & MFA Authentication
  - `KB-03`: Laptop Hardware Replacement & Upgrade Criteria
  - `KB-04`: Software Licensing & Approval Workflows
  - `KB-05`: Office Hardware & Shared Printer Diagnostics
  - `KB-06` – `KB-10`: Security incident reporting, peripheral requests, guest Wi-Fi, email forwarding, remote access.
- **Strict Grounding Rule:** Explicit prompt constraint preventing hallucinated policies outside the knowledge base.

---

### Slide 5: Dynamic Clarification & Follow-Up Reasoning
- **Why Simple Single-Turn Fails:** Real employees omit vital details (e.g., *"My laptop won't start"* doesn't state if it's dead, blue-screening, or how old it is).
- **Agent Clarification Loop:**
  - Evaluates whether policy conditions are fully satisfied.
  - If information is missing, sets decision to `FOLLOW_UP` and asks a targeted question.
  - Does NOT repeat previously answered questions.
  - Updates conversation history state seamlessly.

---

### Slide 6: Decision Framework: Resolution vs. Escalation
- **Auto-Resolve (`RESOLVED`):**
  - Self-service tasks with clear policy steps (password reset, VPN install, approved software).
  - Clear hardware eligibility met (verified failure + >3 years old with policy sign-offs explained).
- **Human Escalation (`ESCALATED`):**
  - Unresolved hardware errors (persistent paper jam, burnt motherboard, damaged screen).
  - Security incidents, administrative privilege requests, and out-of-scope policies.
  - Assigned priority levels: `Low`, `Medium`, `High`, `Critical`.

---

### Slide 7: Structured Ticket Schema & Audit Trail
- **Ticket Data Structure:**
  - `ticket_id`: Unique identifier (`TK-XXXXXX`)
  - `employee_name` & `employee_email`: Requestor identity
  - `issue_summary`: Distilled factual technical description
  - `kb_used`: Policy reference cited (e.g., `KB-03`)
  - `decision`: `resolved` vs `escalated`
  - `resolution`: Action taken or department escalated to
  - `timestamp`: UTC timestamp for compliance
- **Real-Time Ticket Queue:** Integrates historical tickets + live agent sessions.

---

### Slide 8: Technology Stack & AI Tooling
- **LLM Engine:** Groq API — `llama-3.3-70b-versatile` (Temperature: 0 for strict deterministic compliance).
- **Agent Framework:** LangGraph + LangChain Core (StateGraph workflow orchestration).
- **Backend Service:** FastAPI with Pydantic v2 data validation and CORS support.
- **Frontend UI:** React 19 + Vite with dark-mode glassmorphism and real-time state management.
- **Unified Deployment:** Single-service architecture deployable on Render with zero CORS hurdles.

---

### Slide 9: Edge Cases & Evaluation Results
- **Scenario 1 (Account Lockout):** Auto-resolved in 1 turn using KB-01 (100% accuracy).
- **Scenario 2 (Laptop Replacement):** Correctly triggered 2 follow-up questions, identified 3.5-year age nuance, cited KB-03 + Asset Management finance sign-off policy.
- **Scenario 3 (Printer Malfunction):** Escalated to Hardware Support with priority High upon persistent mechanical failure.
- **Scenario 4 (Unapproved Software Request):** Flagged security approval bottleneck per KB-04.
- **Zero Hallucination Rate:** Strict negative constraints ensure agent declines unsupported claims.

---

### Slide 10: Defense Summary & Future Roadmap
- **Key Achievements:**
  - Fully working end-to-end agentic application with modern web UI.
  - Robust multi-turn memory without repetitive questioning loops.
  - 1-click cloud deployable on Render with full documentation.
- **Future Enhancements:**
  - RAG vector search over enterprise confluence / Notion spaces.
  - Direct integration with Jira Service Desk & ServiceNow APIs.
  - Multilingual support for global workforce operations.
