
import sqlite3

conexao = sqlite3.connect("schulz_calibracao.db")

try:
    tabelas = conexao.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

    for (tabela,) in tabelas:
        print(f"\n--- Tabela: {tabela} ---")

        colunas = conexao.execute(
            f'PRAGMA table_info("{tabela}")'
        ).fetchall()

        for coluna in colunas:
            print(coluna)

finally:
    conexao.close()
