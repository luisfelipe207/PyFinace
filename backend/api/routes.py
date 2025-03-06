from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import datetime
from .models import Usuario, Transacao, Categoria
from .database import get_db_session, verificar_conexao  # Importa as funções para gerenciar a conexão
from urllib.parse import quote  # Importa a função para codificar URLs

api = Blueprint('api', __name__)

@api.route('/auth/registro', methods=['POST'])
def registro():
    dados = request.get_json()
    
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    if Usuario.query.filter_by(email=dados['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400
        
    usuario = Usuario(
        nome=dados['nome'],
        email=dados['email']
    )
    usuario.set_senha(dados['senha'])
    
    session.add(usuario)
    session.commit()
    
    return jsonify({'mensagem': 'Usuário registrado com sucesso'}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    dados = request.get_json()
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    usuario = Usuario.query.filter_by(email=dados['email']).first()
    
    if not usuario or not usuario.verificar_senha(dados['senha']):
        return jsonify({'erro': 'Email ou senha inválidos'}), 401
    
    access_token = create_access_token(identity=usuario.id)
    return jsonify({'token': access_token}), 200

@api.route('/transacoes', methods=['POST'])
@jwt_required()
def criar_transacao():
    usuario_id = get_jwt_identity()
    dados = request.get_json()
    
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    transacao = Transacao(
        valor=dados['valor'],
        tipo=dados['tipo'],
        descricao=dados.get('descricao'),
        data_transacao=datetime.strptime(dados['data_transacao'], '%Y-%m-%d').date(),
        categoria_id=dados.get('categoria_id'),
        usuario_id=usuario_id
    )
    
    session.add(transacao)
    session.commit()
    
    return jsonify({'mensagem': 'Transação criada com sucesso'}), 201

@api.route('/transacoes', methods=['GET'])
@jwt_required()
def listar_transacoes():
    usuario_id = get_jwt_identity()
    
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    filtros = request.args
    query = Transacao.query.filter_by(usuario_id=usuario_id)
    
    if 'data_inicio' in filtros:
        query = query.filter(Transacao.data_transacao >= filtros['data_inicio'])
    if 'data_fim' in filtros:
        query = query.filter(Transacao.data_transacao <= filtros['data_fim'])
    if 'categoria_id' in filtros:
        query = query.filter_by(categoria_id=filtros['categoria_id'])
    if 'tipo' in filtros:
        query = query.filter_by(tipo=filtros['tipo'])
        
    transacoes = query.all()
    return jsonify([{
        'id': t.id,
        'valor': float(t.valor),
        'tipo': t.tipo,
        'descricao': t.descricao,
        'data_transacao': t.data_transacao.strftime('%Y-%m-%d'),
        'categoria_id': t.categoria_id
    } for t in transacoes]), 200

@api.route('/transacoes/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_transacao(id):
    usuario_id = get_jwt_identity()
    
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    transacao = Transacao.query.filter_by(id=id, usuario_id=usuario_id).first()
    
    if not transacao:
        return jsonify({'erro': 'Transação não encontrada'}), 404
        
    dados = request.get_json()
    
    transacao.valor = dados.get('valor', transacao.valor)
    transacao.tipo = dados.get('tipo', transacao.tipo)
    transacao.descricao = dados.get('descricao', transacao.descricao)
    if 'data_transacao' in dados:
        transacao.data_transacao = datetime.strptime(dados['data_transacao'], '%Y-%m-%d').date()
    transacao.categoria_id = dados.get('categoria_id', transacao.categoria_id)
    
    session.commit()
    return jsonify({'mensagem': 'Transação atualizada com sucesso'}), 200

@api.route('/transacoes/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_transacao(id):
    usuario_id = get_jwt_identity()
    
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    transacao = Transacao.query.filter_by(id=id, usuario_id=usuario_id).first()
    
    if not transacao:
        return jsonify({'erro': 'Transação não encontrada'}), 404
        
    session.delete(transacao)
    session.commit()
    return jsonify({'mensagem': 'Transação deletada com sucesso'}), 200

@api.route('/categorias', methods=['POST'])
@jwt_required()
def criar_categoria():
    usuario_id = get_jwt_identity()
    dados = request.get_json()
    
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    categoria = Categoria(
        nome=dados['nome'],
        categoria_pai_id=dados.get('categoria_pai_id'),
        usuario_id=usuario_id
    )
    
    session.add(categoria)
    session.commit()
    
    return jsonify({'mensagem': 'Categoria criada com sucesso'}), 201

@api.route('/categorias', methods=['GET'])
@jwt_required()
def listar_categorias():
    usuario_id = get_jwt_identity()  # Obtém o ID do usuário do token
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    categorias = Categoria.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([{
        'id': c.id,
        'nome': c.nome,
        'categoria_pai_id': c.categoria_pai_id
    } for c in categorias]), 200

@api.route('/relatorios/fluxo', methods=['GET'])
@jwt_required()
def relatorio_fluxo():
    usuario_id = get_jwt_identity()
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Verifica se as datas estão no formato correto
    if not data_inicio or not data_fim:
        return jsonify({'erro': 'As datas de início e fim são obrigatórias.'}), 422

    try:
        # Tente converter as datas para o formato correto
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    except ValueError:
        return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 422

    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    # Obtém as transações do banco de dados
    transacoes = Transacao.query.filter_by(usuario_id=usuario_id).filter(
        Transacao.data_transacao >= data_inicio,
        Transacao.data_transacao <= data_fim
    ).all()

    # Verifica se as transações estão vazias
    if not transacoes:
        return jsonify({'mensagem': 'Nenhuma transação encontrada para o período especificado.'}), 200

    receitas = sum(float(t.valor) for t in transacoes if t.tipo == 'receita')
    despesas = sum(float(t.valor) for t in transacoes if t.tipo == 'despesa')
    saldo = receitas - despesas
    
    return jsonify({
        'receitas': receitas,
        'despesas': despesas,
        'saldo': saldo,
        'transacoes': [{
            'id': t.id,
            'valor': float(t.valor),
            'tipo': t.tipo,
            'data': t.data_transacao.strftime('%Y-%m-%d')
        } for t in transacoes]
    }), 200

@api.route('/relatorios/categorias', methods=['GET'])
@jwt_required()
def relatorio_categorias():
    usuario_id = get_jwt_identity()
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    verificar_conexao()  # Verifica e fecha a conexão se necessário
    session = get_db_session()  # Obtém a sessão do banco de dados

    categorias = Categoria.query.filter_by(usuario_id=usuario_id).all()
    resultado = []
    
    for categoria in categorias:
        query = Transacao.query.filter_by(
            usuario_id=usuario_id,
            categoria_id=categoria.id
        )
        
        if data_inicio:
            query = query.filter(Transacao.data_transacao >= data_inicio)
        if data_fim:
            query = query.filter(Transacao.data_transacao <= data_fim)
            
        transacoes = query.all()
        
        total_receitas = sum(float(t.valor) for t in transacoes if t.tipo == 'receita')
        total_despesas = sum(float(t.valor) for t in transacoes if t.tipo == 'despesa')
        
        resultado.append({
            'categoria': categoria.nome,
            'total_receitas': total_receitas,
            'total_despesas': total_despesas
        })
    
    return jsonify(resultado), 200 