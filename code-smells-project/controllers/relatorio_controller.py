import logging
from models import relatorio as relatorio_model

logger = logging.getLogger(__name__)


def get_relatorio_vendas():
    return relatorio_model.relatorio_vendas()
