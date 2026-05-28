import os
os.system ("cls")

from database import criar_banco, conectar
from empresa import cadastrar_empresa, listar_empresas, buscar_empresa
from fonte import cadastrar_fonte, listar_fontes, editar_fonte, desativar_fonte

from validacoes import TIPOS_VALIDOS
import os

os.system("cls")


from validacoes import TIPOS_VALIDOS, validar_tamanho_cnpj

def menu_fontes(conn, empresa_id):
    while True:
        print("\n----Fontes de Emissão----")
        print("[1] Cadastrar nova fonte")
        print("[2] Listar fontes ativas")
        print("[3] Editar fonte")
        print("[4] Desativar fonte")
        print("[5] Voltar")

        try:
            opcao = int(input("\nEscolha: "))
        except ValueError:
            print("Opção inválida. Digite apenas números.")
            continue
        
        if opcao == 1:
            nome = input("Nome da fonte: ").strip()
            print("Tipos disponíveis:")
            for t in TIPOS_VALIDOS:
                print(" -", t)
            tipo = input("Tipo: ").strip()
            unidade = input("Unidade (ex: L, kWh, kg, t): ").strip()
            cadastrar_fonte(conn, empresa_id, nome, tipo, unidade)
        
        elif opcao == 2:
            listar_fontes(conn, empresa_id)
        
        elif opcao == 3:
            listar_fontes(conn, empresa_id)
            try:
                fonte_id = int(input("\nInsira o ID da fonte que deseja alterar (ou 0 para cancelar): "))
            except ValueError:
                print("ID inválido. Digite apenas números.")
                continue  
            
            if fonte_id == 0:
                print("Operação cancelada.")
            else:
                novo_nome = input("Insira o novo nome da fonte: ").strip()
                print("Tipos disponíveis:")
                for t in TIPOS_VALIDOS:
                    print(" -", t)
                novo_tipo = input("Insira o novo tipo da fonte: ").strip()
                nova_unidade = input("Insira a nova unidade: ").strip()
                editar_fonte(conn, fonte_id, novo_nome, novo_tipo, nova_unidade)

        elif opcao == 4:
            listar_fontes(conn, empresa_id)
            try:
                fonte_id = int(input("Insira o ID da fonte que deseja desativar (ou 0 para cancelar): "))
            except ValueError:
                print("ID inválido. Digite apenas números.")
                continue 
            
            if fonte_id == 0:
                print("Operação cancelada")
            else:
                confirma = input("Tem certeza? (s/n): ").strip()
                if confirma.lower() == "s":
                    desativar_fonte(conn, fonte_id)
                else:
                    print("Operação cancelada.")

        elif opcao == 5:
            break

        else:
            print("Opção Inválida.")

def menu_principal(conn):

    while True:
        print("\n=================================")
        print("         CARBON TRACK PME          ")
        print("===================================")
        print("[1] Cadastre sua empresa")
        print("[2] Listar empresas")
        print("[3] Gerencie suas fontes de emissão")
        print("[0] Sair")

        try:    
            opcao = int(input("\nEscolha: "))
        except ValueError:
            print("Opção inválida. Digite apenas números.")
            continue
        
        if opcao == 1:
            os.system('cls')
            razao_social = input("Razão social: ").strip()

            cnpj = input("CNPJ: ").strip()
            while not validar_tamanho_cnpj(cnpj):
                print("CNPJ inválido! Digite novamente.")
                cnpj = input("Digite o CNPJ: ")

                
            setor = input("Setor: ").strip()   
            cadastrar_empresa(conn, razao_social, cnpj, setor)

        elif opcao == 2:
            listar_empresas(conn)
        
        elif opcao == 3:
            try:
                empresa_id = int(input("Insira o ID da empresa:"))
            except ValueError:
                print("ID inválido. Digite apenas números.")
                continue  
            
            menu_fontes(conn, empresa_id)

        elif opcao == 0: 
            print("Encerrando. Até logo!")
            break

        else:
            print("Opção Inválida.")


criar_banco()
conn = conectar()
print("Banco iniciado com sucesso.")

menu_principal(conn)

conn.close()


        






