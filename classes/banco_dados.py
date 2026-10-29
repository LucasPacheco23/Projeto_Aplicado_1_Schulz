
import sqlite3
from contextlib import closing
from pathlib import Path

from .tecnico import Tecnico
from .equipamento import Equipamento
from .medicao import Medicao


CAMINHO_BANCO = (
    Path(__file__).resolve().parent.parent
    / "schulz_calibracao.db"
)


class BancoDados:

    def __init__(self, caminho=CAMINHO_BANCO):
        self.caminho = str(caminho)

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    # ==========================================================
    # TECNICO
    # ==========================================================

    def salvar_tecnico(self, tecnico: Tecnico) -> int:
        tecnico.validar()

        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO tecnico
                        (nome_tecnico, matricula, email, setor)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        tecnico.nome_tecnico,
                        tecnico.matricula,
                        tecnico.email,
                        tecnico.setor,
                    ),
                )
                tecnico.id_tecnico = cursor.lastrowid

        return tecnico.id_tecnico

    def buscar_tecnico(self, matricula: str):
        with closing(self.conectar()) as conexao:
            return conexao.execute(
                "SELECT * FROM tecnico WHERE matricula = ?",
                (matricula,),
            ).fetchone()

    # ==========================================================
    # EQUIPAMENTO
    # ==========================================================

    def salvar_equipamento(self, equipamento: Equipamento) -> int:
        equipamento.validar()

        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO equipamento
                        (codigo_tag, nome_equipamento, fabricante, modelo)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        equipamento.codigo_tag,
                        equipamento.nome_equipamento,
                        equipamento.fabricante,
                        equipamento.modelo,
                    ),
                )
                equipamento.id_equipamento = cursor.lastrowid

        return equipamento.id_equipamento

    def buscar_equipamento(self, codigo_tag: str):
        with closing(self.conectar()) as conexao:
            return conexao.execute(
                "SELECT * FROM equipamento WHERE codigo_tag = ?",
                (codigo_tag,),
            ).fetchone()

    # ==========================================================
    # MEDICAO
    # ==========================================================

    def salvar_medicao(self, medicao: Medicao) -> int:
        medicao.validar()

        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    """
                    INSERT INTO medicao (
                        id_equipamento,
                        id_tecnico,
                        parametro_medido,
                        valor_nominal,
                        tolerancia_min,
                        tolerancia_max,
                        valor_obtido,
                        status_resultado
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        medicao.id_equipamento,
                        medicao.id_tecnico,
                        medicao.parametro_medido,
                        medicao.valor_nominal,
                        medicao.tolerancia_min,
                        medicao.tolerancia_max,
                        medicao.media,
                        medicao.status_resultado,
                    ),
                )
                medicao.id_medicao = cursor.lastrowid

        return medicao.id_medicao

    def listar_medicoes(self):
        with closing(self.conectar()) as conexao:
            return conexao.execute(
                """
                SELECT
                    m.id_medicao,
                    e.codigo_tag,
                    e.nome_equipamento,
                    t.nome_tecnico,
                    m.parametro_medido,
                    m.valor_nominal,
                    m.tolerancia_min,
                    m.tolerancia_max,
                    m.valor_obtido,
                    m.status_resultado,
                    m.data_medicao
                FROM medicao AS m
                INNER JOIN equipamento AS e
                    ON e.id_equipamento = m.id_equipamento
                INNER JOIN tecnico AS t
                    ON t.id_tecnico = m.id_tecnico
                ORDER BY m.id_medicao
                """
            ).fetchall()

    def atualizar_tecnico(self, tecnico: Tecnico) -> bool:
        tecnico.validar()

        if tecnico.id_tecnico is None:
            raise ValueError("O técnico precisa ter um ID.")

        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    """
                    UPDATE tecnico
                    SET nome_tecnico = ?, matricula = ?,
                        email = ?, setor = ?
                    WHERE id_tecnico = ?
                    """,
                    (
                        tecnico.nome_tecnico,
                        tecnico.matricula,
                        tecnico.email,
                        tecnico.setor,
                        tecnico.id_tecnico,
                    ),
                )

        return cursor.rowcount > 0

    def atualizar_equipamento(self, equipamento: Equipamento) -> bool:
        equipamento.validar()

        if equipamento.id_equipamento is None:
            raise ValueError("O equipamento precisa ter um ID.")

        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    """
                    UPDATE equipamento
                    SET codigo_tag = ?, nome_equipamento = ?,
                        fabricante = ?, modelo = ?
                    WHERE id_equipamento = ?
                    """,
                    (
                        equipamento.codigo_tag,
                        equipamento.nome_equipamento,
                        equipamento.fabricante,
                        equipamento.modelo,
                        equipamento.id_equipamento,
                    ),
                )

        return cursor.rowcount > 0

    def atualizar_medicao(self, medicao: Medicao) -> bool:
        medicao.validar()

        if medicao.id_medicao is None:
            raise ValueError("A medição precisa ter um ID.")

        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    """
                    UPDATE medicao
                    SET id_equipamento = ?,
                        id_tecnico = ?,
                        parametro_medido = ?,
                        valor_nominal = ?,
                        tolerancia_min = ?,
                        tolerancia_max = ?,
                        valor_obtido = ?,
                        status_resultado = ?
                    WHERE id_medicao = ?
                    """,
                    (
                        medicao.id_equipamento,
                        medicao.id_tecnico,
                        medicao.parametro_medido,
                        medicao.valor_nominal,
                        medicao.tolerancia_min,
                        medicao.tolerancia_max,
                        medicao.media,
                        medicao.status_resultado,
                        medicao.id_medicao,
                    ),
                )

        return cursor.rowcount > 0
