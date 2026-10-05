from models.tatuagens.tatuagem import Tatuagem

class Floral(Tatuagem):
    def __init__(self, preco, tamanho, imagem, descricao, tipo_flor, id=None):
        super().__init__(preco, tamanho, imagem, descricao, id)
        self._tipo_flor = tipo_flor

    @property
    def tipo_flor(self):
        return self._tipo_flor

    @tipo_flor.setter
    def tipo_flor(self, valor):
        self._tipo_flor = valor