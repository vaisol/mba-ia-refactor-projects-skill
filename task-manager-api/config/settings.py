import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///tasks.db")
