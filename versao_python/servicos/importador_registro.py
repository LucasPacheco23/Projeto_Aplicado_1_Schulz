
from pathlib import Path
from openpyxl import load_workbook


def importar_registro(caminho_excel):
    """
    Lê as medições da aba Registro.

    Utiliza os valores calculados e salvos no Excel.
    Não altera a planilha original.
    """

    caminho = Path(caminho_excel)

    if not caminho.is_file():
        raise FileNotFoundError(
            f"Planilha não encontrada: {caminho}"
        )

    wb = load_workbook(
        caminho,
        data_only=True,
        read_only=True,
    )

    try:
        if "Registro" not in wb.sheetnames:
            raise ValueError("A aba Registro não foi encontrada.")

        ws = wb["Registro"]
        registros = []

        for linha in range(30, 65):
            parametro = ws[f"B{linha}"].value

            if parametro is None or not str(parametro).strip():
                continue

            registro = {
                "linha_excel": linha,
                "dimension": str(parametro).strip(),
                "nominal": ws[f"C{linha}"].value,
                "tolerancia_positiva": ws[f"D{linha}"].value,
                "tolerancia_negativa": ws[f"E{linha}"].value,
                "medicao_1": ws[f"F{linha}"].value,
                "medicao_2": ws[f"G{linha}"].value,
                "media_excel": ws[f"H{linha}"].value,
                "desvio_excel": ws[f"I{linha}"].value,
            }

            registros.append(registro)

        return registros

    finally:
        wb.close()
