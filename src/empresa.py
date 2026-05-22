import os
import re

os.system ("cls")

empresas = []
contador_id = 0


class Empresa:

    def __init__(self, id_empresa, razao_social, cnpj, ramo):

        self.id = id_empresa
        self.razao_social = razao_social.strip()
        self.cnpj = cnpj.strip()
        self.ramo = ramo.strip().title()

    def exibir_dados(self):

        print("\n--- EMPRESA CADASTRADA ---")
        print(f"ID: {self.id}")
        print(f"Razão Social: {self.razao_social}")
        print(f"CNPJ: {self.cnpj}")
        print(f"Ramo: {self.ramo}")


def validar_cnpj(cnpj):

    cnpj = re.sub(r"\D", "", cnpj)

    if len(cnpj) != 14:
        return False

    return True


def buscar_empresa(id_empresa):

    for empresa in empresas:

        if empresa.id == id_empresa:
            return empresa

    return None


def listar_empresas():

    if len(empresas) == 0:

        print("\nNenhuma empresa cadastrada.")
        return

    print("\n--- EMPRESAS CADASTRADAS ---")

    for empresa in empresas:
        empresa.exibir_dados()


def cadastrar_empresa():

    global contador_id

    print("\n--- CADASTRO DE EMPRESA ---")

    razao_social = input("Digite a razão social: ")

    cnpj = input("Digite o CNPJ: ")

    while not validar_cnpj(cnpj):

        print("CNPJ inválido! Digite novamente.")
        cnpj = input("Digite o CNPJ: ")

    ramo = input("Digite o ramo da empresa: ")

    contador_id += 1

    empresa = Empresa(contador_id, razao_social, cnpj, ramo)

    empresas.append(empresa)

    print("\nEmpresa cadastrada com sucesso!")

    return empresa


continuar = "s"

while continuar.lower() == "s":

    print("\n========= MENU =========")
    print("1 - Cadastrar empresa")
    print("2 - Listar empresas")
    print("3 - Buscar empresa por ID")
    print("4 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":

        empresa_cadastrada = cadastrar_empresa()
        empresa_cadastrada.exibir_dados()

    elif opcao == "2":

        listar_empresas()

    elif opcao == "3":

        id_busca = int(input("\nDigite o ID da empresa: "))

        empresa = buscar_empresa(id_busca)

        if empresa:

            print("\nEmpresa encontrada!")
            empresa.exibir_dados()

        else:

            print("\nEmpresa não encontrada.")

    elif opcao == "4":

        print("\nSistema encerrado.")
        break

    else:

        print("\nOpção inválida.")

    while True:

        continuar = input("\nDeseja continuar? (s/n): ").lower()

        if continuar == "s" or continuar == "n":
            break

        print("Resposta inválida. Digite apenas 's' ou 'n'.")

print("\nFim do programa.")