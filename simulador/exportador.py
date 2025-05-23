import csv

def exportar_parcelas_para_csv(parcelas, nome_arquivo="parcelas_simulacao.csv"):
    with open(nome_arquivo, mode='w', newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["mes", "parcela", "juros", "amortizacao", "saldo_devedor"])
        escritor.writeheader()
        for linha in parcelas:
            escritor.writerow(linha)
    print(f"\n📤 Arquivo exportado com sucesso: {nome_arquivo}")
