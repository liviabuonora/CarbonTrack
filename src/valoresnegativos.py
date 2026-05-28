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