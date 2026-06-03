import os
os.system("cls")

def verificar_meta_anual(meta_tco2, total_emitido):
    percentual = (total_emitido / meta_tco2) * 100
 
    print(f"\nMeta definida:      {meta_tco2} tCO2eq")
    print(f"Total emitido:       {total_emitido} tCO2eq")
    print(f"Percentual atingido: {percentual:.1f}%")
 
    if percentual >= 100:
        print("ALERTA! Meta anual ultrapassada.")
    elif percentual >= 80:
        print("ATENÇÃO! Próximo do limite da meta.")
    else:
        print("Dentro da meta anual.")
 
def main():
    print("Acompanhamento de Meta Anual\n")
 
    meta = float(input("Digite a meta anual (tCO2eq): "))
    emitido = float(input("Digite o total emitido até    agora (tCO2eq): "))
 
    verificar_meta_anual(meta, emitido)
 
 
main()