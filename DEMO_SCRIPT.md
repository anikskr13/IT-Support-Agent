# 🎥 Demo Video Script & Defense Guide (Assignment 2: Internal Service Agent)

> **Duration:** 3–5 minutes  
> **Format:** Screen recording with voiceover (Loom, OBS, or Windows Game Bar `Win + G`)  
> **Upload:** Upload to Google Drive, set sharing permissions to **"Anyone with the link can view"**, and paste the link in `README.md` and the submission form.

---

## 🕒 Video Outline & Timing

| Segment | Time | Screen / Action | What to Say |
|---|---|---|---|
| **1. Introduction** | 0:00 - 0:40 | Show the Home Screen with header, employee profile selector, and ticket counter. | *"Hello everyone. Today I'm presenting Assignment 2 from the Agentic AI Factory: an Internal IT Support Agent built for Veridian Corp employees. The agent is built with a 4-node LangGraph pipeline on FastAPI and a React glassmorphic UI."* |
| **2. Architecture Overview** | 0:40 - 1:15 | Show the Architecture diagram in `README.md` or Slide 3. | *"Under the hood, the agent follows a 4-step cyclical workflow: Understand the Issue, Match IT Policy from 10 KB articles, Decide and Respond with session memory, and Create an Auditable Ticket. It uses Llama 3.3 70B via Groq for high-precision policy reasoning."* |
| **3. Test Demo 1: Auto-Resolution** | 1:15 - 2:00 | Click John Doe, type: `"I am locked out of my account after multiple failed password attempts"` | *"Let's test our first scenario: an employee locked out. The agent processes the message, consults KB-01, recognizes the 30-minute lockout rule, provides step-by-step password reset instructions, and marks it RESOLVED with a green badge. Notice the Ticket Panel instantly updates with ticket ID TK-... and timestamp."* |
| **4. Test Demo 2: Follow-up Clarification** | 2:00 - 2:50 | Type: `"My laptop won't turn on at all, had it about 3.5 years now"` | *"In the second scenario, the employee asks for a laptop replacement. Notice the agent doesn't jump to a hasty decision—it recognizes that KB-03 requires a verified hardware failure and asks a clarifying follow-up question with an amber Follow-up badge."* |
| **5. Multi-turn Resolution** | 2:50 - 3:35 | Reply: `"It is completely dead, no lights and technician confirmed motherboard failure"` | *"When the employee confirms verified hardware failure, the agent maintains full conversation memory across turns. It notes that at 3.5 years it qualifies for replacement under KB-03, but since it's under 4 years, both IT approval and Finance sign-off are required per Asset Management policy."* |
| **6. Test Demo 3: Escalation** | 3:35 - 4:15 | Click Sarah Jenkins, type: `"The printer on the 3rd floor is showing a paper jam error even though there is no paper stuck"` | *"Next, a persistent hardware printer issue. When basic spooler steps fail, the agent correctly escalates under KB-05 to hardware technicians with priority 'High', showing an amber Escalated badge."* |
| **7. Ticket Queue & Audit Trail** | 4:15 - 4:45 | Scroll the right-hand Ticket Panel showing pre-existing + newly created tickets. | *"Every interaction logs a structured ticket containing Ticket ID, Employee name, Issue Summary, KB Policy reference, Decision, and Timestamp. This maintains a complete audit trail."* |
| **8. Conclusion & Defense Summary** | 4:45 - 5:00 | Show GitHub repo & live deployed link. | *"In summary, the agent handles clear resolutions, safe escalations, and intelligent follow-ups without hallucinating policies. The full source code, test suites, and deployment blueprints are available on GitHub. Thank you!"* |

---

## 💡 Quick Tips for Recording
1. **Resolution:** 1080p (1920x1080) recommended.
2. **Audio:** Use a clean microphone or headset; avoid background noise.
3. **Cursor:** Enable mouse pointer highlights if available.
4. **Google Drive Permission:** **CRITICAL!** Right-click the video file in Google Drive → Share → Change "Restricted" to **"Anyone with the link" (Viewer)**.
