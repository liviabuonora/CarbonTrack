from calculo import buscar_fator, calcular_tco2


def registrar_consumo(conn, fonte_id, quantidade, mes_ref, ano_ref):

    cursor = conn.cursor()

    if mes_ref < 1 or mes_ref > 12:
        print("Erro: mês deve estar entre 1 e 12.")
        return

    if ano_ref < 2000:
        print("Erro: ano deve ser maior ou igual a 2000.")
        return

    if quantidade <= 0:
        print("Erro: quantidade deve ser maior que zero.")
        return

    cursor.execute("""
        SELECT tipo, unidade, ativo
        FROM fontes_emissao
        WHERE id = ?
    """, (fonte_id,))

    fonte = cursor.fetchone()

    if fonte is None:
        print("Erro: fonte não encontrada.")
        return

    tipo, unidade, ativo = fonte

    if ativo == 0:
        print("Erro: esta fonte está desativada.")
        return

    cursor.execute("""
        SELECT id
        FROM consumos
        WHERE fonte_id = ?
        AND mes_ref = ?
        AND ano_ref = ?
    """, (fonte_id, mes_ref, ano_ref))

    duplicado = cursor.fetchone()

    if duplicado:
        print("Erro: já existe consumo registrado para essa fonte nesse período.")
        return

    fator_data = buscar_fator(conn, tipo)

    if fator_data is None:
        print("Erro: fator de emissão não encontrado.")
        return

    fator = fator_data["fator_conversao"]

    tco2_eq = calcular_tco2(quantidade, fator)

    cursor.execute("""
        INSERT INTO consumos (
            fonte_id,
            quantidade,
            mes_ref,
            ano_ref,
            tco2_eq
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        fonte_id,
        quantidade,
        mes_ref,
        ano_ref,
        tco2_eq
    ))

    conn.commit()

    print("Consumo registrado com sucesso!")
    print(f"tCO₂e calculado: {tco2_eq}")


def listar_consumos(conn, fonte_id):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.mes_ref,
            c.ano_ref,
            c.quantidade,
            f.unidade,
            c.tco2_eq
        FROM consumos c
        JOIN fontes_emissao f
            ON c.fonte_id = f.id
        WHERE c.fonte_id = ?
        ORDER BY c.ano_ref, c.mes_ref
    """, (fonte_id,))

    consumos = cursor.fetchall()

    if len(consumos) == 0:
        print("Nenhum consumo encontrado.")
        return

    print("\n--- Histórico de Consumos ---")

    for consumo in consumos:

        mes, ano, quantidade, unidade, tco2_eq = consumo

        print(
            f"{mes:02d}/{ano} | "
            f"{quantidade} {unidade} | "
            f"{tco2_eq} tCO₂e"
        )