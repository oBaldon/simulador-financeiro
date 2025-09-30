from decimal import Decimal
from simfin.consorcio import ConsorcioInput, simular_consorcio

def test_consorcio_basico_sem_correcao_sem_taxas():
    ci = ConsorcioInput(
        administradora="X", grupo="G", cota="1",
        carta_credito_inicial=Decimal('100000'), prazo_total_meses=10,
        correcao_modo="anual_constante", correcao_anual=Decimal('0.0'),
        taxa_adm_total_pct=Decimal('0.0'), fundo_reserva_pct=Decimal('0.0'),
        seguro_mensal_valor=Decimal('0.0'),
        taxa_adesao_valor=Decimal('0.0'), taxas_contemplacao_valor=Decimal('0.0'),
        parcela_reduzida=False, parcela_reduzida_pct=Decimal('100'),
        parcela_reduzida_meses=0, mes_contemplacao_alvo=3,
    )
    r = simular_consorcio(ci)
    assert r.parcelas[0]["parcela"] == Decimal('10000.00')
    assert r.parcelas[-1]["parcela"] == Decimal('10000.00')
    assert r.total_pago == Decimal('100000.00')
