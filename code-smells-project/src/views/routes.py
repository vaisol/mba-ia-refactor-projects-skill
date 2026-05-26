from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.pedido_model import PedidoModel
from src.models.produto_model import ProdutoModel
from src.models.usuario_model import UsuarioModel

api_bp = Blueprint('api', __name__)

@api_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    dados = request.get_json()
    usuario_id = dados.get("usuario_id")
    itens = dados.get("itens", [])

    if not usuario_id or not itens:
        return jsonify({"erro": "Dados inválidos"}), 400

    total = 0
    itens_processados = []
    for item in itens:
        prod = ProdutoModel.get_by_id(item["produto_id"])
        if not prod or prod["estoque"] < item["quantidade"]:
            return jsonify({"erro": f"Estoque insuficiente para {prod['nome'] if prod else 'ID ' + str(item['produto_id'])}"}), 400

        total += prod["preco"] * item["quantidade"]
        itens_processados.append({
            "produto_id": item["produto_id"],
            "quantidade": item["quantidade"],
            "preco_unitario": prod["preco"]
        })

    pedido_id = PedidoModel.create(usuario_id, total, itens_processados)
    return jsonify({"dados": {"pedido_id": pedido_id, "total": total}, "sucesso": True}), 201

@api_bp.route('/pedidos/usuario/<int:usuario_id>', methods=['GET'])
def listar_pedidos_usuario(usuario_id):
    pedidos = PedidoModel.get_by_user(usuario_id)
    return jsonify({"dados": pedidos, "sucesso": True}), 200

@api_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = PedidoModel.get_all()
    return jsonify({"dados": pedidos, "sucesso": True}), 200

@api_bp.route('/pedidos/<int:pedido_id>/status', methods=['PUT'])
def atualizar_status(pedido_id):
    dados = request.get_json()
    status = dados.get("status")
    if status not in ["pendente", "aprovado", "enviado", "entregue", "cancelado"]:
        return jsonify({"erro": "Status inválido"}), 400

    PedidoModel.update_status(pedido_id, status)
    return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200

@api_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = ProdutoModel.get_all()
    return jsonify({"dados": produtos, "sucesso": True}), 200

@api_bp.route('/produtos/<int:id>', methods=['GET'])
def buscar_produto(id):
    produto = ProdutoModel.get_by_id(id)
    if produto:
        return jsonify({"dados": produto, "sucesso": True}), 200
    return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404

@api_bp.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.get_json()
    if not dados or "nome" not in dados or "preco" not in dados:
        return jsonify({"erro": "Dados obrigatórios ausentes"}), 400

    id = ProdutoModel.create(
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados.get("estoque", 0),
        dados.get("categoria", "geral")
    )
    return jsonify({"dados": {"id": id}, "sucesso": True, "mensagem": "Produto criado"}), 201

@api_bp.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.get_json()
    if not ProdutoModel.get_by_id(id):
        return jsonify({"erro": "Produto não encontrado"}), 404

    ProdutoModel.update(
        id,
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados.get("estoque", 0),
        dados.get("categoria", "geral")
    )
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

@api_bp.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    if not ProdutoModel.get_by_id(id):
        return jsonify({"erro": "Produto não encontrado"}), 404
    ProdutoModel.delete(id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200

@api_bp.route('/produtos/pesquisa', methods=['GET'])
def pesquisar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria")
    preco_min = request.args.get("preco_min")
    preco_max = request.args.get("preco_max")

    resultados = ProdutoModel.search(termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200

@api_bp.route('/relatorio/vendas', methods=['GET'])
def relatorio_vendas():
    try:
        relatorio = PedidoModel.get_vendas_report()
        return jsonify({"dados": relatorio, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e), "sucesso": False}), 500

@api_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = UsuarioModel.get_all()
    return jsonify({"dados": usuarios, "sucesso": True}), 200

@api_bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    usuario = UsuarioModel.get_by_id(id)
    if usuario:
        return jsonify({"dados": usuario, "sucesso": True}), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

@api_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    if not dados or "email" not in dados or "senha" not in dados or "nome" not in dados:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    senha_hash = generate_password_hash(dados["senha"])
    try:
        id = UsuarioModel.create(dados["nome"], dados["email"], senha_hash)
        return jsonify({"dados": {"id": id}, "sucesso": True}), 201
    except Exception as e:
        return jsonify({"erro": "Erro ao criar usuário, verifique os dados.", "detalhes": str(e)}), 400

@api_bp.route('/usuarios/login', methods=['POST'])
def login_usuario():
    dados = request.get_json()
    if not dados or "email" not in dados or "senha" not in dados:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = UsuarioModel.get_by_email(dados.get("email"))
    if usuario and check_password_hash(usuario["senha"], dados.get("senha")):
        usuario.pop("senha", None)
        return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
    return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
