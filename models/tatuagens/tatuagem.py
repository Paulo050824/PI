from models.tatuagens.avaliacao import Avaliacao


class Tatuagem:
    def __init__(self, nome, preco, tamanho, imagem, descricao, id=None):
        self._id = id
        self._nome = nome
        self._preco = float(preco)
        self._tamanho = float(tamanho)
        self._imagem = imagem
        self._descricao = descricao
        self._avaliacoes = []

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
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor):
        self._preco = float(valor)

    @property
    def tamanho(self):
        return self._tamanho

    @tamanho.setter
    def tamanho(self, valor):
        self._tamanho = float(valor)

    @property
    def imagem(self):
        return self._imagem

    @imagem.setter
    def imagem(self, valor):
        self._imagem = valor

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = valor

    @property
    def avaliacoes(self):
        return list(self._avaliacoes)

    def avaliar_tatuagem(self, cliente, nota):
        avaliacao = Avaliacao(cliente, nota)
        self._avaliacoes.append(avaliacao)

    def listar_avaliacoes_tatuagem(self):
        return list(self._avaliacoes)