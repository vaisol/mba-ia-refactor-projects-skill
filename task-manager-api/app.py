from flask import Flask
from flask_cors import CORS
from database import db
from config.settings import SECRET_KEY, DEBUG, HOST, PORT, SQLALCHEMY_DATABASE_URI
from routes import register_routes
from middlewares.error_handler import register_error_handlers
import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

CORS(app)
db.init_app(app)

register_error_handlers(app)
register_routes(app)


@app.route('/health')
def health():
    return {'status': 'ok', 'timestamp': str(datetime.datetime.now())}


@app.route('/')
def index():
    return {'message': 'Task Manager API', 'version': '1.0'}


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
