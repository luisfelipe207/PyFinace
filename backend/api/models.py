from datetime import datetime
from .database import db  # Certifique-se de que está importando db do database.py
from werkzeug.security import generate_password_hash, check_password_hash

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

    @classmethod
    def criar_usuario(cls, nome, email, senha):
        novo_usuario = cls(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario

    @classmethod
    def obter_usuario(cls, usuario_id):
        return cls.query.get(usuario_id)

    @classmethod
    def atualizar_usuario(cls, usuario_id, nome=None, email=None, senha=None):
        usuario = cls.query.get(usuario_id)
        if usuario:
            if nome:
                usuario.nome = nome
            if email:
                usuario.email = email
            if senha:
                usuario.set_senha(senha)
            db.session.commit()
        return usuario

    @classmethod
    def deletar_usuario(cls, usuario_id):
        usuario = cls.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
        return usuario

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria_pai_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    subcategorias = db.relationship('Categoria', backref=db.backref('categoria_pai', remote_side=[id]))
    transacoes = db.relationship('Transacao', backref='categoria', lazy=True)

    @classmethod
    def criar_categoria(cls, nome, usuario_id, categoria_pai_id=None):
        nova_categoria = cls(nome=nome, usuario_id=usuario_id, categoria_pai_id=categoria_pai_id)
        db.session.add(nova_categoria)
        db.session.commit()
        return nova_categoria

    @classmethod
    def obter_categoria(cls, categoria_id):
        return cls.query.get(categoria_id)

    @classmethod
    def atualizar_categoria(cls, categoria_id, nome=None, categoria_pai_id=None):
        categoria = cls.query.get(categoria_id)
        if categoria:
            if nome:
                categoria.nome = nome
            if categoria_pai_id is not None:
                categoria.categoria_pai_id = categoria_pai_id
            db.session.commit()
        return categoria

    @classmethod
    def deletar_categoria(cls, categoria_id):
        categoria = cls.query.get(categoria_id)
        if categoria:
            db.session.delete(categoria)
            db.session.commit()
        return categoria

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

    @classmethod
    def criar_transacao(cls, valor, tipo, descricao, data_transacao, categoria_id, usuario_id):
        nova_transacao = cls(valor=valor, tipo=tipo, descricao=descricao, data_transacao=data_transacao, categoria_id=categoria_id, usuario_id=usuario_id)
        db.session.add(nova_transacao)
        db.session.commit()
        return nova_transacao

    @classmethod
    def obter_transacao(cls, transacao_id):
        return cls.query.get(transacao_id)

    @classmethod
    def atualizar_transacao(cls, transacao_id, valor=None, tipo=None, descricao=None, data_transacao=None, categoria_id=None):
        transacao = cls.query.get(transacao_id)
        if transacao:
            if valor is not None:
                transacao.valor = valor
            if tipo is not None:
                transacao.tipo = tipo
            if descricao is not None:
                transacao.descricao = descricao
            if data_transacao is not None:
                transacao.data_transacao = data_transacao
            if categoria_id is not None:
                transacao.categoria_id = categoria_id
            db.session.commit()
        return transacao

    @classmethod
    def deletar_transacao(cls, transacao_id):
        transacao = cls.query.get(transacao_id)
        if transacao:
            db.session.delete(transacao)
            db.session.commit()
        return transacao 