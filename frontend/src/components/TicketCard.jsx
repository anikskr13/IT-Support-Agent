export default function TicketCard({ ticket }) {
  const isResolved = ticket.decision === 'resolved';

  return (
    <div className={`ticket-card ${isResolved ? 'resolved' : 'escalated'}`} id={`ticket-${ticket.ticket_id}`}>
      <div className="ticket-card-header">
        <span className="ticket-id">{ticket.ticket_id}</span>
        <span className={`badge ${isResolved ? 'badge-resolved' : 'badge-escalated'}`}>
          {isResolved ? '✅ Resolved' : '🔺 Escalated'}
        </span>
      </div>

      <p className="ticket-issue">{ticket.issue_summary}</p>

      <div className="ticket-card-footer">
        {ticket.kb_used && ticket.kb_used !== 'NONE' && (
          <span className="badge badge-kb">📚 {ticket.kb_used}</span>
        )}
        <span className="ticket-time">{ticket.timestamp}</span>
      </div>
    </div>
  );
}
