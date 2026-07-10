from flask import Flask
from flask_cors import CORS
from config.settings import SECRET_KEY, DEBUG, HOST, PORT
from database import get_db, init_db
from routes import register_routes
from middlewares.error_handler import register_error_handlers
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = DEBUG
CORS(app)

register_error_handlers(app)
register_routes(app)

with app.app_context():
    init_db()

if __name__ == "__main__":
    get_db()
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print(f"Rodando em http://{HOST}:{PORT}")
    print("=" * 50)
    app.run(host=HOST, port=PORT, debug=DEBUG)
