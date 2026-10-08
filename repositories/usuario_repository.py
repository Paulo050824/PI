from banco.db import conectar
from models.usuario import Usuario


def criar_tabela_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            email VARCHAR(254) NOT NULL UNIQUE,
            senha_hash VARCHAR(254) NOT NULL,
            is_admin TINYINT(1) NOT NULL DEFAULT 0
        )
    """)

    # Se a tabela já existia sem a coluna is_admin, adiciona
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'usuario'
          AND COLUMN_NAME = 'is_admin'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "ALTER TABLE usuario ADD COLUMN is_admin TINYINT(1) NOT NULL DEFAULT 0"
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
        VALUES (%s, %s, %s)
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
        "SELECT id, nome, email, senha_hash, is_admin FROM usuario WHERE email = %s",
        (email,)
    )
    resultado = cursor.fetchone()
    conexao.close()

    return _montar_usuario(resultado) if resultado else None


def buscar_por_id(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, email, senha_hash, is_admin FROM usuario WHERE id = %s",
        (id_usuario,)
    )
    resultado = cursor.fetchone()
    conexao.close()

    return _montar_usuario(resultado) if resultado else None