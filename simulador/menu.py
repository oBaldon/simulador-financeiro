from simulador.models import FinanciamentoSimulacaoEntrada

# Armazena os últimos valores informados durante a execução
valores_anteriores = {}

def pedir_input(nome, tipo=float, obrigatorio=True, sufixo="") -> float:
    """
    Solicita entrada do usuário, mantendo o valor anterior se não for informado.
    Converte o valor para o tipo especificado.
    """
    atual = valores_anteriores.get(nome)
    label = f"{nome.replace('_', ' ').capitalize()}"

    if atual is not None:
        entrada = input(f"{label} [atual: {atual}{sufixo}]: ").strip()
    else:
        entrada = input(f"{label}{sufixo}: ").strip()

    if entrada == "":
        if atual is not None:
            return atual
        elif not obrigatorio:
            return None
        else:
            raise ValueError(f"{label} é obrigatório.")
    
    valor = tipo(entrada.replace(",", "."))
    valores_anteriores[nome] = valor
    return valor


def exibir_menu() -> FinanciamentoSimulacaoEntrada:
    """
    Exibe um menu interativo para coleta de parâmetros da simulação.
    Retorna um objeto FinanciamentoSimulacaoEntrada com os dados preenchidos.
    """
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
