import { useEffect, useState } from "react";
import api from "./api";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";

function App() {
  const [page, setPage] = useState("login");
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) return;

    api.get("/auth/me")
      .then((response) => {
        setUser(response.data);
        setPage("dashboard");
      })
      .catch(() => {
        localStorage.removeItem("token");
      });
  }, []);

  const handleAuth = (data) => {
    localStorage.setItem("token", data.token);
    setUser(data.user);
    setPage("dashboard");
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setPage("login");
  };

  if (user && page === "dashboard") {
    return <Dashboard user={user} onLogout={logout} />;
  }

  if (page === "register") {
    return (
      <Register
        onSuccess={handleAuth}
        goToLogin={() => setPage("login")}
      />
    );
  }

  return (
    <Login
      onSuccess={handleAuth}
      goToRegister={() => setPage("register")}
    />
  );
}

export default App;
