import pytest
from models.tatuagens.tatuagem import Tatuagem

def test_tatuagem_samurai():
    tatuagem = Tatuagem(
        "Samurai da Morte",
        0,
        25,
        "tatto_paulo.png",
        "Caveira com armadura e capacete de samurai.",
        1
       
    )

    assert tatuagem._nome == "Samurai da Morte"
    assert tatuagem._tamanho == 25
    assert tatuagem._descricao == "Caveira com armadura e capacete de samurai."
    assert tatuagem.imagem ==  "tatto_paulo.png"
    assert tatuagem.preco == 0
    assert tatuagem.id == 1
