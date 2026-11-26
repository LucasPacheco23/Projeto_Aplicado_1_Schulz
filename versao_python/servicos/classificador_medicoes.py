
from math import isfinite


def classificar_medicao(
    valor_obtido,
    limite_inferior,
    limite_superior,
):
    """
    Classifica uma medição usando somente
    os limites de tolerância.

    A incerteza não participa da decisão.
    """

    valores = (
        valor_obtido,
        limite_inferior,
        limite_superior,
    )

    for valor in valores:
        if not isinstance(valor, (int, float)):
            raise TypeError("Os valores devem ser numéricos.")

        if not isfinite(valor):
            raise ValueError("Os valores devem ser finitos.")

    if limite_inferior > limite_superior:
        raise ValueError("Limites de tolerância invertidos.")

    if limite_inferior <= valor_obtido <= limite_superior:
        return "APROVADO"

    return "REPROVADO"
