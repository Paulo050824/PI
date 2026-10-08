from banco.db import conectar
from models.usuario import Usuario


def criar_tabela_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Se a tabela já existia sem a coluna is_admin, adiciona
    cursor.execute("PRAGMA table_info(usuario)")
    colunas = [linha[1] for linha in cursor.fetchall()]
    if "is_admin" not in colunas:
        cursor.execute(
            "ALTER TABLE usuario ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0"
        )

    conexao.commit()
    conexao.close()


def criar_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    # is_admin não é inserido: todo cadastro novo nasce com 0 (padrão do banco)
    cursor.execute(
        """
        INSERT INTO usuario(nome, email, senha_hash)
        VALUES (?, ?, ?)
        """,
        (usuario.nome, usuario.email, usuario.senha_hash)
    )
    conexao.commit()
    id_gerado = cursor.lastrowid
    conexao.close()

    usuario.id = id_gerado
    return id_gerado


def _montar_usuario(resultado):
    id_usuario, nome, email, senha_hash, is_admin = resultado
    return Usuario(nome, email, senha_hash, id_usuario, bool(is_admin))


def buscar_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, email, senha_hash, is_admin FROM usuario WHERE email = ?",
        (email,)
    )
    resultado = cursor.fetchone()
    conexao.close()

    return _montar_usuario(resultado) if resultado else None


def buscar_por_id(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, email, senha_hash, is_admin FROM usuario WHERE id = ?",
        (id_usuario,)
    )
    resultado = cursor.fetchone()
    conexao.close()

    return _montar_usuario(resultado) if resultado else None