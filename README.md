# Simfin — Simulador de Financiamento (SAC) refatorado

Refatoração do seu simulador antigo, agora como pacote Python moderno, tipado e com **CLI**:

- Cálculo **SAC** com **juros**, **TR** e **IPCA** (aplicados ao saldo).
- **Encargos** fixos mensais.
- **Exportação CSV** com o detalhamento mês a mês.
- **Comparação com Consórcio** (carta de crédito): cronograma próprio, total nominal, total **líquido pós-FR** e **VPL** com taxa de desconto.
- **Modo interativo** ou **parâmetros via CLI**.
- Matemática com `Decimal` para evitar erros de arredondamento.
- **Taxas aceitas em % ou fração** (ex.: `8.47` ou `0.0847`; para VPL: `10` ou `0.10`).

---

## Instalação local (modo dev)

```bash
cd simfin-refatorado
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
````

> Se o comando `simfin` não aparecer no PATH, use: `python -m simfin.cli …`

---

## Uso rápido

### Interativo (financiamento)

```bash
simfin --interactive
```

> Observação: a comparação com **consórcio** está disponível no modo por flags (exemplos abaixo).

### Parametrizado (financiamento por prazo)

```bash
simfin --tipo prazo \
  --valor-imovel 250000 --entrada 87500 \
  --juros-anual 8.47 --juros-em-percent \
  --prazo 360 --encargos 120 \
  --tr-anual 0.0 --ipca-anual 0.0 \
  --csv parcelas.csv
```

### Parametrizado (por **valor máximo total**)

```bash
simfin --tipo valor \
  --valor-imovel 250000 --entrada 87500 \
  --juros-anual 8.47 --juros-em-percent \
  --valor-max 274238.30 \
  --prazo-oficial 360 --encargos 120
```

---

## Comparação com Consórcio

1. Crie um JSON com os dados do consórcio (ex.: `exemplo_consorcio.json`):

```json
{
  "administradora": "Exemplo Consórcios",
  "grupo": "1234",
  "cota": "56",
  "carta_credito_inicial": 250000,
  "prazo_total_meses": 180,

  "indice_correcao": "INCC",
  "correcao_modo": "anual_constante",
  "correcao_anual": 0.05,
  "correcao_serie_mensal": [],

  "taxa_adm_total_pct": 16.0,
  "taxa_adm_forma": "diluida",
  "fundo_reserva_pct": 2.0,
  "seguro_mensal_valor": 0.0,
  "taxa_adesao_valor": 0.0,
  "taxas_contemplacao_valor": 800.0,

  "parcela_reduzida": true,
  "parcela_reduzida_pct": 70.0,
  "parcela_reduzida_meses": 12,

  "lance": { "tipo": "livre", "percent_carta": 25.0, "fonte": "proprio" },
  "mes_contemplacao_alvo": 3,

  "hipoteses": {
    "aluguel_mensal_enquanto_espera": 1800.0,
    "taxa_desconto_anual": 0.10,
    "crescimento_preco_imovel_anual": 0.04
  }
}
```

2. Rode a simulação **+** comparação:

```bash
simfin --tipo prazo \
  --valor-imovel 250000 --entrada 87500 \
  --juros-anual 8.47 --juros-em-percent \
  --prazo 360 --encargos 120 \
  --consorcio-json exemplo_consorcio.json \
  --taxa-desconto-anual 10 \
  --csv parcelas_fin.csv \
  --csv-consorcio parcelas_cons.csv
```

* `--taxa-desconto-anual` aceita **10** (interpreta como 10%) **ou** **0.10** (fração).
* Saída no terminal: totais do financiamento e do consórcio (nominal e **líquido pós-FR**) e **VPL** de ambos (se taxa informada).

---

## Formatos de saída

### Financiamento (CSV)

Colunas:

```
mes, parcela, juros, amortizacao, saldo_devedor
```

### Consórcio (CSV)

Colunas:

```
mes, parcela, contribuicao_base, taxa_adm, fundo_reserva, seguro,
taxas_pontuais, aluguel, lance, saldo_a_contribuir, carta_atualizada
```

---

## Notas importantes

* **TR/IPCA**: aplicados **mensalmente** ao saldo antes dos juros (SAC).
* **Arredondamento**: `Decimal` com 2 casas decimais, arredondamento `ROUND_HALF_UP`.
* Para reproduzir contratos/consórcios reais com precisão, use **séries mensais** de índices (ex.: INCC/IPCA/TR) em `correcao_serie_mensal`.

---

## Testes (opcional)

```bash
pip install pytest
pytest -q
```