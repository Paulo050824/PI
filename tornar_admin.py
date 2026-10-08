import sys
from banco.db import conectar

if len(sys.argv) != 2:
    print("Uso: python tornar_admin.py email@exemplo.com")
    sys.exit(1)

conexao = conectar()
cursor = conexao.cursor()
cursor.execute("UPDATE usuario SET is_admin = 1 WHERE email = %s", (sys.argv[1],))
conexao.commit()
print("OK, agora é admin." if cursor.rowcount else "Usuário não encontrado.")
conexao.close()