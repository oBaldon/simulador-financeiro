from simulador.menu import exibir_menu
from simulador.financiamento import simular_por_prazo, simular_por_valor
from simulador.exportador import exportar_parcelas_para_csv

dados = exibir_menu()

if dados.tipo_simulacao == "prazo":
    resultado = simular_por_prazo(dados)
elif dados.tipo_simulacao == "valor":
    resultado = simular_por_valor(dados)
else:
    raise ValueError("Tipo de simulação inválido.")

print("\nResultado da Simulação:")
print(f"Prazo utilizado: {resultado.prazo_utilizado} meses")
print(f"Primeira parcela: R$ {resultado.primeira_parcela:.2f}")
print(f"Última parcela: R$ {resultado.ultima_parcela:.2f}")
print(f"Valor total pago: R$ {resultado.valor_total_pago:.2f}")

# após mostrar o resultado:
if resultado.parcelas_detalhadas:
    exportar = input("\nDeseja exportar as parcelas para CSV? (s/n): ").strip().lower()
    if exportar == "s":
        exportar_parcelas_para_csv(resultado.parcelas_detalhadas)