def verificar_alerta_periodo(conn, empresa_id, mes_ref, ano_ref):
    if ano_ref < 2000:
        print("Erro: ano deve ser maior ou igual a 2000.")
        return
    if mes_ref < 1 or mes_ref > 12:
        print("Erro: mês deve estar entre 1 e 12.")
        return

    mes_ant = mes_ref - 1
    ano_ant = ano_ref
    if mes_ant == 0:
        mes_ant = 12
        ano_ant -= 1

    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT SUM(c.tco2_eq) FROM historico_consumo c
        JOIN fontes_emissao f ON c.fonte_id = f.id
        WHERE f.empresa_id = ? AND c.mes_ref = ? AND c.ano_ref = ?
    """, (empresa_id, mes_ref, ano_ref))
    atual = cursor.fetchone()[0]
    if atual is None:
        print("Sem dados para o período informado.")
        return
    
    cursor.execute("""
        SELECT SUM(c.tco2_eq) FROM historico_consumo c
        JOIN fontes_emissao f ON c.fonte_id = f.id
        WHERE f.empresa_id = ? AND c.mes_ref = ? AND c.ano_ref = ?
    """, (empresa_id, mes_ant, ano_ant))
    anterior = cursor.fetchone()[0]
    if anterior is None:
        print("Primeiro período cadastrado ou sem histórico anterior suficiente para alerta.")
        return

    if anterior == 0:
        print(f"\nATENÇÃO: O consumo anterior foi zero e o atual é {atual:.1f} tCO2e!")
        print("Mais atenção para as proximas medições.")
        return
    
    diferenca = ((atual - anterior) / anterior) * 100

    if diferenca >= 30:
        print(f"\nATENÇÃO: Alerta de emissões!")
        print(f"{mes_ref:02d}/{ano_ref} ({atual:.1f} tCO2e) é {diferenca:.1f}% acima de {mes_ant:02d}/{ano_ant} ({anterior:.1f} tCO2e)")
    else:
        print(f"Variação dentro do aceitável ({diferenca:.1f}% em relação ao período anterior).")
