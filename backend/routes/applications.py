from datetime import datetime, date
from math import isfinite
from urllib.parse import urlparse
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import JobApplication

applications_bp = Blueprint("applications", __name__)
VALID_STATUSES = {"Applied", "Assessment", "Interview", "Selected", "Rejected"}


def current_user_id():
    return int(get_jwt_identity())


def parse_text(data, key, current, required=False, max_length=150):
    if key not in data:
        if required and not current:
            raise ValueError(f"{key.replace('_', ' ').title()} is required")
        return current
    value = data[key]
    if not isinstance(value, str):
        raise ValueError(f"{key} must be text")
    value = value.strip()
    if required and not value:
        raise ValueError(f"{key.replace('_', ' ').title()} is required")
    if len(value) > max_length:
        raise ValueError(f"{key.replace('_', ' ').title()} must be {max_length} characters or fewer")
    return value


def application_from_data(data, application):
    application.company = parse_text(data, "company", application.company, True, 150)
    application.job_role = parse_text(data, "job_role", application.job_role, True, 150)
    application.location = parse_text(data, "location", application.location, True, 150)

    if "applied_date" in data:
        try:
            application.applied_date = datetime.strptime(data["applied_date"], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            raise ValueError("applied_date must be a valid date in YYYY-MM-DD format")

    if "salary" in data:
        value = data["salary"]
        if value in ("", None):
            application.salary = None
        else:
            try:
                salary = float(value)
            except (ValueError, TypeError):
                raise ValueError("Salary must be a valid number")
            if not isfinite(salary) or salary < 0 or salary > 1_000_000_000:
                raise ValueError("Salary must be between 0 and 1,000,000,000")
            application.salary = salary

    if "job_link" in data:
        link = data["job_link"]
        if link is None or link == "":
            application.job_link = None
        elif not isinstance(link, str) or len(link) > 500:
            raise ValueError("Job link must be a URL of 500 characters or fewer")
        else:
            parsed = urlparse(link.strip())
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("Job link must start with http:// or https://")
            application.job_link = link.strip()

    if "status" in data:
        status = data["status"]
        if not isinstance(status, str) or status not in VALID_STATUSES:
            raise ValueError("Status must be Applied, Assessment, Interview, Selected or Rejected")
        application.status = status


def json_object():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


@applications_bp.get("")
@jwt_required()
def get_applications():
    user_id = current_user_id()
    search = request.args.get("search", "").strip()[:150]
    status = request.args.get("status", "").strip()
    sort_by = request.args.get("sort", "applied_date")
    order = request.args.get("order", "desc")
    if status and status not in VALID_STATUSES:
        return jsonify({"message": "Invalid status filter"}), 400
    query = JobApplication.query.filter_by(user_id=user_id)
    if search:
        pattern = f"%{search}%"
        query = query.filter(db.or_(JobApplication.company.ilike(pattern), JobApplication.job_role.ilike(pattern), JobApplication.location.ilike(pattern)))
    if status:
        query = query.filter_by(status=status)
    sort_columns = {"applied_date": JobApplication.applied_date, "company": JobApplication.company, "status": JobApplication.status, "salary": JobApplication.salary}
    column = sort_columns.get(sort_by)
    if column is None:
        return jsonify({"message": "Invalid sort field"}), 400
    if order not in {"asc", "desc"}:
        return jsonify({"message": "Order must be asc or desc"}), 400
    query = query.order_by(column.asc() if order == "asc" else column.desc(), JobApplication.id.desc())
    return jsonify([item.to_dict() for item in query.all()])


@applications_bp.get("/stats")
@jwt_required()
def stats():
    user_id = current_user_id()
    counts = dict(db.session.query(JobApplication.status, db.func.count(JobApplication.id)).filter_by(user_id=user_id).group_by(JobApplication.status).all())
    return jsonify({"total": sum(counts.values()), "applied": counts.get("Applied", 0), "assessment": counts.get("Assessment", 0), "interviews": counts.get("Interview", 0), "selected": counts.get("Selected", 0), "rejected": counts.get("Rejected", 0)})


@applications_bp.post("")
@jwt_required()
def create_application():
    data = json_object()
    if data is None:
        return jsonify({"message": "Send a valid JSON object"}), 400
    application = JobApplication(company="", job_role="", location="", user_id=current_user_id())
    try:
        application_from_data(data, application)
    except ValueError as error:
        return jsonify({"message": str(error)}), 400
    if not application.applied_date:
        application.applied_date = date.today()
    db.session.add(application)
    db.session.commit()
    return jsonify(application.to_dict()), 201


@applications_bp.get("/<int:application_id>")
@jwt_required()
def get_application(application_id):
    application = JobApplication.query.filter_by(id=application_id, user_id=current_user_id()).first()
    if not application:
        return jsonify({"message": "Application not found"}), 404
    return jsonify(application.to_dict())


@applications_bp.put("/<int:application_id>")
@jwt_required()
def update_application(application_id):
    application = JobApplication.query.filter_by(id=application_id, user_id=current_user_id()).first()
    if not application:
        return jsonify({"message": "Application not found"}), 404
    data = json_object()
    if data is None:
        return jsonify({"message": "Send a valid JSON object"}), 400
    try:
        application_from_data(data, application)
    except ValueError as error:
        return jsonify({"message": str(error)}), 400
    db.session.commit()
    return jsonify(application.to_dict())


@applications_bp.delete("/<int:application_id>")
@jwt_required()
def delete_application(application_id):
    application = JobApplication.query.filter_by(id=application_id, user_id=current_user_id()).first()
    if not application:
        return jsonify({"message": "Application not found"}), 404
    db.session.delete(application)
    db.session.commit()
    return jsonify({"message": "Application deleted successfully"})
