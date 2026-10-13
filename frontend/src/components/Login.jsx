import { useState } from "react";
import api from "../api";

function Login({ onSuccess, goToRegister }) {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/auth/login", form);
      onSuccess(response.data);
    } catch (err) {
      setError(err.response?.data?.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="brand">JobTrack</div>
        <h1>Welcome back</h1>
        <p className="muted">Track your job applications in one place.</p>

        {error && <div className="error" role="alert">{error}</div>}

        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input
            name="email"
            type="email"
            placeholder="you@example.com"
            value={form.email}
            onChange={handleChange}
            required
          />

          <label>Password</label>
          <input
            name="password"
            type="password"
            placeholder="Minimum 6 characters"
            value={form.password}
            onChange={handleChange}
            required
          />

          <button className="primary-btn" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="switch-text">
          Don't have an account?{" "}
          <button className="link-btn" onClick={goToRegister}>
            Create one
          </button>
        </p>
      </div>
    </div>
  );
}

export default Login;
