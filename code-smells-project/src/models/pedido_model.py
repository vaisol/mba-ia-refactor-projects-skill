from src.config.database import get_db

class PedidoModel:
    @staticmethod
    def create(usuario_id, total, itens):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total)
        )
        pedido_id = cursor.lastrowid

        for item in itens:
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item['produto_id'], item['quantidade'], item['preco_unitario'])
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item['quantidade'], item['produto_id'])
            )
        db.commit()
        return pedido_id

    @staticmethod
    def get_by_user(usuario_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.*, ip.produto_id, ip.quantidade, ip.preco_unitario, prod.nome as produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
            LEFT JOIN produtos prod ON ip.produto_id = prod.id
            WHERE p.usuario_id = ?
        """, (usuario_id,))

        rows = cursor.fetchall()
        pedidos = {}
        for row in rows:
            p_id = row['id']
            if p_id not in pedidos:
                pedidos[p_id] = {
                    "id": row['id'],
                    "usuario_id": row['usuario_id'],
                    "status": row['status'],
                    "total": row['total'],
                    "criado_em": row['criado_em'],
                    "itens": []
                }
            if row['produto_id']:
                pedidos[p_id]['itens'].append({
                    "produto_id": row['produto_id'],
                    "produto_nome": row['produto_nome'],
                    "quantidade": row['quantidade'],
                    "preco_unitario": row['preco_unitario']
                })
        return list(pedidos.values())

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.*, ip.produto_id, ip.quantidade, ip.preco_unitario, prod.nome as produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
            LEFT JOIN produtos prod ON ip.produto_id = prod.id
        """)
        rows = cursor.fetchall()
        pedidos = {}
        for row in rows:
            p_id = row['id']
            if p_id not in pedidos:
                pedidos[p_id] = dict(row)
                pedidos[p_id]['itens'] = []
            if row['produto_id']:
                pedidos[p_id]['itens'].append({
                    "produto_id": row['produto_id'],
                    "produto_nome": row['produto_nome'],
                    "quantidade": row['quantidade'],
                    "preco_unitario": row['preco_unitario']
                })
        return list(pedidos.values())

    @staticmethod
    def update_status(pedido_id, status):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, pedido_id))
        db.commit()
        return True

    @staticmethod
    def get_vendas_report():
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM pedidos")
        total_pedidos = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total) FROM pedidos")
        faturamento = cursor.fetchone()[0]
        if faturamento is None:
            faturamento = 0

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
        pendentes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
        aprovados = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
        cancelados = cursor.fetchone()[0]

        return {
            "total_pedidos": total_pedidos,
            "faturamento_total": faturamento,
            "pedidos_por_status": {
                "pendente": pendentes,
                "aprovado": aprovados,
                "cancelado": cancelados
            }
        }
