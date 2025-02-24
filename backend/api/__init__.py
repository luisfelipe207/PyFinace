from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import db
from .routes import api
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializando extensões
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Registrando blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    return app

# Criar uma instância do aplicativo
app = create_app()

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 