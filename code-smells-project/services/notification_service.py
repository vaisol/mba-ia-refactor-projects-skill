import logging

logger = logging.getLogger(__name__)


def notify_order_created(order_id, user_id):
    logger.info(f"NOTIFICATION: Pedido {order_id} criado para usuario {user_id}")


def notify_order_status_changed(order_id, new_status):
    if new_status == "aprovado":
        logger.info(f"NOTIFICATION: Pedido {order_id} foi aprovado! Preparar envio.")
    elif new_status == "cancelado":
        logger.info(f"NOTIFICATION: Pedido {order_id} cancelado. Devolver estoque.")
