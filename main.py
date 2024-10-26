from flask import Flask
from flask_cors import CORS
from config import Config
from routes import register_routes
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configurar CORS
    CORS(app)

    # Registrar rotas
    register_routes(app)

    # Criar pasta de downloads se não existir
    if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
        os.makedirs(app.config['DOWNLOAD_FOLDER'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
