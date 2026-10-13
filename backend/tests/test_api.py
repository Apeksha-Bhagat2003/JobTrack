import os

# Keep tests independent of a local MySQL installation and real secrets.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-only-secret-not-for-production")

import pytest
from app import create_app
from extensions import db


@pytest.fixture()
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-only-secret-not-for-production",
        "CORS_ORIGINS": ["http://localhost:5173"],
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as test_client:
        yield test_client
    with app.app_context():
        db.session.remove()
        db.drop_all()


def register_and_login(client, email="user@example.com"):
    response = client.post("/api/auth/register", json={"name": "Test User", "email": email, "password": "strongpass123"})
    assert response.status_code == 201
    return response.get_json()["token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_register_login_and_current_user(client):
    token = register_and_login(client)
    response = client.get("/api/auth/me", headers=auth(token))
    assert response.status_code == 200
    assert response.get_json()["email"] == "user@example.com"
    login = client.post("/api/auth/login", json={"email": "USER@example.com", "password": "strongpass123"})
    assert login.status_code == 200


def test_rejects_weak_password_and_duplicate_email(client):
    first = client.post("/api/auth/register", json={"name": "User", "email": "user@example.com", "password": "123"})
    assert first.status_code == 400
    register_and_login(client)
    duplicate = client.post("/api/auth/register", json={"name": "User", "email": "USER@example.com", "password": "strongpass123"})
    assert duplicate.status_code == 409


def test_application_crud_and_validation(client):
    token = register_and_login(client)
    headers = auth(token)
    bad = client.post("/api/applications", headers=headers, json={"company": "", "job_role": "Engineer", "location": "Pune"})
    assert bad.status_code == 400
    created = client.post("/api/applications", headers=headers, json={"company": "Example Ltd", "job_role": "Engineer", "location": "Pune", "salary": 500000, "status": "Applied"})
    assert created.status_code == 201
    app_id = created.get_json()["id"]
    invalid = client.put(f"/api/applications/{app_id}", headers=headers, json={"salary": -1})
    assert invalid.status_code == 400
    updated = client.put(f"/api/applications/{app_id}", headers=headers, json={"status": "Interview"})
    assert updated.status_code == 200
    assert updated.get_json()["status"] == "Interview"
    assert client.get("/api/applications/stats", headers=headers).get_json()["interviews"] == 1
    assert client.delete(f"/api/applications/{app_id}", headers=headers).status_code == 200


def test_users_cannot_access_other_users_applications(client):
    first_token = register_and_login(client, "first@example.com")
    second_token = register_and_login(client, "second@example.com")
    created = client.post("/api/applications", headers=auth(first_token), json={"company": "Private Co", "job_role": "Developer", "location": "Pune"})
    app_id = created.get_json()["id"]
    assert client.get(f"/api/applications/{app_id}", headers=auth(second_token)).status_code == 404
    assert client.delete(f"/api/applications/{app_id}", headers=auth(second_token)).status_code == 404
