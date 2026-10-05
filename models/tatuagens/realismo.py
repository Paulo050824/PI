from models.tatuagens.tatuagem import Tatuagem

class Realismo(Tatuagem):
    def __init__(self, preco, tamanho, imagem, descricao, nivel_detalhamento, id=None):
        super().__init__(preco, tamanho, imagem, descricao, id)
        self._nivel_detalhamento = nivel_detalhamento

    @property
    def nivel_detalhamento(self):
        return self._nivel_detalhamento

    @nivel_detalhamento.setter
    def nivel_detalhamento(self, valor):
        self._nivel_detalhamento = valor