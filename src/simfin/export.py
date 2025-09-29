# src/simfin/export.py
from __future__ import annotations
from decimal import Decimal
import csv
from typing import List, Dict

def exportar_csv(parcelas: List[Dict[str, Decimal]], path: str) -> None:
    campos = ["mes", "parcela", "juros", "amortizacao", "saldo_devedor"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for linha in parcelas:
            w.writerow({k: (str(v) if not isinstance(v, (int, str)) else v) for k, v in linha.items()})
