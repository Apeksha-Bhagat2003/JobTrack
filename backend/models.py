from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship(
        "JobApplication",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class JobApplication(db.Model):
    __tablename__ = "job_applications"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    job_role = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    applied_date = db.Column(db.Date, nullable=False, default=date.today)
    salary = db.Column(db.Float, nullable=True)
    job_link = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="Applied")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "job_role": self.job_role,
            "location": self.location,
            "applied_date": self.applied_date.isoformat() if self.applied_date else None,
            "salary": self.salary,
            "job_link": self.job_link,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
