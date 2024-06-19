
from decimal import Decimal
from typing import TypedDict


class TBancoTasa(TypedDict):
    BANCO: str
    COMPRA: Decimal
    VENTA: Decimal

class TDolarItem(TypedDict):
    fecha: str
    tasas: list[TBancoTasa]