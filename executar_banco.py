# ==============================================================================
# SCRIPT PYTHON PARA CONECTAR AO SQLITE E EXECUTAR O ARCHIVE 03_banco.sql
# ==============================================================================
import sqlite3
import os
NOME_BANCO = "schulz_calibracao.db"
ARQUIVO_SQL = "03_banco.sql"
try:
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    with open(ARQUIVO_SQL, "r", encoding="utf-8") as f:
        script_sql = f.read()
    cursor.executescript(script_sql)
    conexao.commit()
    print("=" * 60)
    print(f"SUCESSO: Banco de dados '{NOME_BANCO}' gerado com sucesso!")
    print("As tabelas 'tecnico', 'equipamento' e 'medicao' foram criadas.")
    print("=" * 60)
except Exception as e:
    print(f"ERRO ao executar o script DDL: {e}")
finally:
    conexao.close()