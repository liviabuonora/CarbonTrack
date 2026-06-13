def buscar_fator(conn, tipo_fonte):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT fator_conversao, unidade FROM fatores_emissao WHERE tipo_fonte = ?",
        (tipo_fonte,)
    )
    resultado = cursor.fetchone()
 
    if resultado is None:
        return None
 
    return {
        "fator_conversao": resultado[0],
        "unidade": resultado[1]
    }
 
def calcular_tco2(quantidade, fator):
    if fator is None:
        return None
 
    tco2_eq = quantidade * fator
    return round(tco2_eq, 6)

