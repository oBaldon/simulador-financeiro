# Simfin — Simulador de Financiamento (SAC) refatorado

Refatoração do seu simulador antigo, agora como pacote Python moderno, tipado e com **CLI**:

- Cálculo **SAC** com **juros**, **TR** e **IPCA** (aplicados ao saldo).
- **Encargos** fixos mensais.
- **Exportação CSV** com o detalhamento mês a mês.
- **Modo interativo** ou **parâmetros via CLI**.
- Matemática com `Decimal` para evitar erros de arredondamento.

## Instalação local (modo dev)

```bash
cd simfin-refatorado
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Uso rápido

### Interativo
```bash
simfin --interactive
```

### Parametrizado
```bash
simfin --tipo prazo   --valor-imovel 250000 --entrada 87500   --juros-anual 8.47 --juros-em-percent   --prazo 360 --encargos 120   --tr-anual 0.0 --ipca-anual 0.0   --csv parcelas.csv
```

### Por valor máximo total
```bash
simfin --tipo valor   --valor-imovel 250000 --entrada 87500   --juros-anual 8.47 --juros-em-percent   --valor-max 274238.30   --prazo-oficial 360 --encargos 120
```

## Saída
- Primeira/última parcela, total pago e prazo utilizado.
- Arquivo CSV (opcional) com colunas: `mes, parcela, juros, amortizacao, saldo_devedor`.
