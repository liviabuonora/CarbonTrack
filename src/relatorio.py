"""
Módulo de Relatórios e Consultas (US05, US08 e US09)
Responsável por:
- Buscar os dados históricos de consumo no banco de dados.
- Formatar os resultados das emissões totais de forma clara para o gestor da PME.
"""

def relatorio_evolucao(conn, empresa_id):
    cursor = conn.curor()
    cursor.execute("""
        SELECT mes_ref, ano_ref, SUM(tco2_eq)
        FROM historico_consumo
        WHERE fonte_id IN (
            SELECT id FROM fontes_emissao WHERE empresa_id = ?
        )
        GROUP BY ano_ref, mes_ref
        ORDER BY ano_ref, mes_ref
    """, (empresa_id,))

    periodos = cursor.fetchall()

    if len(periodos) == 0:
        print("Sem dados para gerar relatorio.")
        return

    print("\n--- RELATORIO DE EVOLUCAO ---")

    anterior = None

    for mes_ref, ano_ref, atual in periodos:

        if anterior is None or anterior == 0:
            variacao = "—"
        else:
            variacao = ((atual - anterior) / anterior) * 100
            variacao = f"{variacao:.2f}%"

        print(f"Mês: {mes_ref:2d}/{ano_ref}")
        print(f"Total: {atual:.2f} tCO2e")
        print(f"Variação: {variacao}")
        print("-" * 30)
        anterior = atual

    ultimo_mes = periodos[-1][0]
    ultimo_ano = periodos[-1][1]

    cursor.execute("""
        SELECT f.nome, SUM(c.tco2_eq)
        FROM historico_consumo c
        JOIN fontes_emissao f ON c.fonte_id = f.id
        WHERE f.empresa_id = ?
          AND c.mes_ref = ?
          AND c.ano_ref = ?
        GROUP BY c.fonte_id
        ORDER BY SUM(c.tco2_eq) DESC
        LIMIT 1
    """, (empresa_id, ultimo_mes, ultimo_ano))

    resultado = cursor.fetchone()

    if resultado:

       print(f"\nFonte principal em {ultimo_mes:02d}/{ultimo_ano}: {resultado[0]} ({resultado[1]:.2f} tCO2eq)")