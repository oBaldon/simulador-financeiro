from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import List, Dict, Optional

getcontext().prec = 28
Q = Decimal("0.01")

def _q2(v: Decimal) -> Decimal:
    return v.quantize(Q, rounding=ROUND_HALF_UP)

def _taxa_mensal_equivalente(taxa_anual: Decimal) -> Decimal:
    if taxa_anual == 0:
        return Decimal(0)
    return (Decimal(1) + taxa_anual) ** (Decimal(1) / Decimal(12)) - Decimal(1)

@dataclass
class Lance:
    tipo: str = "livre"          # "livre" | "embutido" (por ora usamos "livre")
    percent_carta: Decimal = Decimal(0)  # 25.0 => 25%
    fonte: str = "proprio"       # "proprio" | "embutido"

@dataclass
class Hipoteses:
    aluguel_mensal_enquanto_espera: Decimal = Decimal(0)
    taxa_desconto_anual: Decimal = Decimal(0)
    crescimento_preco_imovel_anual: Decimal = Decimal(0)

@dataclass
class ConsorcioInput:
    administradora: str
    grupo: str
    cota: str
    carta_credito_inicial: Decimal
    prazo_total_meses: int

    indice_correcao: str = "INCC"        # informativo
    correcao_modo: str = "anual_constante"  # "anual_constante" | "serie_mensal"
    correcao_anual: Decimal = Decimal(0)
    correcao_serie_mensal: Optional[List[Decimal]] = None  # taxas mensais (0.004, 0.003, ...)

    taxa_adm_total_pct: Decimal = Decimal(16)   # % sobre a carta (total no grupo)
    taxa_adm_forma: str = "diluida"            # simplificação: diluída

    fundo_reserva_pct: Decimal = Decimal(0)     # % sobre a carta (pode ser devolvido)
    seguro_mensal_valor: Decimal = Decimal(0)

    taxa_adesao_valor: Decimal = Decimal(0)
    taxas_contemplacao_valor: Decimal = Decimal(0)

    parcela_reduzida: bool = False
    parcela_reduzida_pct: Decimal = Decimal(100)    # ex.: 70 => paga 70% da base
    parcela_reduzida_meses: int = 0

    lance: Lance = field(default_factory=Lance)

    mes_contemplacao_alvo: int = 12
    hipoteses: Hipoteses = field(default_factory=Hipoteses)

@dataclass
class ConsorcioResultado:
    parcelas: List[Dict[str, Decimal]]
    total_pago: Decimal
    total_pago_liquido: Decimal  # descontando devolução do FR no fim (se houver)
    mes_contemplacao: int

def _serie_correcao_mensal(ci: ConsorcioInput) -> List[Decimal]:
    if ci.correcao_modo == "serie_mensal" and ci.correcao_serie_mensal:
        return list(ci.correcao_serie_mensal)
    m = _taxa_mensal_equivalente(ci.correcao_anual)
    return [m] * ci.prazo_total_meses

def simular_consorcio(ci: ConsorcioInput) -> ConsorcioResultado:
    taxa_adm_total = (ci.taxa_adm_total_pct / Decimal(100)) * ci.carta_credito_inicial
    adm_mensal = taxa_adm_total / Decimal(ci.prazo_total_meses)

    fr_total = (ci.fundo_reserva_pct / Decimal(100)) * ci.carta_credito_inicial
    fr_mensal = fr_total / Decimal(ci.prazo_total_meses)

    base_mensal_inicial = ci.carta_credito_inicial / Decimal(ci.prazo_total_meses)
    series = _serie_correcao_mensal(ci)

    carta_atualizada = ci.carta_credito_inicial
    saldo_a_contribuir = ci.carta_credito_inicial
    parcelas: List[Dict[str, Decimal]] = []

    reducao_base_por_lance = Decimal(0)
    mes_contemplacao_real = min(max(1, ci.mes_contemplacao_alvo), ci.prazo_total_meses)

    for mes in range(1, ci.prazo_total_meses + 1):
        idx = series[mes-1] if mes-1 < len(series) else series[-1]
        fator = (Decimal(1) + idx)
        carta_atualizada = carta_atualizada * fator

        base_mensal = base_mensal_inicial * fator

        if ci.parcela_reduzida and mes <= ci.parcela_reduzida_meses:
            base_mensal *= (ci.parcela_reduzida_pct / Decimal(100))

        if reducao_base_por_lance > 0 and mes > mes_contemplacao_real:
            base_mensal = max(Decimal(0), base_mensal - reducao_base_por_lance)

        taxa_adm_do_mes = adm_mensal
        fr_do_mes = fr_mensal
        seguro = ci.seguro_mensal_valor

        taxas_pontuais = Decimal(0)
        if mes == 1 and ci.taxa_adesao_valor:
            taxas_pontuais += ci.taxa_adesao_valor
        if mes == mes_contemplacao_real and ci.taxas_contemplacao_valor:
            taxas_pontuais += ci.taxas_contemplacao_valor

        aluguel = Decimal(0)
        if mes < mes_contemplacao_real and ci.hipoteses.aluguel_mensal_enquanto_espera:
            aluguel = ci.hipoteses.aluguel_mensal_enquanto_espera

        lance_mes = Decimal(0)
        if mes == mes_contemplacao_real and ci.lance and ci.lance.fonte == "proprio":
            lance_mes = (ci.lance.percent_carta / Decimal(100)) * carta_atualizada
            saldo_a_contribuir = max(Decimal(0), saldo_a_contribuir - lance_mes)
            meses_restantes = max(1, ci.prazo_total_meses - mes)
            reducao_base_por_lance = (lance_mes / Decimal(meses_restantes))

        contrib_base = min(base_mensal, saldo_a_contribuir)
        saldo_a_contribuir = max(Decimal(0), saldo_a_contribuir - contrib_base)

        parcela = contrib_base + taxa_adm_do_mes + fr_do_mes + seguro + taxas_pontuais + aluguel + lance_mes

        parcelas.append({
            "mes": Decimal(mes),
            "carta_atualizada": _q2(carta_atualizada),
            "contribuicao_base": _q2(contrib_base),
            "taxa_adm": _q2(taxa_adm_do_mes),
            "fundo_reserva": _q2(fr_do_mes),
            "seguro": _q2(seguro),
            "taxas_pontuais": _q2(taxas_pontuais),
            "aluguel": _q2(aluguel),
            "lance": _q2(lance_mes),
            "parcela": _q2(parcela),
            "saldo_a_contribuir": _q2(saldo_a_contribuir),
        })

    total_pago = sum(p["parcela"] for p in parcelas)
    total_pago_liquido = total_pago - fr_total

    return ConsorcioResultado(
        parcelas=parcelas,
        total_pago=_q2(total_pago),
        total_pago_liquido=_q2(total_pago_liquido),
        mes_contemplacao=mes_contemplacao_real,
    )
