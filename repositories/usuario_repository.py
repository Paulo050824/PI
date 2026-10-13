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


# =========================
# AVALIAÇÕES DO USUÁRIO
# =========================

def remover_avaliacao_do_usuario(id_avaliacao, id_usuario):
    """
    Remove a avaliação somente se ela pertencer ao usuário informado.
    A checagem de dono é feita no próprio DELETE (atômico).
    Retorna True se removeu; False se não existe ou é de outra pessoa.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "DELETE FROM avaliacoes WHERE id = %s AND id_usuario = %s",
            (id_avaliacao, id_usuario)
        )
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conexao.close()


# =========================
# COMENTÁRIOS DO USUÁRIO
# =========================

def criar_tabela_comentarios():
    # Precisa rodar depois de criar as tabelas usuario e tatuagem
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_tatuagem INT NOT NULL,
            id_usuario INT NOT NULL,
            texto VARCHAR(500) NOT NULL,
            criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_tatuagem) REFERENCES tatuagem(id) ON DELETE CASCADE,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
        )
    """)
    conexao.commit()
    cursor.close()
    conexao.close()


def deixar_comentario(id_usuario, id_tatuagem, texto):
    """
    Salva um comentário do usuário em uma tatuagem.
    Retorna o id do comentário criado.
    Levanta ValueError se o texto for vazio ou passar de 500 caracteres.
    """
    texto = (texto or "").strip()
    if not texto:
        raise ValueError("O comentário não pode ficar vazio.")
    if len(texto) > 500:
        raise ValueError("O comentário pode ter no máximo 500 caracteres.")

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO comentarios (id_tatuagem, id_usuario, texto)
            VALUES (%s, %s, %s)
            """,
            (id_tatuagem, id_usuario, texto)
        )
        conexao.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conexao.close()


def listar_comentarios_por_tatuagem(id_tatuagem):
    """Devolve uma lista de dicts: id, id_usuario, nome, texto, criado_em."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            SELECT c.id, c.id_usuario, u.nome, c.texto, c.criado_em
            FROM comentarios c
            JOIN usuario u ON u.id = c.id_usuario
            WHERE c.id_tatuagem = %s
            ORDER BY c.criado_em DESC, c.id DESC
            """,
            (id_tatuagem,)
        )
        return [
            {"id": i, "id_usuario": uid, "nome": nome,
             "texto": texto, "criado_em": criado_em}
            for i, uid, nome, texto, criado_em in cursor.fetchall()
        ]
    finally:
        cursor.close()
        conexao.close()


def remover_comentario_do_usuario(id_comentario, id_usuario):
    """Remove o comentário somente se for do usuário. Retorna True/False."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "DELETE FROM comentarios WHERE id = %s AND id_usuario = %s",
            (id_comentario, id_usuario)
        )
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conexao.close()