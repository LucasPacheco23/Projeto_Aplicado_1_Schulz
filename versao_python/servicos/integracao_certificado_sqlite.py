import json
import sqlite3

from pathlib import Path


def carregar_dados_certificado(
    caminho_banco,
    id_calibracao,
):
    """
    Recupera todos os dados de uma calibração
    exclusivamente do banco SQLite.

    Utiliza JOIN entre as tabelas:
    - calibracao
    - medicao
    - tecnico
    - equipamento

    Não consulta arquivos Excel.
    Não modifica o banco de dados.
    """

    banco = Path(caminho_banco)

    if not banco.is_file():
        raise FileNotFoundError(
            f"Banco não encontrado: {banco}"
        )

    endereco = banco.resolve().as_uri() + "?mode=ro"

    conexao = sqlite3.connect(endereco, uri=True)
    conexao.row_factory = sqlite3.Row

    try:
        # Recuperar os dados gerais da calibração
        calibracao = conexao.execute(
            """
            SELECT
                c.*,

                t.nome_tecnico,
                t.matricula,
                t.email,
                t.setor,

                e.codigo_tag,
                e.nome_equipamento,
                e.fabricante,
                e.modelo

            FROM calibracao AS c

            INNER JOIN tecnico AS t
                ON c.id_tecnico = t.id_tecnico

            INNER JOIN equipamento AS e
                ON c.id_equipamento = e.id_equipamento

            WHERE c.id_calibracao = ?
            """,
            (id_calibracao,),
        ).fetchone()

        if calibracao is None:
            raise ValueError(
                "Calibração não encontrada no SQLite."
            )

        # Recuperar as medições vinculadas
        medicoes = conexao.execute(
            """
            SELECT
                m.id_medicao,
                m.id_calibracao,
                m.id_tecnico,
                m.id_equipamento,
                m.parametro_medido,
                m.valor_nominal,
                m.tolerancia_min,
                m.tolerancia_max,
                m.medicao_1,
                m.medicao_2,
                m.valor_obtido,
                m.desvio_padrao,
                m.status_resultado,
                m.data_medicao

            FROM medicao AS m

            INNER JOIN calibracao AS c
                ON m.id_calibracao = c.id_calibracao

            WHERE c.id_calibracao = ?

            ORDER BY m.id_medicao
            """,
            (id_calibracao,),
        ).fetchall()

    finally:
        conexao.close()

    if not medicoes:
        raise ValueError(
            "Nenhuma medição vinculada à calibração."
        )

    resultados = []

    for medicao in medicoes:

        parametro = medicao["parametro_medido"]

        # Verificar a consistência dos vínculos
        if (
            medicao["id_tecnico"]
            != calibracao["id_tecnico"]

            or medicao["id_equipamento"]
            != calibracao["id_equipamento"]
        ):
            raise ValueError(
                f"Vínculo inconsistente: {parametro}"
            )

        campos_obrigatorios = (
            "medicao_1",
            "medicao_2",
            "desvio_padrao",
        )

        for campo in campos_obrigatorios:
            if medicao[campo] is None:
                raise ValueError(
                    f"Dado ausente: {parametro} - {campo}"
                )

        nominal = float(
            medicao["valor_nominal"]
        )

        limite_inferior = float(
            medicao["tolerancia_min"]
        )

        limite_superior = float(
            medicao["tolerancia_max"]
        )

        valor_obtido = float(
            medicao["valor_obtido"]
        )

        resultados.append({
            "parametro": parametro,
            "nominal": nominal,

            "tolerancia_positiva": (
                limite_superior - nominal
            ),

            "tolerancia_negativa": (
                limite_inferior - nominal
            ),

            "medicao_1": float(
                medicao["medicao_1"]
            ),

            "medicao_2": float(
                medicao["medicao_2"]
            ),

            "valor_obtido": valor_obtido,

            "desvio_padrao": float(
                medicao["desvio_padrao"]
            ),

            "erro": valor_obtido - nominal,

            "limite_inferior": limite_inferior,
            "limite_superior": limite_superior,

            "status_resultado": (
                medicao["status_resultado"]
            ),
        })

    # Dados de identificação
    identificacao = {
        "id_calibracao": id_calibracao,

        "numero_certificado": (
            f"CAL-{id_calibracao:06d}"
        ),

        "tecnico": calibracao["nome_tecnico"],
        "matricula": calibracao["matricula"],
        "email": calibracao["email"],
        "setor": calibracao["setor"],

        "codigo_tag": calibracao["codigo_tag"],
        "equipamento": calibracao["nome_equipamento"],
        "fabricante": calibracao["fabricante"],
        "modelo": calibracao["modelo"],

        "fabricante_modelo": (
            f"{calibracao['fabricante']} / "
            f"{calibracao['modelo']}"
        ),

        "data_calibracao": (
            calibracao["data_calibracao"]
        ),

        "data_lote": (
            calibracao["data_calibracao"]
        ),

        "solicitante": "Schulz S.A.",

        "arquivo_origem": (
            calibracao["arquivo_origem"]
        ),
    }

    # Recuperar os parâmetros históricos
    parametros_incerteza = json.loads(
        calibracao["parametros_incerteza_json"]
    )

    # Recuperar os resultados da incerteza
    dados_incerteza = {
        "unidade": calibracao["unidade"],

        "maior_desvio_padrao": (
            calibracao["maior_desvio_padrao"]
        ),

        "incerteza_combinada": (
            calibracao["incerteza_combinada"]
        ),

        "graus_liberdade_efetivos": (
            calibracao["graus_liberdade_efetivos"]
        ),

        "fator_abrangencia": (
            calibracao["fator_abrangencia"]
        ),

        "incerteza_expandida": (
            calibracao["incerteza_expandida"]
        ),

        "parametros_incerteza": parametros_incerteza,
    }

    # Recuperar os padrões utilizados
    padroes_utilizados = []

    if calibracao["padroes_utilizados_json"]:
        padroes_utilizados = json.loads(
            calibracao["padroes_utilizados_json"]
        )

    # Resumo dos resultados
    aprovadas = sum(
        resultado["status_resultado"] == "APROVADO"
        for resultado in resultados
    )

    reprovadas = len(resultados) - aprovadas

    return {
        "identificacao": identificacao,
        "resultados": resultados,
        "dados_incerteza": dados_incerteza,
        "padroes_utilizados": padroes_utilizados,
        "procedimento": calibracao["procedimento"],

        "resumo": {
            "total_medicoes": len(resultados),
            "aprovadas": aprovadas,
            "reprovadas": reprovadas,
        },
    }