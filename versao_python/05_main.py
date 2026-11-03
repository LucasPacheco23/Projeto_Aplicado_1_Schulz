
import sqlite3

from classes import BancoDados, Tecnico, Equipamento, Medicao


# Identificadores exclusivos para os registros de demonstração.
MATRICULA_TESTE = "TESTE-AV03-001"
TAG_TESTE = "TESTE-AV03-001"
PARAMETRO_TESTE = "Parâmetro demonstrativo AV03"


def obter_tecnico_teste(banco: BancoDados) -> Tecnico:
    registro = banco.buscar_tecnico(MATRICULA_TESTE)

    if registro is not None:
        print("Técnico de demonstração já cadastrado.")

        return Tecnico(
            nome_tecnico=registro["nome_tecnico"],
            matricula=registro["matricula"],
            email=registro["email"],
            setor=registro["setor"],
            id_tecnico=registro["id_tecnico"],
        )

    tecnico = Tecnico(
        nome_tecnico="Técnico de Demonstração AV03",
        matricula=MATRICULA_TESTE,
        email="teste.av03@example.com",
        setor="Metrologia",
    )

    banco.salvar_tecnico(tecnico)
    print("Técnico de demonstração cadastrado.")

    return tecnico


def obter_equipamento_teste(banco: BancoDados) -> Equipamento:
    registro = banco.buscar_equipamento(TAG_TESTE)

    if registro is not None:
        print("Equipamento de demonstração já cadastrado.")

        return Equipamento(
            codigo_tag=registro["codigo_tag"],
            nome_equipamento=registro["nome_equipamento"],
            fabricante=registro["fabricante"],
            modelo=registro["modelo"],
            id_equipamento=registro["id_equipamento"],
        )

    equipamento = Equipamento(
        codigo_tag=TAG_TESTE,
        nome_equipamento="Equipamento de Demonstração",
        fabricante="Fabricante de Teste",
        modelo="Modelo de Teste",
    )

    banco.salvar_equipamento(equipamento)
    print("Equipamento de demonstração cadastrado.")

    return equipamento


def registrar_medicao_teste(
    banco: BancoDados,
    tecnico: Tecnico,
    equipamento: Equipamento,
) -> None:
    medicoes = banco.listar_medicoes()

    # Evita inserir novamente a medição de demonstração.
    for registro in medicoes:
        if (
            registro["codigo_tag"] == TAG_TESTE
            and registro["parametro_medido"] == PARAMETRO_TESTE
        ):
            print("Medição de demonstração já registrada.")
            return

    medicao = Medicao(
        id_equipamento=equipamento.id_equipamento,
        id_tecnico=tecnico.id_tecnico,
        parametro_medido=PARAMETRO_TESTE,
        valor_nominal=10.00,
        tolerancia_min=9.90,
        tolerancia_max=10.10,
        medida_1=10.02,
        medida_2=10.04,
    )

    banco.salvar_medicao(medicao)

    print("Medição de demonstração registrada.")
    print(f"Média calculada: {medicao.media:.4f}")
    print(f"Desvio padrão: {medicao.desvio_padrao:.6f}")
    print(f"Resultado: {medicao.status_resultado}")


def exibir_relatorio(banco: BancoDados) -> None:
    medicoes = banco.listar_medicoes()

    print("\n" + "=" * 90)
    print("RELATÓRIO DE MEDIÇÕES E CALIBRAÇÃO")
    print("=" * 90)

    if not medicoes:
        print("Nenhuma medição cadastrada.")
        return

    for registro in medicoes:
        print(f"\nID da medição: {registro['id_medicao']}")
        print(f"Equipamento: {registro['nome_equipamento']}")
        print(f"TAG: {registro['codigo_tag']}")
        print(f"Técnico: {registro['nome_tecnico']}")
        print(f"Parâmetro: {registro['parametro_medido']}")
        print(f"Valor nominal: {registro['valor_nominal']:.4f}")
        print(
            f"Faixa aceitável: "
            f"{registro['tolerancia_min']:.4f} a "
            f"{registro['tolerancia_max']:.4f}"
        )
        print(f"Valor obtido (média): {registro['valor_obtido']:.4f}")
        print(f"Resultado: {registro['status_resultado']}")
        print(f"Data: {registro['data_medicao']}")
        print("-" * 90)


def main() -> None:
    print("MVP DE CALIBRAÇÃO - AV03")

    try:
        banco = BancoDados()

        tecnico = obter_tecnico_teste(banco)
        equipamento = obter_equipamento_teste(banco)

        registrar_medicao_teste(
            banco,
            tecnico,
            equipamento,
        )

        exibir_relatorio(banco)

    except ValueError as erro:
        print(f"Erro de validação: {erro}")

    except sqlite3.IntegrityError as erro:
        print(f"Erro de integridade do banco: {erro}")

    except sqlite3.Error as erro:
        print(f"Erro ao acessar o SQLite: {erro}")

    except OSError as erro:
        print(f"Erro de acesso a arquivo: {erro}")


if __name__ == "__main__":
    main()
