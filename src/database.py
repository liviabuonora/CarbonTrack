import sqlite3
import os

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_BANCO = os.path.join(PASTA_PROJETO, "database", "app.db")
CAMINHO_ARQUIVO_SQL = os.path.join(PASTA_PROJETO, "database", "schema.sql")

def conectar():
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_banco():
    conn = conectar()
    try:
        with open(CAMINHO_ARQUIVO_SQL, "r", encoding="utf-8") as arquivo:
            sql = arquivo.read()
        conn.executescript(sql)
    except FileNotFoundError:
        print(f"Erro: arquivo schema.sql não encontrado em {CAMINHO_ARQUIVO_SQL}")
    finally:      
        conn.close()