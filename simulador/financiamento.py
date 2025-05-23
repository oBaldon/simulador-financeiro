from simulador.models import FinanciamentoSimulacaoEntrada, FinanciamentoResultado
from simulador.tr import aplicar_tr_anual
from simulador.ipca import corrigir_saldo_ipca
from simulador.helpers import converter_juros_anual_para_mensal

def simular_por_prazo(dados: FinanciamentoSimulacaoEntrada) -> FinanciamentoResultado:
    """
    Simula um financiamento usando o sistema SAC para um prazo específico (em meses).
    Aplica TR, IPCA e encargos mensais fixos conforme informado.
    Retorna o total pago, primeira e última parcela, e o prazo utilizado.
    """
    # Cálculo do valor financiado
    valor_financiado = dados.valor_imovel - dados.entrada

    # Novo prazo desejado (menor que o oficial)
    novo_prazo = int(dados.parametro)

    # Calcular taxa efetiva mensal apenas com juros contratuais (sem CET ou CESH)
    juros_mensal = converter_juros_anual_para_mensal(dados.juros_anual)

    # Amortização constante
    amortizacao_mensal = valor_financiado / novo_prazo

    saldo_devedor = valor_financiado
    total_pago = 0.0
    primeira_parcela = 0.0
    ultima_parcela = 0.0
    parcelas_detalhadas = []

    for mes in range(1, novo_prazo + 1):
        # Corrigir saldo com TR e IPCA antes de calcular juros
        saldo_corrigido = aplicar_tr_anual(saldo_devedor, dados.tr_anual)
        saldo_corrigido = corrigir_saldo_ipca(saldo_corrigido, dados.ipca_anual)

        juros_mes = saldo_corrigido * juros_mensal
        parcela = amortizacao_mensal + juros_mes
        parcela += dados.encargos_fixos_mensais
        saldo_devedor -= amortizacao_mensal
        total_pago += parcela

        parcelas_detalhadas.append({
            "mes": mes,
            "parcela": round(parcela, 2),
            "juros": round(juros_mes, 2),
            "amortizacao": round(amortizacao_mensal, 2),
            "saldo_devedor": round(saldo_devedor, 2)
        })

        if mes == 1:
            primeira_parcela = parcela
        if mes == novo_prazo:
            ultima_parcela = parcela


    return FinanciamentoResultado(
        valor_total_pago=round(total_pago, 2),
        primeira_parcela=round(primeira_parcela, 2),
        ultima_parcela=round(ultima_parcela, 2),
        prazo_utilizado=novo_prazo,
        parcelas_detalhadas=parcelas_detalhadas
    )


def simular_por_valor(dados: FinanciamentoSimulacaoEntrada) -> FinanciamentoResultado:
    """
    Busca o maior prazo possível no qual o valor total pago seja menor ou igual ao parâmetro informado.
    Internamente utiliza a função simular_por_prazo.
    """

    valor_desejado = dados.parametro
    if valor_desejado <= 0:
        raise ValueError("O valor máximo a pagar deve ser maior que zero.")
    
    melhor_resultado = None

    for prazo in range(12, dados.prazo_oficial + 1):  # do menor para o maior
        tentativa = FinanciamentoSimulacaoEntrada(
            tipo_simulacao="prazo",
            valor_imovel=dados.valor_imovel,
            entrada=dados.entrada,
            parcela_inicial=dados.parcela_inicial,
            parcela_final=dados.parcela_final,
            prazo_oficial=dados.prazo_oficial,
            juros_anual=dados.juros_anual,
            parametro=prazo,
            tr_anual=dados.tr_anual,
            ipca_anual=dados.ipca_anual,
            encargos_fixos_mensais=dados.encargos_fixos_mensais
        )

        resultado = simular_por_prazo(tentativa)

        if resultado.valor_total_pago <= valor_desejado:
            melhor_resultado = resultado  # guarda o melhor até agora (maior prazo possível)

    return melhor_resultado or simular_por_prazo(dados)

