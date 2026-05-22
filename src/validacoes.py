import os
os.system("cls")

empresas = []
consumos = []

#Cadastro da empresa

cnpj = input("Digite o CNPJ da empresa: ")

if cnpj in empresas:
    print("Erro: CNPJ já cadastrado.")
else:
    empresas.append(cnpj)
    print("Empresa cadastrada com sucesso.")

#Registro de consumos

mes = input("Digite o mês: ")
fonte = input("Digite a fonte do consumo: ")

registro = (mes, fonte)

if registro in consumos:
    print("Erro: consumo já registrado.")
else:
    consumos.append(registro)
    print("Consumo registrado com sucesso.")