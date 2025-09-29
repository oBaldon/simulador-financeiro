from __future__ import annotations
from decimal import Decimal, getcontext

def taxa_mensal(taxa_anual: Decimal) -> Decimal:
    # (1 + a)^(1/12) - 1, usando Decimal
    getcontext().prec = 28
    return (Decimal(1) + taxa_anual) ** (Decimal(1) / Decimal(12)) - Decimal(1)

def aplicar_tr_e_ipca(saldo: Decimal, tr_anual: Decimal, ipca_anual: Decimal) -> Decimal:
    tr_m = taxa_mensal(tr_anual) if tr_anual != 0 else Decimal(0)
    ipca_m = taxa_mensal(ipca_anual) if ipca_anual != 0 else Decimal(0)
    return saldo * (Decimal(1) + tr_m) * (Decimal(1) + ipca_m)
