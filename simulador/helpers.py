def converter_juros_anual_para_mensal(juros_anual: float) -> float:
    """
    Converte taxa de juros anual para mensal de forma composta (exata).
    Ex: 8.47% a.a. -> (1 + 0.0847)^(1/12) - 1
    """
    return (1 + juros_anual) ** (1 / 12) - 1
