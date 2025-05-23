from simulador.models import FinanciamentoSimulacaoEntrada

# Armazena os últimos valores informados
valores_anteriores = {}

def pedir_input(nome, tipo=float, obrigatorio=True, sufixo="") -> float:
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

    dados = FinanciamentoSimulacaoEntrada(
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

    print("\n--- Revisar Simulação ---")
    for campo, valor in dados.__dict__.items():
        print(f"{campo.replace('_', ' ').capitalize()}: {valor}")

    confirmar = input("\nConfirmar? (s/n): ").strip().lower()
    if confirmar == "s":
        return dados
    else:
        print("\n🌀 Reiniciando entrada de dados...\n")
        return exibir_menu()  # reinicia o processo
