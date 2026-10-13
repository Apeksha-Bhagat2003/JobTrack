function ApplicationTable({ applications, onEdit, onDelete }) {
  if (applications.length === 0) {
    return (
      <div className="empty-state">
        <h3>No applications found</h3>
        <p>Add an application or change your search/filter.</p>
      </div>
    );
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Company</th>
            <th>Role</th>
            <th>Location</th>
            <th>Applied</th>
            <th>Salary</th>
            <th>Status</th>
            <th>Link</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {applications.map((application) => (
            <tr key={application.id}>
              <td className="company-cell">{application.company}</td>
              <td>{application.job_role}</td>
              <td>{application.location}</td>
              <td>{application.applied_date}</td>
              <td>
                {application.salary
                  ? `₹${Number(application.salary).toLocaleString("en-IN")}`
                  : "-"}
              </td>
              <td>
                <span
                  className={`status status-${application.status.toLowerCase()}`}
                >
                  {application.status}
                </span>
              </td>
              <td>
                {application.job_link ? (
                  <a
                    href={application.job_link}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Open
                  </a>
                ) : (
                  "-"
                )}
              </td>
              <td>
                <div className="actions">
                  <button
                    className="small-btn edit"
                    onClick={() => onEdit(application)}
                  >
                    Edit
                  </button>
                  <button
                    className="small-btn delete"
                    onClick={() => onDelete(application.id)}
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ApplicationTable;
