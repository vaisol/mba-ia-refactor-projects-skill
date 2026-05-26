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
