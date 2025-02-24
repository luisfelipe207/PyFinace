from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    transacoes = db.relationship('Transacao', backref='usuario', lazy=True)
    categorias = db.relationship('Categoria', backref='usuario', lazy=True)
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)
        
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria_pai_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    subcategorias = db.relationship('Categoria', backref=db.backref('categoria_pai', remote_side=[id]))
    transacoes = db.relationship('Transacao', backref='categoria', lazy=True)

class Transacao(db.Model):
    __tablename__ = 'transacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Numeric(10,2), nullable=False)
    tipo = db.Column(db.Enum('receita', 'despesa'), nullable=False)
    descricao = db.Column(db.Text)
    data_transacao = db.Column(db.Date, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow) 