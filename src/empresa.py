empresas = []

def validar_cnpj(cnpj):
    if len(cnpj) == 14:
        return True
    else:
        return False

def cadastrar_empresa():
    print("\n--- CADASTRO DE EMPRESA ---")
    razao_social = input("Digite a razão social: ")
    cnpj = input("Digite o CNPJ: ")

    while not validar_cnpj(cnpj):
        print("CNPJ inválido!")
        cnpj = input("Digite o CNPJ novamente: ")

    setor = input("Digite o setor da empresa: ")

    empresa = {
        "id": len(empresas) + 1,
        "razao_social": razao_social,
        "cnpj": cnpj,
        "setor": setor
    }

    empresas.append(empresa)
    print("Empresa cadastrada com sucesso!")

def listar_empresas():
    if len(empresas) == 0:
        print("\nNenhuma empresa cadastrada.")
        return

    print("\n--- EMPRESAS CADASTRADAS ---")

    for empresa in empresas:
        print(f"\nID: {empresa['id']}")
        print(f"Razão Social: {empresa['razao_social']}")
        print(f"CNPJ: {empresa['cnpj']}")
        print(f"Setor: {empresa['setor']}")

def buscar_empresa():
    id_busca = int(input("Digite o ID da empresa: "))

    for empresa in empresas:

        if empresa["id"] == id_busca:
            print("\nEmpresa encontrada!")
            print(f"ID: {empresa['id']}")
            print(f"Razão Social: {empresa['razao_social'].strip().capitalize()}")
            print(f"CNPJ: {empresa['cnpj'].strip()}")
            print(f"Setor: {empresa['setor'].strip().capitalize()}")
            return

        else:
            print("Empresa não encontrada.")

while True:
    print("\n---- MENU ----")
    print("1- Cadastrar empresa")
    print("2- Listar empresas")
    print("3- Buscar empresa")
    print("4- Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_empresa()

    elif opcao == "2":
        listar_empresas()

    elif opcao == "3":
        buscar_empresa()

    elif opcao == "4":
        print("Programa encerrado.")
        break

    else:
        print("Opção inválida.")