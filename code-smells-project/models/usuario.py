from database import get_db


def get_todos_usuarios():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios")
    rows = cursor.fetchall()
    return [_row_to_dict(row) for row in rows]


def get_usuario_por_id(usuario_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    return _row_to_dict(row) if row else None


def get_usuario_por_id_com_senha(usuario_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nome, email, senha, tipo, criado_em FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    if row:
        return {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "senha": row["senha"],
            "tipo": row["tipo"],
            "criado_em": row["criado_em"],
        }
    return None


def login_usuario(email, senha):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, nome, email, tipo FROM usuarios WHERE email = ? AND senha = ?",
        (email, senha),
    )
    row = cursor.fetchone()
    if row:
        return {"id": row["id"], "nome": row["nome"], "email": row["email"], "tipo": row["tipo"]}
    return None


def criar_usuario(nome, email, senha, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, senha, tipo),
    )
    db.commit()
    return cursor.lastrowid


def _row_to_dict(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }
