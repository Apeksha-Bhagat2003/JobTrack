import { useEffect, useState } from "react";

const initialForm = {
  company: "",
  job_role: "",
  location: "",
  applied_date: new Date().toISOString().split("T")[0],
  salary: "",
  job_link: "",
  status: "Applied",
};

function ApplicationForm({ application, onSave, onCancel, saving = false }) {
  const [form, setForm] = useState(initialForm);

  useEffect(() => {
    if (application) {
      setForm({
        company: application.company || "",
        job_role: application.job_role || "",
        location: application.location || "",
        applied_date: application.applied_date || "",
        salary: application.salary ?? "",
        job_link: application.job_link || "",
        status: application.status || "Applied",
      });
    } else {
      setForm(initialForm);
    }
  }, [application]);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSave(form);
  };

  return (
    <section className="form-panel">
      <div className="section-heading">
        <div>
          <h2>{application ? "Edit Application" : "Add Application"}</h2>
          <p>Enter the job details below.</p>
        </div>
      </div>

      <form className="application-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          <div>
            <label>Company *</label>
            <input
              name="company"
              value={form.company}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label>Job Role *</label>
            <input
              name="job_role"
              value={form.job_role}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label>Location *</label>
            <input
              name="location"
              value={form.location}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label>Applied Date</label>
            <input
              name="applied_date"
              type="date"
              value={form.applied_date}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Salary</label>
            <input
              name="salary"
              type="number"
              min="0"
              placeholder="e.g. 600000"
              value={form.salary}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Status</label>
            <select
              name="status"
              value={form.status}
              onChange={handleChange}
            >
              <option>Applied</option>
              <option>Assessment</option>
              <option>Interview</option>
              <option>Selected</option>
              <option>Rejected</option>
            </select>
          </div>

          <div className="full-width">
            <label>Job Link</label>
            <input
              name="job_link"
              type="url"
              placeholder="https://..."
              value={form.job_link}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="secondary-btn" onClick={onCancel}>
            Cancel
          </button>
          <button type="submit" className="primary-btn" disabled={saving}>
            {saving ? "Saving..." : application ? "Update Application" : "Save Application"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default ApplicationForm;
