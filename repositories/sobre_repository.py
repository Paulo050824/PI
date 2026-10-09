from banco.db import conectar
from models.tatuagens.tatuagem import Tatuagem


def _linha_para_tatuagem(linha):
    return Tatuagem(
        id=linha[0],
        nome=linha[1],
        descricao=linha[2],
        imagem=linha[4],
    )


def criar_tabela_tatuagens():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS tatuagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            imagem TEXT
        )
    """

    cursor.execute(sql)
    conexao.commit()
    conexao.close()


def criar_tatuagem(tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO tatuagens (nome, descricao, imagem)
        VALUES (?, ?, ?, ?)
    """

    cursor.execute(sql, (
        tatuagem.nome,
        tatuagem.descricao,
        tatuagem.imagem,
    ))

    conexao.commit()
    conexao.close()


def listar_tatuagens():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, descricao, imagem
        FROM tatuagens
        ORDER BY nome
    """)

    linhas = cursor.fetchall()
    conexao.close()

    return [_linha_para_tatuagem(l) for l in linhas]


def buscar_tatuagem(tatuagem_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, descricao,  imagem
        FROM tatuagens
        WHERE id = ?
    """, (tatuagem_id,))

    linha = cursor.fetchone()
    conexao.close()

    return _linha_para_tatuagem(linha) if linha else None