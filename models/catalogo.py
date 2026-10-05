class Catalogo:
    def __init__(self, id=None, nome=""):
        self._id = id
        self._nome = nome
        self._tatuagens = []

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
    def tatuagens(self):
        return list(self._tatuagens)

    def adicionar_tatuagem(self, tatuagem):
        self._tatuagens.append(tatuagem)

    def listar_tatuagens(self):
        return list(self._tatuagens)