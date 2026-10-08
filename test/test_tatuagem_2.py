import pytest
from models.tatuagens.tatuagem import Tatuagem

def test_tatuagem_flores():
    tatuagem = Tatuagem(
        "Jardim de Borboletas",
        0,
        30,
        "tattoo_flores",
        "Flores, folhas e borboletas em estilo fine line.", 2
    )

    assert tatuagem._nome == "Jardim de Borboletas"
    assert tatuagem.preco == 0
    assert tatuagem._tamanho == 30
    assert tatuagem.imagem == "tattoo_flores"
    assert tatuagem._descricao == "Flores, folhas e borboletas em estilo fine line.", 2
