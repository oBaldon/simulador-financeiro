# src/simfin/cli.py
from __future__ import annotations
import argparse, json, csv
from decimal import Decimal

from .models import EntradaPrazo, EntradaValor
from .sac import simular_sac_por_prazo, simular_sac_por_valor
from .export import exportar_csv
from .consorcio import ConsorcioInput, Hipoteses, Lance, simular_consorcio
from .indices import taxa_mensal


def _as_decimal(v: str) -> Decimal:
    v = v.replace(",", ".").strip()
    return Decimal(v)

def _D(x):
    if x is None:
        return Decimal(0)
    if isinstance(x, (int, float)):
        return Decimal(str(x))
    return Decimal(str(x).replace(",", ".").strip())

def _as_rate(v: Decimal) -> Decimal:
    """
    Normaliza taxa anual:
      - Se v >= 1, assume que veio em porcentagem (ex.: 10 -> 0.10).
      - Se v  < 1, assume que já está em fração (ex.: 0.10 -> 0.10).
    """
    return (v / Decimal(100)) if v >= 1 else v

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

    # Consórcio
    p.add_argument("--consorcio-json", type=str, help="JSON com dados do consórcio para comparar")
    p.add_argument("--csv-consorcio", type=str, help="Exportar cronograma do consórcio em CSV")
    p.add_argument("--taxa-desconto-anual", type=str, help="(Opcional) Taxa de desconto anual para VPL; se presente, sobrescreve a do JSON")

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

    # ===== Comparação com Consórcio (somente no modo por flags) =====
    if args.consorcio_json:
        with open(args.consorcio_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        lance = data.get("lance", {})
        hip = data.get("hipoteses", {})

        ci = ConsorcioInput(
            administradora=data.get("administradora", ""),
            grupo=data.get("grupo", ""),
            cota=data.get("cota", ""),
            carta_credito_inicial=_D(data["carta_credito_inicial"]),
            prazo_total_meses=int(data["prazo_total_meses"]),
            indice_correcao=data.get("indice_correcao", "INCC"),
            correcao_modo=data.get("correcao_modo", "anual_constante"),
            correcao_anual=_D(data.get("correcao_anual", 0)),
            correcao_serie_mensal=[_D(x) for x in data.get("correcao_serie_mensal", [])] or None,
            taxa_adm_total_pct=_D(data.get("taxa_adm_total_pct", 16)),
            taxa_adm_forma=data.get("taxa_adm_forma", "diluida"),
            fundo_reserva_pct=_D(data.get("fundo_reserva_pct", 0)),
            seguro_mensal_valor=_D(data.get("seguro_mensal_valor", 0)),
            taxa_adesao_valor=_D(data.get("taxa_adesao_valor", 0)),
            taxas_contemplacao_valor=_D(data.get("taxas_contemplacao_valor", 0)),
            parcela_reduzida=bool(data.get("parcela_reduzida", False)),
            parcela_reduzida_pct=_D(data.get("parcela_reduzida_pct", 100)),
            parcela_reduzida_meses=int(data.get("parcela_reduzida_meses", 0)),
            lance=Lance(
                tipo=lance.get("tipo", "livre"),
                percent_carta=_D(lance.get("percent_carta", 0)),
                fonte=lance.get("fonte", "proprio"),
            ),
            mes_contemplacao_alvo=int(data.get("mes_contemplacao_alvo", 12)),
            hipoteses=Hipoteses(
                aluguel_mensal_enquanto_espera=_D(hip.get("aluguel_mensal_enquanto_espera", 0)),
                taxa_desconto_anual=_as_rate(_D(hip.get("taxa_desconto_anual", 0))),
                crescimento_preco_imovel_anual=_D(hip.get("crescimento_preco_imovel_anual", 0)),
            ),
        )

        if args.taxa_desconto_anual:
            ci.hipoteses.taxa_desconto_anual = _as_rate(_D(args.taxa_desconto_anual))

        cres = simular_consorcio(ci)

        if args.csv_consorcio:
            campos = ["mes","parcela","contribuicao_base","taxa_adm","fundo_reserva","seguro","taxas_pontuais","aluguel","lance","saldo_a_contribuir","carta_atualizada"]
            with open(args.csv_consorcio, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=campos)
                w.writeheader()
                for p in cres.parcelas:
                    w.writerow({k: str(p.get(k, "")) for k in campos})
            print(f"CSV (consórcio) exportado em: {args.csv_consorcio}")

        # Comparação: totais e VPL (se taxa de desconto informada)
        disc_a = ci.hipoteses.taxa_desconto_anual
        vpl_fin = vpl_con = None
        if disc_a and disc_a != Decimal(0):
            disc_m = taxa_mensal(disc_a)
            def vpl(parcelas):
                s = Decimal(0)
                for i, p in enumerate(parcelas, start=1):
                    s += p["parcela"] / ((Decimal(1)+disc_m) ** Decimal(i))
                return s
            vpl_fin = vpl(res.parcelas_detalhadas)
            vpl_con = vpl(cres.parcelas)

        print("\n== Comparação com Consórcio ==")
        print(f"Consórcio: {ci.administradora} | grupo {ci.grupo} cota {ci.cota}")
        print(f"Carta inicial: R$ {ci.carta_credito_inicial} | Prazo: {ci.prazo_total_meses} meses")
        print(f"Mês de contemplação (alvo): {cres.mes_contemplacao}")
        print(f"Total nominal Consórcio: R$ {cres.total_pago} (líquido pós-FR: R$ {cres.total_pago_liquido})")
        print(f"Total nominal Financiamento: R$ {res.valor_total_pago}")
        if vpl_fin is not None:
            print(f"VPL (taxa desc. {disc_a*100:.2f}% a.a.) — Consórcio: R$ {vpl_con.quantize(Decimal('0.01'))} | Financiamento: R$ {vpl_fin.quantize(Decimal('0.01'))}")

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
    # (se quiser, depois a gente adiciona perguntas interativas para consórcio aqui)
