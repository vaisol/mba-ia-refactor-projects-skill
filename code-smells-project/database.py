import sqlite3
from src.config.settings import Config

_db_connection = None

def get_db():
    global _db_connection
    if _db_connection is None:
        _db_connection = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
        _db_connection.row_factory = sqlite3.Row
    return _db_connection
