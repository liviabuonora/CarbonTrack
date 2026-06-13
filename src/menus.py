import os
from empresa import cadastrar_empresa, listar_empresas, definir_meta
from fonte import cadastrar_fonte, listar_fontes, editar_fonte, desativar_fonte
from validacoes import TIPOS_VALIDOS, validar_empresa_existe, validar_formato_cnpj
from consumo import registrar_consumo, listar_consumos
from relatorio import menu_relatorios
 
def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
 
def menu_fontes(conn, empresa_id):
    while True:
        limpar_tela()
        print("\n----Fontes de Emissão----")
        print("[1] Cadastrar nova fonte")
        print("[2] Listar fontes")
        print("[3] Editar fonte")
        print("[4] Desativar fonte")
        print("[5] Registrar consumo")
        print("[6] Listar consumos")
        print("[7] Relatórios")
        print("[8] Definir meta anual")
        print("[0] Voltar")
 
        try:
            opcao = int(input("\nEscolha: "))
        except ValueError:
            print("Opção inválida. Digite apenas números.")
            input("\nPressione Enter para continuar...")
            continue
 
        if opcao == 1:
            limpar_tela()
            nome = input("Nome da fonte: ").strip()
            print("Tipos disponíveis:")
            for t in TIPOS_VALIDOS:
                print(" -", t)
            tipo = input("Tipo: ").strip()
            unidade = input("Unidade (ex: L, kWh, kg, t): ").strip()
            cadastrar_fonte(conn, empresa_id, nome, tipo, unidade)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 2:
            limpar_tela()
            listar_fontes(conn, empresa_id)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 3:
            limpar_tela()
            listar_fontes(conn, empresa_id)
            try:
                fonte_id = int(input("\nInsira o ID da fonte que deseja alterar (ou 0 para cancelar): "))
            except ValueError:
                print("ID inválido. Digite apenas números.")
                input("\nPressione Enter para continuar...")
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
                editar_fonte(conn, empresa_id, fonte_id, novo_nome, novo_tipo, nova_unidade)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 4:
            limpar_tela()
            listar_fontes(conn, empresa_id)
            try:
                fonte_id = int(input("Insira o ID da fonte que deseja desativar (ou 0 para cancelar): "))
            except ValueError:
                print("ID inválido. Digite apenas números.")
                input("\nPressione Enter para continuar...")
                continue
 
            if fonte_id == 0:
                print("Operação cancelada.")
            else:
                confirma = input("Tem certeza? (s/n): ").strip().lower()
                if confirma == "s":
                    desativar_fonte(conn, empresa_id, fonte_id)
                else:
                    print("Operação cancelada.")
            input("\nPressione Enter para continuar...")
 
        elif opcao == 5:
            limpar_tela()
            listar_fontes(conn, empresa_id)
            try:
                fonte_id = int(input("ID da fonte: "))
                quantidade = float(input("Quantidade consumida: "))
                mes_ref = int(input("Mês de referência: "))
                ano_ref = int(input("Ano de referência: "))
            except ValueError:
                print("\033[31mErro:\033[0m digite valores numéricos válidos.")
                input("\nPressione Enter para continuar...")
                continue
            registrar_consumo(conn, empresa_id, fonte_id, quantidade, mes_ref, ano_ref)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 6:
            limpar_tela()
            listar_fontes(conn, empresa_id)
            try:
                fonte_id = int(input("ID da fonte: "))
            except ValueError:
                print("ID inválido.")
                input("\nPressione Enter para continuar...")
                continue
            listar_consumos(conn, empresa_id, fonte_id)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 7:
            menu_relatorios(conn, empresa_id)
 
        elif opcao == 8:
            limpar_tela()
            try:
                meta = float(input("Meta anual de emissões (tCO2e): "))
            except ValueError:
                print("Erro: digite um valor numérico válido.")
                input("\nPressione Enter para continuar...")
                continue
            definir_meta(conn, empresa_id, meta)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 0:
            break
 
        else:
            print("Opção Inválida.")
            input("\nPressione Enter para continuar...")
 
 
def menu_principal(conn):
    while True:
        limpar_tela()
        print("\n===================================")
        print("        CARBON TRACK PME           ")
        print("===================================")
        print("[1] Cadastrar empresa")
        print("[2] Listar empresas")
        print("[3] Gerenciar fontes de emissão")
        print("[0] Sair")
 
        try:
            opcao = int(input("\nEscolha: "))
        except ValueError:
            print("Opção inválida. Digite apenas números.")
            input("\nPressione Enter para continuar...")
            continue
 
        if opcao == 1:
            limpar_tela()
            razao_social = input("Razão social: ").strip()
            cnpj = input("CNPJ (apenas números, 14 dígitos): ").strip()
            while not validar_formato_cnpj(cnpj):
                print("\033[31mErro:\033[0m são necessários 14 dígitos e deve conter apenas números.")
                cnpj = input("Digite o CNPJ: ").strip()
            setor = input("Setor: ").strip()
            cadastrar_empresa(conn, razao_social, cnpj, setor)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 2:
            limpar_tela()
            listar_empresas(conn)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 3:
            limpar_tela()
            listar_empresas(conn)
            try:
                empresa_id = int(input("\nInsira o ID da empresa: "))
            except ValueError:
                print("ID inválido. Digite apenas números.")
                input("\nPressione Enter para continuar...")
                continue
 
            if not validar_empresa_existe(conn, empresa_id):
                print(f"\033[31mErro:\033[0m nenhuma empresa encontrada com ID {empresa_id}.")
                input("\nPressione Enter para continuar...")
                continue
 
            menu_fontes(conn, empresa_id)
 
        elif opcao == 0:
            limpar_tela()
            print("Encerrando. Até logo!")
            break
 
        else:
            print("Opção Inválida.")
            input("\nPressione Enter para continuar...")
 
