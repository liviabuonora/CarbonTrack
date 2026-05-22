from database import criar_banco
from empresa import cadastrar_empresa
from fonte import cadastrar_fonte, listar_fontes, editar_fonte, desativar_fonte

criar_banco()
print("Banco iniciado com sucesso.")

def menu_fontes(empresa_id):
    while True:
        print("\n___Fontes de Emissão___")
        print("[1] Cadastrar nova fonte")
        print("[2] Listar fontes ativas")
        print("[3] Editar fonte")
        print("[4] Desativar fonte")
        print("[5] Voltar")

        opcao = input("\nEscolha: ").strip()

        
        if opcao == "3":

            listar_fontes(empresa_id)

            fonte_id = int(input("Insira o ID da fonte que deseja alterar: "))
            novo_nome = input("Insira o novo nome da fonte: ").strip()
            novo_tipo = input("Insira o novo tipo da fonte: ").strip()
            unidade = input("Insira a unidade: ").strip()
            editar_fonte(fonte_id,novo_nome,novo_tipo,unidade)

        elif opcao == "4":

            listar_fontes(empresa_id)

            fonte_id = int(input("Insira o ID da fonte que deseja desativar: "))
            desativar_fonte(fonte_id)

        elif opcao == "5":
            break

        else:
            print("Opção Inválida.")

def menu_principal(empresa_id):

    while True:
        print("\n=================================")
        print("         CARBON TRACK PME          ")
        print("===================================")
        print("[1] Cadastre sua empresa")
        print("[2] Gerencie suas fontes de emissão")
        print("[0] Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            cadastrar_empresa()

        elif opcao == "2":
            menu_fontes(empresa_id)

        elif opcao == "3": 
            print("Encerrando. Até logo!")
            break

        else:
            print("Opção Inválida.")


        






