import os

class Config:
    DB_PATH = os.environ.get("DB_PATH", "loja.db")
    DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
