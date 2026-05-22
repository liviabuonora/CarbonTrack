"""
Módulo de Fontes de Emissão (US02 e US07)
Responsável por:
- Vincular fontes de emissão (ex: Diesel, Energia Elétrica, GLP) a uma empresa.
- Ativar ou desativar fontes de emissão no sistema.
"""


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

def desativar_fonte(conn, empresa_id):
    
    listar_fontes(conn, empresa_id)

    fonte_id = input("\nID da fonte que deseja desativar (ou 0 para cancelar): ").strip()
    if not fonte_id:
        return
    
    cursor = conn.execute("""
        SELECT nome FROM fontes_emissao
        WHERE id = ? AND empresa_id = ? AND ativo = 1
    """, (fonte_id, empresa_id))
    fonte = cursor.fetchone()

    if not fonte:
        print("Fonte não encontrada ou já desativada.")
        return 
    
    confirma = input(f"Desativar {fonte[0]}?")
    if confirma.lower() != "s":
        print("Operação Cancelada.")
        return
    
    conn.execute("""
    UPDATE fontes_emissao SET ativo = 0
    WHERE id = ? AND empresa_id = ?
    """, (fonte_id,empresa_id,))

    conn.commit()
    print(f"A fonte {fonte[0]} foi desativada. O histórico foi mantido.")









 




