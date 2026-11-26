from math import isfinite

from servicos.calculo_incerteza import (
    calcular_dispersao_registro,
    calcular_contribuicao_incerteza,
    calcular_incerteza_combinada,
    calcular_veff_por_componentes,
    calcular_fator_abrangencia,
    calcular_incerteza_expandida,
    converter_incerteza_para_certificado,
)


def executar_motor_incerteza(registros, fontes_incerteza):
    """
    Executa o cálculo de incerteza do modelo
    CONTROLE DIMENSIONAL - Volumétrico.

    Referências da aba Incerteza:
        B48: dispersão das medidas
        G56: incerteza combinada
        H57: graus de liberdade efetivos
        F58: fator de abrangência
        G58: incerteza expandida

    Retorna os resultados e parâmetros necessários
    para armazenamento e rastreabilidade no SQLite.

    Reproduz as conversões utilizadas na planilha.
    Não modifica arquivos Excel.
    """

    if not registros:
        raise ValueError("Nenhuma medição informada.")

    fontes_incerteza = list(fontes_incerteza)

    if len(fontes_incerteza) != 7:
        raise ValueError(
            "O modelo volumétrico exige sete fontes "
            "de incerteza além da dispersão das medidas."
        )

    # 1. Dispersão das medidas
    dispersao = calcular_dispersao_registro(
        registros,
        fator_conversao=1000.0,
    )

    quantidade_medicoes = (
        dispersao["quantidade_medicoes"]
    )

    graus_dispersao = quantidade_medicoes - 1

    # 2. Primeiro componente: dispersão
    componentes = [{
        "descricao": "Dispersão das medidas",
        "contribuicao": dispersao["incerteza_dispersao"],
        "graus_liberdade": graus_dispersao,
    }]

    parametros_utilizados = [{
        "descricao": "Dispersão das medidas",
        "valor_original": dispersao["maior_desvio_original"],
        "fator_conversao": dispersao["fator_conversao"],
        "valor": dispersao["maior_desvio"],
        "divisor": dispersao["divisor"],
        "coeficiente_sensibilidade": 1.0,
        "graus_liberdade": graus_dispersao,
        "incerteza_padrao": dispersao["incerteza_dispersao"],
        "contribuicao": dispersao["incerteza_dispersao"],
    }]

    # 3. Demais componentes do modelo volumétrico
    for fonte in fontes_incerteza:

        resultado = calcular_contribuicao_incerteza(
            fonte["valor"],
            fonte["divisor"],
            fonte["coeficiente_sensibilidade"],
        )

        graus = float(fonte["graus_liberdade"])

        if not isfinite(graus) or graus <= 0:
            raise ValueError(
                "Graus de liberdade inválidos: "
                f"{fonte['descricao']}"
            )

        componentes.append({
            "descricao": fonte["descricao"],
            "contribuicao": resultado["contribuicao"],
            "graus_liberdade": graus,
        })

        parametros_utilizados.append({
            "descricao": fonte["descricao"],
            "valor": float(fonte["valor"]),
            "divisor": float(fonte["divisor"]),
            "coeficiente_sensibilidade": float(
                fonte["coeficiente_sensibilidade"]
            ),
            "graus_liberdade": graus,
            "incerteza_padrao": resultado["incerteza_padrao"],
            "contribuicao": resultado["contribuicao"],
        })

    # 4. Incerteza combinada - G56
    contribuicoes = [
        item["contribuicao"]
        for item in componentes
    ]

    uc = calcular_incerteza_combinada(
        contribuicoes
    )

    # 5. Graus de liberdade antes do arredondamento
    veff_original = calcular_veff_por_componentes(
        componentes,
        aplicar_int=False,
    )

    # 6. Graus de liberdade efetivos - H57
    veff = calcular_veff_por_componentes(
        componentes,
        aplicar_int=True,
    )

    # 7. Fator de abrangência - F58
    k = calcular_fator_abrangencia(veff)

    # 8. Incerteza expandida - G58
    u_expandida = calcular_incerteza_expandida(
        uc,
        k,
    )

    # 9. Conversão para apresentação no certificado
    u_certificado = converter_incerteza_para_certificado(
        u_expandida
    )

    # 10. Resultados e rastreabilidade
    return {
        "modelo_incerteza": "Volumétrico",

        "unidade": "µm",

        "maior_desvio_padrao_original": (
            dispersao["maior_desvio_original"]
        ),

        "maior_desvio_padrao": (
            dispersao["maior_desvio"]
        ),

        "fator_conversao_dispersao": (
            dispersao["fator_conversao"]
        ),

        "quantidade_medicoes": quantidade_medicoes,

        "incerteza_dispersao": (
            dispersao["incerteza_dispersao"]
        ),

        "incerteza_combinada": uc,

        "graus_liberdade_efetivos_original": (
            veff_original
        ),

        "graus_liberdade_efetivos": veff,

        "fator_abrangencia": k,

        "incerteza_expandida": u_expandida,

        "incerteza_certificado": u_certificado,

        "unidade_certificado": "mm",

        "componentes": componentes,

        "parametros_incerteza": parametros_utilizados,
    }