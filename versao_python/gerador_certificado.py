import pandas as pd
from classes import BancoDados, Tecnico, Equipamento, Medicao

def importar_planilha(caminho_excel: str, banco: BancoDados):
    df = pd.read_excel(caminho_excel)
    df = df.iloc[:10]

    cabecalho = {
        "measurement_plan": df.iloc[3,1],
        "date": df.iloc[3,3],
        "order": df.iloc[3,5],
        "drawing_no": df.iloc[6,1],
        "time": df.iloc[6,3],
        "part_no": df.iloc[6,5],
        "metrologista": df.iloc[9,1],
        "mmc": df.iloc[9,3],
        "fornecedor": df.iloc[9,5]
    }

    df = pd.read_excel(caminho_excel, skiprows=12)
    df = df.dropna(how='all')
    df = df.reset_index(drop=True)

    tecnico = banco.buscar_tecnico_por_nome(cabecalho['metrologista'])
    if tecnico is None:
        raise ValueError(
            f"Técnico não encontrado: {cabecalho['metrologista']}"
        )
    id_tecnico = tecnico['id_tecnico']

    equipamento = banco.buscar_equipamento(str(cabecalho['mmc']))
    if equipamento is None:
        raise ValueError(
            f"Equipamento não encontrado: {cabecalho['mmc']}"
        )
    id_equipamento = equipamento['id_equipamento']

    medicoes_salvas = []
    for parametro, grupo in df.groupby('Characteristic', sort=False):

        data = f"{cabecalho['date'].strftime("%Y-%m-%d")}"
        hora = f"{cabecalho['time']}"
        data_hora = f"{data} {hora}"
        
        leituras = grupo['Actual'].tolist()
        linha_base = grupo.iloc[0]
        tol_min = linha_base['Nominal'] + linha_base['Lower Tol']
        tol_max = linha_base["Nominal"] + linha_base['Upper Tol']

        medicao = Medicao(  
            id_equipamento    =    id_equipamento,
            id_tecnico        =    id_tecnico,
            parametro_medido  =    parametro,
            valor_nominal     =    linha_base["Nominal"],
            tolerancia_min    =    tol_min, 
            tolerancia_max    =    tol_max,
            medida_1          =    leituras[0],
            medida_2          =    leituras[1],
            data_medicao      =    data_hora

        )

        banco.salvar_medicao(medicao)
        medicoes_salvas.append(medicao)

    return cabecalho, medicoes_salvas
