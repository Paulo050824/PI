from banco.db import conectar
from models.tatuagens.tatuagem import Tatuagem


def criar_tabela_tatuagens():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tatuagem(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            preco DECIMAL(10,2) NOT NULL,
            tamanho DECIMAL(10,2) NOT NULL,
            imagem VARCHAR(255),
            descricao TEXT
        )
    """)

    # Se a tabela já existia com colunas diferentes, adiciona as que faltam
    colunas = {
        'nome': "VARCHAR(150) NOT NULL DEFAULT ''",
        'preco': "DECIMAL(10,2) NOT NULL DEFAULT 0",
        'tamanho': "DECIMAL(10,2) NOT NULL DEFAULT 0",
        'imagem': "VARCHAR(255)",
        'descricao': "TEXT",
    }
    for coluna, definicao in colunas.items():
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'tatuagem'
              AND COLUMN_NAME = %s
        """, (coluna,))
        if cursor.fetchone()[0] == 0:
            cursor.execute(f"ALTER TABLE tatuagem ADD COLUMN {coluna} {definicao}")

    conexao.commit()
    conexao.close()


def criar_tatuagem(tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO tatuagem(nome, preco, tamanho, imagem, descricao)
        VALUES (%s, %s, %s, %s, %s)
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
        "SELECT id, nome, preco, tamanho, imagem, descricao FROM tatuagem WHERE id = %s",
        (id_tatuagem,)
    )
    linha = cursor.fetchone()
    conexao.close()

    return _montar_tatuagem(linha) if linha else None


def excluir_tatuagem(id_tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()

    # Apaga primeiro as avaliações, senão a chave estrangeira bloqueia a exclusão
    cursor.execute("DELETE FROM avaliacoes WHERE id_tatuagem = %s", (id_tatuagem,))
    cursor.execute("DELETE FROM tatuagem WHERE id = %s", (id_tatuagem,))

    conexao.commit()
    conexao.close()