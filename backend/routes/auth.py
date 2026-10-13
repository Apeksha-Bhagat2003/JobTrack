import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def user_payload(user):
    return {"id": user.id, "name": user.name, "email": user.email}


def read_json_object():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


@auth_bp.post("/register")
def register():
    data = read_json_object()
    if data is None:
        return jsonify({"message": "Send a valid JSON object"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not all(isinstance(value, str) for value in (name, email, password)):
        return jsonify({"message": "Name, email and password are required"}), 400

    name, email = name.strip(), email.strip().lower()
    if not name or len(name) > 100:
        return jsonify({"message": "Name must contain 1–100 characters"}), 400
    if len(email) > 150 or not EMAIL_PATTERN.match(email):
        return jsonify({"message": "Enter a valid email address"}), 400
    if len(password) < 8 or len(password) > 128:
        return jsonify({"message": "Password must be 8–128 characters long"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email is already registered"}), 409

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email is already registered"}), 409

    return jsonify({"message": "Registration successful", "token": create_access_token(identity=str(user.id)), "user": user_payload(user)}), 201


@auth_bp.post("/login")
def login():
    data = read_json_object()
    if data is None:
        return jsonify({"message": "Send a valid JSON object"}), 400
    email, password = data.get("email"), data.get("password")
    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"message": "Email and password are required"}), 400
    user = User.query.filter_by(email=email.strip().lower()).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401
    return jsonify({"message": "Login successful", "token": create_access_token(identity=str(user.id)), "user": user_payload(user)})


@auth_bp.get("/me")
@jwt_required()
def me():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user_payload(user))
