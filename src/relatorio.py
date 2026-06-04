import csv
import os 

PASTA_CSV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def exportar_csv(conn, empresa_id):
    cursor = conn.execute()
    cursor.execute("""
        SELECT
            f.nome,
            f.tipo,
            c.mes_ref,
            c.ano_ref,
            c.quantidade,
            f.unidade,
            c.tco2_eq,
                
        FROM historico_consumo c
        JOIN fontes_emissao f
            ON c.fonte_id = f.id
        WHERE f.empresa_id = ?
        ORDER BY c.ano_ref, c.mes_ref, f.nome
                 """, (empresa_id))
    
    dados = cursor.fetchall()

    if len(dados)==0:
        print("Nenhum dado encontrado.")
        return 
    
    nome_arquivo = f"Relatorio_empresa{empresa_id}"
    caminho = os.path.join(PASTA_CSV,nome_arquivo)
    with open (caminho, mode = "w" , newline="" , encoding="utf-8-sig")as arquivo:
