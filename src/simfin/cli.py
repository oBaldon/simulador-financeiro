from __future__ import annotations
import argparse
from decimal import Decimal
from typing import Optional

from .models import EntradaPrazo, EntradaValor
from .sac import simular_sac_por_prazo, simular_sac_por_valor
from .export import exportar_csv

def _as_decimal(v: str) -> Decimal:
    v = v.replace(",", ".").strip()
    return Decimal(v)

def main() -> None:
    p = argparse.ArgumentParser(prog="simfin", description="Simulador SAC (TR/IPCA, encargos, CSV)")
    p.add_argument("--interactive", action="store_true", help="Modo interativo via terminal")

    p.add_argument("--tipo", choices=["prazo", "valor"], help="Tipo de simulação")
    p.add_argument("--valor-imovel", type=str, help="Valor do imóvel")
    p.add_argument("--entrada", type=str, help="Valor da entrada")
    p.add_argument("--juros-anual", type=str, help="Juros anual (ex.: 8.47 ou 0.0847)")
    p.add_argument("--juros-em-percent", action="store_true", help="Interpreta juros anual em % (8.47 => 0.0847)")
    p.add_argument("--tr-anual", type=str, default="0.0", help="TR anual (ex.: 0.0 ou 0.02)")
    p.add_argument("--ipca-anual", type=str, default="0.0", help="IPCA anual (ex.: 0.0 ou 0.06)")
    p.add_argument("--encargos", type=str, default="0.0", help="Encargos fixos mensais")
    p.add_argument("--prazo", type=int, help="Prazo em meses (para tipo=prazo)")
    p.add_argument("--prazo-oficial", type=int, default=360, help="Prazo oficial do banco (máximo)")
    p.add_argument("--valor-max", type=str, help="Valor máximo total a pagar (para tipo=valor)")
    p.add_argument("--csv", type=str, help="Exportar parcelas em CSV para o caminho informado")

    args = p.parse_args()

    if args.interactive:
        _interactive()
        return

    if not args.tipo:
        p.error("--tipo é obrigatório (prazo|valor) quando não estiver em modo interativo.")

    valor_imovel = _as_decimal(args.valor_imovel)
    entrada = _as_decimal(args.entrada)
    juros = _as_decimal(args.juros_anual)
    if args.juros_em_percent:
        juros = juros / Decimal(100)

    tr = _as_decimal(args.tr_anual)
    ipca = _as_decimal(args.ipca_anual)
    encargos = _as_decimal(args.encargos)

    if args.tipo == "prazo":
        if not args.prazo:
            p.error("--prazo é obrigatório para tipo=prazo")
        entrada_prazo = EntradaPrazo(
            valor_imovel=valor_imovel, entrada=entrada, juros_anual=juros,
            tr_anual=tr, ipca_anual=ipca, encargos_fixos_mensais=encargos,
            prazo=args.prazo, prazo_oficial=args.prazo_oficial
        )
        res = simular_sac_por_prazo(entrada_prazo)
    else:
        if not args.valor_max:
            p.error("--valor-max é obrigatório para tipo=valor")
        entrada_valor = EntradaValor(
            valor_imovel=valor_imovel, entrada=entrada, juros_anual=juros,
            tr_anual=tr, ipca_anual=ipca, encargos_fixos_mensais=encargos,
            valor_maximo=_as_decimal(args.valor_max), prazo_oficial=args.prazo_oficial
        )
        res = simular_sac_por_valor(entrada_valor)

    print("\nResultado da simulação")
    print(f"Prazo utilizado: {res.prazo_utilizado} meses")
    print(f"Primeira parcela: R$ {res.primeira_parcela}")
    print(f"Última parcela: R$ {res.ultima_parcela}")
    print(f"Total pago: R$ {res.valor_total_pago}")

    if args.csv:
        exportar_csv(res.parcelas_detalhadas, args.csv)
        print(f"CSV exportado em: {args.csv}")

def _ask_decimal(prompt: str) -> Decimal:
    return _as_decimal(input(prompt).strip())

def _interactive() -> None:
    print("Simfin — modo interativo\n")
    tipo = input("Tipo de simulação ('prazo' ou 'valor'): ").strip().lower()
    valor_imovel = _ask_decimal("Valor do imóvel: ")
    entrada = _ask_decimal("Entrada: ")
    juros = _ask_decimal("Juros anual (ex. 8.47 ou 0.0847): ")
    juros_em_percent = input("O valor anterior está em %? (s/n): ").strip().lower() == "s"
    if juros_em_percent:
        from decimal import Decimal
        juros = juros / Decimal(100)
    tr = _ask_decimal("TR anual (ex. 0.0 ou 0.02): ")
    ipca = _ask_decimal("IPCA anual (ex. 0.0 ou 0.06): ")
    encargos = _ask_decimal("Encargos fixos mensais: ")
    prazo_oficial = int(input("Prazo oficial (máximo) em meses [360]: ") or "360")

    if tipo == "prazo":
        prazo = int(input("Prazo desejado (meses): "))
        res = simular_sac_por_prazo(EntradaPrazo(
            valor_imovel=valor_imovel, entrada=entrada, juros_anual=juros,
            tr_anual=tr, ipca_anual=ipca, encargos_fixos_mensais=encargos,
            prazo=prazo, prazo_oficial=prazo_oficial
        ))
    else:
        valor_max = _ask_decimal("Valor total máximo a pagar: ")
        res = simular_sac_por_valor(EntradaValor(
            valor_imovel=valor_imovel, entrada=entrada, juros_anual=juros,
            tr_anual=tr, ipca_anual=ipca, encargos_fixos_mensais=encargos,
            valor_maximo=valor_max, prazo_oficial=prazo_oficial
        ))

    print("\nResultado da simulação")
    print(f"Prazo utilizado: {res.prazo_utilizado} meses")
    print(f"Primeira parcela: R$ {res.primeira_parcela}")
    print(f"Última parcela: R$ {res.ultima_parcela}")
    print(f"Total pago: R$ {res.valor_total_pago}")
