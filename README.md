# 💰 Simulador de Financiamento

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)]()
[![Autor](https://img.shields.io/badge/autor-oBaldon-blueviolet)](https://github.com/oBaldon)

Simulador interativo de financiamento habitacional no sistema SAC, com possibilidade de ajustar:

- Prazo de pagamento
- Valor máximo total a pagar
- Juros anuais
- TR, IPCA e encargos fixos mensais
- Exportação das parcelas para CSV

> 🔧 Desenvolvido para fins educacionais, comparação de cenários de financiamento e tomada de decisão.

---

## ✨ Funcionalidades

- ✅ Simulação por **prazo personalizado**
- ✅ Simulação por **valor total máximo desejado**
- ✅ Cálculo mês a mês com:
  - Amortização constante (SAC)
  - Juros decrescentes
  - Correções por **TR** e **IPCA**
  - Inclusão de **seguros e taxas administrativas**
- 📤 Exportação para `.csv` com todos os meses
- 🧾 Relatório final: primeira parcela, última parcela, total pago

---

## 📦 Requisitos

- Python **3.10+**
- Bibliotecas padrão do Python (`dataclasses`, `csv`, etc.)

---

## 🚀 Como executar

Clone o repositório:

```bash
git clone https://github.com/oBaldon/simulador-financeiro.git
cd simulador-financeiro
```

Instale (opcionalmente) um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

Execute o simulador:

```bash
python main.py
```

Siga o menu interativo para preencher os dados da simulação.

---

## 📊 Exportação de parcelas

Ao final da simulação, o sistema oferece a opção de exportar o resultado completo em `.csv`.  
O arquivo gerado será salvo como:

```
parcelas_simulacao.csv
```

E pode ser aberto no Excel ou Google Sheets.

---

## 📁 Estrutura do projeto

```
simulador-financeiro/
│
├── simulador/
│   ├── menu.py              # Menu interativo no terminal
│   ├── financiamento.py     # Cálculos principais da simulação
│   ├── exportador.py        # Exporta parcelas detalhadas para CSV
│   ├── models.py            # Estrutura dos dados
│   ├── tr.py / ipca.py      # Correções de saldo
│
├── main.py                  # Script principal
├── parcelas_simulacao.csv   # (gerado após simulação)
```

---

## 📌 Exemplo de uso

```
Tipo de simulação ('prazo' ou 'valor'): prazo
Valor do imóvel: 250000
Entrada: 87500
...
Resultado da Simulação:
Prazo utilizado: 185 meses
Primeira parcela: R$ 1980.94
Última parcela: R$ 983.80
Valor total pago: R$ 274238.30
```

---

## 👨‍💻 Autor

Douglas Baldon — [@oBaldon](https://github.com/oBaldon)  
Contribuições e sugestões são bem-vindas!  
Abra uma issue ou envie um pull request 🚀

---

## 📄 Licença