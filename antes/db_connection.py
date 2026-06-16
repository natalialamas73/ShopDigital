# antes/db_connection.py
import sqlite3

# Credenciais hardcoded expostas no código
DB_USER = "admin_shopdigital"
DB_PASS = "senha_super_secreta_123"

def buscar_produto(termo_busca):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # VULNERABILIDADE 1: Concatenação direta abrindo espaço para SQL Injection
    query = "SELECT nome, preco, descricao FROM produtos WHERE nome LIKE '%" + termo_busca + "%'"
    
    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # VULNERABILIDADE 2: Retorno direto sem sanitização (risco de XSS no front-end)
        html_output = "<ul>"
        for row in resultados:
            html_output += f"<li>{row[0]} - R${row[1]}: {row[2]}</li>"
        html_output += "</ul>"
        
        return html_output
    except Exception as e:
        return str(e)
    finally:
        conn.close()

# Teste simulado
print(buscar_produto("celular"))
