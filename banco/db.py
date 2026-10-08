import os
import sqlite3

# O arquivo do banco fica na mesma pasta deste db.py (independe de onde o app é executado)
CAMINHO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "silveriotatooink.db")


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    # No SQLite as chaves estrangeiras vêm desligadas por padrão, é preciso ativar a cada conexão
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao