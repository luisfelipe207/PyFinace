from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import db
from .routes import api
from .database import init_db, verificar_conexao  # Importa as funções de inicialização e verificação
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializando extensões
    init_db(app)  # Inicializa o banco de dados
    jwt = JWTManager(app)
    CORS(app)
    
    # Registrando blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    return app

# Criar uma instância do aplicativo
app = create_app()

# Verificar conexões ativas antes de cada requisição
@app.before_request
def before_request():
    verificar_conexao()  # Verifica e fecha a conexão se necessário

if __name__ == '__main__':
    app.run(debug=True) 