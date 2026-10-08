from banco.db import conectar
from models.tatuagens.avaliacao import Avaliacao


def criar_tabela_avaliacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_tatuagem INT NOT NULL,
            cliente VARCHAR(150) NOT NULL,
            nota DECIMAL(3,1) NOT NULL,

            FOREIGN KEY (id_tatuagem)
            REFERENCES tatuagem(id)
        )
    """)

    conexao.commit()
    cursor.close()
    conexao.close()


def criar_avaliacao(id_tatuagem, avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()

    # Corrigido: 'nome' alterado para 'cliente'
    cursor.execute("""
        INSERT INTO avaliacoes (id_tatuagem, cliente, nota)
        VALUES (%s, %s, %s)
    """, (id_tatuagem, avaliacao.cliente, avaliacao.nota))

    conexao.commit()
    cursor.close()
    conexao.close()


def listar_avaliacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    # Corrigido: 'nome' alterado para 'cliente'
    cursor.execute("""
        SELECT cliente, nota
        FROM avaliacoes
    """)

    avaliacoes = cursor.fetchall()
    cursor.close()
    conexao.close()

    return [
        Avaliacao(cliente, float(nota))
        for cliente, nota in avaliacoes
    ]


def listar_avaliacoes_por_tatuagem(id_tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()

    # Corrigido: 'nome' alterado para 'cliente'
    cursor.execute("""
        SELECT cliente, nota
        FROM avaliacoes
        WHERE id_tatuagem = %s
    """, (id_tatuagem,))

    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()

    return [
        Avaliacao(cliente, float(nota))
        for cliente, nota in resultado
    ]


def listar_completo(id_tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()

    # Corrigido: 'nome' alterado para 'cliente'
    cursor.execute("""
        SELECT id, id_tatuagem, cliente, nota
        FROM avaliacoes
        WHERE id_tatuagem = %s
    """, (id_tatuagem,))

    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()

    return resultado


# --- MÉTODOS DE REMOÇÃO ---

def remover_avaliacao(id_avaliacao):
    """Remove uma avaliação específica pelo seu ID."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM avaliacoes
        WHERE id = %s
    """, (id_avaliacao,))

    conexao.commit()
    cursor.close()
    conexao.close()


def remover_avaliacoes_por_tatuagem(id_tatuagem):
    """Remove todas as avaliações associadas a uma determinada tatuagem."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM avaliacoes
        WHERE id_tatuagem = %s
    """, (id_tatuagem,))

    conexao.commit()
    cursor.close()
    conexao.close()