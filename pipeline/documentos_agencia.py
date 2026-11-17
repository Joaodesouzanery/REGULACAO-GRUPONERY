"""Documento público da AGÊNCIA (não de empresa): panorama da diretoria, decisões, temas, prazos, relatorias, mandatos/vacância e transparência.
Vai para agencias/<ag>/documentos/panorama_<ag>.pdf (pode ir ao GitHub: só dado público agregado). Uso: python3 pipeline/documentos_agencia.py <ag>"""
import sys, os, re, json, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, prazos, design as d
E = d.E
AG = sys.argv[1].lower(); D = "data" if AG == "antt" else f"data/{AG}"; NOME = d.NOME_AG.get(AG, AG.upper())
ld = lambda p, x: json.load(open(p)) if os.path.exists(p) else x
c = previsao.conn(AG); HOJE = datetime.date.today()
KIT = d.kit(d.SETOR_AG.get(AG, "portos")); DIV = KIT["divisores"] + [KIT["capa"]] * 3
R = c.execute("select count(*), min(data), max(data) from reunioes where data>='2018-01-01'").fetchone()
IT = list(c.execute("select i.*, r.data, r.numero from itens i join reunioes r on r.id=i.reuniao_id where r.data>='2018-01-01'"))
res = lambda i: (i["resultado"] or "").lower()
div_ids = {x for (x,) in c.execute("select distinct item_id from votos where categoria in ('vencido','revisor_diverge')")}
n = len(IT); nv = sum(1 for i in IT if re.match(r"\s*(pedido de )?vista", res(i))); nr = sum(1 for i in IT if re.match(r"\s*retirad", res(i)))
ndiv = sum(1 for i in IT if i["id"] in div_ids)
temas = collections.Counter(t for (t,) in c.execute("select tema from item_temas t join itens i on i.id=t.item_id join reunioes r on r.id=i.reuniao_id where r.data>=?", (f"{HOJE.year - 3}-01-01",)))
rel = collections.Counter(i["relator"] for i in IT if i["relator"] and i["data"] >= f"{HOJE.year - 3}-01-01")
DUR = prazos.duracoes(AG); por = collections.defaultdict(list)
for v in DUR.values(): por[v[1]].append(v)
est = sorted([(t, e) for t in por if (e := prazos.estatistica(DUR, t))], key=lambda x: x[1]["mediana"])
MA = ld("data/mandatos_agencias.json", {}).get("agencias", {}).get(NOME, [])
TR = ld(f"{D}/transparencia.json", {})
ano = collections.Counter(i["data"][:4] for i in IT)
parcial = AG == "aneel"

S = [d.capa(KIT["capa"], "50% 55%", "Panorama da agência", NOME, "Como a diretoria colegiada decide",
            f"Reuniões de diretoria de {R[1][:4]} a {R[2][:4]}" + (" (base em expansão: parte dos anos ainda em análise)" if parcial else "") + ". Fontes públicas da agência.",
            [(f"{n:,}".replace(",", "."), "itens decididos pela diretoria"), (f"{100 * (n - ndiv - nv - nr) / max(n, 1):.0f}%", "sem divergência, vista ou retirada"), (f"{100 * nv / max(n, 1):.1f}%", "com pedido de vista"), (R[0], "reuniões analisadas")])]
SEC = [("Números e temas", "o que a diretoria decide"), ("Quem decide", "diretoria, mandatos e vagas"), ("Quanto tempo leva", "prazos por tipo de processo"), ("Transparência", "como acompanhar a agência")]
S.append(d.sumario(SEC, DIV[0]))
S.append(d.divisor(1, SEC[0][0], f"Tudo o que a diretoria da {NOME} decidiu em reuniões públicas, por ano e por tema.", DIV[0]))
anos = d.barras([(a, ano[a], "itens") for a in sorted(ano)])
tm = d.barras([(t.replace("_", " "), v, "itens") for t, v in temas.most_common(8)])
S.append(d.tecnica("01 · Números e temas", "O que a diretoria decide", d.numeros([(f"{n:,}".replace(",", "."), "itens desde 2018"), (f"{100 * ndiv / max(n, 1):.1f}%", "com voto divergente ou vencido"), (f"{100 * nv / max(n, 1):.1f}%", "com pedido de vista"), (f"{100 * nr / max(n, 1):.1f}%", "retirados de pauta")])
                   + d.grade(d.conceito("", "Itens por ano", "", texto=anos), d.conceito("", "Temas mais frequentes", f"últimos 3 anos", texto=tm), cols=2), AG,
                   "Contagens a partir das reuniões analisadas; um item pode ter mais de um tema. Legenda automática pode errar nomes e números."))
S.append(d.divisor(2, SEC[1][0], "A composição atual, quem relata e as cadeiras sem titular.", DIV[1]))
rows = [[f"<b>{E(p['nome'])}</b>" if p["tipo"] == "titular" else "<b>VAGO</b>", E(p["cargo"]) if p["tipo"] == "titular" else f"{E(p['cargo'])} (ex-{E(p.get('ex_titular') or '')})",
         (f"{p['inicio'][8:]}/{p['inicio'][5:7]}/{p['inicio'][:4]} a {p['fim'][8:]}/{p['fim'][5:7]}/{p['fim'][:4]}" if p["tipo"] == "titular" and p.get("inicio") and p.get("fim") else (f"vaga desde {p['vaga_desde'][8:]}/{p['vaga_desde'][5:7]}/{p['vaga_desde'][:4]}" if p.get("vaga_desde") else "")),
         E(p.get("substituto") or "")] for p in MA]
cad = ld(f"{D}/cadeiras.json", {}).get("cadeiras")
corpo = d.tabela(["Diretor(a)", "Cargo", "Mandato", "Substituto"], rows, ["30%", "26%", "22%", "22%"]) + d.conceito("", "Quem mais relatou (3 anos)", "", texto=d.barras([(k, v, "relatorias") for k, v in rel.most_common(7)]))
S.append(d.tecnica("02 · Quem decide", "Diretoria hoje e relatorias", corpo, AG, "Composição conferida com o Diário Oficial (auditoria em docs/auditoria_mandatos.md)."))
if cad: S.append(d.tecnica("02 · Quem decide", "Controle da diretoria por cadeira", d.quadro_mandatos(cad, ex=True), AG))
S.append(d.divisor(3, SEC[2][0], "Quando um processo não sai na primeira sessão, quanto tempo ele fica na diretoria.", DIV[2]))
S.append(d.tecnica("03 · Quanto tempo leva", "Prazo na diretoria por tipo de processo", d.barras([(t.replace("_", " "), e["mediana"], f'n={e["n"]} · faixa {e["p25"]:.0f}–{e["p75"]:.0f} dias') for t, e in est], lambda v: f"{v:.0f} dias")
                   + '<p style="font-size:8.5pt;color:#6B7780;margin-top:.15in">Mediana de dias entre a 1ª sessão e a decisão final, só para processos que passaram por mais de uma sessão (vista, retirada, diligência), desde 2018. Não inclui o tempo na área técnica antes da pauta.</p>', AG))
S.append(d.divisor(4, SEC[3][0], "O que a agência publica e quão fácil é acompanhá-la.", DIV[3]))
tr = [[E(x["nome"]), str(x["nota"]) + "/2", E(x["evidencia"][:260])] for x in TR.get("criterios", [])]
S.append(d.tecnica("04 · Transparência", "Como acompanhar a agência", (d.tabela(["Critério", "Nota", "Evidência"], tr, ["24%", "8%", "68%"]) if tr else "<p>Avaliação em preparação.</p>"), AG, "Notas 0–2 por critério; comparativo entre agências em docs/transparencia_agencias.md."))
S.append(d.fim("Panorama feito só com fontes públicas: vídeos oficiais das reuniões, pautas, calendário e Diário Oficial. Contagens dependem da legenda automática e da análise item a item; a taxa de conferência cega está em agencias/" + AG + "/qualidade.", "Grupo Nery · inteligência regulatória", DIV[0]))
os.makedirs(f"agencias/{AG}/documentos", exist_ok=True)
print(d.documento(S, f"Panorama {NOME}", f"agencias/{AG}/documentos/panorama_{AG}"), len(S), "páginas")
