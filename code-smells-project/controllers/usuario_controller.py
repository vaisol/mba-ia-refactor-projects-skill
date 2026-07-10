import logging
from models import usuario as usuario_model

logger = logging.getLogger(__name__)


def get_all_usuarios():
    return usuario_model.get_todos_usuarios()


def get_usuario(usuario_id):
    return usuario_model.get_usuario_por_id(usuario_id)


def create_usuario(data):
    errors = validate_usuario_data(data)
    if errors:
        return None, errors

    nome = data.get("nome", "")
    email = data.get("email", "")
    senha = data.get("senha", "")

    usuario_id = usuario_model.criar_usuario(nome, email, senha)
    logger.info(f"Usuário criado: {email}")
    return {"id": usuario_id}, None


def login(email, senha):
    if not email or not senha:
        return None, "Email e senha são obrigatórios"

    usuario = usuario_model.login_usuario(email, senha)
    if usuario:
        logger.info(f"Login bem-sucedido: {email}")
        return usuario, None
    logger.info(f"Login falhou: {email}")
    return None, "Email ou senha inválidos"


def validate_usuario_data(data):
    errors = []
    if not data:
        return ["Dados inválidos"]
    nome = data.get("nome", "")
    email = data.get("email", "")
    senha = data.get("senha", "")
    if not nome:
        errors.append("Nome é obrigatório")
    if not email:
        errors.append("Email é obrigatório")
    if not senha:
        errors.append("Senha é obrigatória")
    return errors
