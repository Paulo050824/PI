from banco.db import conectar
from models.tatuagens.avaliacao import Avaliacao


def _coluna_ja_existe(erro):
    """True se o erro do MySQL for 'Duplicate column name' (código 1060)."""
    return "1060" in str(erro) or "duplicate column" in str(erro).lower()


def criar_tabela_avaliacoes():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        # Cria a tabela já com o id_usuario para evitar alter table complexo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_tatuagem INT NOT NULL,
                id_usuario INT NULL,
                cliente VARCHAR(150) NOT NULL,
                nota DECIMAL(3,1) NOT NULL,
                FOREIGN KEY (id_tatuagem) REFERENCES tatuagem(id) ON DELETE CASCADE,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE SET NULL
            )
        """)
        conexao.commit()

        # Caso a tabela já exista de uma versão anterior sem o id_usuario, 
        # garantimos a adição da coluna e da chave estrangeira de forma separada:
        try:
            cursor.execute("ALTER TABLE avaliacoes ADD COLUMN id_usuario INT NULL")
            conexao.commit()
        except Exception as erro:
            if not _coluna_ja_existe(erro):
                raise

        try:
            cursor.execute("""
                ALTER TABLE avaliacoes 
                ADD CONSTRAINT fk_avaliacoes_usuario 
                FOREIGN KEY (id_usuario) REFERENCES usuario(id) 
                ON DELETE SET NULL
            """)
            conexao.commit()
        except Exception as erro:
            # Ignora se a constraint/fk já existir (código comum do MySQL para duplicate foreign key é 1826 ou similar)
            if "1826" not in str(erro) and "already exists" not in str(erro).lower():
                pass

    finally:
        cursor.close()
        conexao.close()


def criar_avaliacao(id_tatuagem, avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO avaliacoes (id_tatuagem, cliente, nota, id_usuario)
            VALUES (%s, %s, %s, %s)
        """, (id_tatuagem, avaliacao.cliente, avaliacao.nota, avaliacao.id_usuario))
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()


def listar_avaliacoes():
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT cliente, nota
            FROM avaliacoes
        """)
        avaliacoes = cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

    return [
        Avaliacao(cliente, float(nota))
        for cliente, nota in avaliacoes
    ]


def listar_avaliacoes_por_tatuagem(id_tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id, cliente, nota, id_usuario
            FROM avaliacoes
            WHERE id_tatuagem = %s
        """, (id_tatuagem,))
        resultado = cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

    return [
        Avaliacao(cliente, float(nota), id_avaliacao, id_usuario)
        for id_avaliacao, cliente, nota, id_usuario in resultado
    ]


def listar_completo(id_tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id, id_tatuagem, cliente, nota
            FROM avaliacoes
            WHERE id_tatuagem = %s
        """, (id_tatuagem,))
        resultado = cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

    return resultado


# --- MÉTODOS DE REMOÇÃO ---

def remover_avaliacao(id_avaliacao):
    """Remove uma avaliação específica pelo seu ID."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            DELETE FROM avaliacoes
            WHERE id = %s
        """, (id_avaliacao,))
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()


def remover_avaliacoes_por_tatuagem(id_tatuagem):
    """Remove todas as avaliações associadas a uma determinada tatuagem."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            DELETE FROM avaliacoes
            WHERE id_tatuagem = %s
        """, (id_tatuagem,))
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()