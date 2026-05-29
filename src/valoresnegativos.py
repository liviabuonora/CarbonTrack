import os
os.system("cls")

def verificar_valor(valor):
    if valor < 0:
        print(f"Erro: o valor {valor} é inválido.")
    elif valor == 0:
        print(f"Erro: o valor {valor} é inválido.")
    else:
        print(f"O valor {valor} é válido.")

def main():
    print("Sistema de validação de valores.")

    while True:
        comeco = input("Digite um valor (ou SAIR para finalizar): ")

        if comeco.lower() == "sair":
            print("Sistema finalizado.")
            break

        try:
            valor = float(comeco)
            verificar_valor(valor)
        except ValueError:
            print("Entrada inválida. Digite um valor válido.")

        print()

main()

def validar_quantidade(quantidade):
    if quantidade <= 0:
        print("Quantidade deve ser maior que zero.")
        return False
    return True

def validar_discrepancia(conn, fonte_id, quantidade):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT quantidade FROM consumos
        WHERE fonte_id = ?
        ORDER BY id DESC
        LIMIT 3
    """, (fonte_id,))
    
    historico = cursor.fetchall()
    
    if len(historico) == 0:
        return True
    
    valores = [item[0] for item in historico]
    media = sum(valores) / len(valores)
    
    if quantidade > media * 5:
        print("Aviso: quantidade muito acima do histórico recente!")
        resposta = input("Deseja continuar? (s/n): ")
        if resposta.lower() != "s":
            print("Consumo não registrado.")
            return False
    
    return True