from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict, Optional

@dataclass
class EntradaComum:
    valor_imovel: Decimal
    entrada: Decimal
    juros_anual: Decimal            # 0.0847 = 8.47% (ou em % se sinalizado na CLI)
    tr_anual: Decimal               # 0.0 a 0.02 por ex.
    ipca_anual: Decimal             # 0.0 a 0.06 por ex.
    encargos_fixos_mensais: Decimal # taxas/seguros

@dataclass
class EntradaPrazo(EntradaComum):
    prazo: int
    prazo_oficial: int

@dataclass
class EntradaValor(EntradaComum):
    valor_maximo: Decimal
    prazo_oficial: int

@dataclass
class Resultado:
    valor_total_pago: Decimal
    primeira_parcela: Decimal
    ultima_parcela: Decimal
    prazo_utilizado: int
    parcelas_detalhadas: List[Dict[str, Decimal]]
