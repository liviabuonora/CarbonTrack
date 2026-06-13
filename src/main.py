import os
from database import criar_banco, conectar
from menus import menu_principal

criar_banco()
conn = conectar()
print("\033[32mBanco iniciado com sucesso.\033[0m")

try:
    menu_principal(conn)
finally:
    conn.close()