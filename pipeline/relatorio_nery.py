"""Relatório da EMPRESA no padrão Grupo Nery (azul + lilás; brochura com divisores de seção e páginas técnicas brancas).
Mesmo conteúdo do relatorio_painel.py, mais as narrativas analíticas (clientes/<x>/<pasta>/narrativas.json) e a história do contrato.
Uso: python3 pipeline/relatorio_nery.py clientes/<x>/<pasta>   → <pasta>/relatorio_empresa.pdf
Setor/fotos: kit por agência (docs/marca/setores/kit.json); foto do cliente (empresa.json → foto_capa) tem prioridade na capa."""
import sys, os, re, json, datetime, collections, math, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, mapa_tema, design as d
from desfecho import desfecho_item
E = d.E

P = sys.argv[1].rstrip("/")
if not os.path.exists(f"{P}/empresa.json"): sys.exit(f"Pasta do cliente não encontrada: {P}")
EMP = json.load(open(f"{P}/empresa.json")); AG = EMP.get("agencias", ["antaq"])[0]
D = "data" if AG == "antt" else f"data/{AG}"; NOME = d.NOME_AG.get(AG, AG.upper())
ld = lambda p, x: json.load(open(p)) if os.path.exists(p) else x
MAN, NAR = ld(f"{P}/desfechos_manuais.json", {}), ld(f"{P}/narrativas.json", {})
HOJE = datetime.date.today(); TRES = (HOJE - datetime.timedelta(days=3 * 365)).isoformat(); DESDE = "2018-01-01"
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if s and re.match(r"\d{4}-\d\d-\d\d", str(s)) else str(s or "—")
c = previsao.conn(AG); des = lambda i: (MAN.get(str(i)) or {}).get("desfecho") or desfecho_item(c, i)
KIT = d.kit(EMP.get("setor") or d.SETOR_AG.get(AG, "portos"))
FOTO = EMP.get("foto_capa") or KIT["capa"]; FOCO = EMP.get("foco", "50% 55%"); CLI = EMP.get("logo")
DIV = KIT["divisores"] + [FOTO] * 4
nome_curto = EMP["nome"].split("(")[0].strip()
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")

# ---------- dados ----------
pr = previsao.calcular(AG, EMP["aliases"]); board = pr["colegiado"]
its = [i for i in pr["itens"] if i["data"] >= DESDE]
bios = {b["diretor"]: b for b in ld(f"{D}/bios.json", [])}; mand = ld(f"{D}/mandatos.json", [])
vac = [v for v in ld(f"{D}/vacancias.json", []) if not v.get("fim")]; sups = ld(f"{D}/superintendentes.json", [])
cal = [x for x in ld(f"{D}/calendario.json", []) if x["data"] >= HOJE.isoformat()][:2]
def mandato(n):
    ms = [m for m in mand if m.get("diretor") == n]; m = ms[-1] if ms else {}
    return m.get("inicio"), m.get("fim_legal") or m.get("fim")
def foto(n, b=None):
    for p in [(b or {}).get("foto"), f"{D}/dirigentes/{slug(n)}.jpg", f"docs/marca/diretores/{AG}/{slug(n)}.jpg"]:
        if p and os.path.exists(p): return f'<div class="av" style="background-image:url({d.b64(p)})"></div>'
    return '<div class="av ini">' + E("".join(w[0] for w in n.split()[:2]).upper()) + "</div>"
STATUS = lambda i: "decidido" if re.search(r"aprovad|desprov|indefer|acolhid|negad|provid", i["resultado"] or "", re.I) else "retirado" if "retirad" in (i["resultado"] or "").lower() else "vista" if "vista" in (i["resultado"] or "").lower() else "decidido"
procs = collections.OrderedDict()
for i in reversed(its):
    k = (i["processo"] or "").strip()[:20] or i["assunto"][:40]
    procs.setdefault(k, i)
unan = sum(1 for i in its if not c.execute("select 1 from votos where item_id=? and categoria in ('vencido','revisor_diverge')", (i["id"],)).fetchone())
aberto = sum(1 for i in procs.values() if STATUS(i) != "decidido")
link = mapa_tema.link


def narrativa(chave):
    n = NAR.get(chave) or {}
    ps = "".join(f"<p>{E(p)}</p>" for p in n.get("paragrafos", []))
    cs = "".join(d.citacao(q["texto"], q.get("quem", ""), f'{q.get("reuniao", "")}{" · item " + str(q["item"]) if q.get("item") else ""}', q.get("link")) for q in n.get("citacoes", [])[:2])
    return ps, cs


S = []
S.append(d.capa(FOTO, FOCO, f"Inteligência regulatória · {NOME}", nome_curto, EMP["nome"][len(nome_curto):].strip(" ()") or EMP.get("subtitulo", ""), EMP.get("cnpj", ""),
                [(len(its), f"decisões da diretoria sobre a empresa desde {fmtd(its[0]['data'])[-4:] if its else '—'}"), (f"{100 * unan / max(len(its), 1):.0f}%", "decididas sem voto divergente"),
                 (" · ".join(fmtd(x["data"])[:5] for x in cal) or "—", "próximas reuniões da diretoria"), (aberto, "processos em aberto (vista ou retirados)")], CLI))
SEC = [("A empresa na agência", "processos, calendário e desfechos"), ("Quem decide", "diretoria, perfis e superintendentes"), ("Como a diretoria decide", "temas da empresa, com as falas"),
       ("Contratos em foco", "a história de cada contrato"), ("Antecipar", "item em aberto e previsão (estimativa)")]
S.append(d.sumario(SEC, DIV[0]))

# 01 empresa
S.append(d.divisor(1, SEC[0][0], f"Tudo o que a diretoria da {NOME} decidiu sobre a {nome_curto} desde 2018, o que está em aberto e o que vem na agenda.", DIV[0]))
tab = d.tabela(["Situação", "Última sessão", "Processo", "Assunto", "Para a empresa"],
               [[E(STATUS(i)), fmtd(i["data"]), f'<span style="color:#6B7780">{E(k)}</span>', E((i["assunto"] or "")[:95]), E(des(i["id"]))] for k, i in list(procs.items())[:14]], ["10%", "11%", "17%", "47%", "15%"])
DES = collections.Counter(des(i["id"]) for i in its)
calh = d.tabela(["Data", "Evento", "Observação"], [[fmtd(x["data"]), f'{x["reuniao"]}ª reunião da diretoria', E(x.get("formato", ""))] for x in cal] +
                [[fmtd(mandato(n)[1]), "fim de mandato", E(n)] for n in board if mandato(n)[1] and HOJE.isoformat() <= str(mandato(n)[1]) <= (HOJE + datetime.timedelta(days=460)).isoformat()])
pn = NAR.get("painel") or {}
pars0 = pn.get("paragrafos", [])
rot = ["O que a diretoria decidiu", "O que está em aberto", "O que vem a seguir"] + [f"Ponto {k}" for k in range(4, 9)]
S.append(d.tecnica("01 · A empresa na agência", "Onde a empresa está hoje na diretoria",
                   d.whitepaper("Painel", [(rot[k], f"<p>{E(x)}</p>") for k, x in enumerate(pars0)], foto=FOTO, foco=FOCO, h_foto="1.25in"), AG, logo_cliente=CLI))
cs_all = "".join(d.citacao(q["texto"], q.get("quem", ""), f'{q.get("reuniao", "")}{" · item " + str(q["item"]) if q.get("item") else ""}', q.get("link")) for q in pn.get("citacoes", [])[:3])
S.append(d.tecnica("01 · A empresa na agência", "Desfechos, falas e calendário", d.grade(d.conceito("", "Desfecho histórico", "decisões desde 2018 (conferidas à mão quando ambíguas)", texto=d.rosca(dict(DES.most_common()), "decisões")),
                                                                                    d.conceito("", "O que foi dito", "trechos literais, com link no minuto", texto=cs_all),
                                                                                    d.conceito("", "Próximos passos", "calendário oficial e mandatos", texto=calh), cols=3), AG, logo_cliente=CLI))
S.append(d.tecnica("01 · A empresa na agência", "Processos da empresa na diretoria", tab, AG,
                   "Situação pela última sessão da diretoria. Nº de processo vem da legenda automática — conferir no SEI.", CLI))

# 02 quem decide
S.append(d.divisor(2, SEC[1][0], "Os diretores em exercício, como cada um atua nos temas da empresa e quem é quem nas superintendências.", DIV[1] if len(DIV) > 1 else FOTO))
nd = NAR.get("diretoria", {})
pars = {p.split(":")[0].strip(): p for p in nd.get("paragrafos", [])}
pes = []
for n in board:
    b = bios.get(n, {}); ini, fim_ = mandato(n)
    txt = next((p for k, p in pars.items() if n.split()[0] in k or n in p[:80]), (b.get("minibio") or "")[:260])
    pes.append(d.pessoa(foto(n, b), n, f'{(b.get("cargo") or "Diretor(a)")[:70]} · mandato até {fmtd(fim_)}', [E(txt[:420]), f'<span style="color:#6B7780">Formação: {E((b.get("formacao") or "—")[:120])}</span>']))
S.append(d.tecnica("02 · Quem decide", "Diretoria em exercício", d.grade(*pes, cols=2), AG, "Perfis com fontes oficiais; mandatos conferidos todo dia 1.", CLI))
CAD = ld(f"{D}/cadeiras.json", {}).get("cadeiras")
if CAD:
    S.append(d.tecnica("02 · Quem decide", "Controle da diretoria: cadeiras, mandatos e substitutos", d.quadro_mandatos(CAD, foto_fn=lambda n: foto(n)), AG,
                       "Fontes: Senado, DOU e agência; datas marcadas «a confirmar» na base quando o ato não foi localizado. Faixa hachurada = cadeira sem titular nem substituto registrado (vago).", CLI))
sc = "".join(f'<li><b>{E(s.get("nome", ""))}</b> — {E((s.get("superintendencia") or s.get("cargo") or "")[:70])}</li>' for s in sups[:14])
vh = "; ".join(f'{E(v["cadeira"])} (desde {fmtd(v["inicio"])}; interinos: {E(v.get("interinos") or "—")})' for v in vac) or "nenhuma"
S.append(d.tecnica("02 · Quem decide", "Superintendências e cadeiras vagas", d.grade(d.conceito("", "Superintendentes", "quem conduz a instrução técnica dos processos", texto=f'<ul class="arr">{sc}</ul>'),
                                                                                   d.conceito("", "Mandatos e vagas", "o que pode mudar na composição", texto=f"<p>{vh}</p>"), cols=2), AG, logo_cliente=CLI))

# 03 como decide
S.append(d.divisor(3, SEC[2][0], "Como cada diretor vota nos temas da empresa, os argumentos que a diretoria usa e as decisões semelhantes.", DIV[2] if len(DIV) > 2 else FOTO))
for k, tc in enumerate(EMP.get("temas_consultoria", [])):
    m = mapa_tema.mapear(AG, tc["regex"], TRES); chave = ["reequilibrio", "passivo"][k] if k < 2 else f"tema{k}"
    ps, cs = narrativa(chave)
    linhas = [(n, st["p_acomp"], f'n={st["n"]}' + (" · insuficiente" if st["n"] < 5 else "")) for n, st in m["por_diretor"].items()]
    prec = "".join(f'<li>{fmtd(i["data"])} · {i["numero"]}ª — {E((i["assunto"] or "")[:85])} → {E(des(i["id"]))} <a href="{link(i["video_id"], i["ts"])}">vídeo</a></li>' for i in m["itens"][-4:][::-1])
    S.append(d.tecnica("03 · Como a diretoria decide", re.sub(r"^\w\)\s*", "", tc["titulo"]).split(":")[0],
                       d.grade(f'<div class="nar">{ps}</div>', '<div>' + cs + d.conceito("", "Chance de acompanhar o relator", f"estimativa · {len(m['itens'])} decisões nos últimos 3 anos, {m['unanimes']} sem divergência", texto=d.barras(linhas, lambda v: f"{v:.0%}"))
                                + d.conceito("", "Decisões semelhantes", "", texto=f'<ul class="arr sm">{prec}</ul>') + '</div>', cols=2).replace("repeat(2,1fr)", "1.25fr 1fr"), AG,
                       "Chance = histórico de cada diretor no tema (prior 97%, peso 10); estimativa, não certeza.", CLI))

# 04 contratos
S.append(d.divisor(4, SEC[3][0], "A trajetória de cada contrato da empresa na diretoria: o que foi pedido, quem votou o quê e o que vem a seguir.", DIV[3] if len(DIV) > 3 else FOTO))
for chave in ("atu12", "atu18"):
    if chave not in NAR: continue
    n = NAR[chave]; ps = [f"<p>{E(p)}</p>" for p in n.get("paragrafos", [])]; cs = [d.citacao(q["texto"], q.get("quem", ""), f'{q.get("reuniao", "")}{" · item " + str(q["item"]) if q.get("item") else ""}', q.get("link")) for q in n.get("citacoes", [])]
    meio = max(1, (len(ps) + 1) // 2)
    S.append(d.tecnica("04 · Contratos em foco", n.get("titulo", chave.upper()), d.grade("<div>" + "".join(ps[:meio]) + "".join(cs[:2]) + "</div>", "<div>" + "".join(ps[meio:]) + "".join(cs[2:4]) + "</div>", cols=2), AG, logo_cliente=CLI))

# 05 antecipar
S.append(d.divisor(5, SEC[4][0], "O item em aberto que interessa à empresa e o que o histórico de votos permite estimar — sempre como estimativa.", DIV[4] if len(DIV) > 4 else FOTO))
ps, cs = narrativa("item17")
calh2 = "".join(f'<li><b>{E(x["data"])}</b> {E(x["reuniao"])} — {E(x["obs"])}</li>' for x in (EMP.get("item_antecipado") or {}).get("calendario", []))
S.append(d.tecnica("05 · Antecipar", (EMP.get("item_antecipado") or {}).get("titulo", "Item em aberto"), d.grade(f'<div class="nar">{ps}</div>', '<div>' + d.conceito("", "Próximas reuniões", "calendário oficial", texto=f'<ul class="arr">{calh2}</ul>') + cs + '</div>', cols=2), AG, logo_cliente=CLI))
def faixa(ps_):
    lo = hi = mid = 1.0
    for p, nn in ps_:
        se = math.sqrt(max(p * (1 - p), .01) / (nn + 10)); mid *= p; lo *= max(p - 1.3 * se, 0); hi *= min(p + 1.3 * se, 1)
    return lo, mid, hi
lo, mid, hi = faixa([pr["por_diretor"][n] for n in board if n in pr["por_diretor"]]); ac, tt = pr["backtest"]
pas = d.barras([(n, p, f"n={k}") for n, (p, k) in pr["por_diretor"].items()], lambda v: f"{v:.0%}")
fut = (f'<p>{d.selo("estimativa — não é certeza")}</p><div class="nums" style="grid-template-columns:1fr 1fr"><div><b>{pr["placar_esperado"][0]} × {pr["placar_esperado"][1]}</b><span>placar mais provável</span></div>'
       f'<div><b>{100 * lo:.0f}–{"≥99" if hi >= .99 else f"{100 * hi:.0f}"}%</b><span>chance de decisão unânime com o relator</span></div></div>'
       f'<ul class="arr"><li>O voto do relator define o resultado na grande maioria dos casos.</li><li>Pode mudar: troca de diretor (mandatos em dez/2026 e fev/2027), voto-vista, divergência do Diretor-Geral em metodologia de cálculo.</li>'
       f'<li>Teste no passado: acertou {ac} de {tt} ({100 * ac / max(tt, 1):.0f}%) — igual à taxa de unanimidade; a regra não antecipa divergências.</li></ul>')
S.append(d.tecnica("05 · Antecipar", "Previsão para os próximos processos da empresa", d.grade(d.conceito("Passado", "Quanto cada diretor acompanha o relator", f"temas {', '.join(t.replace('_', ' ') for t in pr['temas'])} · 3 anos", texto=pas),
                                                                                                 d.conceito("Futuro", "O que esperar", "", texto=fut), cols=2), AG,
                   "Estimativa estatística a partir do histórico de votos; não substitui a publicação oficial nem orientação jurídica. Legenda automática pode errar nomes e números.", CLI))
cob = f"Base: {len(its)} decisões da diretoria da {NOME} sobre a empresa desde 2018, com o voto de cada diretor e link para o vídeo oficial no minuto. Fontes públicas (vídeos das reuniões, pautas e calendário da agência, Senado, DOU). Previsões são estimativas."
S.append(d.fim(cob, EMP.get("contato", "Circle Consultoria em parceria com Grupo Nery"), DIV[0]))
print(d.documento(S, f"{nome_curto} · {NOME}", f"{P}/relatorio_empresa"), len(S), "páginas")
