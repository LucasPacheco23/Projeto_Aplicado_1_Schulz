#Arquivo agregador das classes exigidas na AV03.
# As implementações foram separadas em módulos para manter a organização,
# o encapsulamento e a separação de responsabilidades.

from classes import BancoDados, Tecnico, Equipamento, Medicao

__all__ = ["BancoDados", "Tecnico", "Equipamento", "Medicao"]

if __name__ == "__main__":
    print("Classes disponíveis para MVP:")
    print("- BancoDados")
    print("- Tecnico")
    print("- Equipamento")
    print("- Medicao")
