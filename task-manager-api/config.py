import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///task_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EMAIL_USER = os.environ.get('EMAIL_USER', '')
    EMAIL_PASS = os.environ.get('EMAIL_PASS', '')
