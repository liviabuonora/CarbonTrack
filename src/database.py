import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "app.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_banco():
    conn = conectar()
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as arquivo:
            sql = arquivo.read()
        conn.executescript(sql)
    except FileNotFoundError:
        print(f"Erro: arquivo schema.sql não encontrado em {SCHEMA_PATH}")
    finally:      
        conn.close()