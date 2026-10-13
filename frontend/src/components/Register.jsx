import { useState } from "react";
import api from "../api";

function Register({ onSuccess, goToLogin }) {
  const [form, setForm] = useState({
    name: "",
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
      const response = await api.post("/auth/register", form);
      onSuccess(response.data);
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="brand">JobTrack</div>
        <h1>Create account</h1>
        <p className="muted">Start managing your job search.</p>

        {error && <div className="error" role="alert">{error}</div>}

        <form onSubmit={handleSubmit}>
          <label>Full Name</label>
          <input
            name="name"
            placeholder="Apeksha Bhagat"
            value={form.name}
            onChange={handleChange}
            required
          />

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
            placeholder="At least 8 characters"
            minLength={8}
            maxLength={128}
            value={form.password}
            onChange={handleChange}
            required
          />

          <button className="primary-btn" disabled={loading}>
            {loading ? "Creating..." : "Create Account"}
          </button>
        </form>

        <p className="switch-text">
          Already have an account?{" "}
          <button className="link-btn" onClick={goToLogin}>
            Login
          </button>
        </p>
      </div>
    </div>
  );
}

export default Register;
