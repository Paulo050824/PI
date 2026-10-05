class Usuario:
    def __init__(self, nome, email, senha_hash, id=None):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha_hash = senha_hash

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
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = valor

    @property
    def senha_hash(self):
        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, valor):
        self._senha_hash = valor