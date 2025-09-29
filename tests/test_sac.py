from decimal import Decimal
from simfin.models import EntradaPrazo
from simfin.sac import simular_sac_por_prazo

def test_basico_sem_indices():
    e = EntradaPrazo(
        valor_imovel=Decimal('250000'),
        entrada=Decimal('87500'),
        juros_anual=Decimal('0.0847'),
        tr_anual=Decimal('0.0'),
        ipca_anual=Decimal('0.0'),
        encargos_fixos_mensais=Decimal('120'),
        prazo=360,
        prazo_oficial=360,
    )
    r = simular_sac_por_prazo(e)
    # Sanity checks
    assert r.prazo_utilizado == 360
    assert r.parcelas_detalhadas[0]["parcela"] > 0
    assert r.primeira_parcela >= r.ultima_parcela
    assert len(r.parcelas_detalhadas) == 360
