from database import conectar

connect = conectar()

with open("database/schema.sql", "r", encoding ="utf-8") as arquivo:
    sql = arquivo.read()

connect.executescript(sql)

print("Banco criado")

connect.close()