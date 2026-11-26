
import sqlite3
import tkinter as tk
import sys

from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from classes import BancoDados, Tecnico, Equipamento

from datetime import datetime
import json

from math import isfinite
from statistics import mean, stdev

from servicos.importador_registro import importar_registro
from servicos.classificador_medicoes import classificar_medicao

from servicos.integracao_certificado_sqlite import (
    carregar_dados_certificado,
)
from servicos.incerteza_certificado import (
    calcular_incerteza_certificado,
)
from servicos.gerador_certificado import gerar_certificado


if getattr(sys, "frozen", False):
    PASTA_PROJETO = Path(sys.executable).resolve().parent
else:
    PASTA_PROJETO = Path(__file__).resolve().parent

BANCO = PASTA_PROJETO / "schulz_calibracao.db"


def listar_lotes():
    """
    Lista as calibrações registradas no novo
    modelo de armazenamento do SQLite.
    """

    if not BANCO.is_file():
        raise FileNotFoundError(
            "Banco SQLite não encontrado."
        )

    endereco = BANCO.resolve().as_uri() + "?mode=ro"

    conexao = sqlite3.connect(endereco, uri=True)

    try:
        lotes = conexao.execute("""
            SELECT
                c.id_calibracao,
                c.data_calibracao,
                t.nome_tecnico,
                e.codigo_tag,
                e.nome_equipamento,
                COUNT(m.id_medicao) AS quantidade

            FROM calibracao AS c

            INNER JOIN tecnico AS t
                ON c.id_tecnico = t.id_tecnico

            INNER JOIN equipamento AS e
                ON c.id_equipamento = e.id_equipamento

            INNER JOIN medicao AS m
                ON c.id_calibracao = m.id_calibracao

            GROUP BY
                c.id_calibracao,
                c.data_calibracao,
                t.nome_tecnico,
                e.codigo_tag,
                e.nome_equipamento

            ORDER BY c.id_calibracao DESC
        """).fetchall()

    finally:
        conexao.close()

    return lotes

def gerar_pdf():

    try:
        lotes = listar_lotes()

        if not lotes:
            messagebox.showwarning(
                "Certificados",
                "Nenhuma calibração completa encontrada.\n\n"
                "Importe uma calibração antes de gerar "
                "o certificado.",
            )
            return

        selecao = tk.Toplevel()
        selecao.title("Selecionar calibração")
        selecao.geometry("850x330")
        selecao.resizable(False, False)
        selecao.grab_set()

        quadro = ttk.Frame(selecao, padding=20)
        quadro.pack(fill="both", expand=True)

        ttk.Label(
            quadro,
            text="Selecione a calibração para emitir o certificado",
            font=("Arial", 12, "bold"),
        ).pack(pady=(0, 15))

        opcoes = []

        for lote in lotes:

            (
                id_calibracao,
                data,
                tecnico,
                tag,
                equipamento,
                quantidade,
            ) = lote

            opcoes.append(
                f"CAL-{id_calibracao:06d} | "
                f"{data} | {tag} | {equipamento} | "
                f"{tecnico} | {quantidade} medições"
            )

        escolha = ttk.Combobox(
            quadro,
            values=opcoes,
            state="readonly",
            width=115,
        )

        escolha.pack(fill="x", pady=10)
        escolha.current(0)

        def confirmar_lote():

            indice = escolha.current()

            if indice < 0:
                messagebox.showwarning(
                    "Seleção",
                    "Selecione uma calibração.",
                    parent=selecao,
                )
                return

            id_calibracao = lotes[indice][0]

            try:
                # Recuperar todos os dados do SQLite
                dados = carregar_dados_certificado(
                    caminho_banco=BANCO,
                    id_calibracao=id_calibracao,
                )

                identificacao = dados["identificacao"]
                resultados = dados["resultados"]
                dados_incerteza = dados["dados_incerteza"]
                resumo = dados["resumo"]

                numero_certificado = (
                    identificacao["numero_certificado"]
                )

                # Selecionar somente o destino do PDF
                destino = filedialog.asksaveasfilename(
                    parent=selecao,
                    title="Salvar certificado",
                    defaultextension=".pdf",
                    filetypes=[("PDF", "*.pdf")],
                    initialfile=(
                        f"certificado_{numero_certificado}.pdf"
                    ),
                )

                if not destino:
                    return

                # Gerar o certificado
                caminho_pdf = gerar_certificado(
                    resultados=resultados,
                    caminho_saida=destino,
                    dados_identificacao=identificacao,
                    dados_incerteza=dados_incerteza,
                    padroes_utilizados=dados["padroes_utilizados"],
                    procedimento=dados["procedimento"],
                )

                status.set(
                    f"Certificado {numero_certificado} "
                    "gerado com sucesso."
                )

                messagebox.showinfo(
                    "Certificado gerado",
                    f"Certificado: {numero_certificado}\n\n"
                    f"Medições: {resumo['total_medicoes']}\n"
                    f"Aprovadas: {resumo['aprovadas']}\n"
                    f"Reprovadas: {resumo['reprovadas']}\n\n"
                    f"Arquivo salvo em:\n{caminho_pdf}",
                    parent=selecao,
                )

                selecao.destroy()

            except Exception as erro:
                messagebox.showerror(
                    "Erro ao gerar certificado",
                    str(erro),
                    parent=selecao,
                )

        ttk.Button(
            quadro,
            text="Gerar certificado da calibração selecionada",
            command=confirmar_lote,
        ).pack(pady=20)

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            str(erro),
        )

def abrir_formulario_cadastro(titulo, campos, salvar):
    formulario = tk.Toplevel()
    formulario.title(titulo)
    formulario.geometry("440x340")
    formulario.resizable(False, False)
    formulario.grab_set()

    quadro = ttk.Frame(formulario, padding=20)
    quadro.pack(fill="both", expand=True)

    entradas = {}

    for linha, (chave, rotulo) in enumerate(campos):
        ttk.Label(
            quadro,
            text=rotulo,
        ).grid(row=linha, column=0, sticky="w", pady=8)

        entrada = ttk.Entry(quadro, width=30)
        entrada.grid(
            row=linha,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=8,
        )

        entradas[chave] = entrada

    def confirmar():
        valores = {
            chave: entrada.get().strip()
            for chave, entrada in entradas.items()
        }

        try:
            salvar(valores)
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Cadastro",
                "Já existe um registro com essa matrícula ou TAG.",
                parent=formulario,
            )
            return
        except (ValueError, sqlite3.Error) as erro:
            messagebox.showerror(
                "Erro no cadastro",
                str(erro),
                parent=formulario,
            )
            return

        messagebox.showinfo(
            "Cadastro",
            "Registro salvo com sucesso!",
            parent=formulario,
        )
        formulario.destroy()

    ttk.Button(
        quadro,
        text="Salvar cadastro",
        command=confirmar,
    ).grid(row=len(campos), column=0, columnspan=2, pady=20)

    quadro.columnconfigure(1, weight=1)


def cadastrar_tecnico():
    def salvar(valores):
        banco = BancoDados(BANCO)

        if banco.buscar_tecnico(valores["matricula"]) is not None:
            raise ValueError(
                "Já existe um técnico com essa matrícula."
            )

        tecnico = Tecnico(
            nome_tecnico=valores["nome_tecnico"],
            matricula=valores["matricula"],
            email=valores["email"],
            setor=valores["setor"],
        )

        banco.salvar_tecnico(tecnico)

    abrir_formulario_cadastro(
        "Cadastrar técnico",
        [
            ("nome_tecnico", "Nome:"),
            ("matricula", "Matrícula:"),
            ("email", "E-mail:"),
            ("setor", "Setor:"),
        ],
        salvar,
    )


def cadastrar_equipamento():
    def salvar(valores):
        banco = BancoDados(BANCO)

        if banco.buscar_equipamento(valores["codigo_tag"]) is not None:
            raise ValueError(
                "Já existe um equipamento com essa TAG."
            )

        equipamento = Equipamento(
            codigo_tag=valores["codigo_tag"],
            nome_equipamento=valores["nome_equipamento"],
            fabricante=valores["fabricante"],
            modelo=valores["modelo"],
        )

        banco.salvar_equipamento(equipamento)

    abrir_formulario_cadastro(
        "Cadastrar equipamento",
        [
            ("codigo_tag", "Código TAG:"),
            ("nome_equipamento", "Equipamento:"),
            ("fabricante", "Fabricante:"),
            ("modelo", "Modelo:"),
        ],
        salvar,
    )

def importar_medicoes_interface():

    # Consultar os cadastros existentes
    try:
        if not BANCO.is_file():
            raise FileNotFoundError(
                "Banco SQLite não encontrado."
            )

        endereco = BANCO.resolve().as_uri() + "?mode=ro"
        conexao = sqlite3.connect(endereco, uri=True)

        try:
            tecnicos = conexao.execute("""
                SELECT id_tecnico, nome_tecnico, matricula
                FROM tecnico
                ORDER BY nome_tecnico
            """).fetchall()

            equipamentos = conexao.execute("""
                SELECT id_equipamento, codigo_tag,
                       nome_equipamento
                FROM equipamento
                ORDER BY codigo_tag
            """).fetchall()

        finally:
            conexao.close()

        if not tecnicos:
            raise ValueError(
                "Cadastre um técnico antes de importar."
            )

        if not equipamentos:
            raise ValueError(
                "Cadastre um equipamento antes de importar."
            )

    except Exception as erro:
        messagebox.showerror("Importação", str(erro))
        return

    formulario = tk.Toplevel()
    formulario.title("Importar calibração")
    formulario.geometry("680x390")
    formulario.resizable(False, False)
    formulario.grab_set()

    quadro = ttk.Frame(formulario, padding=20)
    quadro.pack(fill="both", expand=True)

    ttk.Label(
        quadro,
        text="Importação de calibração para o SQLite",
        font=("Arial", 12, "bold"),
    ).pack(pady=(0, 15))

    caminho_excel = tk.StringVar()

    ttk.Label(
        quadro,
        text="Planilha Excel:",
    ).pack()

    ttk.Entry(
        quadro,
        textvariable=caminho_excel,
        width=75,
        state="readonly",
    ).pack(pady=5)

    def selecionar_excel():
        caminho = filedialog.askopenfilename(
            parent=formulario,
            title="Selecionar planilha",
            filetypes=[("Excel", "*.xlsx")],
            initialdir=str(PASTA_PROJETO),
        )

        if caminho:
            caminho_excel.set(caminho)

    ttk.Button(
        quadro,
        text="Selecionar planilha Excel",
        command=selecionar_excel,
    ).pack(pady=5)

    # Lista suspensa de técnicos
    ttk.Label(
        quadro,
        text="Técnico responsável:",
    ).pack(pady=(10, 0))

    escolha_tecnico = ttk.Combobox(
        quadro,
        values=[
            f"{nome} | Matrícula: {matricula}"
            for _, nome, matricula in tecnicos
        ],
        state="readonly",
        width=75,
    )

    escolha_tecnico.pack(pady=5)
    escolha_tecnico.current(0)

    # Lista suspensa de equipamentos
    ttk.Label(
        quadro,
        text="Equipamento:",
    ).pack(pady=(10, 0))

    escolha_equipamento = ttk.Combobox(
        quadro,
        values=[
            f"{tag} | {nome}"
            for _, tag, nome in equipamentos
        ],
        state="readonly",
        width=75,
    )

    escolha_equipamento.pack(pady=5)
    escolha_equipamento.current(0)

    def confirmar_importacao():

        try:
            caminho = Path(caminho_excel.get().strip())

            if not caminho.is_file():
                raise ValueError(
                    "Selecione uma planilha Excel válida."
                )

            indice_tecnico = escolha_tecnico.current()
            indice_equipamento = escolha_equipamento.current()

            if indice_tecnico < 0 or indice_equipamento < 0:
                raise ValueError(
                    "Selecione o técnico e o equipamento."
                )

            # Recuperar automaticamente os IDs
            tecnico_id = tecnicos[indice_tecnico][0]
            equipamento_id = equipamentos[
                indice_equipamento
            ][0]

            # Importar as medições
            registros = importar_registro(caminho)

            if not registros:
                raise ValueError(
                    "Nenhuma medição encontrada na aba Registro."
                )

            medicoes = []

            for registro in registros:

                parametro = str(
                    registro["dimension"] or ""
                ).strip()

                if not parametro:
                    raise ValueError(
                        "Parâmetro de medição vazio."
                    )

                nominal = float(registro["nominal"])

                tolerancia_negativa = float(
                    registro["tolerancia_negativa"]
                )

                tolerancia_positiva = float(
                    registro["tolerancia_positiva"]
                )

                leitura_1 = float(registro["medicao_1"])
                leitura_2 = float(registro["medicao_2"])

                valores = (
                    nominal,
                    tolerancia_negativa,
                    tolerancia_positiva,
                    leitura_1,
                    leitura_2,
                )

                if not all(isfinite(v) for v in valores):
                    raise ValueError(
                        f"Valor numérico inválido: {parametro}"
                    )

                limite_inferior = (
                    nominal + tolerancia_negativa
                )

                limite_superior = (
                    nominal + tolerancia_positiva
                )

                valor_obtido = mean([
                    leitura_1,
                    leitura_2,
                ])

                desvio_padrao = stdev([
                    leitura_1,
                    leitura_2,
                ])

                resultado = classificar_medicao(
                    valor_obtido,
                    limite_inferior,
                    limite_superior,
                )

                medicoes.append((
                    equipamento_id,
                    tecnico_id,
                    parametro,
                    nominal,
                    limite_inferior,
                    limite_superior,
                    valor_obtido,
                    resultado,
                    leitura_1,
                    leitura_2,
                    desvio_padrao,
                ))

            # Calcular a incerteza da calibração
            incerteza = calcular_incerteza_certificado(
                caminho,
                registros=registros,
            )

            # Preservar os parâmetros utilizados
            parametros_json = json.dumps(
                {
                    "quantidade_medicoes": (
                        incerteza["quantidade_medicoes"]
                    ),
                    "incerteza_dispersao": (
                        incerteza["incerteza_dispersao"]
                    ),
                    "parametros": (
                        incerteza["parametros_incerteza"]
                    ),
                    "componentes": (
                        incerteza["componentes"]
                    ),
                },
                ensure_ascii=False,
                allow_nan=False,
            )

            padroes_json = json.dumps(
                incerteza["padroes_utilizados"],
                ensure_ascii=False,
                allow_nan=False,
            )

            procedimento = incerteza["procedimento"]

            aprovadas = sum(
                m[7] == "APROVADO"
                for m in medicoes
            )

            reprovadas = len(medicoes) - aprovadas

            valor_u = incerteza["incerteza_expandida"]
            valor_k = incerteza["fator_abrangencia"]

            if not messagebox.askyesno(
                "Confirmar calibração",
                f"Medições: {len(medicoes)}\n"
                f"Aprovadas: {aprovadas}\n"
                f"Reprovadas: {reprovadas}\n\n"
                f"Incerteza expandida: {valor_u:.6f} µm\n"
                f"Fator de abrangência: {valor_k:.2f}\n\n"
                "Deseja gravar a calibração no SQLite?",
                parent=formulario,
            ):
                return

            if not BANCO.is_file():
                raise FileNotFoundError(
                    "Banco SQLite não encontrado."
                )

            conexao = sqlite3.connect(BANCO)

            try:
                conexao.execute("PRAGMA foreign_keys = ON")
                conexao.execute("BEGIN IMMEDIATE")

                data_calibracao = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                # Gravar os dados gerais da calibração
                cursor = conexao.execute("""
                    INSERT INTO calibracao (
                        id_tecnico,
                        id_equipamento,
                        data_calibracao,
                        maior_desvio_padrao,
                        incerteza_combinada,
                        graus_liberdade_efetivos,
                        fator_abrangencia,
                        incerteza_expandida,
                        unidade,
                        parametros_incerteza_json,
                        padroes_utilizados_json,
                        procedimento,
                        arquivo_origem
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?
                    )
                """, (
                    tecnico_id,
                    equipamento_id,
                    data_calibracao,
                    incerteza["maior_desvio_padrao"],
                    incerteza["incerteza_combinada"],
                    incerteza["graus_liberdade_efetivos"],
                    incerteza["fator_abrangencia"],
                    incerteza["incerteza_expandida"],
                    incerteza["unidade"],
                    parametros_json,
                    padroes_json,
                    procedimento,
                    caminho.name,
                ))

                id_calibracao = cursor.lastrowid

                # Gravar as medições vinculadas
                conexao.executemany("""
                    INSERT INTO medicao (
                        id_equipamento,
                        id_tecnico,
                        parametro_medido,
                        valor_nominal,
                        tolerancia_min,
                        tolerancia_max,
                        valor_obtido,
                        status_resultado,
                        medicao_1,
                        medicao_2,
                        desvio_padrao,
                        data_medicao,
                        id_calibracao
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?
                    )
                """, [
                    (
                        *medicao,
                        data_calibracao,
                        id_calibracao,
                    )
                    for medicao in medicoes
                ])

                conexao.commit()

            except Exception:
                conexao.rollback()
                raise

            finally:
                conexao.close()

            status.set(
                f"Calibração {id_calibracao} registrada: "
                f"{len(medicoes)} medições."
            )

            messagebox.showinfo(
                "Importação concluída",
                f"Calibração nº {id_calibracao}\n\n"
                f"Medições gravadas: {len(medicoes)}\n"
                f"Aprovadas: {aprovadas}\n"
                f"Reprovadas: {reprovadas}\n\n"
                f"Incerteza: {valor_u:.6f} µm\n"
                f"Fator k: {valor_k:.2f}",
                parent=formulario,
            )

            formulario.destroy()

        except Exception as erro:
            messagebox.showerror(
                "Erro na importação",
                str(erro),
                parent=formulario,
            )

    ttk.Button(
        quadro,
        text="Importar e gravar calibração",
        command=confirmar_importacao,
    ).pack(pady=15)

def main():
    global status

    janela = tk.Tk()
    janela.title("Schulz - Sistema de Calibração")
    janela.geometry("560x450")
    janela.resizable(False, False)

    quadro = ttk.Frame(janela, padding=25)
    quadro.pack(fill="both", expand=True)

    ttk.Label(
        quadro,
        text="SCHULZ - SISTEMA DE CALIBRAÇÃO",
        font=("Arial", 15, "bold"),
    ).pack(pady=(10, 12))

    ttk.Label(
        quadro,
        text="Sistema de Calibração de Dispositivos",
        font=("Arial", 10),
    ).pack(pady=(0, 20))

    ttk.Button(
        quadro,
        text="Cadastrar técnico",
        command=cadastrar_tecnico,
    ).pack(fill="x", pady=5)

    ttk.Button(
        quadro,
        text="Cadastrar equipamento",
        command=cadastrar_equipamento,
    ).pack(fill="x", pady=5)

    ttk.Button(
        quadro,
        text="Importar medições do Excel",
        command=importar_medicoes_interface,
    ).pack(fill="x", pady=5)

    ttk.Button(
        quadro,
        text="Gerar certificado PDF",
        command=gerar_pdf,
    ).pack(fill="x", pady=5)

    status = tk.StringVar(
        value="Pronto para gerar o certificado."
    )

    ttk.Label(
        quadro,
        textvariable=status,
        wraplength=480,
    ).pack(pady=25)

    ttk.Label(
        quadro,
        text="A emissão oficial requer validação metrológica.",
        font=("Arial", 9),
    ).pack(side="bottom")

    janela.mainloop()


if __name__ == "__main__":
    main()
