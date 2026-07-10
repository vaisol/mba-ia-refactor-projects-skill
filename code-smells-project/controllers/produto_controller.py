import logging
from models import produto as produto_model

logger = logging.getLogger(__name__)

VALID_CATEGORIAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]


def get_all_produtos():
    return produto_model.get_todos_produtos()


def get_produto(produto_id):
    return produto_model.get_produto_por_id(produto_id)


def create_produto(data):
    errors = validate_produto_data(data)
    if errors:
        return None, errors

    produto_id = produto_model.criar_produto(
        data["nome"],
        data.get("descricao", ""),
        data["preco"],
        data["estoque"],
        data.get("categoria", "geral"),
    )
    logger.info(f"Produto criado com ID: {produto_id}")
    return {"id": produto_id}, None


def update_produto(produto_id, data):
    existing = produto_model.get_produto_por_id(produto_id)
    if not existing:
        return None, ["Produto não encontrado"]

    errors = validate_produto_data(data)
    if errors:
        return None, errors

    produto_model.atualizar_produto(
        produto_id,
        data["nome"],
        data.get("descricao", ""),
        data["preco"],
        data["estoque"],
        data.get("categoria", "geral"),
    )
    return {"mensagem": "Produto atualizado"}, None


def delete_produto(produto_id):
    produto = produto_model.get_produto_por_id(produto_id)
    if not produto:
        return False, "Produto não encontrado"
    produto_model.deletar_produto(produto_id)
    logger.info(f"Produto {produto_id} deletado")
    return True, None


def search_produtos(termo, categoria=None, preco_min=None, preco_max=None):
    return produto_model.buscar_produtos(termo, categoria, preco_min, preco_max)


def validate_produto_data(data):
    errors = []
    if not data:
        return ["Dados inválidos"]
    if "nome" not in data:
        errors.append("Nome é obrigatório")
    if "preco" not in data:
        errors.append("Preço é obrigatório")
    if "estoque" not in data:
        errors.append("Estoque é obrigatório")
    if errors:
        return errors

    nome = data["nome"]
    preco = data["preco"]
    estoque = data["estoque"]
    categoria = data.get("categoria", "geral")

    if len(nome) < 2:
        errors.append("Nome muito curto")
    if len(nome) > 200:
        errors.append("Nome muito longo")
    if preco < 0:
        errors.append("Preço não pode ser negativo")
    if estoque < 0:
        errors.append("Estoque não pode ser negativo")
    if categoria not in VALID_CATEGORIAS:
        errors.append(f"Categoria inválida. Válidas: {VALID_CATEGORIAS}")
    return errors
