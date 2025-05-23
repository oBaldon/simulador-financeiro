def aplicar_tr_anual(saldo_devedor: float, tr_anual: float) -> float:
    """
    Aplica a correção mensal pela TR sobre o saldo devedor.
    """
    if tr_anual == 0:
        return saldo_devedor
    tr_mensal = (1 + tr_anual) ** (1 / 12) - 1
    return saldo_devedor * (1 + tr_mensal)
