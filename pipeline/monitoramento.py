"""Monitoramento de Processos: documentos 3 e 4 do pacote (mesmo visual do relatório em painel).
  raio_x  → «Raio-X dos Processos» (blocos 1 Visão geral, 2 Mapeamento, 3 Prazo, 8 Visão do cliente)
  agenda  → «Agenda e Inteligência Comparativa» (blocos 4 Agenda, 6 Busca, 7 Comparativa)
Uso: python3 pipeline/monitoramento.py clientes/<x>/<pasta> raio_x|agenda
Dados do cliente (opcional, fora do git): <pasta>/processos.json
  [{"processo": "50300.008966/2023-83", "titulo": "...", "etapa_sei": "...", "area": "SOG/GPO", "andamentos": [{"data": "AAAA-MM-DD", "texto": "..."}]}]
Sem processos.json: usa os processos que já passaram pela diretoria e marca «etapa no SEI: a informar»."""
import sys, os, re, json, html, base64, datetime, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design as dz, previsao, mapa_tema, similares, prazos
from desfecho import desfecho_item
from pdf_leve import leve_html, leve_pdf

P, MODO = sys.argv[1].rstrip("/"), sys.argv[2]
if not os.path.exists(f"{P}/empresa.json"): sys.exit(f"Pasta do cliente sem empresa.json: {P} (a pasta clientes/ fica só no chat, fora do git)")
EMP = json.load(open(f"{P}/empresa.json")); AG = EMP.get("agencias", ["antaq"])[0]
D = "data" if AG == "antt" else f"data/{AG}"; NOME = {"antt": "ANTT", "anm": "ANM", "antaq": "ANTAQ", "aneel": "ANEEL"}.get(AG, AG.upper())
E = html.escape; HOJE = datetime.date.today(); TRES = (HOJE - datetime.timedelta(days=3 * 365)).isoformat()
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
MAN = ld(f"{P}/desfechos_manuais.json", {})
AC, AC2, GOLD = dz.AZUL, dz.LILAS, dz.AZUL2
b64 = lambda p: ("data:image/" + p.rsplit(".", 1)[-1].replace("jpg", "jpeg") + ";base64," + base64.b64encode(open(p, "rb").read()).decode()) if p and os.path.exists(p) else ""
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if s and re.match(r"\d{4}-\d\d-\d\d", str(s)) else str(s or "—")
c = previsao.conn(AG)
des = lambda iid: (MAN.get(str(iid)) or {}).get("desfecho") or desfecho_item(c, iid)
CORES = {"favorável": dz.TONS[0], "parcial": dz.TONS[2], "neutro": dz.TONS[4], "desfavorável": dz.TINTA, "pendente": dz.LILAS}
LOGO_B, LOGO_P = b64("docs/marca/circle/logo_circle_branco.png"), b64("docs/marca/circle/logo_circle_preto.png")
NERY_B, CLI, FOTO = b64("docs/marca/grupo_nery/logo_branco.png"), b64(EMP.get("logo")), b64(EMP.get("foto_capa"))
nome_curto = EMP["nome"].split("(")[0].strip()
cal = [x for x in ld(f"{D}/calendario.json", []) if x["data"] >= HOJE.isoformat()][:3]
S = []


def top(n, t):
    return (f'<header class="hd"><span class="num">{n:02d}</span><span>{E(NOME)} · {E(t)}</span><span class="sp"></span>'
            + (f'<img src="{CLI}" class="hcli">' if CLI else "") + f'<img src="{dz.img("nery_a")}" class="hl"></header>')


KIT = dz.kit(EMP.get("setor") or dz.SETOR_AG.get(AG, "portos")); FOTOP = EMP.get("foto_capa") or KIT["capa"]; FOCO = EMP.get("foco", "50% 55%")


def capa(titulo, sub, blocos, kps):
    S.append(dz.capa(FOTOP, FOCO, f"Monitoramento de processos · {NOME}", titulo, f"{nome_curto} · {sub}", f"Emitido em {HOJE:%d/%m/%Y} · fontes públicas + informações do cliente (identificadas) · estimativas não são certeza",
                    [(re.sub("<[^>]+>", "", str(a)), t) for a, t in kps][:4], EMP.get("logo")))
    S.append(dz.sumario([(re.sub(r"^\d+ · ", "", b), "") for b in blocos], KIT["divisores"][0]))


def falas(lista, n=5):
    """linhas «sessão · quem → trecho literal ▶ minuto» a partir dos votos com trecho (relator primeiro)."""
    rows, vistos = [], set()
    for i in lista:
        for v in c.execute("select * from votos where item_id=? and trecho is not null and trecho!='' order by eh_relator desc, id limit 3", (i["id"],)):
            if v["trecho"][:60] in vistos: continue
            vistos.add(v["trecho"][:60])
            rows.append(f'<tr><td class="pn">{fmtd(i["data"])}<br>{i["numero"]}ª, item {E(str(i["item"]))}</td><td><b>{E(v["diretor"])}</b>{" (relator)" if v["eh_relator"] else ""}<br><span class="pn">{E((v["justificativa"] or v["voto"] or "")[:110])}</span></td>'
                        f'<td><i>«{E(v["trecho"][:220])}»</i> <a href="{mapa_tema.link(i["video_id"], v["ts"] or i["ts"], v["trecho_t"])}">▶ minuto</a></td></tr>')
            if len(rows) >= n: break
        if len(rows) >= n: break
    return ('<table class="tb"><tr><th style="width:12%">Sessão</th><th style="width:30%">Quem e o voto</th><th>O que foi dito (trecho literal da legenda)</th></tr>' + "".join(rows) + "</table>") if rows else ""


def itens_ids(ids):
    q = ",".join("?" * len(ids)) or "null"
    rs = {r["id"]: r for r in c.execute(f"select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where i.id in ({q})", list(ids))}
    return [rs[x] for x in ids if x in rs]


def semelhantes(lst, n=3):
    if not lst: return []
    ids = {i["id"] for i in lst}
    sim = [x["id"] for x in similares.similares(AG, lst[-1]["assunto"] or "", 12) if x["id"] not in ids and "não lido" not in (x["assunto"] or "")]
    if sim: return itens_ids(sim[:n * 2])
    nums = {i["numero"] for i in lst}
    return [x for x in its if x["numero"] in nums and x["id"] not in ids]  # assunto ilegível: outros itens da empresa na mesma sessão


# processos do cliente
its = [i for i in previsao.itens_empresa(c, EMP["aliases"]) if i["data"] >= "2018-01-01"]
PJ = {prazos.chave(x["processo"]): x for x in ld(f"{P}/processos.json", []) if prazos.chave(x.get("processo"))}
ALI = MAN.get("_processos_alias", {})  # números lidos de forma diferente pela legenda → mesmo processo
ITEM_PROC = MAN.get("_item_processo", {})
grupos = collections.OrderedDict()
for i in its:
    k = ITEM_PROC.get(str(i["id"])) or prazos.chave(i["processo"]); k = ALI.get(k, k) if k else k
    k = k or f"sem nº · {i['assunto'][:40]}"
    grupos.setdefault(k, []).append(i)
for k in PJ:
    grupos.setdefault(k, [])
DUR = prazos.duracoes(AG)

if MODO == "raio_x":
    def status(lst):
        if not lst: return "em instrução (antes da diretoria)"
        u = lst[-1]; r = (u["resultado"] or "").lower()
        if re.match(r"\s*(retirad|não lido|nao lido)", r): return "retirado de pauta"
        if re.match(r"\s*((pedido de |renovação de |renovacao de )?vista|vista renovada|convertido.*dilig)", r): return "com vista"
        return "decidido"
    procs = sorted(grupos.items(), key=lambda kv: (kv[1][-1]["data"] if kv[1] else "9999"), reverse=True)
    ativos = [kv for kv in procs if status(kv[1]) != "decidido"]
    capa("Raio-X dos Processos", "status, linha do tempo e prazo de cada processo", ["1 · Visão geral", "2 · Mapeamento do processo", "3 · Inteligência de prazo", "8 · Visão do cliente"],
         [(len(procs), "processos monitorados"), (len(ativos), "em aberto (vista, retirado ou em instrução)"), (sum(1 for k in grupos if k in PJ), "com etapa do SEI informada"), (len(cal), "próximas reuniões oficiais")])
    # visão geral
    linhas = ""
    for k, lst in procs[:15]:
        st = status(lst); u = lst[-1] if lst else None; pj = PJ.get(k, {})
        d = DUR.get(k); tema = d[1] if d else (pj.get("tema") or "—")
        linhas += (f'<tr><td><span class="st st-{st.split()[0]}">{E(st)}</span></td><td class="pn">{E(k)}</td><td>{E((pj.get("titulo") or (u["assunto"] if u else ""))[:90])}</td>'
                   f'<td>{E(pj.get("area") or (u["relator"] if u else "") or "—")}</td><td>{E(pj.get("etapa_sei") or "a informar")}</td><td>{fmtd(u["data"]) if u else "—"}</td></tr>')
    S.append(f'''<section class="pg">{top(1, "Visão geral")}<h2>Processos da empresa: onde cada um está</h2><div class="card"><table class="tb"><tr><th>Status</th><th>Processo</th><th>Assunto</th><th>Responsável (relator / área)</th><th>Etapa no SEI</th><th>Última sessão</th></tr>{linhas}</table>
<p class="nt">Status pela última sessão da diretoria. Etapa no SEI e área técnica: informadas pelo cliente (processos.json); sem essa informação aparece «a informar». Nº do processo vem da legenda; conferir no SEI.</p></div></section>''')
    # mapeamento: linha do tempo dos processos em aberto + 3 mais recentes
    foco = (ativos + [kv for kv in procs if kv not in ativos])[:3]
    for n, (k, lst) in enumerate(foco, 2):
        pj = PJ.get(k, {})
        ev = [(a["data"], "SEI (cliente)", a["texto"], None) for a in pj.get("andamentos", [])]
        ev += [(i["data"], f"{i['numero']}ª reunião · item {i['item']}", f"{i['assunto'][:120]}: {(i['resultado'] or '')[:80]} ({des(i['id'])})", mapa_tema.link(i["video_id"], i["ts"])) for i in lst]
        ev.sort()
        tl = "".join(f'<div class="vt"><span class="vd">{fmtd(d)}</span><i style="background:{AC if "reunião" in o else AC2}"></i><div><b>{E(o)}</b> {E(t)} {f"<a href={chr(34)}{lk}{chr(34)}>▶</a>" if lk else ""}</div></div>' for d, o, t, lk in ev)
        st = status(lst); d = DUR.get(k); e = prazos.estatistica(DUR, d[1]) if d else None
        if e and d and d[2] > 1:
            pos = "acima" if d[0] > e["p75"] else "abaixo" if d[0] < e["p25"] else "dentro"
            pz = f'<div class="pz"><b>{d[0]} dias</b> na diretoria até {"a decisão" if d[3] else "hoje"} · semelhantes ({E(d[1].replace("_", " "))}, n={e["n"]}): mediana <b>{e["mediana"]:.0f}</b> dias, faixa típica {e["p25"]:.0f}–{e["p75"]:.0f} → <b>{pos}</b> da faixa</div>'
        elif d and d[2] <= 1 and e:
            pz = f'<div class="pz">{"Decidido na 1ª sessão da diretoria (sem vista ou retirada); não entra na comparação de prazo." if d[3] else f"{d[0]} dias desde a 1ª sessão; a comparação passa a valer se voltar à pauta."} Referência ({E(d[1].replace("_", " "))}, n={e["n"]}): mediana {e["mediana"]:.0f} dias, faixa {e["p25"]:.0f}–{e["p75"]:.0f}.</div>'
        else: pz = '<div class="pz">Prazo: sem base comparável suficiente (menos de 5 processos semelhantes com mais de uma sessão).</div>'
        prox = ("Próximo passo provável: volta à pauta na " + (f"{cal[0]['reuniao']}ª ({fmtd(cal[0]['data'])}, {cal[0]['formato']}) ou {cal[1]['reuniao']}ª ({fmtd(cal[1]['data'])})" if len(cal) > 1 else "próxima reunião") + " (inferência).") if st != "decidido" else "Decidido. Próximo passo: cumprimento/recurso, se houver (acompanhar publicação do acórdão)."
        S.append(f'''<section class="pg">{top(n, "Mapeamento do processo")}<h2>{E(k)} · {E(status(lst))}</h2><p class="lead">{E((pj.get("titulo") or (lst[-1]["assunto"] if lst else ""))[:200])}</p>
<div class="g2"><div class="card"><h3>Linha do tempo</h3><div class="vtl">{tl or "<p class=nt>Sem sessões na diretoria ainda.</p>"}</div></div>
<div class="col"><div class="card"><h3>Prazo (inteligência de prazo)</h3>{pz}<p class="nt">Medido da 1ª sessão da diretoria até a decisão final, só para processos com mais de uma sessão. Com as datas do SEI informadas pelo cliente, a medida passa a ir da entrada até a decisão.</p></div>
<div class="card"><h3>Próximos passos e alertas</h3><p>{E(prox)}</p><p class="nt">Etapa no SEI: {E(pj.get("etapa_sei") or "a informar pelo cliente")} · área: {E(pj.get("area") or "a informar")}</p></div></div></div>
{f'<div class="card mt"><h3>O que foi dito na diretoria sobre este processo</h3>{fl}</div>' if (fl := falas(lst[::-1], 4)) else ""}
{f'<div class="card mt"><h3>Casos semelhantes (ou, sem assunto legível, os outros itens da empresa na mesma sessão), com o que foi dito</h3>{fs}</div>' if (fl.count("<tr>") < 3 and (fs := falas(semelhantes(lst), 4 - fl.count("<tr>") + (1 if not fl else 0)))) else ""}</section>''')
    # prazos por tipo
    n = len(foco) + 2
    import statistics
    por = collections.defaultdict(list)
    for v in DUR.values(): por[v[1]].append(v)
    est = [(t, prazos.estatistica(DUR, t)) for t in por]; est = [(t, e) for t, e in est if e]
    mx = max([e["p75"] for _, e in est] + [1])
    bars = "".join(f'<div class="pb"><span class="bl">{E(t.replace("_", " "))}</span><span class="bt"><i class="iqr" style="left:{100 * e["p25"] / mx:.0f}%;width:{100 * (e["p75"] - e["p25"]) / mx:.0f}%"></i><i class="md" style="left:{100 * e["mediana"] / mx:.0f}%"></i></span><b>{e["mediana"]:.0f} d</b><em>n={e["n"]}</em></div>' for t, e in sorted(est, key=lambda x: x[1]["mediana"]))
    S.append(f'''<section class="pg">{top(n, "Inteligência de prazo")}<h2>Quanto tempo a diretoria leva, por tipo de processo</h2><div class="card"><div class="lgx"><i class="iqr"></i>faixa típica (25%–75%) <i class="md"></i>mediana</div>{bars}
<p class="nt">Processos que passaram por mais de uma sessão da diretoria (vista, retirada, retorno), desde 2018. Estimativa: não inclui o tempo na área técnica antes da pauta.</p></div>
<div class="card mt"><h3>Quando um processo da empresa demorou: vistas e retiradas, com o que foi dito</h3>{falas([i for i in its if re.search("vista|retirad", (i["resultado"] or "").lower())][::-1], 4) or "<p>Nenhum processo da empresa teve vista ou retirada.</p>"}</div></section>''')
    out = f"{P}/raio_x_processos"
else:
    temas = EMP.get("temas_consultoria", [])
    capa("Agenda e Inteligência Comparativa", "o que vem pela frente e como a agência decidiu casos parecidos", ["4 · Agenda regulatória", "6 · Busca e banco de dados", "7 · Inteligência comparativa"],
         [(len(cal), "próximas reuniões oficiais"), (len(its), "decisões sobre a empresa desde 2018"), (len(temas), "temas monitorados"), ("3 anos", "recorte padrão (contexto desde 2018)")])
    # agenda
    pautas = {str(x.get("reuniao")): x for x in (ld(f, {}) for f in __import__("glob").glob(f"{D}/pautas/*.json"))}
    ag_h = "".join(f'<tr><td><b>{x["reuniao"]}ª</b></td><td>{fmtd(x["data"])}</td><td>{E(x.get("formato", ""))}</td><td>{("<a href=" + chr(34) + pautas[x["reuniao"]]["pauta"] + chr(34) + ">pauta publicada</a>") if pautas.get(x["reuniao"], {}).get("itens") else "pauta a publicar"}</td><td>{"sem transmissão; resultado em ata" if x.get("formato") == "virtual" else "transmitida (link no minuto no dia seguinte)"}</td></tr>' for x in cal)
    ult = c.execute("select id, numero, data, video_id from reunioes order by data desc limit 1").fetchone()
    RX = re.compile("|".join(map(re.escape, EMP["aliases"])), re.I)
    res = "".join(f'<li><b>Item {E(str(i["item"]))}</b> {E((i["assunto"] or "")[:110])}: <i>{E((i["resultado"] or "")[:70])}</i> <a href="{mapa_tema.link(ult["video_id"], i["ts"])}">▶</a></li>' for i in c.execute("select * from itens where reuniao_id=?", (ult["id"],)) if RX.search(f"{i['interessado'] or ''} {i['assunto'] or ''}") or str(i["item"]) in map(str, EMP.get("itens_acompanhar", [])))
    S.append(f'''<section class="pg">{top(1, "Agenda regulatória")}<h2>Próximas reuniões e resultado da última</h2><div class="g2"><div class="card"><h3>Calendário oficial</h3><table class="tb"><tr><th>Reunião</th><th>Data</th><th>Formato</th><th>Pauta</th><th>Resultado</th></tr>{ag_h}</table>
<p class="nt">Calendário aprovado pela diretoria (fonte oficial em data/{AG}/calendario.json). O alerta pré-pauta sai quando a pauta é publicada.</p></div>
<div class="card"><h3>Resultado da {ult["numero"]}ª reunião ({fmtd(ult["data"])}) para a empresa</h3><ul class="lst">{res or "<li>Nenhum item da empresa.</li>"}</ul></div></div>
<div class="card mt"><h3>O que foi dito nas duas últimas reuniões sobre os itens da empresa</h3>{falas([i for i in its if i["numero"] in sorted({x["numero"] for x in its})[-2:]][::-1], 6) or "<p>Sem falas registradas.</p>"}</div></section>''')
    # comparativa por tema
    n = 1
    for tc in temas:
        n += 1; m = mapa_tema.mapear(AG, tc["regex"], TRES); itsm = m["itens"]
        decid = [i for i in itsm if des(i["id"]) != "pendente" and not re.match(r"\s*(retirad|(pedido de )?vista|vista renovada)", (i["resultado"] or "").lower())]
        ndiv = sum(1 for i in decid if c.execute("select 1 from votos where item_id=? and categoria in ('vencido','revisor_diverge')", (i["id"],)).fetchone())
        unan = 100 * (len(decid) - ndiv) / max(len(decid), 1); m["unanimes"] = len(decid) - ndiv; m_dec = len(decid); m_pend = len(itsm) - len(decid)
        relc = collections.Counter(i["relator"] for i in itsm if i["relator"])
        desf = collections.Counter(des(i["id"]) for i in itsm)
        # possíveis contradições: desfechos opostos no mesmo tema em < 24 meses
        mt = lambda i: {t for (t,) in c.execute("select microtema from item_microtema where item_id=?", (i["id"],))}
        op, usados = [], set()
        for k_, a in enumerate(decid):
            for b in decid[k_ + 1:]:
                if a["id"] in usados or b["id"] in usados: continue
                pa_, pb_ = (prazos.chave((c.execute("select processo from itens where id=?", (x["id"],)).fetchone() or [""])[0]) for x in (a, b))
                mesmo = (pa_ and pa_ == pb_) or (mt(a) & mt(b))
                if mesmo and {des(a["id"]), des(b["id"])} == {"favorável", "desfavorável"} and abs((prazos._d(b["data"]) - prazos._d(a["data"])).days) < 730:
                    op.append((a, b)); usados |= {a["id"], b["id"]}
        def just(i):
            r = c.execute("select justificativa from votos where item_id=? and eh_relator=1", (i["id"],)).fetchone()
            return (r[0] if r and r[0] else (i["resumo"] or ""))[:120]
        ct = "".join(f'<div class="ctr"><div><b>{fmtd(a["data"])} · {a["numero"]}ª</b> {E(a["assunto"][:80])} → <span style="color:{CORES[des(a["id"])]}">{des(a["id"])}</span><br><i>{E(just(a))}</i> <a href="{mapa_tema.link(a["video_id"], a["ts"])}">▶</a></div>'
                     f'<div><b>{fmtd(b["data"])} · {b["numero"]}ª</b> {E(b["assunto"][:80])} → <span style="color:{CORES[des(b["id"])]}">{des(b["id"])}</span><br><i>{E(just(b))}</i> <a href="{mapa_tema.link(b["video_id"], b["ts"])}">▶</a></div></div>' for a, b in op[-3:])
        prec = "".join(f'<li><b>{fmtd(i["data"])} · {i["numero"]}ª</b> {E(i["assunto"][:100])} → <span style="color:{CORES.get(des(i["id"]), "#999")}">{des(i["id"])}</span> · relator {E(i["relator"] or "—")} <a href="{mapa_tema.link(i["video_id"], i["ts"])}">▶</a></li>' for i in [x for x in itsm if x in decid][-6:][::-1])
        S.append(f'''<section class="pg">{top(n, "Inteligência comparativa")}<h2>{E(re.sub(r"^\w\)\s*", "", tc["titulo"]).split(":")[0])}</h2>
<div class="g3"><div class="card"><h3>Padrão da agência (3 anos)</h3><div class="big">{unan:.0f}%</div><p>decididos sem divergência ({m["unanimes"]} de {m_dec} decisões{f"; {m_pend} itens eram vista/retirada" if m_pend else ""})</p>
<p><b>Desfecho:</b> {E(" · ".join(f"{k} {v}" for k, v in desf.most_common()))}</p><p><b>Quem relata:</b> {E(" · ".join(f"{k} {v}" for k, v in relc.most_common()))}</p></div>
<div class="card"><h3>Casos semelhantes mais recentes</h3><ul class="lst">{prec}</ul></div>
<div class="card"><h3>Possíveis contradições <span class="est">inferência</span></h3>{ct or "<p>Nenhum par com desfechos opostos em menos de 24 meses neste tema.</p>"}<p class="nt">Pares do mesmo tema com desfecho oposto; podem ter fatos diferentes. Leia as justificativas antes de usar.</p></div></div>
<div class="card mt"><h3>O que a diretoria disse nos casos semelhantes</h3>{falas([x for x in itsm if x in decid][::-1] + [x for x in its if x not in itsm][::-1], 6 - min(len([x for x in itsm if x in decid][-6:]), 6) // 2)}</div></section>''')
    # busca e banco
    n += 1
    perg = [l[2:].split("[")[0].strip() for l in open(f"{P}/perguntas/perguntas.md")] if os.path.exists(f"{P}/perguntas/perguntas.md") else []
    tot = c.execute("select count(*), min(r.data) from itens i join reunioes r on r.id=i.reuniao_id where r.data>='2018-01-01'").fetchone()
    S.append(f'''<section class="pg">{top(n, "Busca e banco de dados")}<h2>O banco à disposição da empresa</h2><div class="g2"><div class="card"><h3>Base consultável</h3><div class="big">{f"{tot[0]:,}".replace(",", ".")}</div><p>decisões da diretoria da {NOME} desde {fmtd(tot[1])}, com voto de cada diretor, relator, resultado, justificativa e link no minuto.</p>
<p>Busca por processo, empresa, tema ou diretor; cruzamento com pautas e reuniões; planilha da empresa atualizada todo mês.</p></div>
<div class="card"><h3>Consultas do mês</h3><ol class="lst">{"".join(f"<li>{E(q)}</li>" for q in perg) or "<li>Envie suas perguntas para a edição do mês.</li>"}</ol><p class="nt">Respostas completas no boletim mensal.</p></div></div>
<div class="card mt"><h3>Exemplo do que a base devolve: as últimas decisões sobre a empresa, com a fala</h3>{falas([i for i in its if i["numero"] != its[-1]["numero"]][::-1], 5)}</div></section>''')
    out = f"{P}/agenda_comparativa"

S.append(dz.fim("Fontes públicas: vídeos oficiais das reuniões, pautas e calendário da agência. Informações do cliente (etapa no SEI, andamentos) aparecem identificadas. Legenda automática pode errar nomes e números. Prazos, previsões e «possíveis contradições» são estimativas e inferências: não substituem a publicação oficial nem orientação jurídica.",
                 EMP.get("contato", "Circle Consultoria em parceria com Grupo Nery"), KIT["divisores"][0]))
TOT = len(S)
S = [s.replace("</section>", f'<div class="pag">{k + 1:02d} / {TOT:02d}</div></section>', 1) if 1 < k < TOT - 1 else s for k, s in enumerate(S)]
CSS = dz.CSS + f"""@page{{size:13.333in 7.5in;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:'Inter Display',Inter,system-ui,sans-serif;color:{dz.TINTA};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg:not(.capa):not(.sum):not(.fim):not(.div){{background:#fff;padding:.45in .6in .4in}}h1,h2,h3{{margin:0;font-weight:500}}a{{color:{AC};font-weight:500;text-decoration:none}}
.hd{{display:flex;align-items:center;gap:12px;border-top:1px solid {dz.TINTA};padding-top:.1in;margin-bottom:.2in;font-size:7.6pt;letter-spacing:.14em;text-transform:uppercase;color:{dz.CINZA}}}.num{{color:{dz.AZUL2};font-weight:600}}.sp{{flex:1}}.hcli{{height:.22in}}.hl{{height:.2in}}
h2{{font-size:20pt;font-weight:400;color:{dz.AZUL};margin:0 0 .16in}}h3{{font-size:10.5pt;margin:0 0 .08in}}.lead{{font-size:9.5pt;color:#3A3833;margin:-.04in 0 .12in}}.card{{background:#fff;border-radius:0;padding:.1in 0 0;border:none;border-top:1px solid {dz.FIO}}}
.g2{{display:grid;grid-template-columns:1.3fr 1fr;gap:.16in}}.g3{{display:grid;grid-template-columns:.8fr 1.2fr 1.3fr;gap:.14in}}.col{{display:flex;flex-direction:column;gap:.14in}}
.tb{{width:100%;border-collapse:collapse;font-size:8pt}}.tb th{{text-align:left;color:{dz.CINZA};font-weight:600;border-bottom:2px solid {dz.TINTA};padding:3px 5px}}.tb td{{border-bottom:1px solid {dz.FIO};padding:6px 5px;vertical-align:top}}.pn{{font-size:7.4pt;color:{dz.CINZA}}}
.st{{font-size:6.8pt;font-weight:500;text-transform:uppercase;border-radius:99px;padding:1px 7px;white-space:nowrap}}.st-decidido{{background:{dz.NEVOA};color:{dz.AZUL}}}.st-retirado,.st-com{{background:{dz.LILAS};color:{dz.AZUL}}}.st-em{{background:{dz.NEVOA};color:{AC}}}
.nt{{font-size:7pt;color:#7A766F;margin:.08in 0 0}}.vtl{{display:flex;flex-direction:column;gap:5px;border-left:3px solid {dz.FIO};margin-left:.85in;padding-left:.2in}}.vt{{position:relative;font-size:8pt;border-bottom:1px solid {dz.FIO};padding:3px 0}}.vd{{position:absolute;left:-1.07in;top:4px;width:.75in;text-align:right;font-size:7.4pt;color:{dz.CINZA}}}.vt>i{{position:absolute;left:-.29in;top:6px;width:11px;height:11px;border-radius:50%;border:2px solid #fff}}
.pz{{font-size:9pt;line-height:1.5}}.card p{{font-size:8.6pt;line-height:1.45;margin:.05in 0}}.pb{{display:grid;grid-template-columns:2in 1fr .55in .5in;align-items:center;gap:8px;font-size:8.6pt;margin:7px 0}}.bt{{position:relative;height:14px;background:{dz.NEVOA};border-radius:7px}}
.iqr{{position:absolute;top:0;bottom:0;background:{AC};opacity:.3;border-radius:7px}}.md{{position:absolute;top:-3px;width:4px;height:20px;background:{AC};border-radius:2px}}.pb em{{font-size:7.4pt;color:#7A766F;font-style:normal}}.lgx{{font-size:7.6pt;color:{dz.CINZA};margin-bottom:.08in}}.lgx i{{display:inline-block;width:14px;height:9px;margin:0 4px 0 10px;position:relative;border-radius:3px}}.lgx i.md{{width:4px;top:0;height:12px}}
.big{{font-size:30pt;font-weight:500;line-height:1.05}}.lst{{margin:0;padding-left:1.1em;font-size:8.2pt;line-height:1.42}}.lst li{{margin-bottom:.05in}}.est{{font-size:6.6pt;font-weight:500;text-transform:uppercase;color:{dz.AZUL};background:{dz.LILAS};border-radius:99px;padding:2px 7px;margin-left:4px}}
.mt{{margin-top:.14in}}.ctr{{display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:7.6pt;border-bottom:1px solid {dz.FIO};padding:5px 0;line-height:1.35}}
.pag{{position:absolute;right:.45in;bottom:.15in;font-size:7.5pt;font-weight:500;color:{GOLD}}}"""
open(out + ".html", "w").write(leve_html(dz.sem_travessao(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(nome_curto)}</title><style>{CSS}</style></head><body>{"".join(S)}</body></html>')))
js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(out)}.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(out)}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
if r.returncode == 0: leve_pdf(out + ".pdf"); dz.densidade(out + ".html")
print(out + ".pdf" if r.returncode == 0 else r.stderr[-400:], TOT, "páginas", os.path.getsize(out + ".pdf") // 1024 if r.returncode == 0 else 0, "KB")
