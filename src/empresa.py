from validacoes import validar_cnpj_duplicado, validar_texto, validar_formato_cnpj

def cadastrar_empresa(conn, razao_social, cnpj, setor):
    if not validar_texto(razao_social, "Razão social"):
        return
    if not validar_texto(cnpj, "CNPJ"):
        return
    if not validar_texto(setor, "Setor"):
        return
    if not validar_formato_cnpj(cnpj):
        return
    if validar_cnpj_duplicado(conn, cnpj ):
        print("\033[31mErro:\033[0m CNPJ já cadastrado.")
        return
    
    conn.execute(""" INSERT INTO empresas (razao_social, cnpj, setor) VALUES (?, ?, ?) """, (razao_social, cnpj, setor))
    conn.commit()
    print(f"\033[32mEmpresa '{razao_social}' cadastrada com sucesso!\033[0m")

def listar_empresas(conn):
    cursor = conn.execute("""
        SELECT id, razao_social, cnpj, setor FROM empresas ORDER BY razao_social """)
    empresas = cursor.fetchall()

    if len(empresas) == 0:
        print("Nenhuma empresa cadastrada.")
        return

    print("\n--- Empresas cadastradas ---")
    for empresa in empresas:
        print(f"ID: {empresa[0]} | Razão Social: {empresa[1]} | CNPJ: {empresa[2]} | Setor: {empresa[3]}")

def buscar_empresa(conn, empresa_id):
    cursor = conn.execute("""
        SELECT id, razao_social, cnpj, setor FROM empresas WHERE id = ? """, (empresa_id,))
    return cursor.fetchone()

def definir_meta(conn, empresa_id, meta):
    if meta <= 0:
        print("Erro: a meta deve ser um valor positivo.")
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM empresas WHERE id = ?", (empresa_id,))
    if cursor.fetchone() is None:
        print("Erro: empresa não encontrada.")
        return

    cursor.execute("""
        UPDATE empresas SET meta_anual_tco2 = ? WHERE id = ?
    """, (meta, empresa_id))
    conn.commit()
    print(f"Meta anual definida: {meta:.2f} tCO2e")