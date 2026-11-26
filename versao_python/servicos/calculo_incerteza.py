from math import sqrt, fsum, isfinite, floor
from statistics import stdev


def calcular_incerteza_combinada(contribuicoes):
    """
    Calcula a incerteza combinada pela raiz
    da soma dos quadrados das contribuições.

    Modelo volumétrico:
    Incerteza!G56
    """

    valores = list(contribuicoes)

    if not valores:
        raise ValueError("Nenhuma contribuição informada.")

    for valor in valores:
        if not isinstance(valor, (int, float)):
            raise TypeError(
                "As contribuições devem ser numéricas."
            )

        if not isfinite(valor):
            raise ValueError(
                "As contribuições devem ser finitas."
            )

    soma_quadrados = fsum(
        valor ** 2 for valor in valores
    )

    return sqrt(soma_quadrados)


def calcular_dispersao_registro(
    registros,
    fator_conversao=1000.0,
):
    """
    Reproduz a dispersão do modelo volumétrico.

    B48 = maior desvio padrão * 1000
    C48 = raiz quadrada da quantidade de medições
    D48 = B48 / C48
    """

    if not registros:
        raise ValueError("Nenhum registro informado.")

    if not isfinite(fator_conversao):
        raise ValueError("Fator de conversão inválido.")

    if fator_conversao <= 0:
        raise ValueError(
            "O fator de conversão deve ser positivo."
        )

    desvios = []

    for registro in registros:

        medidas = [
            float(registro["medicao_1"]),
            float(registro["medicao_2"]),
        ]

        if not all(
            isfinite(valor) for valor in medidas
        ):
            raise ValueError("Medição não finita.")

        desvios.append(stdev(medidas))

    maior_desvio_original = max(desvios)

    maior_desvio = (
        maior_desvio_original * fator_conversao
    )

    quantidade_medicoes = 2

    divisor = sqrt(quantidade_medicoes)

    incerteza_dispersao = maior_desvio / divisor

    return {
        "maior_desvio_original": maior_desvio_original,
        "maior_desvio": maior_desvio,
        "fator_conversao": fator_conversao,
        "quantidade_medicoes": quantidade_medicoes,
        "divisor": divisor,
        "incerteza_dispersao": incerteza_dispersao,
    }


def calcular_contribuicao_incerteza(
    valor,
    divisor,
    coeficiente_sensibilidade=1.0,
):
    """
    Calcula a contribuição de uma fonte de incerteza.

    D = B / C
    G = D * F
    """

    valores = (
        valor,
        divisor,
        coeficiente_sensibilidade,
    )

    for numero in valores:

        if not isinstance(numero, (int, float)):
            raise TypeError(
                "Os parâmetros devem ser numéricos."
            )

        if not isfinite(numero):
            raise ValueError(
                "Os parâmetros devem ser finitos."
            )

    if divisor <= 0:
        raise ValueError(
            "O divisor deve ser positivo."
        )

    incerteza_padrao = valor / divisor

    contribuicao = (
        incerteza_padrao * coeficiente_sensibilidade
    )

    return {
        "incerteza_padrao": incerteza_padrao,
        "contribuicao": contribuicao,
    }


def calcular_graus_liberdade_efetivos(
    incerteza_combinada,
    termos_denominador,
    aplicar_int=False,
):
    """
    Calcula os graus de liberdade efetivos.

    Quando aplicar_int=True, reproduz a função
    INT utilizada no modelo volumétrico.
    """

    if not isinstance(
        incerteza_combinada, (int, float)
    ):
        raise TypeError(
            "A incerteza deve ser numérica."
        )

    if not isfinite(incerteza_combinada):
        raise ValueError(
            "A incerteza deve ser finita."
        )

    if incerteza_combinada < 0:
        raise ValueError(
            "A incerteza não pode ser negativa."
        )

    termos = list(termos_denominador)

    if not termos:
        raise ValueError("Nenhum termo informado.")

    for termo in termos:

        if not isinstance(termo, (int, float)):
            raise TypeError(
                "Os termos devem ser numéricos."
            )

        if not isfinite(termo) or termo < 0:
            raise ValueError(
                "Os termos devem ser finitos "
                "e não negativos."
            )

    denominador = fsum(termos)

    if denominador == 0:
        raise ValueError(
            "O denominador é zero. "
            "Não é possível calcular Veff."
        )

    veff = (
        incerteza_combinada ** 4 / denominador
    )

    if aplicar_int:
        return floor(veff)

    return veff


def calcular_fator_abrangencia(veff):
    """
    Seleciona o fator k conforme as faixas
    de graus de liberdade efetivos.

    Modelo volumétrico:
    Incerteza!E60:E63 e F58.
    """

    if not isinstance(veff, (int, float)):
        raise TypeError("Veff deve ser numérico.")

    if not isfinite(veff) or veff < 0:
        raise ValueError("Veff inválido.")

    faixas = [
        (2, 13.97),
        (3, 4.53),
        (4, 3.31),
        (5, 2.87),
        (6, 2.65),
        (7, 2.52),
        (8, 2.43),
        (10, 2.37),
        (12, 2.28),
        (14, 2.23),
        (16, 2.20),
        (18, 2.17),
        (20, 2.15),
        (25, 2.13),
        (30, 2.11),
        (35, 2.09),
        (40, 2.07),
        (50, 2.06),
        (60, 2.05),
        (80, 2.04),
        (100, 2.03),
    ]

    for limite_superior, k in faixas:

        if veff < limite_superior:
            return k

    if veff == 100:
        return 2.02

    return 2.0


def calcular_incerteza_expandida(
    incerteza_combinada,
    fator_abrangencia,
):
    """
    Calcula a incerteza expandida.

    Incerteza!G58 = G56 * F58
    """

    for valor in (
        incerteza_combinada,
        fator_abrangencia,
    ):

        if not isinstance(valor, (int, float)):
            raise TypeError(
                "Os valores devem ser numéricos."
            )

        if not isfinite(valor) or valor < 0:
            raise ValueError("Valor inválido.")

    return (
        incerteza_combinada * fator_abrangencia
    )


def calcular_veff_por_componentes(
    componentes,
    aplicar_int=False,
):
    """
    Calcula Veff pelo método de
    Welch-Satterthwaite.

    Cada componente deve conter:
        - contribuicao
        - graus_liberdade
    """

    if not componentes:
        raise ValueError(
            "Nenhum componente informado."
        )

    contribuicoes = []
    termos = []

    for indice, componente in enumerate(
        componentes,
        start=1,
    ):

        u = float(
            componente["contribuicao"]
        )

        graus = float(
            componente["graus_liberdade"]
        )

        if not isfinite(u) or not isfinite(graus):
            raise ValueError(
                f"Componente {indice}: "
                "valor não finito."
            )

        if graus <= 0:
            raise ValueError(
                f"Componente {indice}: "
                "graus de liberdade devem ser positivos."
            )

        contribuicoes.append(u)

        termos.append(u ** 4 / graus)

    uc = calcular_incerteza_combinada(
        contribuicoes
    )

    return calcular_graus_liberdade_efetivos(
        incerteza_combinada=uc,
        termos_denominador=termos,
        aplicar_int=aplicar_int,
    )


def converter_incerteza_para_certificado(
    incerteza_expandida,
):
    """
    Reproduz a conversão utilizada na planilha
    para apresentação da incerteza no certificado.

    Converte de micrometros para milímetros.
    """

    valor = float(incerteza_expandida)

    if not isfinite(valor) or valor < 0:
        raise ValueError(
            "Incerteza expandida inválida."
        )

    return valor / 1000.0