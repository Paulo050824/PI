from models.tatuagens.tatuagem import Tatuagem

class Oriental(Tatuagem):
    def __init__(self, preco, tamanho, imagem, descricao, elemento_principal, id=None):
        super().__init__(preco, tamanho, imagem, descricao, id)
        self._elemento_principal = elemento_principal

    @property
    def elemento_principal(self):
        return self._elemento_principal

    @elemento_principal.setter
    def elemento_principal(self, valor):
        self._elemento_principal = valor