function formatTime(date) {
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

export default function MessageBubble({ msg }) {
  const isUser = msg.role === 'user';

  if (msg.role === 'typing') {
    return (
      <div className="typing-row">
        <div className="message-avatar agent">🤖</div>
        <div className="typing-bubble">
          <div className="typing-dot" />
          <div className="typing-dot" />
          <div className="typing-dot" />
        </div>
      </div>
    );
  }

  return (
    <div className={`message-row ${isUser ? 'user' : 'agent'}`}>
      {/* Avatar */}
      <div className={`message-avatar ${isUser ? 'user-avatar' : 'agent'}`}>
        {isUser ? '👤' : '🤖'}
      </div>

      <div className="message-content">
        {/* Badges (agent only) */}
        {!isUser && (msg.kb_used || msg.decision) && (
          <div className="message-badges">
            {msg.kb_used && msg.kb_used !== 'NONE' && (
              <span className="badge badge-kb">📚 {msg.kb_used}</span>
            )}
            {msg.decision === 'resolved' && (
              <span className="badge badge-resolved">✅ Resolved</span>
            )}
            {msg.decision === 'escalated' && (
              <span className="badge badge-escalated">🔺 Escalated</span>
            )}
            {msg.decision === 'follow_up' && (
              <span className="badge badge-followup">💬 Follow-up</span>
            )}
          </div>
        )}

        {/* Bubble */}
        <div className={`message-bubble ${isUser ? 'user-bubble' : 'agent-bubble'}`}>
          {msg.text}
        </div>

        {/* Timestamp */}
        <span className="message-time">{formatTime(msg.time)}</span>
      </div>
    </div>
  );
}
