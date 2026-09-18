import { useRef, useEffect, useState } from 'react';
import MessageBubble from './MessageBubble';
import { sendMessage } from '../api';

export default function ChatPanel({ employee, onNewTicket }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-resize textarea
  function handleInputChange(e) {
    setInput(e.target.value);
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = 'auto';
      ta.style.height = Math.min(ta.scrollHeight, 120) + 'px';
    }
  }

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;

    // Add user message
    const userMsg = { role: 'user', text, time: new Date() };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';

    // Show typing indicator
    setMessages((prev) => [...prev, { role: 'typing' }]);
    setLoading(true);

    try {
      const data = await sendMessage({
        message: text,
        employee_name: employee.name,
        employee_email: employee.email,
        session_id: sessionId,
      });

      // Save session_id from first response
      if (!sessionId && data.session_id) {
        setSessionId(data.session_id);
      }

      // Remove typing indicator, add agent response
      const agentMsg = {
        role: 'agent',
        text: data.response,
        kb_used: data.kb_used,
        decision: data.decision,
        time: new Date(),
      };

      setMessages((prev) => prev.filter((m) => m.role !== 'typing').concat(agentMsg));

      // Pass ticket up to App
      if (data.ticket) {
        onNewTicket(data.ticket);
      }
    } catch (err) {
      const errMsg = {
        role: 'agent',
        text: '⚠️ Could not reach the server. Make sure the backend is running at localhost:8000.',
        time: new Date(),
      };
      setMessages((prev) => prev.filter((m) => m.role !== 'typing').concat(errMsg));
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="chat-panel">
      {/* Messages */}
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <div className="empty-chat-icon">💬</div>
            <p className="empty-chat-title">Hi {employee.name.split(' ')[0]}, how can we help?</p>
            <p className="empty-chat-text">
              Describe your IT issue and our agent will resolve it or escalate it to the right team.
            </p>
          </div>
        ) : (
          messages.map((msg, i) => <MessageBubble key={msg.id || i} msg={msg} />)
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="chat-input-area">
        <div className="chat-input-wrapper">
          <textarea
            ref={textareaRef}
            className="chat-input"
            placeholder="Describe your IT issue..."
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={loading}
            id="chat-input"
          />
          <button
            className="chat-send-btn"
            onClick={handleSend}
            disabled={!input.trim() || loading}
            id="send-btn"
            aria-label="Send message"
          >
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M2 21L23 12 2 3v7l15 2-15 2v7z" />
            </svg>
          </button>
        </div>
        <p className="input-hint">Press Enter to send · Shift+Enter for new line</p>
      </div>
    </div>
  );
}
