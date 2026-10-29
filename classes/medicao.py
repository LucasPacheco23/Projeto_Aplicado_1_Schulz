
from dataclasses import dataclass
from statistics import mean, stdev
from typing import Optional
import math


@dataclass
class Medicao:
    id_equipamento: int
    id_tecnico: int
    parametro_medido: str
    valor_nominal: float
    tolerancia_min: float
    tolerancia_max: float
    medida_1: float
    medida_2: float
    id_medicao: Optional[int] = None

    def validar(self) -> None:
        if not self.parametro_medido.strip():
            raise ValueError("O parâmetro medido é obrigatório.")

        valores = {
            "valor nominal": self.valor_nominal,
            "tolerância mínima": self.tolerancia_min,
            "tolerância máxima": self.tolerancia_max,
            "medida 1": self.medida_1,
            "medida 2": self.medida_2,
        }

        for nome, valor in valores.items():
            if isinstance(valor, bool) or not isinstance(
                valor, (int, float)
            ):
                raise ValueError(f"{nome} deve ser numérico.")

            if not math.isfinite(valor):
                raise ValueError(f"{nome} contém um valor inválido.")

        if self.tolerancia_min > self.tolerancia_max:
            raise ValueError(
                "A tolerância mínima não pode superar a máxima."
            )

        if self.id_equipamento <= 0 or self.id_tecnico <= 0:
            raise ValueError(
                "Os IDs do equipamento e do técnico devem ser válidos."
            )

    @property
    def media(self) -> float:
        return mean([self.medida_1, self.medida_2])

    @property
    def desvio_padrao(self) -> float:
        return stdev([self.medida_1, self.medida_2])

    @property
    def status_resultado(self) -> str:
        self.validar()

        if self.tolerancia_min <= self.media <= self.tolerancia_max:
            return "APROVADO"

        return "REPROVADO"
