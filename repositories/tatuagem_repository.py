from banco.db import conectar
from models.tatuagens.tatuagem import Tatuagem


def criar_tabela_tatuagens():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tatuagem(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            tamanho REAL NOT NULL,
            imagem TEXT,
            descricao TEXT
        )
    """)

    # Se a tabela já existia com colunas diferentes, adiciona as que faltam
    colunas = {
        'nome': "TEXT NOT NULL DEFAULT ''",
        'preco': "REAL NOT NULL DEFAULT 0",
        'tamanho': "REAL NOT NULL DEFAULT 0",
        'imagem': "TEXT",
        'descricao': "TEXT",
    }

    # PRAGMA table_info retorna (cid, name, type, notnull, dflt_value, pk)
    cursor.execute("PRAGMA table_info(tatuagem)")
    existentes = {linha[1] for linha in cursor.fetchall()}

    for coluna, definicao in colunas.items():
        if coluna not in existentes:
            cursor.execute(f"ALTER TABLE tatuagem ADD COLUMN {coluna} {definicao}")

    conexao.commit()
    conexao.close()


def criar_tatuagem(tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO tatuagem(nome, preco, tamanho, imagem, descricao)
        VALUES (?, ?, ?, ?, ?)
        """,
        (tatuagem.nome, tatuagem.preco, tatuagem.tamanho,
         tatuagem.imagem, tatuagem.descricao)
    )
    conexao.commit()
    id_gerado = cursor.lastrowid
    conexao.close()

    tatuagem.id = id_gerado
    return id_gerado


def _montar_tatuagem(linha):
    id_t, nome, preco, tamanho, imagem, descricao = linha
    return Tatuagem(nome, preco, tamanho, imagem, descricao, id_t)


def listar_tatuagens():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, preco, tamanho, imagem, descricao FROM tatuagem ORDER BY id DESC"
    )
    linhas = cursor.fetchall()
    conexao.close()

    return [_montar_tatuagem(linha) for linha in linhas]


def buscar_por_id(id_tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, preco, tamanho, imagem, descricao FROM tatuagem WHERE id = ?",
        (id_tatuagem,)
    )
    linha = cursor.fetchone()
    conexao.close()

    return _montar_tatuagem(linha) if linha else None


def excluir_tatuagem(id_tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()

    # Apaga primeiro as avaliações, senão a chave estrangeira bloqueia a exclusão
    cursor.execute("DELETE FROM avaliacoes WHERE id_tatuagem = ?", (id_tatuagem,))
    cursor.execute("DELETE FROM tatuagem WHERE id = ?", (id_tatuagem,))

    conexao.commit()
    conexao.close()