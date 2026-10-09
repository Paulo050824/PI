from models.tatuagens.tatuagem import Tatuagem
class Tatuagem:
    def __init__(self, id=None, nome="", descricao="", preco=None, imagem=None):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._preco = preco
        self._imagem = imagem

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = valor

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor):
        self._preco = valor

    @property
    def imagem(self):
        return self._imagem

    @imagem.setter
    def imagem(self, valor):
        self._imagem = valor