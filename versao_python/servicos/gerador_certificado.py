from pathlib import Path
from xml.sax.saxutils import escape
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
    CondPageBreak,
)

from servicos.calculo_incerteza import (
    converter_incerteza_para_certificado,
)


AZUL = colors.HexColor("#17365D")
CINZA = colors.HexColor("#D9D9D9")


def formatar_numero(valor, casas=3):

    if valor is None:
        return "-"

    return f"{float(valor):.{casas}f}".replace(".", ",")


def exibir_data(valor):

    if not valor:
        return "PENDENTE"

    try:
        return date.fromisoformat(
            str(valor)[:10]
        ).strftime("%d/%m/%Y")

    except (ValueError, TypeError):
        return str(valor)


class CanvasNumerado(canvas.Canvas):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.paginas_salvas = []

    def showPage(self):

        self.paginas_salvas.append(
            dict(self.__dict__)
        )

        self._startPage()

    def save(self):

        total_paginas = len(self.paginas_salvas)

        for estado in self.paginas_salvas:

            self.__dict__.update(estado)

            self.desenhar_rodape(total_paginas)

            super().showPage()

        super().save()

    def desenhar_rodape(self, total_paginas):

        largura, altura = A4

        self.saveState()

        self.setStrokeColor(colors.black)
        self.setLineWidth(0.6)

        self.line(
            12 * mm,
            22 * mm,
            largura - 12 * mm,
            22 * mm,
        )

        self.line(
            12 * mm,
            21 * mm,
            largura - 12 * mm,
            21 * mm,
        )

        self.setFillColor(colors.black)
        self.setFont("Helvetica", 8)

        self.drawCentredString(
            largura / 2,
            17 * mm,
            f"Folha {self._pageNumber:02d}/"
            f"{total_paginas:02d}",
        )

        self.setFont("Helvetica", 6)

        self.drawCentredString(
            largura / 2,
            12 * mm,
            "SCHULZ Metrologia - Rua Dona Francisca, "
            "6901 - Distrito Industrial - Joinville - SC",
        )

        self.drawCentredString(
            largura / 2,
            9 * mm,
            "CEP 89219-600 | Fone (47) 3451-6342 | "
            "metrologia@schulz.com.br",
        )

        self.drawCentredString(
            largura / 2,
            6 * mm,
            "CNPJ 84.684.182/0001-57 | "
            "Insc. Est. 250.135.558 | www.schulz.com.br",
        )

        self.restoreState()


def gerar_certificado(
    resultados,
    caminho_saida="certificado_calibracao.pdf",
    dados_identificacao=None,
    dados_incerteza=None,
    padroes_utilizados=None,
    procedimento=None,
):

    """Gera o PDF de calibração com tabela dinâmica."""

    if not resultados:
        raise ValueError(
            "Não existem resultados para gerar o PDF."
        )

    dados_identificacao = dados_identificacao or {}

    saida = Path(caminho_saida)

    saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    pasta_projeto = (
        Path(__file__).resolve().parent.parent
    )

    logo_path = (
        pasta_projeto
        / "assets"
        / "schulz_logo_original.jpg"
    )

    if not logo_path.is_file():

        raise FileNotFoundError(
            f"Logotipo não encontrado: {logo_path}"
        )

    documento = SimpleDocTemplate(
        str(saida),
        pagesize=A4,
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=30 * mm,
        bottomMargin=26 * mm,
        title="Certificado de Calibração",
    )

    estilo_texto = ParagraphStyle(
        "Texto",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        spaceAfter=1,
    )

    estilo_centralizado = ParagraphStyle(
        "Centralizado",
        parent=estilo_texto,
        alignment=TA_CENTER,
    )

    estilo_identificacao = ParagraphStyle(
        "Identificacao",
        parent=estilo_centralizado,
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
    )

    estilo_secao = ParagraphStyle(
        "Secao",
        parent=estilo_texto,
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        spaceBefore=2 * mm,
        spaceAfter=1 * mm,
        keepWithNext=True,
    )

    estilo_celula = ParagraphStyle(
        "Celula",
        parent=estilo_centralizado,
        fontSize=7,
        leading=9,
    )

    estilo_cabecalho = ParagraphStyle(
        "CabecalhoTabela",
        parent=estilo_celula,
        fontName="Helvetica-Bold",
    )

    estilo_notas = ParagraphStyle(
        "Notas",
        parent=estilo_texto,
        fontSize=6.5,
        leading=8,
    )

    estilo_aviso = ParagraphStyle(
        "Aviso",
        parent=estilo_centralizado,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#B00020"),
        fontSize=8,
        leading=10,
    )

    def p(texto, estilo=estilo_texto):

        return Paragraph(
            escape(str(texto)),
            estilo,
        )

    def campo(chave):

        return (
            dados_identificacao.get(chave)
            or "PENDENTE"
        )

    def desenhar_cabecalho(canvas_pdf, doc):

        largura, altura = A4

        canvas_pdf.saveState()

        canvas_pdf.setStrokeColor(AZUL)
        canvas_pdf.setLineWidth(1.2)

        canvas_pdf.line(
            12 * mm,
            altura - 8 * mm,
            largura - 12 * mm,
            altura - 8 * mm,
        )

        logo = Image(str(logo_path))

        fator = min(
            (47 * mm) / logo.imageWidth,
            (12 * mm) / logo.imageHeight,
        )

        logo.drawWidth = logo.imageWidth * fator
        logo.drawHeight = logo.imageHeight * fator

        logo.drawOn(
            canvas_pdf,
            12 * mm,
            altura - 17 * mm - logo.drawHeight / 2,
        )

       # Título com sombreamento
        canvas_pdf.setFont("Helvetica-Bold", 19)

        titulo = "Certificado de Calibração"

        x_titulo = 128 * mm
        y_titulo = altura - 19 * mm

        # Sombra cinza
        canvas_pdf.setFillColor(
            colors.HexColor("#A6A6A6")
        )

        canvas_pdf.drawCentredString(
            x_titulo + 0.5 * mm,
            y_titulo - 0.5 * mm,
            titulo,
        )

        # Título principal azul
        canvas_pdf.setFillColor(AZUL)

        canvas_pdf.drawCentredString(
            x_titulo,
            y_titulo,
            titulo,
        )

        canvas_pdf.setFillColor(CINZA)

        canvas_pdf.rect(
            12 * mm,
            altura - 26 * mm,
            largura - 24 * mm,
            3 * mm,
            fill=1,
            stroke=0,
        )

        canvas_pdf.restoreState()

    conteudo = []

    # 1. Número e data

    numero = campo("numero_certificado")

    data_calibracao = exibir_data(
        campo("data_calibracao")
    )

    conteudo.append(p(
        f"Certificado de Calibração nº {numero}",
        estilo_identificacao,
    ))

    conteudo.append(p(
        f"Data: {data_calibracao}",
        estilo_identificacao,
    ))

    conteudo.append(Spacer(1, 2 * mm))

    conteudo.append(p(
        f"Solicitante: {campo('solicitante')}"
    ))

    # 2. Descrição do instrumento

    conteudo.append(p(
        "1. Descrição do instrumento calibrado",
        estilo_secao,
    ))

    conteudo.append(p(
        f"Denominação: {campo('equipamento')}"
    ))

    conteudo.append(p(
        f"Código: {campo('codigo_tag')}"
    ))

    conteudo.append(p(
        f"Fabricante: {campo('fabricante')}"
    ))

    conteudo.append(p(
        f"Modelo: {campo('modelo')}"
    ))

    # 3. Padrões utilizados

    conteudo.append(p(
        "2. Padrão utilizado",
        estilo_secao,
    ))

    if padroes_utilizados:

        for padrao in padroes_utilizados:

            denominacao = (
                padrao.get("denominacao")
                or "PENDENTE"
            )

            codigo = (
                padrao.get("codigo")
                or "PENDENTE"
            )

            fabricante = (
                padrao.get("fabricante")
                or "PENDENTE"
            )

            certificado = (
                padrao.get("certificado")
                or "PENDENTE"
            )

            executante = (
                padrao.get("executante")
                or "PENDENTE"
            )

            ultima = exibir_data(
                padrao.get("ultima_calibracao")
            )

            proxima = exibir_data(
                padrao.get("proxima_calibracao")
            )

            conteudo.append(p(
                f"*{denominacao} "
                f"{codigo} - {fabricante}"
            ))

            conteudo.append(p(
                f"Certificado de Calibração nº "
                f"{certificado} - {executante}; "
                f"de {ultima} - "
                f"Próxima Calibração: {proxima}"
            ))

            try:

                data_limite = date.fromisoformat(
                    padrao["proxima_calibracao"]
                )

                data_registro = date.fromisoformat(
                    str(
                        dados_identificacao[
                            "data_calibracao"
                        ]
                    )[:10]
                )

                if data_registro > data_limite:

                    conteudo.append(p(
                        "ATENÇÃO: prazo de recalibração "
                        "do padrão ultrapassado.",
                        estilo_aviso,
                    ))

            except (ValueError, TypeError, KeyError):

                conteudo.append(p(
                    "Validade do padrão não verificada.",
                    estilo_aviso,
                ))

    else:

        conteudo.append(p(
            "Identificação do padrão: PENDENTE."
        ))

    # 4. Procedimento de calibração

    conteudo.append(p(
        "3. Procedimento de calibração",
        estilo_secao,
    ))

    if procedimento:

        paragrafos = [
            texto.strip()
            for texto in procedimento.splitlines()
            if texto.strip()
        ]

        for indice, texto in enumerate(paragrafos):

            estilo = (
                estilo_centralizado
                if indice == 0
                else estilo_texto
            )

            conteudo.append(p(texto, estilo))

    else:

        conteudo.append(p(
            "Procedimento de calibração: PENDENTE."
        ))

    # 5. Resultados dinâmicos

    conteudo.append(
        CondPageBreak(25 * mm)
    )

    conteudo.append(p(
        "4. Resultados (mm)",
        estilo_secao,
    ))

    titulos = [
        "Parâmetro avaliado",
        "Valor nominal",
        "Tol. +",
        "Tol. -",
        "Valor obtido",
        "Erro",
        "Resultado",
    ]

    linhas = [[
        p(titulo, estilo_cabecalho)
        for titulo in titulos
    ]]

    for resultado in resultados:

        linhas.append([
            p(
                resultado["parametro"],
                estilo_celula,
            ),

            p(
                formatar_numero(
                    resultado["nominal"]
                ),
                estilo_celula,
            ),

            p(
                formatar_numero(
                    resultado["tolerancia_positiva"]
                ),
                estilo_celula,
            ),

            p(
                formatar_numero(
                    resultado["tolerancia_negativa"]
                ),
                estilo_celula,
            ),

            p(
                formatar_numero(
                    resultado["valor_obtido"]
                ),
                estilo_celula,
            ),

            p(
                formatar_numero(
                    resultado["erro"]
                ),
                estilo_celula,
            ),

            p(
                resultado.get(
                    "status_resultado",
                    "PENDENTE",
                ),
                estilo_celula,
            ),
        ])

    tabela = Table(
        linhas,
        colWidths=[
            39 * mm,
            25 * mm,
            20 * mm,
            20 * mm,
            25 * mm,
            23 * mm,
            29 * mm,
        ],
        repeatRows=1,
        splitByRow=1,
        hAlign="CENTER",
    )

    tabela.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            CINZA,
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.65,
            colors.black,
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE",
        ),
        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "CENTER",
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            2,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            2,
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            3,
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            3,
        ),
    ]))

    conteudo.append(tabela)

    # 6. Incerteza de medição

    if dados_incerteza is not None:

        unidade = dados_incerteza["unidade"]

        valor_u = float(
            dados_incerteza["incerteza_expandida"]
        )

        if unidade in ("µm", "μm", "um"):

            valor_u = (
                converter_incerteza_para_certificado(
                    valor_u
                )
            )

        elif unidade != "mm":

            raise ValueError(
                f"Unidade de incerteza inválida: "
                f"{unidade}"
            )

        valor_k = dados_incerteza[
            "fator_abrangencia"
        ]

        valor_veff = dados_incerteza[
            "graus_liberdade_efetivos"
        ]

        texto_u = formatar_numero(
            valor_u,
            casas=3,
        )

        texto_k = formatar_numero(
            valor_k,
            casas=2,
        )

        texto_veff = formatar_numero(
            valor_veff,
            casas=0,
        )

    else:

        texto_u = "PENDENTE"
        texto_k = "PENDENTE"
        texto_veff = "PENDENTE"

    conteudo.append(Spacer(1, 2 * mm))

    tabela_incerteza = Table(
        [[
            p(
                "5. Incerteza de medição:",
                estilo_secao,
            ),

            p(
                f"{texto_u} mm",
                estilo_centralizado,
            ),

            p(
                f"k = {texto_k}",
                estilo_centralizado,
            ),
        ]],
        colWidths=[
            80 * mm,
            50 * mm,
            50 * mm,
        ],
    )

    tabela_incerteza.setStyle(TableStyle([
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE",
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            0,
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            2,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            2,
        ),
    ]))

    conteudo.append(tabela_incerteza)

    # 7. Observações

    conteudo.append(p(
        "6. Observações",
        estilo_secao,
    ))

    conteudo.append(p(
        "Os parâmetros avaliados correspondem "
        "às características de controle do produto."
    ))

    conteudo.append(p(
        "A classificação considera a média das "
        "medições e os limites de tolerância."
    ))

    # 8. Técnico responsável

    tecnico = campo("tecnico")
    matricula = campo("matricula")

    bloco_responsavel = [
        Spacer(1, 2 * mm),

        p(
            f"Técnico executante: {tecnico}"
        ),

        Spacer(1, 5 * mm),

        p(
            "________________________________",
            estilo_centralizado,
        ),

        p(
            tecnico,
            estilo_centralizado,
        ),

        p(
            f"Matrícula: {matricula}",
            estilo_centralizado,
        ),

        p(
            "Signatário autorizado",
            estilo_centralizado,
        ),
    ]

    conteudo.append(
        KeepTogether(bloco_responsavel)
    )

    # 9. Notas

    conteudo.append(Spacer(1, 2 * mm))

    bloco_notas = [
        p(
            "Notas:",
            estilo_notas,
        ),

        p(
            "A incerteza expandida corresponde "
            "à incerteza combinada multiplicada "
            f"pelo fator de abrangência k = {texto_k}, "
            f"com Veff = {texto_veff}.",
            estilo_notas,
        ),

        p(
            "O cálculo reproduz o modelo volumétrico "
            "da planilha de referência.",
            estilo_notas,
        ),

        p(
            "Os resultados dizem respeito exclusivamente "
            "ao instrumento e às condições registradas.",
            estilo_notas,
        ),

        p(
            "A incerteza é apresentada separadamente "
            "da classificação das medições.",
            estilo_notas,
        ),

        p(
            "Finalização do relatório.",
            estilo_notas,
        ),
    ]

    conteudo.append(
        KeepTogether(bloco_notas)
    )

    # 10. Gerar PDF

    documento.build(
        conteudo,
        onFirstPage=desenhar_cabecalho,
        onLaterPages=desenhar_cabecalho,
        canvasmaker=CanvasNumerado,
    )

    return saida