"""
Módulo de Fontes de Emissão (US02 e US07)
Responsável por:
- Vincular fontes de emissão (ex: Diesel, Energia Elétrica, GLP) a uma empresa.
- Ativar ou desativar fontes de emissão no sistema.
"""
TIPOS_VALIDOS = ["energia_eletrica", "diesel", "gasolina", "etanol", "glp", "residuos"]


def cadastrar_fonte(conn, empresa_id, nome, tipo, unidade):
    cursor = conn.execute("SELECT id FROM empresas WHERE id = ?", (empresa_id,))
    empresa = cursor.fetchone()

    if empresa is None:
        print("Erro: empresa não encontrada.")
        return
    
    if tipo not in TIPOS_VALIDOS:
        print("Erro: tipo inválido. \nTipos aceitos:")
        for t in TIPOS_VALIDOS:
            print(" -", t)
        return
    
    conn.execute("""
        INSERT INTO fontes_emissao (empresa_id, nome, tipo, unidade)
        VALUES (?, ?, ?, ?)
    """, (empresa_id, nome, tipo, unidade))

    conn.commit()
    print(f"Fonte '{nome}' cadastrada com sucesso!")



def listar_fontes(conn, empresa_id, so_ativas=True):

    if so_ativas:
        cursor = conn.execute("""
            SELECT id, nome, tipo, unidade
            FROM fontes_emissao                        
            WHERE empresa_id =? AND ativo =1
            ORDER BY tipo, nome
        """, (empresa_id,) )                                     

    else: 
        cursor = conn.execute("""
            SELECT id, nome, tipo, unidade
            FROM fontes_emissao
            WHERE empresa_id =? 
            ORDER BY tipo, nome
        """,(empresa_id,))                
        
    fontes = cursor.fetchall()

    if len(fontes) == 0:
        print("Nenhuma fonte cadastrada.")
        return

    print("\n--- Fontes cadastradas ---")
    for fonte in fontes:
        print("ID:", fonte[0], "| Nome:", fonte[1], "| Tipo:", fonte[2], "| Unidade:", fonte[3])

def editar_fonte(conn, fonte_id, novo_nome, novo_tipo, nova_unidade):
    cursor = conn.execute("""SELECT id FROM fontes_emissao WHERE id = ? AND ativo = 1""", (fonte_id,))
    fonte = cursor.fetchone()
    
    if fonte is None:
        print("Erro: fonte não encontrada ou já desativada.")
        return
    
    if novo_tipo not in TIPOS_VALIDOS:
        print("Erro: tipo inválido. \nTipos aceitos:")
        for t in TIPOS_VALIDOS:
            print(" -", t)
        return
    
    conn.execute("""
        UPDATE fontes_emissao
        SET nome = ?, tipo = ?, unidade = ?
        WHERE id = ?
    """, (novo_nome, novo_tipo, nova_unidade, fonte_id))

    conn.commit()
    print("Fonte atualizada com sucesso!")


def desativar_fonte(conn, fonte_id):
      
    cursor = conn.execute("""
        SELECT nome FROM fontes_emissao WHERE id = ? AND ativo = 1 """, (fonte_id,))
    fonte = cursor.fetchone()

    if fonte is None:
        print("Fonte não encontrada ou já desativada.")
        return 
     
    conn.execute(""" UPDATE fontes_emissao SET ativo = 0 WHERE id = ? """, (fonte_id,))

    conn.commit()
    print(f"A fonte {fonte[0]} foi desativada. O histórico foi mantido.")









 




