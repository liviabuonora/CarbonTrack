def consultar_historico_por_fonte(conn, empresa_id, fonte_id):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT fe.nome
        FROM fontes_emissao fe
        WHERE fe.id = ?
        AND fe.empresa_id = ?
    """, (fonte_id, empresa_id))

    fonte = cursor.fetchone()

    if fonte is None:
        print("Nenhum consumo encontrado.")
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
        JOIN fontes_emissao fe
            ON c.fonte_id = fe.id
        WHERE c.fonte_id = ?
        AND fe.empresa_id = ?
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
        JOIN fontes_emissao fe
            ON c.fonte_id = fe.id
        WHERE fe.empresa_id = ?
        AND c.mes_ref = ?
        AND c.ano_ref = ?
        ORDER BY fe.nome ASC
    """, (empresa_id, mes_ref, ano_ref))

    registros = cursor.fetchall()

    if len(registros) == 0:
        print("Nenhum consumo encontrado neste periodo.")
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