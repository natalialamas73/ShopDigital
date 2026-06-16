# ai-generated
# Revisão recomendada por pelo menos dois desenvolvedores seniores antes da homologação.

import sqlite3
import html
import os

# ALERTA:
# Credenciais hardcoded removidas.
# Caso sejam necessárias, obtenha-as de variáveis de ambiente
# ou de um mecanismo seguro de gerenciamento de segredos.
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


def buscar_produto(termo_busca):
    """
    Busca produtos por nome utilizando prepared statement
    e aplica sanitização na saída HTML.
    """

    # Sanitização básica da entrada
    termo_busca = str(termo_busca).strip()

    conn = sqlite3.connect("ecommerce.db")

    try:
        cursor = conn.cursor()

        # Prepared statement (sem concatenação direta)
        query = """
            SELECT nome, preco, descricao
            FROM produtos
            WHERE nome LIKE ?
        """

        cursor.execute(query, (f"%{termo_busca}%",))
        resultados = cursor.fetchall()

        html_output = ["<ul>"]

        for nome, preco, descricao in resultados:
            # Sanitização de saída para prevenir XSS
            nome_safe = html.escape(str(nome))
            descricao_safe = html.escape(str(descricao))

            html_output.append(
                f"<li>{nome_safe} - R${preco}: {descricao_safe}</li>"
            )

        html_output.append("</ul>")

        return "".join(html_output)

    except sqlite3.Error:
        # Evita exposição de detalhes internos do banco
        return "Erro ao consultar produtos."

    finally:
        conn.close()
