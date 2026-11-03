
from dataclasses import dataclass
from typing import Optional


@dataclass
class Tecnico:
    nome_tecnico: str
    matricula: str
    email: str
    setor: str
    id_tecnico: Optional[int] = None

    def validar(self) -> None:
        if not self.nome_tecnico.strip():
            raise ValueError("O nome do técnico é obrigatório.")

        if not self.matricula.strip():
            raise ValueError("A matrícula é obrigatória.")

        if not self.email.strip():
            raise ValueError("O e-mail é obrigatório.")

        if not self.setor.strip():
            raise ValueError("O setor é obrigatório.")
