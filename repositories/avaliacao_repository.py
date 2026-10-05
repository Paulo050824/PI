from banco.db import conectar
from models.tatuagens.avaliacao import Avaliacao

def criar_tabela_avaliacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    criar_tabela = """
        CREATE TABLE IF NOT EXISTS avaliacoes(
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_tatuagem INT NOT NULL,
            nome VARCHAR(100) NOT NULL,
            nota FLOAT(2,1) NOT NULL,
            FOREIGN KEY (id_tatuagem) REFERENCES tatuagens(id)
        )
    """

    cursor.execute(criar_tabela)
    conexao.commit()
    conexao.close()


def criar_avaliacao(id_tatuagem, avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO avaliacoes(id_tatuagem, nome, nota)
        VALUES (%s, %s, %s)
    """, (id_tatuagem, avaliacao.cliente, avaliacao.nota))

    conexao.commit()
    conexao.close()


def listar_avaliacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, nota
        FROM avaliacoes
    """)

    avaliacoes = cursor.fetchall()
    conexao.close()

    return [
        Avaliacao(nome, float(nota))
        for nome, nota in avaliacoes
    ]


def listar_avaliacoes_por_tatuagem(id_tatuagem):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, nota
        FROM avaliacoes
        WHERE id_tatuagem = %s
    """, (id_tatuagem,))

    resultado = cursor.fetchall()
    conexao.close()

    return [
        Avaliacao(nome, float(nota))
        for nome, nota in resultado
    ]