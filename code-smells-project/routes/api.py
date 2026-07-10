from flask import Blueprint, request, jsonify
from controllers import produto_controller, usuario_controller, pedido_controller, relatorio_controller
from middlewares.error_handler import AppError
from database import get_db

api_bp = Blueprint("api", __name__)


@api_bp.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health",
        },
    })


@api_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = produto_controller.get_all_produtos()
    return jsonify({"dados": produtos, "sucesso": True}), 200


@api_bp.route("/produtos/busca", methods=["GET"])
def buscar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria", None)
    preco_min = request.args.get("preco_min", None)
    preco_max = request.args.get("preco_max", None)
    if preco_min:
        preco_min = float(preco_min)
    if preco_max:
        preco_max = float(preco_max)
    resultados = produto_controller.search_produtos(termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200


@api_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    produto = produto_controller.get_produto(produto_id)
    if not produto:
        raise AppError("Produto não encontrado", 404)
    return jsonify({"dados": produto, "sucesso": True}), 200


@api_bp.route("/produtos", methods=["POST"])
def criar_produto():
    data = request.get_json()
    result, errors = produto_controller.create_produto(data)
    if errors:
        raise AppError(errors[0], 400)
    return jsonify({"dados": result, "sucesso": True, "mensagem": "Produto criado"}), 201


@api_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    data = request.get_json()
    result, errors = produto_controller.update_produto(produto_id, data)
    if errors:
        status = 404 if "não encontrado" in errors[0].lower() else 400
        raise AppError(errors[0], status)
    return jsonify({"sucesso": True, "mensagem": result["mensagem"]}), 200


@api_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    ok, error = produto_controller.delete_produto(produto_id)
    if not ok:
        raise AppError(error, 404)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200


@api_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = usuario_controller.get_all_usuarios()
    return jsonify({"dados": usuarios, "sucesso": True}), 200


@api_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
def buscar_usuario(usuario_id):
    usuario = usuario_controller.get_usuario(usuario_id)
    if not usuario:
        raise AppError("Usuário não encontrado", 404)
    return jsonify({"dados": usuario, "sucesso": True}), 200


@api_bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    data = request.get_json()
    result, errors = usuario_controller.create_usuario(data)
    if errors:
        raise AppError(errors[0], 400)
    return jsonify({"dados": result, "sucesso": True}), 201


@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        raise AppError("Dados inválidos", 400)
    email = data.get("email", "")
    senha = data.get("senha", "")
    usuario, error = usuario_controller.login(email, senha)
    if error:
        status = 400 if "obrigatórios" in error else 401
        raise AppError(error, status)
    return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200


@api_bp.route("/pedidos", methods=["POST"])
def criar_pedido():
    data = request.get_json()
    result, error = pedido_controller.create_pedido(data)
    if error:
        raise AppError(error, 400)
    return jsonify({"dados": result, "sucesso": True, "mensagem": "Pedido criado com sucesso"}), 201


@api_bp.route("/pedidos", methods=["GET"])
def listar_todos_pedidos():
    pedidos = pedido_controller.get_all_pedidos()
    return jsonify({"dados": pedidos, "sucesso": True}), 200


@api_bp.route("/pedidos/usuario/<int:usuario_id>", methods=["GET"])
def listar_pedidos_usuario(usuario_id):
    pedidos = pedido_controller.get_pedidos_usuario(usuario_id)
    return jsonify({"dados": pedidos, "sucesso": True}), 200


@api_bp.route("/pedidos/<int:pedido_id>/status", methods=["PUT"])
def atualizar_status_pedido(pedido_id):
    data = request.get_json()
    result, error = pedido_controller.update_status_pedido(pedido_id, data)
    if error:
        raise AppError(error, 400)
    return jsonify({"sucesso": True, "mensagem": result["mensagem"]}), 200


@api_bp.route("/relatorios/vendas", methods=["GET"])
def relatorio_vendas():
    relatorio = relatorio_controller.get_relatorio_vendas()
    return jsonify({"dados": relatorio, "sucesso": True}), 200


@api_bp.route("/health", methods=["GET"])
def health_check():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    produtos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos = cursor.fetchone()[0]
    return jsonify({
        "status": "ok",
        "database": "connected",
        "counts": {"produtos": produtos, "usuarios": usuarios, "pedidos": pedidos},
    }), 200


@api_bp.route("/admin/reset-db", methods=["POST"])
def reset_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
