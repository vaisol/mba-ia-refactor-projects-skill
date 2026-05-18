from flask import Flask, jsonify
from flask_cors import CORS
from src.config.settings import Config
from src.views.routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route("/")
    def index():
        return jsonify({"mensagem": "Bem-vindo à API da Loja Refatorada", "versao": "1.1.0"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))
