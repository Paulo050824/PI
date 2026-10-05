from models.tatuagens.tatuagem import Tatuagem

class Fineline(Tatuagem):
    def __init__(self, preco, tamanho, imagem, descricao, espessura_traco, id=None):
        super().__init__(preco, tamanho, imagem, descricao, id)
        self._espessura_traco = espessura_traco

    @property
    def espessura_traco(self):
        return self._espessura_traco

    @espessura_traco.setter
    def espessura_traco(self, valor):
        self._espessura_traco = valor