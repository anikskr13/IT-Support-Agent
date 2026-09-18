export default function WelcomeScreen({ onStart }) {
  function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const name = form.name.value.trim();
    const email = form.email.value.trim();
    if (!name || !email) return;
    onStart({ name, email });
  }

  return (
    <div className="welcome-screen">
      <div className="welcome-card">
        {/* Logo */}
        <div className="welcome-logo">
          <div className="welcome-logo-icon">🛡️</div>
          <div className="welcome-logo-text">
            <span className="welcome-logo-company">Veridian Corp</span>
            <span className="welcome-logo-product">IT Support Agent</span>
          </div>
        </div>

        {/* Heading */}
        <h1 className="welcome-title">How can we help you today?</h1>
        <p className="welcome-subtitle">
          Enter your details to start a support session. Our AI agent will resolve your issue or escalate it to the right team.
        </p>

        {/* Form */}
        <form onSubmit={handleSubmit} id="welcome-form">
          <div className="form-group">
            <label className="form-label" htmlFor="name">Full Name</label>
            <input
              id="name"
              name="name"
              className="form-input"
              type="text"
              placeholder="e.g. Jane Smith"
              required
              autoComplete="name"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">Work Email</label>
            <input
              id="email"
              name="email"
              className="form-input"
              type="email"
              placeholder="e.g. jane@veridian.com"
              required
              autoComplete="email"
            />
          </div>

          <button className="btn-primary" type="submit" id="start-chat-btn">
            Start Chat Session →
          </button>
        </form>

        {/* Features */}
        <div className="welcome-features">
          <div className="welcome-feature">
            <span className="welcome-feature-icon">⚡</span>
            <span className="welcome-feature-text">Instant Response</span>
          </div>
          <div className="welcome-feature">
            <span className="welcome-feature-icon">📋</span>
            <span className="welcome-feature-text">Auto Ticketing</span>
          </div>
          <div className="welcome-feature">
            <span className="welcome-feature-icon">🔒</span>
            <span className="welcome-feature-text">Policy-Based</span>
          </div>
        </div>
      </div>
    </div>
  );
}
