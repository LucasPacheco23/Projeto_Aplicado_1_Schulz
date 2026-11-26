from pathlib import Path
from datetime import date, datetime
from math import isfinite

from openpyxl import load_workbook

from servicos.importador_registro import importar_registro
from servicos.motor_incerteza import executar_motor_incerteza


def formatar_data_padrao(valor):

    if isinstance(valor, datetime):
        return valor.date().isoformat()

    if isinstance(valor, date):
        return valor.isoformat()

    return None


def extrair_padroes_utilizados(wb):
    """
    Recupera o padrão utilizado na calibração.

    O MVP contempla a máquina de medição
    por coordenadas (MMC).
    """

    if "Padrões" not in wb.sheetnames:
        raise ValueError(
            "A aba Padrões não foi encontrada."
        )

    selecao = wb["Registro"]["C12"].value

    if selecao != 1:
        raise ValueError(
            "O MVP contempla somente calibrações "
            "com máquina de medição por coordenadas."
        )

    ws = wb["Padrões"]

    padrao = {
        "codigo": ws["B3"].value,
        "denominacao": ws["C3"].value,
        "modelo": ws["F3"].value,
        "fabricante": ws["G3"].value,
        "numero_serie": ws["H3"].value,
        "certificado": ws["G5"].value,
        "executante": ws["H5"].value,
        "ultima_calibracao": formatar_data_padrao(
            ws["F5"].value
        ),
        "proxima_calibracao": formatar_data_padrao(
            ws["I5"].value
        ),
    }

    # Converter os campos para armazenamento em JSON
    for chave, valor in padrao.items():

        if valor is not None:
            padrao[chave] = str(valor)

    return [padrao]


def extrair_procedimento(wb):
    """
    Recupera o procedimento da planilha original,
    preservando a separação dos parágrafos.
    """

    if "Certificado" not in wb.sheetnames:
        raise ValueError(
            "A aba Certificado não foi encontrada."
        )

    ws = wb["Certificado"]

    textos = [
        ws["D26"].value,
        ws["A28"].value,
        ws["A29"].value,
    ]

    procedimento = "\n".join(
        str(texto).strip()
        for texto in textos
        if texto is not None
        and str(texto).strip()
    )

    return procedimento or None


def extrair_fontes_volumetricas(wb):
    """
    Recupera as sete fontes adicionais do bloco
    CONTROLE DIMENSIONAL - Volumétrico.

    Referências:
        Linhas 49 a 55 da aba Incerteza.

    A dispersão da linha 48 é calculada
    independentemente pelo motor Python.
    """

    if "Incerteza" not in wb.sheetnames:
        raise ValueError(
            "A aba Incerteza não foi encontrada."
        )

    ws = wb["Incerteza"]

    quantidade_medicoes = ws["C44"].value

    if quantidade_medicoes != 2:
        raise ValueError(
            "O modelo atual exige duas medições "
            "por parâmetro, conforme a célula C44."
        )

    fontes = []

    for linha in range(49, 56):

        fonte = {
            "descricao": ws[f"A{linha}"].value,
            "valor": ws[f"B{linha}"].value,
            "divisor": ws[f"C{linha}"].value,
            "coeficiente_sensibilidade": (
                ws[f"F{linha}"].value
            ),
            "graus_liberdade": ws[f"H{linha}"].value,
        }

        if not fonte["descricao"]:
            raise ValueError(
                f"Descrição ausente na linha {linha}."
            )

        fonte["descricao"] = str(
            fonte["descricao"]
        ).strip()

        campos_numericos = (
            "valor",
            "divisor",
            "coeficiente_sensibilidade",
            "graus_liberdade",
        )

        for campo in campos_numericos:

            valor = fonte[campo]

            if valor is None:
                raise ValueError(
                    f"Valor ausente na linha {linha}, "
                    f"campo {campo}."
                )

            try:
                valor = float(valor)

            except (TypeError, ValueError):
                raise ValueError(
                    f"Valor não numérico na linha "
                    f"{linha}, campo {campo}."
                )

            if not isfinite(valor):
                raise ValueError(
                    f"Valor não finito na linha "
                    f"{linha}, campo {campo}."
                )

            fonte[campo] = valor

        if fonte["divisor"] <= 0:
            raise ValueError(
                f"Divisor inválido na linha {linha}."
            )

        if fonte["graus_liberdade"] <= 0:
            raise ValueError(
                f"Graus de liberdade inválidos "
                f"na linha {linha}."
            )

        fontes.append(fonte)

    return fontes


def calcular_incerteza_certificado(
    caminho_excel,
    registros=None,
):
    """
    Calcula a incerteza pelo modelo volumétrico
    e recupera os padrões e o procedimento.

    Reproduz as conversões utilizadas na planilha.
    Não modifica o arquivo Excel.
    """

    caminho = Path(caminho_excel)

    if not caminho.is_file():
        raise FileNotFoundError(
            f"Planilha não encontrada: {caminho}"
        )

    if registros is None:
        registros = importar_registro(caminho)

    if not registros:
        raise ValueError(
            "Nenhuma medição encontrada na aba Registro."
        )

    wb = load_workbook(
        caminho,
        data_only=True,
        read_only=True,
    )

    try:

        if "Registro" not in wb.sheetnames:
            raise ValueError(
                "A aba Registro não foi encontrada."
            )

        padroes = extrair_padroes_utilizados(wb)

        fontes = extrair_fontes_volumetricas(wb)

        procedimento = extrair_procedimento(wb)

    finally:
        wb.close()

    resultado = executar_motor_incerteza(
        registros,
        fontes,
    )

    resultado["padroes_utilizados"] = padroes

    resultado["procedimento"] = procedimento

    return resultado