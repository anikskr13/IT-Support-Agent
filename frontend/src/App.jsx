import { useState } from 'react';
import './index.css';
import WelcomeScreen from './components/WelcomeScreen';
import ChatPanel from './components/ChatPanel';
import TicketPanel from './components/TicketPanel';

export default function App() {
  const [employee, setEmployee] = useState(null); // { name, email }
  const [tickets, setTickets] = useState([]);

  function handleStart({ name, email }) {
    setEmployee({ name, email });
  }

  function handleNewTicket(ticket) {
    setTickets((prev) => [...prev, ticket]);
  }

  function getInitials(name) {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  }

  // Welcome screen
  if (!employee) {
    return <WelcomeScreen onStart={handleStart} />;
  }

  // Main chat layout
  return (
    <div className="app-layout">
      {/* Header */}
      <header className="app-header">
        <div className="header-brand">
          <div className="header-logo-icon">🛡️</div>
          <div>
            <div className="header-title">IT Support Agent</div>
            <div className="header-subtitle">Veridian Corp</div>
          </div>
        </div>

        <div className="header-status">
          <div className="status-dot" />
          AI Online
        </div>

        <div className="header-user">
          <div className="header-user-info">
            <div className="header-user-name">{employee.name}</div>
            <div className="header-user-email">{employee.email}</div>
          </div>
          <div className="header-avatar">{getInitials(employee.name)}</div>
        </div>
      </header>

      {/* Body */}
      <div className="app-body">
        <ChatPanel employee={employee} onNewTicket={handleNewTicket} />
        <TicketPanel tickets={tickets} />
      </div>
    </div>
  );
}
