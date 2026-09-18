const BASE_URL = import.meta.env.VITE_API_URL !== undefined
  ? import.meta.env.VITE_API_URL
  : (import.meta.env.DEV ? 'http://localhost:8000' : '');

export async function sendMessage({ message, employee_name, employee_email, session_id }) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, employee_name, employee_email, session_id }),
  });

  if (!res.ok) {
    throw new Error(`Server error: ${res.status}`);
  }

  return res.json();
}

export async function getTickets() {
  const res = await fetch(`${BASE_URL}/tickets`);
  if (!res.ok) throw new Error('Failed to fetch tickets');
  return res.json();
}
