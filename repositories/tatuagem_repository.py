from banco.db import conectar
from models.tatuagens.tatuagem import Tatuagem
from models.tatuagens.fineline import Fineline
from models.tatuagens.floral import Floral
from models.tatuagens.lettering import Lettering
from models.tatuagens.oriental import Oriental
from models.tatuagens.realismo import Realismo 


def criar_tabela_tatuagens():
    conexao = conectar()
    cursor = conexao.cursor()
    
    sql = """
    CREATE TABLE IF NOT EXISTS tatuagens(
        id INT PRIMARY KEY AUTO_INCREMENT,
        preco FLOAT(10,2) NOT NULL,
        tamanho FLOAT(5,2) NOT NULL,
        descricao VARCHAR(255) NOT NULL,
        estilo VARCHAR(50) NOT NULL,
        espessura_traco VARCHAR(50),
        tipo_flor VARCHAR(50),
        fonte VARCHAR(50),
        nivel_detalhamento VARCHAR(50),
        elemento_principal VARCHAR(50),
        imagem LONGBLOB
    )
    """
    cursor.execute(sql)
    conexao.commit()
    conexao.close()


def ler_imagem(caminho_imagem):
    with open(caminho_imagem, "rb") as arquivo:
        return arquivo.read()

    
def criar_tatuagem(tatuagem, tatoo, caminho_img):
    espessura_traco = tipo_flor = fonte = nivel_detalhamento = elemento_principal = None

    if isinstance(tatoo, Fineline):
        estilo = 'Fineline'
        espessura_traco = tatoo.espessura_traco
    elif isinstance(tatoo, Realismo):
        estilo = 'Realismo'
        nivel_detalhamento = tatoo.nivel_detalhamento
    elif isinstance(tatoo, Oriental):
        estilo = 'Oriental'
        elemento_principal = tatoo.elemento_principal
    elif isinstance(tatoo, Lettering):
        estilo = 'Letterring'
        fonte = tatoo.fonte
        
    elif isinstance(tatoo, Floral):
        estilo = 'Floral'
        tipo_flor = tatoo.tipo_flor
    else:
        return "Tatuagem não cadastrada"

    conexao = conectar()
    cursor = conexao.cursor()
    imagem = ler_imagem(caminho_img)

    sql = """
        INSERT INTO tatuagens(
            preco, tamanho, descricao, estilo, nivel_detalhamento, 
            fonte, espessura_traco, elemento_principal, tipo_flor, imagem
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        tatuagem.preco,
        tatuagem.tamanho,
        tatuagem.descricao,
        estilo,
        nivel_detalhamento, 
        fonte, 
        espessura_traco, 
        elemento_principal, 
        tipo_flor,
        imagem
    )

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()


def listar_tatuagens():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, preco, tamanho, descricao, estilo, nivel_detalhamento, fonte, espessura_traco, elemento_principal, tipo_flor, imagem 
        FROM tatuagens
    """)
    resultado = cursor.fetchall()
    conexao.close()

    tatuagens = []
    for row in resultado:
        _, preco, tamanho, descricao, estilo, nivel_detalhamento, fonte, espessura_traco, elemento_principal, tipo_flor, imagem = row
        
        if estilo == 'Fineline':
            tatuagens.append(Fineline(preco, tamanho, imagem, descricao, espessura_traco))
        elif estilo == 'Realismo':
            tatuagens.append(Realismo(preco, tamanho, imagem, descricao, nivel_detalhamento))
        elif estilo == 'Oriental':
            tatuagens.append(Oriental(preco, tamanho, imagem, descricao, elemento_principal))
        elif estilo == 'Letterring':
            tatuagens.append(Lettering(preco, tamanho, imagem, descricao, fonte))
        elif estilo == 'Floral':
            tatuagens.append(Floral(preco, tamanho, imagem, descricao, tipo_flor))

    return tatuagens