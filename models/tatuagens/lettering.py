from models.tatuagens.tatuagem import Tatuagem

class Lettering(Tatuagem):
    def __init__(self, preco, tamanho, imagem, descricao, fonte, id=None):
        super().__init__(preco, tamanho, imagem, descricao, id)
        self._fonte = fonte

    @property
    def fonte(self):
        return self._fonte

    @fonte.setter
    def fonte(self, valor):
        self._fonte = valor