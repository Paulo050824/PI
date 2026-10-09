import sys
from banco.db import conectar

if len(sys.argv) != 2:
    print("Uso: python tornar_admin.py email@exemplo.com")
    sys.exit(1)

email = sys.argv[1]

conexao = conectar()
cursor = conexao.cursor()

try:
    # Verifica se a coluna is_admin existe (SQLite); se não, cria
    cursor.execute("PRAGMA table_info(usuario)")
    colunas = [linha[1] for linha in cursor.fetchall()]

    if "is_admin" not in colunas:
        print("Coluna is_admin não existe. Criando...")
        cursor.execute(
            "ALTER TABLE usuario ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0"
        )
        conexao.commit()

    cursor.execute("UPDATE usuario SET is_admin = 1 WHERE email = ?", (email,))
    conexao.commit()

    if cursor.rowcount:
        print("OK, agora é admin.")
    else:
        print("Usuário não encontrado.")

except Exception as e:
    conexao.rollback()
    print("Erro:", e)

finally:
    cursor.close()
    conexao.close()