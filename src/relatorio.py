import csv
import os
from alerta import verificar_alerta_periodo
from datetime import date
 
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
def consultar_historico_por_fonte(conn, empresa_id, fonte_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome
        FROM fontes_emissao
        WHERE id = ? AND empresa_id = ?
    """, (fonte_id, empresa_id))
 
    fonte = cursor.fetchone()
 
    if fonte is None:
        print("Fonte não encontrada para esta empresa.")
        return
 
    cursor.execute("""
        SELECT
            fe.nome,
            c.mes_ref,
            c.ano_ref,
            c.quantidade,
            fe.unidade,
            c.tco2_eq
        FROM historico_consumo c
        JOIN fontes_emissao fe ON c.fonte_id = fe.id
        WHERE c.fonte_id = ? AND fe.empresa_id = ?
        ORDER BY c.ano_ref ASC, c.mes_ref ASC
    """, (fonte_id, empresa_id))
 
    registros = cursor.fetchall()
 
    if len(registros) == 0:
        print("Nenhum consumo encontrado.")
        return
 
    print("\n--- Histórico por Fonte ---")
    for registro in registros:
        nome, mes, ano, quantidade, unidade, tco2_eq = registro
        print(
            f"Fonte: {nome} | "
            f"{mes:02d}/{ano} | "
            f"{quantidade} {unidade} | "
            f"{tco2_eq} tCO₂e"
        )
 
def consultar_historico_por_periodo(conn, empresa_id, mes_ref, ano_ref):
    if ano_ref < 2000:
        print("Erro: ano deve ser maior ou igual a 2000.")
        return
    if mes_ref < 1 or mes_ref > 12:
        print("Erro: mês deve estar entre 1 e 12.")
        return
 
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            fe.nome,
            c.mes_ref,
            c.ano_ref,
            c.quantidade,
            fe.unidade,
            c.tco2_eq
        FROM historico_consumo c
        JOIN fontes_emissao fe ON c.fonte_id = fe.id
        WHERE fe.empresa_id = ? AND c.mes_ref = ? AND c.ano_ref = ?
        ORDER BY fe.nome ASC
    """, (empresa_id, mes_ref, ano_ref))
 
    registros = cursor.fetchall()
 
    if len(registros) == 0:
        print("Nenhum consumo encontrado neste período.")
        return
 
    print(f"\n--- Histórico por Período: {mes_ref:02d}/{ano_ref} ---")
    for registro in registros:
        nome, mes, ano, quantidade, unidade, tco2_eq = registro
        print(
            f"Fonte: {nome} | "
            f"{mes:02d}/{ano} | "
            f"{quantidade} {unidade} | "
            f"{tco2_eq} tCO₂e"
        )
  
def relatorio_evolucao(conn, empresa_id):
    cursor = conn.cursor()
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
        print("Sem dados para gerar relatório.")
        return
 
    print("\n--- RELATÓRIO DE EVOLUÇÃO ---")
 
    anterior = None
    for mes_ref, ano_ref, atual in periodos:
        if anterior is None or anterior == 0:
            variacao = "—"
        else:
            variacao = f"{((atual - anterior) / anterior) * 100:.2f}%"
 
        print(f"Mês: {mes_ref:02d}/{ano_ref}")
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
        WHERE f.empresa_id = ? AND c.mes_ref = ? AND c.ano_ref = ?
        GROUP BY c.fonte_id
        ORDER BY SUM(c.tco2_eq) DESC
        LIMIT 1
    """, (empresa_id, ultimo_mes, ultimo_ano))
 
    resultado = cursor.fetchone()
 
    if resultado:
        print(f"\nFonte principal em {ultimo_mes:02d}/{ultimo_ano}: {resultado[0]} ({resultado[1]:.2f} tCO2e)")
 
def exportar_csv(conn, empresa_id):
    cursor = conn.cursor()
    cursor.execute("SELECT razao_social FROM empresas WHERE id = ?", (empresa_id,))
    resultado_empresa = cursor.fetchone()
 
    if resultado_empresa is None:
        print("Erro: empresa não encontrada para exportação.")
        return
 
    nome_empresa = resultado_empresa[0]
    nome_limpo = nome_empresa.replace(" ", "_").replace("/", "_").lower()
 
    cursor.execute("""
        SELECT
            f.nome,
            f.tipo,
            c.mes_ref,
            c.ano_ref,
            c.quantidade,
            f.unidade,
            c.tco2_eq
        FROM historico_consumo c
        JOIN fontes_emissao f ON c.fonte_id = f.id
        WHERE f.empresa_id = ?
        ORDER BY c.ano_ref, c.mes_ref, f.nome
    """, (empresa_id,))
 
    dados = cursor.fetchall()
 
    if len(dados) == 0:
        print("Nenhum dado encontrado.")
        return
 
    hoje = date.today().strftime("%Y%m%d")
    nome_arquivo = f"relatorio_empresa_{nome_limpo}_{hoje}.csv"
    caminho = os.path.join(PASTA_PROJETO, nome_arquivo)
 
    with open(caminho, mode="w", newline="", encoding="utf-8-sig") as arquivo:
        writer = csv.writer(arquivo, delimiter=";")
        writer.writerow(["fonte", "tipo", "mes", "ano", "quantidade", "unidade", "tco2_eq"])
        for linha in dados:
            writer.writerow(linha)
 
    print(f"Relatório exportado: {caminho}")
 
def relatorio_percentual_fontes(conn, empresa_id, mes_ref, ano_ref):
    if mes_ref < 1 or mes_ref > 12:
        print("Erro: mês deve estar entre 1 e 12.")
        return
    if ano_ref < 2000:
        print("Erro: ano deve ser maior ou igual a 2000.")
        return
 
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.nome, SUM(c.tco2_eq)
        FROM historico_consumo c
        JOIN fontes_emissao f ON c.fonte_id = f.id
        WHERE f.empresa_id = ? AND c.mes_ref = ? AND c.ano_ref = ?
        GROUP BY c.fonte_id
        ORDER BY SUM(c.tco2_eq) DESC
    """, (empresa_id, mes_ref, ano_ref))
 
    fontes = cursor.fetchall()
 
    total = 0.0
    for fonte in fontes:
        total += fonte[1]

    if len(fontes) == 0:
        print("Nenhum dado para o período informado.")
        return
 
    if total == 0:
        print("Total de emissões no período é zero. Não é possível calcular percentuais.")
        return
 
    print(f"\n--- PERCENTUAL POR FONTE — {mes_ref:02d}/{ano_ref} ---")
    for fonte in fontes:
        nome = fonte[0]
        tco2 = fonte[1]
        percentual = (tco2 / total) * 100
        print(f"{nome}: {tco2:.2f} tCO2e ({percentual:.1f}%)")
 
    print(f"\nTotal do período: {total:.2f} tCO2e")
 
def consultar_meta(conn, empresa_id, ano_ref):
    if ano_ref < 2000:
        print("Erro: ano deve ser maior ou igual a 2000.")
        return
 
    cursor = conn.cursor()
    cursor.execute("SELECT meta_anual_tco2 FROM empresas WHERE id = ?", (empresa_id,))
    resultado = cursor.fetchone()
 
    if resultado is None:
        print("Erro: empresa não encontrada.")
        return
 
    meta = resultado[0]
 
    if meta is None:
        print("Nenhuma meta cadastrada para esta empresa.")
        return
 
    cursor.execute("""
        SELECT SUM(c.tco2_eq)
        FROM historico_consumo c
        JOIN fontes_emissao f ON c.fonte_id = f.id
        WHERE f.empresa_id = ? AND c.ano_ref = ?
    """, (empresa_id, ano_ref))
 
    total_resultado = cursor.fetchone()[0]
 
    if total_resultado is None:
        total = 0.0
    else:
        total = total_resultado
 
    percentual = (total / meta) * 100
 
    print(f"\n--- META ANUAL — {ano_ref} ---")
    print(f"Meta definida:       {meta:.2f} tCO2e")
    print(f"Total emitido:       {total:.2f} tCO2e")
    print(f"Percentual atingido: {percentual:.2f}%")
 
    if percentual > 100:
        print("\033[31mATENÇÃO:\033[0m meta anual ultrapassada.")
    else:
        print("Dentro da meta anual.")
 
def menu_relatorios(conn, empresa_id):
    from fonte import listar_fontes 
 
    while True:
        print("\n----Relatórios----")
        print("[1] Consultar histórico por fonte")
        print("[2] Consultar histórico por período")
        print("[3] Relatório de evolução")
        print("[4] Exportar CSV")
        print("[5] Verificar alerta 30%")
        print("[6] Percentual por fonte")
        print("[7] Consultar meta anual")
        print("[0] Voltar")
 
        try:
            opcao = int(input("\nEscolha: "))
        except ValueError:
            print("Opção inválida. Digite apenas números.")
            continue
 
        if opcao == 1:
            listar_fontes(conn, empresa_id)
            try:
                fonte_id = int(input("ID da fonte: "))
            except ValueError:
                print("ID inválido.")
                continue
            consultar_historico_por_fonte(conn, empresa_id, fonte_id)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 2:
            try:
                mes_ref = int(input("Mês de referência: "))
                ano_ref = int(input("Ano de referência: "))
            except ValueError:
                print("Erro: digite valores numéricos válidos.")
                continue
            consultar_historico_por_periodo(conn, empresa_id, mes_ref, ano_ref)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 3:
            relatorio_evolucao(conn, empresa_id)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 4:
            exportar_csv(conn, empresa_id)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 5:
            try:
                mes_ref = int(input("Mês de referência (atual): "))
                ano_ref = int(input("Ano de referência (atual): "))
            except ValueError:
                print("Erro: digite valores numéricos válidos.")
                continue
            verificar_alerta_periodo(conn, empresa_id, mes_ref, ano_ref)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 6:
            try:
                mes_ref = int(input("Mês de referência: "))
                ano_ref = int(input("Ano de referência: "))
            except ValueError:
                print("Erro: digite valores numéricos válidos.")
                continue
            relatorio_percentual_fontes(conn, empresa_id, mes_ref, ano_ref)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 7:
            try:
                ano_ref = int(input("Ano de referência: "))
            except ValueError:
                print("Erro: digite um valor numérico válido.")
                continue
            consultar_meta(conn, empresa_id, ano_ref)
            input("\nPressione Enter para continuar...")
 
        elif opcao == 0:
            break
 
        else:
            print("Opção Inválida.")