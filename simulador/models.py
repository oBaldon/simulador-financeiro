from dataclasses import dataclass
from typing import List, Dict

@dataclass
class FinanciamentoSimulacaoEntrada:
    # Tipo de simulação: 'prazo' ou 'valor'
    tipo_simulacao: str

    # Informações principais do imóvel e entrada
    valor_imovel: float
    entrada: float

    # Valores informativos da simulação da Caixa
    parcela_inicial: float
    parcela_final: float
    prazo_oficial: int

    # Juros contratuais (ex: 0.0766 para 7,66% ao ano)
    juros_anual: float

    # Parâmetro da simulação:
    # → se tipo='prazo', é o número de meses
    # → se tipo='valor', é o valor total máximo a pagar
    parametro: float

    # Indexadores e encargos adicionais
    tr_anual: float = 0.0
    ipca_anual: float = 0.0
    encargos_fixos_mensais: float = 0.0

    
@dataclass
class FinanciamentoResultado:
    valor_total_pago: float
    primeira_parcela: float
    ultima_parcela: float
    prazo_utilizado: int
    parcelas_detalhadas: List[Dict] = None 

@dataclass
class FinanciamentoResultado:
    valor_total_pago: float
    primeira_parcela: float
    ultima_parcela: float
    prazo_utilizado: int
    parcelas_detalhadas: List[Dict] = None  # ← nova lista com info mês a mês
