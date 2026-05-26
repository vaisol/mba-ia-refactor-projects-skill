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
