import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import db, jwt
from routes.auth import auth_bp
from routes.applications import applications_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    # Fail fast rather than silently running with insecure development secrets or DB settings.
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL is missing. Configure it in backend/.env.")
    if not app.config.get("JWT_SECRET_KEY"):
        raise RuntimeError("JWT_SECRET_KEY is missing. Configure it in backend/.env.")

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(applications_bp, url_prefix="/api/applications")

    @app.get("/")
    def home():
        return jsonify({"message": "JobTrack API is running", "docs": "See README.md for endpoints"})

    @app.get("/api/health")
    def health():
        try:
            db.session.execute(db.text("SELECT 1"))
            return jsonify({"status": "ok", "database": "connected"})
        except Exception:
            app.logger.exception("Health check database query failed")
            return jsonify({"status": "error", "database": "unavailable"}), 503

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    # Debug mode should only be used for local development.
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
