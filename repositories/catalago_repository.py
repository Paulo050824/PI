from banco.db import conectar

def criar_tabela_catalogos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS catalogos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL
        )
    """

    cursor.execute(sql)
    conexao.commit()
    conexao.close()


def criar_catalogo(catalogo):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO catalogos (nome)
        VALUES (%s)
    """

    cursor.execute(sql, (catalogo.nome,))

    conexao.commit()
    conexao.close()


def listar_catalogos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT id, nome
        FROM catalogos
    """

    cursor.execute(sql)

    catalogos = cursor.fetchall()
    conexao.close()

    return catalogos