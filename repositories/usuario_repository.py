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
            senha_hash VARCHAR(254) NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()


def criar_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO usuario(nome, email, senha_hash)
        VALUES (%s, %s, %s)
        """,
        (usuario.nome, usuario.email, usuario._senha_hash)
    )
    conexao.commit()
    id_gerado = cursor.lastrowid
    conexao.close()

    usuario.id = id_gerado
    return id_gerado


def buscar_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, email, senha_hash FROM usuario WHERE email = %s",
        (email,)
    )
    resultado = cursor.fetchone()
    conexao.close()

    if resultado is None:
        return None

    id_usuario, nome, email, senha_hash = resultado
    usuario = Usuario(nome, email, senha_hash)
    usuario.id = id_usuario
    return usuario


def buscar_por_id(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT id, nome, email, senha_hash FROM usuario
        WHERE id = %s
        """,
        (id_usuario,)
    )
    resultado = cursor.fetchone()
    conexao.close()

    if resultado is None:
        return None

    id_u, nome, email, senha_hash = resultado
    usuario = Usuario(nome, email, senha_hash)
    usuario.id = id_u
    return usuario