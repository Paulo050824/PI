class Avaliacao:
    def __init__(self, cliente, nota, id=None, id_usuario=None):
        self._id = id
        self._id_usuario = id_usuario
        self._cliente = cliente
        self._nota = float(nota)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        self._cliente = valor

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, valor):
        self._nota = float(valor)

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor):
        self._id_usuario = valor