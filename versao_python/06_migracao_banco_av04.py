import sqlite3
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent
BANCO = PASTA_PROJETO / "schulz_calibracao.db"


def migrar_banco():

    if not BANCO.is_file():
        raise FileNotFoundError(
            f"Banco de dados não encontrado: {BANCO}"
        )

    conexao = sqlite3.connect(BANCO)

    try:
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.execute("BEGIN IMMEDIATE")

        # Criar a tabela de calibrações
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS calibracao (
                id_calibracao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_tecnico INTEGER NOT NULL,
                id_equipamento INTEGER NOT NULL,
                data_calibracao DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                maior_desvio_padrao REAL NOT NULL,
                incerteza_combinada REAL NOT NULL,
                graus_liberdade_efetivos REAL NOT NULL,
                fator_abrangencia REAL NOT NULL,
                incerteza_expandida REAL NOT NULL,

                unidade TEXT NOT NULL DEFAULT 'µm',

                parametros_incerteza_json TEXT NOT NULL,
                padroes_utilizados_json TEXT,
                procedimento TEXT,
                arquivo_origem TEXT,

                FOREIGN KEY (id_tecnico)
                    REFERENCES tecnico (id_tecnico)
                    ON DELETE RESTRICT ON UPDATE CASCADE,

                FOREIGN KEY (id_equipamento)
                    REFERENCES equipamento (id_equipamento)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            )
        """)

        # Consultar as colunas existentes
        colunas = {
            linha[1]
            for linha in conexao.execute(
                "PRAGMA table_info(medicao)"
            )
        }

        # Acrescentar somente as colunas ausentes
        novas_colunas = {
            "id_calibracao": """
                INTEGER REFERENCES calibracao(id_calibracao)
                ON DELETE RESTRICT ON UPDATE CASCADE
            """,
            "medicao_1": "REAL",
            "medicao_2": "REAL",
            "desvio_padrao": "REAL"
        }

        for nome, definicao in novas_colunas.items():

            if nome not in colunas:

                conexao.execute(
                    f"ALTER TABLE medicao "
                    f"ADD COLUMN {nome} {definicao}"
                )

                print(f"Coluna adicionada: {nome}")

            else:
                print(f"Coluna já existente: {nome}")

        # Criar índice para consulta das calibrações
        conexao.execute("""
            CREATE INDEX IF NOT EXISTS
                idx_medicao_calibracao
            ON medicao (id_calibracao)
        """)

        # Verificar integridade referencial
        inconsistencias = conexao.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if inconsistencias:
            raise RuntimeError(
                f"Inconsistências encontradas: {inconsistencias}"
            )

        conexao.commit()

        print("\nMIGRAÇÃO CONCLUÍDA COM SUCESSO!")

        print("\nTabelas do banco:")

        tabelas = conexao.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()

        for tabela in tabelas:
            print(f" - {tabela[0]}")

        print("\nQuantidade de registros:")

        for tabela in (
            "tecnico",
            "equipamento",
            "medicao",
            "calibracao"
        ):
            quantidade = conexao.execute(
                f"SELECT COUNT(*) FROM {tabela}"
            ).fetchone()[0]

            print(f"{tabela}: {quantidade}")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    migrar_banco()