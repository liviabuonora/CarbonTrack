import sqlite3

def conectar():

    conn = sqlite3.connect("database/app.db")

    conn.execute("PRAGMA foreign_keys = ON")

    return conn