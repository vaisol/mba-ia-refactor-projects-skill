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
        # Eager loading items with a join to avoid N+1
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
from src.config.database import get_db

class ProdutoModel:
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM produtos")
        return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def create(nome, descricao, preco, estoque, categoria):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
            (nome, descricao, preco, estoque, categoria)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update(id, nome, descricao, preco, estoque, categoria):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?",
            (nome, descricao, preco, estoque, categoria, id)
        )
        db.commit()
        return True

    @staticmethod
    def delete(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
        db.commit()
        return True

    @staticmethod
    def search(termo, categoria=None, preco_min=None, preco_max=None):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []
        if termo:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            params.extend([f"%{termo}%", f"%{termo}%"])
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if preco_min:
            query += " AND preco >= ?"
            params.append(preco_min)
        if preco_max:
            query += " AND preco <= ?"
            params.append(preco_max)
        
        cursor.execute(query, tuple(params))
        return [dict(row) for row in cursor.fetchall()]
from src.config.database import get_db

class UsuarioModel:
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, nome, email, tipo FROM usuarios")
        return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, nome, email, tipo FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_by_email(email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def create(nome, email, senha_hash, tipo="cliente"):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash, tipo)
        )
        db.commit()
        return cursor.lastrowid
