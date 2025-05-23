def corrigir_saldo_ipca(saldo_devedor: float, ipca_anual: float) -> float:
    """
    Aplica a correção mensal pela inflação (IPCA) sobre o saldo devedor.
    """
    if ipca_anual == 0:
        return saldo_devedor
    ipca_mensal = (1 + ipca_anual) ** (1 / 12) - 1
    return saldo_devedor * (1 + ipca_mensal)
