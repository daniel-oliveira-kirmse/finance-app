from dataclasses import dataclass


@dataclass
class Transaction:
    id: int | None
    user_id: int
    tipo: str
    valor: float
    categoria: str
    data: str