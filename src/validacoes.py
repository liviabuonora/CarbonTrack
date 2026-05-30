TIPOS_VALIDOS = ["energia_eletrica", "diesel", "gasolina", "etanol", "glp", "residuos"]

def validar_cnpj_duplicado(conn, cnpj ):
    cursor = conn.execute("SELECT id FROM empresas WHERE cnpj = ?", (cnpj,))
    return cursor.fetchone() is not None

def validar_empresa_existe( conn, empresa_id):
    cursor = conn.execute("SELECT id FROM empresas WHERE id = ?", (empresa_id,))
    return cursor.fetchone() is not None

def validar_tipo_fonte(tipo):
    return tipo in TIPOS_VALIDOS

def validar_texto(valor, nome_campo):
    if valor == "":
        print(f"Erro: {nome_campo} não pode ser vazio.")
        return False
    return True

def validar_formato_cnpj(cnpj):
    if not cnpj.isdigit():
        return False
    if len(cnpj) != 14:
        return False
    return True

def validar_quantidade(quantidade):
    if quantidade < 0:
        print("Erro: quantidade não pode ser negativa.")
        return False
    if quantidade == 0:
        print("Erro: quantidade deve ser maior que zero.")
        return False
    return True

def validar_discrepancia(conn, fonte_id, quantidade):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT quantidade FROM historico_consumo
        WHERE fonte_id = ?
        ORDER BY ano_ref DESC, mes_ref DESC
        LIMIT 3
    """, (fonte_id,))
    
    historico = cursor.fetchall()
    
    if len(historico) == 0:
        return True
    
    valores = [item[0] for item in historico]
    media = sum(valores) / len(valores)
    
    if quantidade > media * 5:
        print(f"Aviso: quantidade {quantidade} é muito acima do histórico recente!")
        resposta = input("Deseja confirmar mesmo assim? (s/n): ").strip().lower()
        if resposta != "s":
            print("Consumo não registrado.")
            return False
    
    return True