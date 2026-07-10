import logging
from models import pedido as pedido_model
from services.notification_service import (
    notify_order_created,
    notify_order_status_changed,
)

logger = logging.getLogger(__name__)


def create_pedido(data):
    if not data:
        return None, "Dados inválidos"

    usuario_id = data.get("usuario_id")
    itens = data.get("itens", [])

    if not usuario_id:
        return None, "Usuario ID é obrigatório"
    if not itens or len(itens) == 0:
        return None, "Pedido deve ter pelo menos 1 item"

    resultado = pedido_model.criar_pedido(usuario_id, itens)

    if "erro" in resultado:
        return None, resultado["erro"]

    notify_order_created(resultado["pedido_id"], usuario_id)
    return resultado, None


def get_pedidos_usuario(usuario_id):
    return pedido_model.get_pedidos_usuario(usuario_id)


def get_all_pedidos():
    return pedido_model.get_todos_pedidos()


def update_status_pedido(pedido_id, data):
    novo_status = data.get("status", "")
    valid_statuses = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]
    if novo_status not in valid_statuses:
        return None, "Status inválido"

    pedido_model.atualizar_status_pedido(pedido_id, novo_status)
    notify_order_status_changed(pedido_id, novo_status)
    return {"mensagem": "Status atualizado"}, None
