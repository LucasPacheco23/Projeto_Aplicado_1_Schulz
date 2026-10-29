
from dataclasses import dataclass
from typing import Optional


@dataclass
class Equipamento:
    codigo_tag: str
    nome_equipamento: str
    fabricante: str
    modelo: str
    id_equipamento: Optional[int] = None

    def validar(self) -> None:
        if not self.codigo_tag.strip():
            raise ValueError("O código TAG é obrigatório.")

        if not self.nome_equipamento.strip():
            raise ValueError("O nome do equipamento é obrigatório.")

        if not self.fabricante.strip():
            raise ValueError("O fabricante é obrigatório.")

        if not self.modelo.strip():
            raise ValueError("O modelo é obrigatório.")
