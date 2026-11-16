"""Documento «Monitoramento de processos: os 8 blocos» para 1–3 processos de um cliente (padrão Grupo Nery, página cheia).
Blocos: 1 visão geral · 2 mapeamento · 3 inteligência de prazo · 4 agenda · 5 quem conduz · 6 busca e banco · 7 comparativa · 8 visão do cliente.
Uso: python3 pipeline/monitor_8blocos.py clientes/<x>/<pasta> "<proc principal>[,<relacionados>]" "<proc2>[,...]"
   ex.: ... "50300.000128/2023,50300.012675/2026,50300.009640/2026" "50300.008966/2023,50300.015279/2026"
Saída: <pasta>/monitoramento_8_blocos.pdf. Dados do SEI só aparecem se o cliente informar (processos.json); senão, «a informar pelo cliente»."""
import sys, os, re, json, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, prazos, similares, mapa_tema, design as d
from desfecho import desfecho_item
E = d.E

P = sys.argv[1].rstrip("/"); GRUPOS = [g.split(",") for g in sys.argv[2:]]
EMP = json.load(open(f"{P}/empresa.json")); AG = EMP.get("agencias", ["antaq"])[0]; D = "data" if AG == "antt" else f"data/{AG}"
ld = lambda p, x: json.load(open(p)) if os.path.exists(p) else x
MAN = ld(f"{P}/desfechos_manuais.json", {}); NAR = ld(f"{P}/narrativas.json", {}); PJ = {prazos.chave(x["processo"]): x for x in ld(f"{P}/processos.json", []) if prazos.chave(x.get("processo"))}
ROT = {"favorável": "a favor da empresa", "parcial": "em parte", "neutro": "sem efeito direto", "desfavorável": "contra a empresa", "pendente": "sem decisão ainda"}
c = previsao.conn(AG); HOJE = datetime.date.today()
des = lambda i: ROT.get(x := ((MAN.get(str(i)) or {}).get("desfecho") or desfecho_item(c, i)), x)
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if s and re.match(r"\d{4}-\d\d-\d\d", str(s)) else str(s or "")
link = mapa_tema.link
KIT = d.kit(EMP.get("setor") or d.SETOR_AG.get(AG, "portos")); FT = EMP.get("foto_capa") or KIT["capa"]; FOCO = EMP.get("foco", "50% 55%"); CLI = EMP.get("logo")
bios = {b["diretor"]: b for b in ld(f"{D}/bios.json", [])}
cal = [x for x in ld(f"{D}/calendario.json", []) if x["data"] >= HOJE.isoformat()][:3]
sups = ld(f"{D}/superintendentes.json", [])
its_emp = previsao.itens_empresa(c, EMP["aliases"])
ALI, IP = MAN.get("_processos_alias", {}), MAN.get("_item_processo", {})
chave = lambda i: (lambda k: ALI.get(k, k))(IP.get(str(i["id"])) or prazos.chave(i["processo"]))
DUR = prazos.duracoes(AG)


def votos(iid):
    return list(c.execute("select * from votos where item_id=? order by eh_relator desc, id", (iid,)))


def processo(grupo):
    principal = grupo[0]
    sess = sorted([i for i in its_emp if chave(i) in grupo], key=lambda i: (i["data"], str(i["item"])))
    tema = (c.execute("select tema from item_temas where item_id=? limit 1", (sess[0]["id"],)).fetchone() or ["outros"])[0] if sess else "outros"
    pend = [k for k in grupo if not any(chave(i) == k for i in sess)]
    return {"principal": principal, "grupo": grupo, "sess": sess, "tema": tema, "pend": pend, "pj": PJ.get(principal, {})}


PR = [processo(g) for g in GRUPOS]
nome_curto = EMP["nome"].split("(")[0].strip()


def titulo(p):
    return (p["pj"].get("titulo") or (p["sess"][0]["assunto"] if p["sess"] else p["principal"]))


def status(p):
    if p["pend"]: return "em andamento (desdobramento a julgar)"
    u = p["sess"][-1] if p["sess"] else None
    if not u: return "sem sessão na diretoria"
    r = (u["resultado"] or "").lower()
    return "retirado de pauta" if "retirad" in r else "com vista" if re.match(r"\s*(pedido de )?vista", r) else "decidido"


def fala(i, n=1, diretor=None):
    out = []
    for v in votos(i["id"]):
        if diretor and v["diretor"] != diretor: continue
        if v["trecho"]: out.append(v)
        if len(out) >= n: break
    return out


def tabela_falas(lista, n=4):
    rows, vistos = [], set()
    for i in lista:
        for v in fala(i, 3):
            if v["trecho"][:60] in vistos: continue
            vistos.add(v["trecho"][:60])
            rows.append([f'{fmtd(i["data"])}<br><span class="nw">{i["numero"]}ª, item {E(str(i["item"]))}</span>', f'<b>{E(v["diretor"])}</b>{" (relator)" if v["eh_relator"] else ""}<br><span style="color:#6B7780">{E((v["justificativa"] or v["voto"] or "")[:120])}</span>',
                         f'<i>«{E(v["trecho"][:230])}»</i> <a href="{link(i["video_id"], v["ts"] or i["ts"], v["trecho_t"])}">▶ minuto</a>'])
            if len(rows) >= n: break
        if len(rows) >= n: break
    return d.tabela(["Sessão", "Quem e o voto", "O que foi dito (trecho literal)"], rows, ["13%", "30%", "57%"]) if rows else ""


def col(p, corpo, k):
    return f'<div><div class="ccn">Processo {k + 1}</div><div class="cct">↳ {E(p["principal"])}</div><div class="ccs">{E(titulo(p)[:110])}</div>{corpo}</div>'


S = []
nums = [(len(PR), "processos monitorados neste documento"), (sum(len(p["sess"]) for p in PR), "sessões da diretoria sobre eles"), (sum(1 for p in PR if status(p) != "decidido"), "em andamento"), (len(cal), "próximas reuniões no calendário")]
S.append(d.capa(FT, FOCO, f"Monitoramento de processos · {d.NOME_AG.get(AG, AG.upper())}", nome_curto, "Os 8 blocos do monitoramento, aplicados a processos reais",
                "Monitorar → analisar → antecipar. Fontes públicas da agência; informações do cliente aparecem identificadas; estimativas não são certeza.", nums, CLI))
BL = [("Visão geral", "status, etapa, relator e responsáveis"), ("Mapeamento do processo", "linha do tempo sessão a sessão"), ("Inteligência de prazo", "tempo até cada marco e comparação"),
      ("Agenda regulatória", "próximas reuniões e associação com o processo"), ("Inteligência sobre a agência", "quem conduz e como atua no tema"), ("Busca e banco de dados", "o que a base devolve sobre o processo"),
      ("Inteligência comparativa", "casos semelhantes, padrões e justificativas"), ("Visão do cliente", "resumo, marcos, alertas e ações")]
S.append(d.sumario(BL, KIT["divisores"][0]))
SEC = lambda k: f"{k:02d} · {BL[k - 1][0]}"

# 1 visão geral
cols = []
for k, p in enumerate(PR):
    u = p["sess"][-1] if p["sess"] else None
    linhas = [("Status", status(p)), ("Etapa atual", p["pj"].get("etapa_sei") or ("julgamento do desdobramento " + ", ".join(p["pend"]) if p["pend"] else "decisão final da diretoria publicada")),
              ("Relator(es)", ", ".join(dict.fromkeys(i["relator"] for i in p["sess"] if i["relator"])) or "a definir"),
              ("Área técnica", p["pj"].get("area") or "a informar pelo cliente (SEI)"), ("Tema", p["tema"].replace("_", " ")),
              ("Sessões na diretoria", f'{len(p["sess"])} (de {fmtd(p["sess"][0]["data"])} a {fmtd(u["data"])})' if u else "nenhuma"),
              ("Última decisão", f'{u["numero"]}ª, item {u["item"]}: {(u["resultado"] or "")[:120]} ({des(u["id"])}) <a href="{link(u["video_id"], u["ts"])}">▶ minuto</a>' if u else "")]
    cols.append(col(p, d.tabela(["Campo", "Situação"], [[E(a), b if "<a" in str(b) else E(b)] for a, b in linhas], ["30%", "70%"]), k))
S.append(d.tecnica(SEC(1), "Onde cada processo está", d.grade(*cols, cols=len(PR)) + d.conceito("", "Movimentações mais relevantes", "as últimas sessões dos dois processos, com o que foi dito", texto=tabela_falas(sorted([i for p in PR for i in p["sess"]], key=lambda i: i["data"], reverse=True), 2)), AG,
                   "Etapa no SEI e área técnica: informadas pelo cliente (processos.json); sem essa informação aparece «a informar».", CLI))

# 2 mapeamento (1 página por processo)
for k, p in enumerate(PR):
    rows = []
    for i in p["sess"]:
        vs = votos(i["id"]); vt = ", ".join(f'{v["diretor"].split()[0]}: {"relator" if v["eh_relator"] else (v["categoria"] or "vota")}' for v in vs)
        f1 = fala(i, 1); tr = f'<i>«{E(f1[0]["trecho"][:150])}»</i> ' if f1 else ""
        rows.append([f'{fmtd(i["data"])}<br><span class="nw">{i["numero"]}ª, item {E(str(i["item"]))}</span>', f'{E((i["assunto"] or "")[:120])}<br><span style="color:#6B7780">{E(vt)}</span>', f'{E((i["resultado"] or "")[:110])} → <b>{E(des(i["id"]))}</b>', f'{tr}<a href="{link(i["video_id"], (f1[0]["ts"] if f1 else None) or i["ts"])}">▶ minuto</a>'])
    prox = [["a seguir", " / ".join(p["pend"]) + ": desdobramento ainda sem sessão na diretoria", "próximo passo previsto", (f'{cal[0]["reuniao"]}ª reunião, {fmtd(cal[0]["data"])}' if cal else "calendário")]] if p["pend"] else []
    S.append(d.tecnica(SEC(2), f"Processo {k + 1}: {p['principal']}, passo a passo", f'<p class="lead" style="font-size:9.5pt;margin:0 0 .1in">{E(titulo(p))}</p>' + d.tabela(["Sessão", "O que estava em jogo e como votaram", "Resultado", "Fala e vídeo"], rows + prox, ["11%", "39%", "24%", "26%"]), AG,
                       "Votos por diretor a partir do vídeo da sessão (legenda automática); minuto de quem só acompanha o relator é aproximado. Movimentações internas do SEI: a informar pelo cliente.", CLI))

# 3 prazo
cols = []
for k, p in enumerate(PR):
    dd = [(i, (prazos._d(i["data"]) - prazos._d(p["sess"][0]["data"])).days) for i in p["sess"]] if p["sess"] else []
    e = prazos.estatistica(DUR, p["tema"])
    marcos = d.tabela(["Marco", "Data", "Dias desde a 1ª sessão"], [[f'{i["numero"]}ª: {E((i["resultado"] or "")[:60])}', fmtd(i["data"]), str(x)] for i, x in dd], ["55%", "20%", "25%"])
    if e and dd:
        tot = dd[-1][1] if status(p) == "decidido" and not p["pend"] else (HOJE - prazos._d(p["sess"][0]["data"])).days
        pos = "acima" if tot > e["p75"] else "abaixo" if tot < e["p25"] else "dentro"
        comp = (f'<p><b>{tot} dias</b> na diretoria {"até a decisão" if pos and not p["pend"] else "até hoje"}. Processos semelhantes ({E(p["tema"].replace("_", " "))}, n={e["n"]} com mais de uma sessão): mediana <b>{e["mediana"]:.0f} dias</b>, faixa típica {e["p25"]:.0f}–{e["p75"]:.0f}. '
                f'Este processo está <b>{pos}</b> da faixa.</p>' + (f'<p>{d.selo("estimativa")} Desdobramento pendente: se seguir a mediana, a decisão sairia por volta de {(HOJE + datetime.timedelta(days=int(e["mediana"]))).strftime("%m/%Y")} (inferência).</p>' if p["pend"] else ""))
    else:
        comp = "<p>Sem base comparável suficiente (menos de 5 semelhantes com mais de uma sessão).</p>"
    cols.append(col(p, marcos + comp, k))
por = collections.defaultdict(list)
for v in DUR.values(): por[v[1]].append(v)
est = sorted([(t, prazos.estatistica(DUR, t)) for t in por if prazos.estatistica(DUR, t)], key=lambda x: x[1]["mediana"])
S.append(d.tecnica(SEC(3), "Quanto tempo leva e como se compara", d.grade(*cols, cols=len(PR)) + d.conceito("", "Histórico de duração por tipo de processo", "mediana de dias na diretoria (processos com mais de uma sessão, desde 2018)", texto=d.barras([(t.replace("_", " "), e["mediana"], f'n={e["n"]} · faixa {e["p25"]:.0f}–{e["p75"]:.0f}') for t, e in est[:3]], lambda v: f"{v:.0f} d")), AG,
                   "Prazo medido da 1ª sessão da diretoria até a decisão; o tempo na área técnica antes da pauta depende das datas do SEI informadas pelo cliente. Estimativas não são certeza.", CLI))

# 4 agenda
ult = c.execute("select id, numero, data, video_id from reunioes order by data desc limit 1").fetchone()
ag_rows = [[f'{x["reuniao"]}ª', fmtd(x["data"]), E(x.get("formato", "")), "pauta publicada" if x.get("pauta") else "pauta a publicar", "; ".join(f'Processo {k + 1}: {"pode voltar (desdobramento pendente)" if p["pend"] else "sem previsão"}' for k, p in enumerate(PR))] for x in cal]
assoc = [[f'{i["numero"]}ª ({fmtd(i["data"])})', f'item {E(str(i["item"]))}', E(p["principal"]), E((i["resultado"] or "")[:80]), f'<a href="{link(i["video_id"], i["ts"])}">▶</a>'] for p in PR for i in p["sess"]]
S.append(d.tecnica(SEC(4), "Reuniões, pautas e o que cada uma decidiu", d.conceito("", "Próximas reuniões (calendário oficial)", "e a relação com os processos monitorados", texto=d.tabela(["Reunião", "Data", "Formato", "Pauta", "Processos"], ag_rows, ["9%", "11%", "14%", "14%", "52%"]))
                   + '<div style="height:.12in"></div>' + d.conceito("", "Reunião → item → processo → resultado", "todas as sessões dos processos monitorados", texto=d.tabela(["Reunião", "Item", "Processo", "Resultado", "Vídeo"], assoc, ["16%", "9%", "17%", "52%", "6%"]))
                   + d.conceito("", "Registro do resultado: o que foi dito na última sessão de cada processo", "", texto=tabela_falas([p["sess"][-1] for p in PR if p["sess"]], 1)), AG,
                   "Aviso prévio: o alerta pré-pauta sai quando a pauta é publicada (documento do boletim). Reuniões virtuais da ANTAQ não têm vídeo: resultado só em ata.", CLI))

# 5 quem conduz
rels = list(dict.fromkeys(i["relator"] for p in PR for i in p["sess"] if i["relator"]))[:3]
cards = []
for n in rels:
    b = bios.get(n, {}); m = mapa_tema.mapear(AG, "|".join(re.escape(x) for x in EMP["aliases"]), "2018-01-01")["por_diretor"].get(n, {})
    foto = next((f for f in [b.get("foto"), f"{D}/dirigentes/{re.sub(r'[^a-z0-9]+', '-', n.lower())}.jpg"] if f and os.path.exists(f)), None)
    fh = f'<div class="av" style="background-image:url({d.b64(foto)})"></div>' if foto else '<div class="av ini">' + E("".join(w[0] for w in n.split()[:2])) + "</div>"
    cards.append(d.pessoa(fh, n, (b.get("cargo") or "Diretor(a)")[:80], [E((b.get("minibio") or "")[:300]), f'<span style="color:#6B7780">Formação: {E((b.get("formacao") or "")[:110])}</span>',
                                                                       f'Nos processos da empresa desde 2018: <b>{sum(1 for i in its_emp if i["relator"] == n)}</b> relatorias; nestes processos: <b>{sum(1 for p in PR for i in p["sess"] if i["relator"] == n)}</b>.']))
sp = [s for s in sups if re.search(r"regula|outorga|portu|fiscaliz", (s.get("superintendencia") or s.get("cargo") or ""), re.I)][:4]
S.append(d.tecnica(SEC(5), "Quem conduz os processos", d.grade(*cards, cols=min(len(cards), 3) or 1) + '<div style="height:.12in"></div>' + d.conceito("", "Superintendências que instruem esses temas", "quem prepara a análise técnica antes da diretoria",
                   texto='<ul class="arr sm">' + "".join(f'<li><b>{E(s.get("nome", ""))}</b>, {E((s.get("superintendencia") or s.get("cargo") or "")[:80])}</li>' for s in sp) + "</ul>"), AG, "Perfis com fontes oficiais; mandatos conferidos com o DOU.", CLI))

# 6 busca e banco
tot = c.execute("select count(*), min(r.data) from itens i join reunioes r on r.id=i.reuniao_id where r.data>='2018-01-01'").fetchone()
cons = []
for k, p in enumerate(PR):
    q = re.sub(r"[^\w\s]", " ", titulo(p))[:120]
    sim = [x for x in similares.similares(AG, q, 10) if not any(x["id"] == i["id"] for i in p["sess"])][:5]
    cons.append(col(p, f'<p style="color:#6B7780">Consulta: “{E(q[:80])}” → {len(sim)} casos mais parecidos na base</p>' + d.tabela(["Sessão", "Assunto", "Desfecho", "Relator", ""], [[f'{fmtd(s["data"])}<br>{s["numero"]}ª', E((s["assunto"] or "")[:90]), E(ROT.get(s["desfecho"], s["desfecho"])), E(s["relator"] or ""), f'<a href="{s["link"]}">▶</a>'] for s in sim], ["15%", "50%", "14%", "15%", "6%"]), k))
S.append(d.tecnica(SEC(6), "O que a base devolve sobre estes processos", d.numeros([(f"{tot[0]:,}".replace(",", "."), f"decisões da diretoria desde {fmtd(tot[1])[-4:]}"), (len(its_emp), "decisões sobre a empresa"), (sum(len(p["sess"]) for p in PR), "sessões destes processos"), ("3+ anos", "histórico mínimo consultável")]) + d.grade(*cons, cols=len(PR)), AG,
                   "Busca por processo, empresa, tema ou diretor; cruzamento processo × reunião × pauta. Base consultada sob demanda (consulta avulsa).", CLI))

# 7 comparativa
cols = []
for k, p in enumerate(PR):
    sim = similares.similares(AG, re.sub(r"[^\w\s]", " ", titulo(p))[:120], 12)
    ids = [x["id"] for x in sim if not any(x["id"] == i["id"] for i in p["sess"])][:6]
    q = ",".join("?" * len(ids)) or "null"
    rs = list(c.execute(f"select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where i.id in ({q}) order by r.data desc", ids))
    cnt = collections.Counter(ROT.get(x["desfecho"], x["desfecho"]) for x in sim[:8])
    padrao = f'<p><b>Padrão nos {min(len(sim), 8)} casos mais parecidos:</b> ' + ", ".join(f"{v} {k_}" for k_, v in cnt.most_common()) + ".</p>"
    cols.append(col(p, padrao + tabela_falas(rs, 3), k))
S.append(d.tecnica(SEC(7), "Como a agência decidiu casos parecidos", d.grade(*cols, cols=len(PR)), AG,
                   "Casos semelhantes por busca de texto (assunto e resumo). Diferença de desfecho não é contradição por si só: leia as justificativas (inferência).", CLI))

# 8 visão do cliente (1 página por processo, formato whitepaper)
for k, p in enumerate(PR):
    u = p["sess"][-1] if p["sess"] else None
    e = prazos.estatistica(DUR, p["tema"])
    nar = next((NAR[x] for x in ("atu12", "passivo", "item17", "painel") if x in NAR and p["principal"][:12] in " ".join(NAR[x].get("paragrafos", []))), None)
    itens = [("Status e etapa", f"<p>{E(status(p))}. {E(p['pj'].get('etapa_sei') or 'Etapa no SEI: a informar pelo cliente.')}</p>"),
             ("Próximos marcos", f"<p>{E('Julgamento de ' + ', '.join(p['pend']) + '.' if p['pend'] else 'Cumprimento da decisão e eventual recurso.')} Próximas reuniões: " + E(", ".join(f'{x["reuniao"]}ª em {fmtd(x["data"])}' for x in cal) or "calendário a publicar") + ".</p>"),
             ("Prazo estimado", f'<p>{d.selo("estimativa")} ' + (f'mediana de {e["mediana"]:.0f} dias para o tema (faixa {e["p25"]:.0f}–{e["p75"]:.0f}, n={e["n"]}).' if e else "sem base comparável suficiente.") + "</p>"),
             ("Responsáveis", f"<p>Relator: {E(u['relator'] if u and u['relator'] else 'a definir')}. Área técnica: {E(p['pj'].get('area') or 'a informar pelo cliente')}.</p>"),
             ("Alertas e ações", "<p>" + (" ".join(E(x) for x in (nar or {}).get("paragrafos", [])[:1])[:700] if nar else f"Acompanhar a pauta das próximas reuniões; preparar memorial com os argumentos que convenceram a diretoria nos casos parecidos (bloco 7).") + "</p>")]
    S.append(d.tecnica(SEC(8), f"Processo {k + 1}: o resumo para a empresa", d.whitepaper(p["principal"], itens, intro=f"<p>{E(titulo(p))}</p>") + d.conceito("", "Histórico do processo nas falas da diretoria", "", texto=tabela_falas(p["sess"][::-1], 3)), AG, "Resumo para decisão. Estimativas não são certeza; informações do SEI dependem do cliente.", CLI))

S.append(d.fim("Fontes públicas: vídeos oficiais das reuniões, pautas e calendário da agência, Senado e DOU. Informações do cliente aparecem identificadas. Prazos, previsões e comparações são estimativas e inferências.",
               EMP.get("contato", "Circle Consultoria em parceria com Grupo Nery"), KIT["divisores"][0]))
print(d.documento(S, f"Monitoramento 8 blocos · {nome_curto}", f"{P}/monitoramento_8_blocos"), len(S), "páginas")
