from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import List, Dict, Optional

from .models import Resultado, EntradaPrazo, EntradaValor
from .indices import taxa_mensal, aplicar_tr_e_ipca

Q = Decimal("0.01")

def _quant(v: Decimal) -> Decimal:
    return v.quantize(Q, rounding=ROUND_HALF_UP)

def simular_sac_por_prazo(e: EntradaPrazo) -> Resultado:
    getcontext().prec = 28

    valor_financiado = e.valor_imovel - e.entrada
    if e.prazo <= 0 or e.prazo > e.prazo_oficial:
        raise ValueError("Prazo inválido: deve ser entre 1 e prazo_oficial.")

    juros_m = taxa_mensal(e.juros_anual)
    amortizacao = (valor_financiado / Decimal(e.prazo))

    saldo = valor_financiado
    parcelas: List[Dict[str, Decimal]] = []

    for mes in range(1, e.prazo + 1):
        saldo_corrigido = aplicar_tr_e_ipca(saldo, e.tr_anual, e.ipca_anual)
        juros = saldo_corrigido * juros_m
        # Ajuste final para não deixar saldo negativo
        amort = amortizacao if saldo_corrigido > amortizacao else saldo_corrigido
        parcela = amort + juros + e.encargos_fixos_mensais
        novo_saldo = saldo_corrigido - amort

        parcelas.append({
            "mes": Decimal(mes),
            "parcela": _quant(parcela),
            "juros": _quant(juros),
            "amortizacao": _quant(amort),
            "saldo_devedor": _quant(novo_saldo),
        })

        saldo = novo_saldo

    total_pago = sum(p["parcela"] for p in parcelas)

    return Resultado(
        valor_total_pago=_quant(total_pago),
        primeira_parcela=parcelas[0]["parcela"],
        ultima_parcela=parcelas[-1]["parcela"],
        prazo_utilizado=e.prazo,
        parcelas_detalhadas=parcelas,
    )

def simular_sac_por_valor(e: EntradaValor) -> Resultado:
    # Busca linear simples pelo maior prazo cujo total <= valor_maximo.
    # Alternativamente, poderíamos usar bisseção. Mantemos simples e previsível.
    melhor: Optional[Resultado] = None
    for prazo in range(6, e.prazo_oficial + 1):
        r = simular_sac_por_prazo(EntradaPrazo(
            valor_imovel=e.valor_imovel,
            entrada=e.entrada,
            juros_anual=e.juros_anual,
            tr_anual=e.tr_anual,
            ipca_anual=e.ipca_anual,
            encargos_fixos_mensais=e.encargos_fixos_mensais,
            prazo=prazo,
            prazo_oficial=e.prazo_oficial,
        ))
        if r.valor_total_pago <= e.valor_maximo:
            melhor = r
    # Se não encontrou nenhum prazo viável, retorna o cenário mínimo (6 meses)
    if melhor is None:
        melhor = simular_sac_por_prazo(EntradaPrazo(
            valor_imovel=e.valor_imovel,
            entrada=e.entrada,
            juros_anual=e.juros_anual,
            tr_anual=e.tr_anual,
            ipca_anual=e.ipca_anual,
            encargos_fixos_mensais=e.encargos_fixos_mensais,
            prazo=6,
            prazo_oficial=e.prazo_oficial,
        ))
    return melhor
