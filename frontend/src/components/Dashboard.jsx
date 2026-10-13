import { useEffect, useState } from "react";
import api from "../api";
import ApplicationForm from "./ApplicationForm";
import ApplicationTable from "./ApplicationTable";

const emptyStats = {
  total: 0,
  applied: 0,
  assessment: 0,
  interviews: 0,
  selected: 0,
  rejected: 0,
};

function Dashboard({ user, onLogout }) {
  const [applications, setApplications] = useState([]);
  const [stats, setStats] = useState(emptyStats);
  const [editingApplication, setEditingApplication] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [sort, setSort] = useState("applied_date");
  const [order, setOrder] = useState("desc");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [applicationsResponse, statsResponse] = await Promise.all([
        api.get("/applications", {
          params: { search, status, sort, order },
        }),
        api.get("/applications/stats"),
      ]);

      setApplications(applicationsResponse.data);
      setStats(statsResponse.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.message || "Could not load data. Check that the backend and database are running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [search, status, sort, order]);

  const saveApplication = async (form) => {
    setSaving(true);
    try {
      if (editingApplication) {
        await api.put(`/applications/${editingApplication.id}`, form);
      } else {
        await api.post("/applications", form);
      }

      setEditingApplication(null);
      setShowForm(false);
      await loadData();
    } catch (err) {
      setError(err.response?.data?.message || "Could not save application");
    } finally {
      setSaving(false);
    }
  };

  const deleteApplication = async (id) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this application?"
    );

    if (!confirmed) return;

    try {
      await api.delete(`/applications/${id}`);
      await loadData();
    } catch (err) {
      setError(err.response?.data?.message || "Could not delete application");
    }
  };

  const editApplication = (application) => {
    setEditingApplication(application);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const cancelForm = () => {
    setEditingApplication(null);
    setShowForm(false);
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <div className="brand">JobTrack</div>
          <span className="welcome">Hi, {user.name}</span>
        </div>
        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>
      </header>

      <main className="container">
        <section className="hero">
          <div>
            <h1>Job Application Dashboard</h1>
            <p>Keep your applications organized and track every stage.</p>
          </div>
          <button
            className="primary-btn add-btn"
            onClick={() => {
              setEditingApplication(null);
              setShowForm(true);
            }}
          >
            + Add Application
          </button>
        </section>

        {error && <div className="error" role="alert">{error}</div>}

        <section className="stats-grid">
          <div className="stat-card">
            <span>Total Applications</span>
            <strong>{stats.total}</strong>
          </div>
          <div className="stat-card">
            <span>Applied</span>
            <strong>{stats.applied}</strong>
          </div>
          <div className="stat-card">
            <span>Assessments</span>
            <strong>{stats.assessment}</strong>
          </div>
          <div className="stat-card">
            <span>Interviews</span>
            <strong>{stats.interviews}</strong>
          </div>
          <div className="stat-card">
            <span>Selected</span>
            <strong>{stats.selected}</strong>
          </div>
          <div className="stat-card">
            <span>Rejected</span>
            <strong>{stats.rejected}</strong>
          </div>
        </section>

        {showForm && (
          <ApplicationForm
            application={editingApplication}
            onSave={saveApplication}
            onCancel={cancelForm}
            saving={saving}
          />
        )}

        <section className="panel">
          <div className="toolbar">
            <input
              className="search-input"
              placeholder="Search company, role or location..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />

            <select
              value={status}
              onChange={(event) => setStatus(event.target.value)}
            >
              <option value="">All Statuses</option>
              <option value="Applied">Applied</option>
              <option value="Assessment">Assessment</option>
              <option value="Interview">Interview</option>
              <option value="Selected">Selected</option>
              <option value="Rejected">Rejected</option>
            </select>

            <select
              value={sort}
              onChange={(event) => setSort(event.target.value)}
            >
              <option value="applied_date">Sort: Date</option>
              <option value="company">Sort: Company</option>
              <option value="status">Sort: Status</option>
              <option value="salary">Sort: Salary</option>
            </select>

            <select
              value={order}
              onChange={(event) => setOrder(event.target.value)}
            >
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>

          {loading ? (
            <div className="empty-state" role="status">Loading your applications...</div>
          ) : <ApplicationTable
            applications={applications}
            onEdit={editApplication}
            onDelete={deleteApplication}
          />}
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
