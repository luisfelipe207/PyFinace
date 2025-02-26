from flask_sqlalchemy import SQLAlchemy
from flask import current_app

# Inicializa o objeto SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask."""
    db.init_app(app)

def get_db_session():
    """Retorna a sessão do banco de dados."""
    return db.session

def fechar_conexao():
    """Fecha a conexão atual com o banco de dados."""
    db.session.remove()  # Remove a sessão atual e fecha a conexão

def verificar_conexao():
    """Verifica se a conexão está ativa e a fecha se necessário."""
    if db.session.is_active:
        fechar_conexao() 