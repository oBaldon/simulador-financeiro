def exibir_menu() -> FinanciamentoSimulacaoEntrada:
    print("=== Simulador de Financiamento ===")
    
    tipo = input("Tipo de simulação ('prazo' ou 'valor'): ").strip().lower()
    if tipo not in ("prazo", "valor"):
        raise ValueError("Tipo inválido. Use 'prazo' ou 'valor'.")

    valor_imovel = pedir_input("valor_imovel")
    entrada = pedir_input("entrada")
    parcela_inicial = pedir_input("parcela_inicial")
    parcela_final = pedir_input("parcela_final")
    prazo_oficial = pedir_input("prazo_oficial", tipo=int)
    juros_anual = pedir_input("juros_anual (%)") / 100
    tr_anual = pedir_input("tr_anual (%)", obrigatorio=False) / 100
    ipca_anual = pedir_input("ipca_anual (%)", obrigatorio=False) / 100
    encargos_fixos_mensais = pedir_input("encargos_fixos_mensais", obrigatorio=False)

    if tipo == "prazo":
        parametro = pedir_input("prazo_simulado", tipo=int)
    else:
        parametro = pedir_input("valor_maximo_a_pagar")
        if parametro < valor_imovel - entrada:
            raise ValueError("O valor desejado está abaixo do valor financiado. Simulação impossível.")

    return FinanciamentoSimulacaoEntrada(
        tipo_simulacao=tipo,
        valor_imovel=valor_imovel,
        entrada=entrada,
        parcela_inicial=parcela_inicial,
        parcela_final=parcela_final,
        prazo_oficial=prazo_oficial,
        juros_anual=juros_anual,
        tr_anual=tr_anual,
        ipca_anual=ipca_anual,
        encargos_fixos_mensais=encargos_fixos_mensais,
        parametro=parametro
    )
