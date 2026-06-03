import os
os.system("cls")

def calcular_variacao(periodo_anterior, periodo_atual):
    return ((periodo_atual - periodo_anterior) / periodo_anterior) * 100
 
 
def verificar_alerta(fonte, periodo_anterior, periodo_atual):
    variacao = calcular_variacao(periodo_anterior, periodo_atual)
 
    if variacao > 30:
        print(f"ALERTA! Fonte '{fonte}': emissões aumentaram {variacao:.1f}% em relação ao período anterior.")
    else:
        print(f"Fonte '{fonte}': variação de {variacao:.1f}%. Dentro do esperado.")
 
 
def main():
    print("Sistema de Alerta de Emissões\n")
 
    fonte = input("Nome da fonte (ex: energia, transporte): ")
    periodo_anterior = float(input("Emissão do período anterior: "))
    periodo_atual = float(input("Emissão do período atual: "))
 
    print()
    verificar_alerta(fonte, periodo_anterior, periodo_atual)
 
 
main()