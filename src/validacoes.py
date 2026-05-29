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