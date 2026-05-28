"""
Módulo de Gerenciamento de Empresas (US01 e RNF04)
Responsável por:
- Cadastrar empresas (Razão Social, CNPJ, Setor, Meta Anual).
- Validar a duplicidade de CNPJ para garantir integridade.
"""
from validacoes import validar_cnpj_duplicado, validar_texto

def cadastrar_empresa(conn, razao_social, cnpj, setor):
    if not validar_texto(razao_social, "Razão social"):
        return
    if not validar_texto(cnpj, "CNPJ"):
        return
    if not validar_texto(setor, "Setor"):
        return
    if validar_cnpj_duplicado(conn, cnpj ):
        print("Erro: CNPJ já cadastrado.")
        return
    
    conn.execute(""" INSERT INTO empresas (razao_social, cnpj, setor) VALUES (?, ?, ?) """, (razao_social, cnpj, setor))
    conn.commit()
    print(f"Empresa '{razao_social}' cadastrada com sucesso!")

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

