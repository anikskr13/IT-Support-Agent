import TicketCard from './TicketCard';

export default function TicketPanel({ tickets }) {
  return (
    <div className="ticket-panel">
      <div className="ticket-panel-header">
        <span className="ticket-panel-title">
          🎫 Tickets
        </span>
        <span className="ticket-count-badge">{tickets.length}</span>
      </div>

      <div className="ticket-list">
        {tickets.length === 0 ? (
          <div className="empty-tickets">
            <div className="empty-tickets-icon">🎫</div>
            <p className="empty-tickets-text">
              No tickets yet. Start a chat and tickets will appear here automatically.
            </p>
          </div>
        ) : (
          /* Newest first */
          [...tickets].reverse().map((ticket) => (
            <TicketCard key={ticket.ticket_id} ticket={ticket} />
          ))
        )}
      </div>
    </div>
  );
}
