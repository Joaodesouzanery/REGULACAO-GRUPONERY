"""Relatório da EMPRESA em formato PAINEL (produto B, design 2026-11): capa com a foto do cliente (sem corte do assunto),
painel-resumo (processos · calendário · desfechos · risco por diretor), diretoria com barra de mandato, decisões setoriais,
mapeamentos por assunto, análise antecipada, contrato em foco, previsão passado × futuro (faixa, nunca certeza) e cobertura.
Uso: python3 pipeline/relatorio_painel.py clientes/<x>/<pasta>
empresa.json: nome, cnpj, aliases, agencias, logo, foto_capa, foco ("50% 55%"), cor ("#3D1FE0"), cor2, temas_consultoria,
item_antecipado, contrato_foco, itens_acompanhar; desfechos_manuais.json opcional (item_id → {desfecho, motivo}).
Recorte: decisões de 2018 em diante."""
import sys, os, re, json, html, base64, datetime, subprocess, collections, math, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, mapa_tema
from desfecho import desfecho_item
from pdf_leve import leve_html, leve_pdf

P = sys.argv[1].rstrip("/")
EMP = json.load(open(f"{P}/empresa.json"))
AG = EMP.get("agencias", ["antaq"])[0]
D = "data" if AG == "antt" else f"data/{AG}"
NOME = {"antt": "ANTT", "anm": "ANM", "antaq": "ANTAQ"}[AG]
DESDE = "2018-01-01"
TRES = (datetime.date.today() - datetime.timedelta(days=3 * 365)).isoformat()  # recorte padrão das peças: últimos 3 anos (+ contexto desde 2018)
HOJE = datetime.date.today()
E = html.escape
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
MAN = ld(f"{P}/desfechos_manuais.json", {})
AC, AC2 = EMP.get("cor", "#3D1FE0"), EMP.get("cor2", "#F28C1A")
GOLD = "#C99A06"


def b64(p, mime=None):
    if not p or not os.path.exists(p): return ""
    ext = (mime or p.rsplit(".", 1)[-1].lower()).replace("jpg", "jpeg")
    return f"data:image/{ext};base64," + base64.b64encode(open(p, "rb").read()).decode()


def fmtd(s, curto=False):
    try:
        d = datetime.date.fromisoformat(str(s)[:10]); return d.strftime("%d/%m" if curto else "%d/%m/%Y")
    except Exception: return str(s or "—")


def des(c, iid):
    m = MAN.get(str(iid)); return m["desfecho"] if m else desfecho_item(c, iid)


slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")


def foto_dir(nome, b=None):
    for p in [(b or {}).get("foto"), f"{D}/dirigentes/{slug(nome)}.jpg", f"docs/marca/diretores/{AG}/{slug(nome)}.jpg"]:
        if p and os.path.exists(p): return f'<div class="av" style="background-image:url({b64(p)})"></div>'
    return '<div class="av ini">' + E("".join(w[0] for w in nome.split()[:2]).upper()) + "</div>"


# ---------------- dados ----------------
c = previsao.conn(AG)
pr = previsao.calcular(AG, EMP["aliases"])
its = [i for i in pr["itens"] if i["data"] >= DESDE]
board = pr["colegiado"]
bios = {b["diretor"]: b for b in ld(f"{D}/bios.json", [])}
mand = ld(f"{D}/mandatos.json", [])
vac = [v for v in ld(f"{D}/vacancias.json", []) if not v.get("fim")]
sups = ld(f"{D}/superintendentes.json", [])
cal = [x for x in ld(f"{D}/calendario.json", []) if x["data"] >= HOJE.isoformat()][:2]
DES = collections.Counter(des(c, i["id"]) for i in its)
ids = [i["id"] for i in its]


def mandato(d):
    ms = [m for m in mand if m.get("diretor") == d]; m = ms[-1] if ms else {}
    return m.get("inicio"), m.get("fim_legal") or m.get("fim"), m.get("cargo") or ""


VOT = {}
for d in board:
    vs = c.execute("select categoria, eh_relator from votos where diretor=? and item_id in (%s)" % ",".join("?" * len(ids)), [d] + ids).fetchall() if ids else []
    cat = collections.Counter(v[0] for v in vs)
    VOT[d] = {"n": len(vs), "rel": sum(v[1] for v in vs), "ac": cat["acompanha"] + cat["revisor_acompanha"], "dv": cat["vencido"] + cat["revisor_diverge"], "vista": cat["vista"]}
# processos (último status por processo/assunto)
procs = collections.OrderedDict()
for i in reversed(its):
    k = (i["processo"] or "").strip()[:20] or i["assunto"][:40]
    if k not in procs: procs[k] = i
STATUS = lambda i: ("decidido" if re.search(r"aprovad|desprov|indefer|acolhid|negad|provid", i["resultado"] or "", re.I) else "retirado" if "retirad" in (i["resultado"] or "").lower() else "vista" if "vista" in (i["resultado"] or "").lower() else "decidido")


# ---------------- gráficos SVG ----------------
CORES = {"favorável": "#2F855A", "parcial": "#C99A06", "neutro": "#9A958C", "desfavorável": "#B83227", "pendente": "#5B6AD0"}


def rosca(cont, cores, tam=170, rot=""):
    tot = sum(cont.values()) or 1; r, cx = 62, tam / 2; a0 = -math.pi / 2; arcs = ""
    for k, v in cont.items():
        if not v: continue
        a1 = a0 + 2 * math.pi * v / tot; big = 1 if a1 - a0 > math.pi else 0
        x0, y0, x1, y1 = cx + r * math.cos(a0), cx + r * math.sin(a0), cx + r * math.cos(a1 - 1e-4), cx + r * math.sin(a1 - 1e-4)
        arcs += f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {big} 1 {x1:.1f},{y1:.1f}" stroke="{cores.get(k, "#BBB")}" stroke-width="26" fill="none"/>'
        a0 = a1
    leg = "".join(f'<div class="lg"><i style="background:{cores.get(k, "#BBB")}"></i>{E(str(k).replace("_", " "))} <b>{v}</b></div>' for k, v in cont.items() if v)
    return f'<div class="rosca"><svg width="{tam}" height="{tam}" viewBox="0 0 {tam} {tam}">{arcs}<text x="{cx}" y="{cx - 2}" text-anchor="middle" class="rt">{tot}</text><text x="{cx}" y="{cx + 16}" text-anchor="middle" class="rs">{E(rot)}</text></svg><div class="leg">{leg}</div></div>'


def barras(linhas, cor=AC, fmt=lambda v: f"{v}"):
    mx = max([v for _, v, _ in linhas] + [1e-9])
    return "".join(f'<div class="br"><span class="bl">{E(l)}</span><span class="bt"><i style="width:{100 * v / mx:.0f}%;background:{cor}"></i></span><b>{fmt(v)}</b><em>{E(x)}</em></div>' for l, v, x in linhas)


def faixa(ps):
    """chance de unanimidade como faixa: produto das taxas com ±1,3 desvio por diretor (n pequeno → faixa larga)."""
    lo = hi = mid = 1.0
    for p, n in ps:
        se = math.sqrt(max(p * (1 - p), 0.01) / (n + 10)); mid *= p; lo *= max(p - 1.3 * se, 0); hi *= min(p + 1.3 * se, 1)
    return lo, mid, hi


# ---------------- páginas ----------------
LOGO_B, LOGO_P = b64("docs/marca/circle/logo_circle_branco.png"), b64("docs/marca/circle/logo_circle_preto.png")
NERY_B, NERY_P = b64("docs/marca/grupo_nery/logo_branco.png"), b64("docs/marca/grupo_nery/logo_preto.png")
CLI, FOTO = b64(EMP.get("logo")), b64(EMP.get("foto_capa"))
FOCO = EMP.get("foco", "50% 55%")
S = []


def top(n, t):
    return (f'<header class="hd"><div class="band"></div>'
            f'<div class="hdt"><span class="num">{n:02d}</span><span>{E(t)}</span><span class="sp"></span>'
            + (f'<img src="{CLI}" class="hcli">' if CLI else "") + (f'<img src="{LOGO_P}" class="hl">' if LOGO_P else "") + '</div></header>')


nome_curto = EMP["nome"].split("(")[0].strip()
unan = sum(1 for i in its if not c.execute("select 1 from votos where item_id=? and categoria in ('vencido','revisor_diverge')", (i["id"],)).fetchone())
aberto = sum(1 for i in procs.values() if STATUS(i) != "decidido")
kp = [(len(its), "decisões de diretoria sobre a empresa", f"{NOME}, {fmtd(its[0]['data'])[-4:] if its else '—'}–{HOJE.year}"),
      (f"{100 * unan / max(len(its), 1):.0f}%", "sem voto divergente", f"{unan} de {len(its)}"),
      (len(cal), "próximas reuniões oficiais", " · ".join(fmtd(x["data"], True) for x in cal) or "—"),
      (aberto, "processos em aberto", "vista ou retirado de pauta")]
S.append(f'''<section class="pg capa"><div class="cfoto" style="background-image:url({FOTO});background-position:{FOCO}"></div>
<div class="cpainel"><div class="marcas">{f'<img src="{LOGO_B}" class="lc">' if LOGO_B else ''}<div class="parc">em parceria com {f'<img src="{NERY_B}">' if NERY_B else 'Grupo Nery'}</div></div>
<div class="eb">Inteligência regulatória · {NOME}</div>{f'<div class="clibox"><img src="{CLI}"></div>' if CLI else ''}<h1>{E(nome_curto)}</h1>
<div class="sub">{E(EMP["nome"][len(nome_curto):].strip(" ()"))}</div><div class="cnpj">{E(EMP.get("cnpj", ""))}</div>
<div class="kps">{"".join(f'<div class="kp"><b>{a}</b><span>{E(t)}</span><em>{E(x)}</em></div>' for a, t, x in kp)}</div>
<div class="meta">Emitido em {HOJE.strftime("%d/%m/%Y")} · base até {fmtd(pr["base_ate"])} · decisões desde 2018</div></div></section>''')

# 1 painel
tab = "".join(f'<tr><td><span class="st st-{STATUS(i)}">{STATUS(i)}</span></td><td>{fmtd(i["data"])}</td><td class="pn">{E(k)}</td><td>{E((i["assunto"] or "")[:78])}</td><td><span class="ds" style="background:{CORES.get(des(c, i["id"]), "#999")}">{E(des(c, i["id"]))}</span></td></tr>' for k, i in list(procs.items())[:7])
ev = [(x["data"], f'{x["reuniao"]}ª ROD', x.get("formato", "")) for x in cal]
for d in board:
    _, fim, _ = mandato(d)
    if fim and HOJE.isoformat() <= fim <= (HOJE + datetime.timedelta(days=460)).isoformat(): ev.append((fim, "fim do mandato", d.split()[0]))
ev.sort(); t0, t1 = HOJE, HOJE + datetime.timedelta(days=470)
pos = lambda d: 4 + 92 * (datetime.date.fromisoformat(d[:10]) - t0).days / (t1 - t0).days
lin = "".join(f'<div class="ev2"><i class="{"r" if "ROD" in a else "m"}"></i><b>{fmtd(d)}</b><span>{E(a)}</span><em>{E(b)}</em></div>' for d, a, b in ev[:6])
risco = [(d.split()[0] + " " + d.split()[-1], 1 - pr["por_diretor"].get(d, (0.97, 0))[0], f"n={pr['por_diretor'].get(d, (0, 0))[1]}") for d in board]
S.append(f'''<section class="pg">{top(1, "Painel da empresa")}<div class="g2">
<div class="card"><h3>Processos da empresa na diretoria</h3><table class="tb"><tr><th>Status</th><th>Última decisão</th><th>Processo (legenda)</th><th>Assunto</th><th>Para a empresa*</th></tr>{tab}</table>
<p class="nt">*Desfecho pela decisão; casos ambíguos conferidos à mão. Nº de processo vem da legenda — conferir no SEI.</p></div>
<div class="col"><div class="card"><h3>Calendário e próximos passos</h3><div class="tl2">{lin}</div></div>
<div class="g2b"><div class="card"><h3>Desfecho histórico</h3>{rosca(DES, CORES, 150, "decisões")}</div>
<div class="card"><h3>Chance de divergir do relator</h3>{barras(risco, AC2, lambda v: f"{100 * v:.0f}%")}<p class="nt">Temas da empresa, últimos 3 anos (prior 97%).</p></div></div></div></div></section>''')

# 2 diretoria
cards = ""
for d in board:
    b = bios.get(d, {}); ini, fim, cargo = mandato(d)
    try:
        a, z = datetime.date.fromisoformat(ini[:10]), datetime.date.fromisoformat(fim[:10]); pct = max(0, min(100, 100 * (HOJE - a).days / (z - a).days))
        barra = f'<div class="mb"><i style="width:{pct:.0f}%"></i></div><div class="mbl"><span>{fmtd(ini)}</span><span>até <b>{fmtd(fim)}</b></span></div>'
    except Exception: barra = f'<div class="mbl"><span>Mandato até <b>{fmtd(fim)}</b></span></div>'
    v = VOT[d]
    cards += f'''<div class="dc">{foto_dir(d, b)}<div class="dn">{E(d)}</div><div class="dcg">{E((b.get("cargo") or cargo or "Diretor(a)")[:60])}</div>
<p>{E((b.get("minibio") or "")[:190])}</p>{barra}<div class="dv">Na empresa: <b>{v["n"]}</b> votos · <b>{v["rel"]}</b> relatorias · {v["dv"]} divergências · {v["vista"]} vistas</div></div>'''
sc = "".join(f'<div class="sc"><b>{E(s.get("nome", ""))}</b><span>{E((s.get("superintendencia") or s.get("cargo") or "")[:70])}</span></div>' for s in sups[:8])
vh = " · ".join(f'{E(v["cadeira"])} (desde {fmtd(v["inicio"])}; interinos: {E(v.get("interinos") or "—")})' for v in vac) or "nenhuma"
S.append(f'''<section class="pg">{top(2, f"Diretoria · {NOME}")}<h2>Quem decide hoje</h2><div class="dgrid" style="grid-template-columns:repeat({len(board)},1fr)">{cards}</div>
<div class="g2c"><div class="card"><h3>Superintendentes</h3><div class="sgrid">{sc}</div></div><div class="card vg"><h3>Mandatos e vagas</h3><p><b>Vaga aberta:</b> {vh}</p><p class="nt">Mandatos: Senado/DOU, conferidos todo dia 1. Barra = tempo de mandato já cumprido.</p></div></div></section>''')

# 2b ficha dos diretores (todos os temas da agência, 3 anos)
def ficha(d):
    R = c.execute("select v.categoria, v.eh_relator, v.item_id, v.justificativa, v.trecho, v.trecho_t, v.ts, r.numero, r.video_id from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.diretor=? and r.data>=?", (d, TRES)).fetchall()
    cat = collections.Counter(r["categoria"] for r in R); rel = [r for r in R if r["eh_relator"]]
    tm = collections.Counter(t for r in rel for (t,) in c.execute("select tema from item_temas where item_id=?", (r["item_id"],)))
    proc = re.compile(r"processo n|item \d+ da pauta|aprovad|em vota|>>|interessad|trata-se", re.I)
    boas = [r for r in R if r["trecho"] and len(r["trecho"]) > 60 and not proc.search(r["trecho"][:90])]
    fr = max(boas, key=lambda r: (r["categoria"] in ("vencido", "revisor_diverge", "vista"), r["eh_relator"], len(r["trecho"] or "")), default=None)
    ju = [r["justificativa"] for r in rel if r["justificativa"]][-2:]
    return {"n": len(R), "rel": len(rel), "dv": cat["vencido"] + cat["revisor_diverge"], "vista": cat["vista"], "temas": tm.most_common(3), "fr": fr, "ju": ju}
FI = {d: ficha(d) for d in board}
linhas_f = [("Formação", lambda d: (bios.get(d) or {}).get("formacao") or "não informada nas fontes oficiais"),
            ("Origem / carreira", lambda d: re.split(r"\.\s", (bios.get(d) or {}).get("minibio") or "—")[0][:160]),
            ("Mandato", lambda d: f"diretor substituto · convocação até {fmtd(mandato(d)[1])}" if "substitut" in ((bios.get(d) or {}).get("cargo", "")).lower() else f"até {fmtd(mandato(d)[1])} · 5 anos, sem recondução (Lei 13.848/2019)"),
            ("Votos em 3 anos", lambda d: f"{FI[d]['n']} votos · {FI[d]['rel']} relatorias · {FI[d]['dv']} divergências · {FI[d]['vista']} vistas"),
            ("Temas que mais relata", lambda d: ", ".join(f"{t.replace('_', ' ')} ({k})" for t, k in FI[d]["temas"]) or "—"),
            ("Argumentos recorrentes (inferência)", lambda d: " / ".join(j[:110] for j in FI[d]["ju"]) or "—")]
fhead = "".join(f'<th>{foto_dir(d, bios.get(d))}<div class="dn">{E(d)}</div></th>' for d in board)
fbody = "".join(f'<tr><td class="fl">{E(r)}</td>' + "".join(f'<td>{E(str(f(d)))}</td>' for d in board) + "</tr>" for r, f in linhas_f)
fbody += '<tr><td class="fl">Frase típica</td>' + "".join(f'<td class="fq">{("«" + E(FI[d]["fr"]["trecho"][:150]) + "» <a href=" + chr(34) + mapa_tema.link(FI[d]["fr"]["video_id"], FI[d]["fr"]["ts"], FI[d]["fr"]["trecho_t"]) + chr(34) + ">▶</a>") if FI[d]["fr"] else "—"}</td>' for d in board) + "</tr>"
S.append(f'''<section class="pg">{top(2, f"Ficha dos diretores · {NOME}")}<h2>Os diretores lado a lado</h2><table class="ft"><tr><th></th>{fhead}</tr>{fbody}</table>
<p class="nt">Todos os temas da agência, últimos 3 anos (desde {fmtd(TRES)}). Frase: trecho literal da legenda automática, com link no minuto. Argumentos: justificativas registradas quando relator.</p></section>''')

# 3 decisões setoriais
TM = collections.Counter(t for i in its for (t,) in c.execute("select tema from item_temas where item_id=?", (i["id"],)))
pal = ["#3D1FE0", "#F28C1A", "#2EC4A6", GOLD, "#8E5CF0", "#9A958C", "#5B6AD0", "#B83227"]
tcor = {t: pal[k % len(pal)] for k, (t, _) in enumerate(TM.most_common(8))}
vb = "".join(f'<div class="vb"><span class="bl">{E(d)}</span><span class="bt3"><i style="width:{100 * v["rel"] / max(v["n"], 1):.0f}%;background:{AC}"></i><i style="width:{100 * v["ac"] / max(v["n"], 1):.0f}%;background:#CFCAC0"></i><i style="width:{100 * (v["dv"] + v["vista"]) / max(v["n"], 1):.0f}%;background:{AC2}"></i></span><b>{v["n"]}</b></div>' for d, v in VOT.items())
evs = ""
for i in list(reversed(its))[:2]:
    r = c.execute("select diretor, voto, justificativa from votos where item_id=? and eh_relator=1", (i["id"],)).fetchone()
    evs += f'''<div class="evc"><div class="evh">RD {E(str(i["numero"]))} · {fmtd(i["data"])} · item {E(str(i["item"]))}</div><p><b>{E((i["assunto"] or "")[:140])}</b></p>
<p>Relator {E(r["diretor"] if r else "—")}: {E(((r["voto"] if r else "") or "")[:110])}</p>{f'<p class="q">«{E((r["justificativa"] or "")[:150])}»</p>' if r and r["justificativa"] else ""}<a href="{mapa_tema.link(i["video_id"], i["ts"])}">▶ assistir no minuto</a></div>'''
S.append(f'''<section class="pg">{top(3, f"Decisões setoriais · {NOME}")}<h2>O que a diretoria decidiu sobre a empresa</h2><div class="g3">
<div class="card"><h3>Por tema</h3>{rosca(dict(TM.most_common(8)), tcor, 170, "itens")}</div>
<div class="card"><h3>Como cada diretor votou nos itens da empresa</h3><div class="lgx"><i style="background:{AC}"></i>relatou <i style="background:#CFCAC0"></i>acompanhou <i style="background:{AC2}"></i>divergiu/vista</div>{vb}</div>
<div class="col">{evs}</div></div></section>''')

# 4.. mapeamentos por assunto
n = 3
for tc in EMP.get("temas_consultoria", []):
    n += 1; m = mapa_tema.mapear(AG, tc["regex"], TRES); m18 = mapa_tema.mapear(AG, tc["regex"], DESDE)
    dc = ""
    for d, st in m["por_diretor"].items():
        e = st["ev"]; pct = st["p_acomp"]
        dc += f'''<div class="mc">{foto_dir(d, bios.get(d))}<div class="dn">{E(d)}</div><div class="gauge"><svg viewBox="0 0 120 66" width="120" height="66"><path d="M10,60 A50,50 0 0 1 110,60" stroke="#E7E3DA" stroke-width="12" fill="none"/>
<path d="M10,60 A50,50 0 0 1 110,60" stroke="{AC}" stroke-width="12" fill="none" stroke-dasharray="{157 * pct:.0f} 200"/></svg><b>{pct:.0%}</b></div><div class="ml">chance de acompanhar o relator · n={st["n"]}</div>
<div class="ms">relatou {st["rel"]} · divergiu {st["dv"]} · vista {st["vista"]}</div>{f'<div class="mq">RD {E(str(e["numero"]))}: «{E((e["justificativa"] or e["voto"] or "")[:80])}» <a href="{mapa_tema.link(e["video_id"], e["ts"], e["trecho_t"])}">▶</a></div>' if e else ""}</div>'''
    lst = "".join(f'<div class="ti"><span>{fmtd(i["data"])}</span><b>RD {E(str(i["numero"]))}</b> {E((i["assunto"] or "")[:120])} — <i>{E(des(c, i["id"]))}</i> <a href="{mapa_tema.link(i["video_id"], i["ts"])}">▶</a></div>' for i in m["itens"][-5:][::-1])
    S.append(f'''<section class="pg">{top(n, "Mapeamento por assunto")}<h2>{E(tc["titulo"])}</h2>
<p class="lead"><b>{len(m["itens"])} decisões nos últimos 3 anos</b> (desde {fmtd(TRES)}) · {m["unanimes"]} sem voto divergente · contexto: {len(m18["itens"])} desde 2018 · desfecho: {E(" · ".join(f"{k} {v}" for k, v in collections.Counter(des(c, i["id"]) for i in m["itens"]).most_common()))}</p>
<div class="mgrid" style="grid-template-columns:repeat({len(m["por_diretor"])},1fr)">{dc}</div><h3 class="h3s">Decisões semelhantes mais recentes</h3><div class="tlist">{lst}</div></section>''')

# análise antecipada
ia = EMP.get("item_antecipado")
if ia:
    n += 1; m = mapa_tema.mapear(AG, ia["regex"], DESDE)
    lo, mid, hi = faixa([(st["p_acomp"], st["n"]) for st in m["por_diretor"].values()])
    evh = "".join(f'<li>{E(x["txt"])} <a href="https://www.youtube.com/watch?v={x["vid"]}&t={max(int(x["t"]) - 3, 0)}s">▶ {int(x["t"]) // 3600}:{int(x["t"]) // 60 % 60:02d}:{int(x["t"]) % 60:02d}</a></li>' for x in ia.get("evidencias", []))
    calh = "".join(f'<div class="cr"><b>{E(x["data"])}</b><span>{E(x["reuniao"])}</span><em>{E(x["obs"])}</em></div>' for x in ia.get("calendario", []))
    pv = "".join(f'<div class="br"><span class="bl">{E(d)}</span><span class="bt"><i style="width:{100 * st["p_acomp"]:.0f}%;background:{AC}"></i></span><b>{st["p_acomp"]:.0%}</b><em>n={st["n"]}</em></div>' for d, st in m["por_diretor"].items())
    S.append(f'''<section class="pg">{top(n, "Análise antecipada")}<h2>{E(ia["titulo"])}</h2><div class="g3a">
<div class="card cl"><div class="tag t1">O que o cliente informou</div><p>{E(ia.get("informado", "Retirado de pauta para análise do Diretor-Geral."))}</p><div class="tag t2">O que o vídeo mostra</div><ul>{evh}</ul></div>
<div class="card"><h3>Próximas reuniões (calendário oficial)</h3>{calh}<p class="nt">Reunião virtual: sem transmissão; resultado só em ata.</p></div>
<div class="card"><h3>Previsão por diretor <span class="est">estimativa</span></h3>{pv}<div class="fx">Unanimidade com o relator: <b>{100 * lo:.0f}–{min(100 * hi, 99):.0f}%</b> (faixa larga = poucos votos no tema)</div><p class="nt">{E(ia.get("leitura", ""))[:520]}</p></div></div></section>''')

# contrato em foco
cf = EMP.get("contrato_foco")
if cf:
    n += 1; m = mapa_tema.mapear(AG, cf["regex"], DESDE)
    def tipo(a):
        a = (a or "").lower()
        return ("passivo", "#2EC4A6") if "passivo" in a else ("preço-teto", AC2) if "preço" in a or "price" in a else ("autorização", AC) if "autoriza" in a else ("recurso", "#B83227") if "recurso" in a or "cautelar" in a else ("outro", "#9A958C")
    tl = "".join(f'<div class="vt"><span class="vd">{fmtd(i["data"])}</span><i style="background:{tipo(i["assunto"])[1]}"></i><div><span class="vk" style="color:{tipo(i["assunto"])[1]}">{tipo(i["assunto"])[0]}</span> <b>RD {E(str(i["numero"]))} · item {E(str(i["item"]))}</b> {E((i["assunto"] or "")[:130])} — <em>{E(des(c, i["id"]))}</em> <a href="{mapa_tema.link(i["video_id"], i["ts"])}">▶</a></div></div>' for i in m["itens"][-9:])
    S.append(f'''<section class="pg">{top(n, "Contrato em foco")}<h2>{E(cf["titulo"])}</h2><p class="lead">{E(cf.get("texto", ""))}</p><div class="vtl">{tl}</div></section>''')

# previsão passado × futuro
n += 1
lo, mid, hi = faixa([pr["por_diretor"][d] for d in board if d in pr["por_diretor"]])
ac, tt = pr["backtest"]
pas = "".join(f'<div class="br"><span class="bl">{E(d)}</span><span class="bt"><i style="width:{100 * p:.0f}%;background:#9A958C"></i></span><b>{p:.0%}</b><em>n={k}</em></div>' for d, (p, k) in pr["por_diretor"].items())
S.append(f'''<section class="pg">{top(n, "Previsão futura · passado × futuro")}<h2>O que esperar dos próximos processos da empresa</h2><div class="g2p pp">
<div class="card"><div class="tag t2">Passado</div><h3>Quanto cada diretor acompanhou o relator nos temas da empresa (3 anos)</h3>{pas}<p class="nt">Regra testada em 2025–26 com dados até 2024: acertou {ac} de {tt} ({100 * ac / max(tt, 1):.0f}%).</p></div>
<div class="card fut"><div class="tag t1">Futuro</div><div class="stamp">ESTIMATIVA — não é certeza</div><div class="plac">{pr["placar_esperado"][0]}<span>×</span>{pr["placar_esperado"][1]}</div><div class="pl">placar mais provável</div>
<div class="fxb"><div class="fxl"><i style="left:{100 * lo:.0f}%;width:{100 * (hi - lo):.0f}%"></i><b style="left:{100 * mid:.0f}%"></b></div><div class="fxt">Chance de decisão unânime com o relator: <b>{100 * lo:.0f}% a {min(100 * hi, 99):.0f}%</b></div></div>
<ul class="muda"><li>O relator define o resultado na grande maioria dos casos: a leitura do voto do relator é o fator nº 1.</li><li>Pode mudar a previsão: troca de diretor (mandatos em dez/2026 e fev/2027), voto-vista, divergência do Diretor-Geral em metodologia de cálculo.</li><li>Não prevê o mérito de um caso específico; é estatística do histórico de votos.</li></ul></div></div></section>''')

# fim
cob = E(subprocess.run(["python3", "pipeline/cobertura_resposta.py", AG], capture_output=True, text=True).stdout.strip().replace("**", "")).replace("\n", "<br>")
S.append(f'''<section class="pg fim"><div class="ffoto" style="background-image:url({FOTO});background-position:{FOCO}"></div><div class="fc">{f'<img src="{LOGO_B}" class="lc">' if LOGO_B else ''}<div class="parc">em parceria com {f'<img src="{NERY_B}">' if NERY_B else 'Grupo Nery'}</div>
<h2>Como ler e cobertura</h2><div class="fimc">{cob}<br><br>Fontes públicas: vídeos oficiais das reuniões, pautas e calendário da agência, Senado e DOU. Previsões são estimativas e não substituem a publicação oficial nem orientação jurídica.</div></div></section>''')

TOT = len(S)
S = [s.replace("</section>", f'<div class="pag">{k + 1:02d} / {TOT:02d}</div></section>', 1) if k else s for k, s in enumerate(S)]
CSS = f"""@page{{size:13.333in 7.5in;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:'Inter Display',Inter,system-ui,sans-serif;color:#0B0B0B;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:13.333in;height:7.5in;position:relative;overflow:hidden;page-break-after:always;background:#F6F5F1;padding:0 .45in .4in}}h1,h2,h3{{margin:0;font-weight:650}}
.capa{{padding:0;display:grid;grid-template-columns:4.6in 1fr;background:#0B0B0B}}.cfoto{{grid-column:2;grid-row:1;background-size:cover}}.cpainel{{grid-column:1;grid-row:1;padding:.42in .45in;color:#fff;display:flex;flex-direction:column}}
.marcas{{display:flex;flex-direction:column;gap:.1in}}.lc{{height:.36in;width:auto;align-self:flex-start}}.parc{{display:flex;align-items:center;gap:8px;font-size:7.5pt;color:#BDB8AE;letter-spacing:.08em;text-transform:uppercase}}.parc img{{height:.22in;width:auto}}
.eb{{margin-top:.32in;font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:#E2B93B}}.clibox{{background:#fff;border-radius:10px;padding:8px 12px;align-self:flex-start;margin-top:.14in}}.clibox img{{height:.42in;display:block}}
.capa h1{{font-size:30pt;line-height:1.05;margin-top:.14in}}.sub{{font-size:11pt;color:#E8E5DE;margin-top:.05in}}.cnpj{{font-size:7.3pt;color:#9A958C;margin-top:.08in;line-height:1.35}}
.kps{{display:grid;grid-template-columns:1fr 1fr;gap:.12in;margin-top:auto}}.kp{{border-top:3px solid {AC2};padding-top:.06in}}.kp b{{font-size:24pt;display:block;line-height:1.05}}.kp span{{font-size:8pt;display:block}}.kp em{{font-size:7pt;color:#9A958C;font-style:normal}}.meta{{font-size:7pt;color:#7A766F;margin-top:.16in}}
.hd{{margin:0 -.45in .18in}}.band{{height:.16in;background:linear-gradient(90deg,{AC2},{AC} 45%,#2EC4A6)}}.hdt{{display:flex;align-items:center;gap:.12in;padding:.1in .45in 0;font-size:8.5pt;letter-spacing:.1em;text-transform:uppercase;color:#6E6A63}}.num{{color:{GOLD};font-weight:700}}.sp{{flex:1}}.hcli{{height:.24in}}.hl{{height:.2in}}
h2{{font-size:19pt;margin:0 0 .14in}}h3{{font-size:10.5pt;margin:0 0 .08in}}.h3s{{margin-top:.14in}}.lead{{font-size:9.5pt;color:#3A3833;margin:-.06in 0 .12in}}
.card{{background:#fff;border-radius:12px;padding:.14in .16in;border:1px solid #E7E3DA}}.g2{{display:grid;grid-template-columns:1.25fr 1fr;gap:.16in}}.col{{display:flex;flex-direction:column;gap:.14in}}.g2b{{display:grid;grid-template-columns:1fr 1fr;gap:.14in}}
.tb{{width:100%;border-collapse:collapse;font-size:7.8pt}}.tb th{{text-align:left;color:#6E6A63;font-weight:600;border-bottom:2px solid #0B0B0B;padding:3px 4px}}.tb td{{border-bottom:1px solid #EEEAE2;padding:5px 4px;vertical-align:top}}.pn{{font-size:7pt;color:#6E6A63}}
.st{{font-size:6.8pt;font-weight:700;text-transform:uppercase;border-radius:99px;padding:1px 7px}}.st-decidido{{background:#E8F3EC;color:#2F855A}}.st-vista,.st-retirado{{background:#FFF3D2;color:#8A6400}}.ds{{color:#fff;font-size:6.8pt;border-radius:99px;padding:1px 7px;font-weight:600}}.nt{{font-size:6.8pt;color:#7A766F;margin:.06in 0 0}}
.tl{{position:relative;height:1.05in;margin-top:.06in}}.lnh{{position:absolute;left:2%;right:2%;top:.32in;height:3px;background:#E7E3DA}}.hoje{{position:absolute;left:2%;top:.05in;font-size:7pt;color:#6E6A63}}
.ev{{position:absolute;top:.24in;transform:translateX(-50%);text-align:center;width:1in;font-size:7pt}}.ev i{{display:block;width:13px;height:13px;border-radius:50%;margin:0 auto .05in;border:3px solid #fff}}.ev i.r{{background:{AC}}}.ev i.m{{background:{AC2}}}.ev b{{display:block;font-size:8pt}}.ev span{{display:block}}.ev em{{color:#7A766F;font-style:normal}}
.rosca{{display:flex;align-items:center;gap:.1in}}.rt{{font-size:22pt;font-weight:700}}.rs{{font-size:7.5pt;fill:#6E6A63}}.leg{{font-size:7.6pt;display:flex;flex-direction:column;gap:3px}}.lg i{{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px}}
.br,.vb{{display:grid;grid-template-columns:1.25in 1fr .42in .45in;align-items:center;gap:6px;font-size:8pt;margin:4px 0}}.bt,.bt3{{height:10px;background:#F0EDE6;border-radius:5px;overflow:hidden;display:flex}}.bt i,.bt3 i{{display:block;height:100%}}.br em{{font-size:7pt;color:#7A766F;font-style:normal}}
.dgrid{{display:grid;gap:.12in}}.dc{{background:#fff;border-radius:12px;padding:.14in;border:1px solid #E7E3DA;border-top:4px solid {AC};text-align:center}}.av{{width:.95in;height:.95in;border-radius:50%;background-size:cover;background-position:center 20%;margin:0 auto .06in;background-color:#E7E3DA}}.av.ini{{display:flex;align-items:center;justify-content:center;font-size:20pt;color:#6E6A63}}
.dn{{font-weight:650;font-size:10.5pt}}.dcg{{font-size:7.3pt;color:#6E6A63;margin:.02in 0 .05in}}.dc p{{font-size:7.4pt;line-height:1.35;text-align:left;margin:0 0 .06in;color:#3A3833}}.mb{{height:6px;background:#EEEAE2;border-radius:3px;overflow:hidden}}.mb i{{display:block;height:100%;background:{AC2}}}.mbl{{display:flex;justify-content:space-between;font-size:7pt;color:#6E6A63;margin-top:3px}}.dv{{font-size:7pt;margin-top:.05in;color:#3A3833}}
.g2c{{display:grid;grid-template-columns:2fr 1fr;gap:.14in;margin-top:.14in}}.sgrid{{display:grid;grid-template-columns:1fr 1fr;gap:4px 14px}}.sc b{{font-size:8pt;display:block}}.sc span{{font-size:6.9pt;color:#6E6A63}}.vg p{{font-size:8pt;line-height:1.4}}
.g3{{display:grid;grid-template-columns:1fr 1.2fr 1.1fr;gap:.14in}}.lgx{{font-size:7.3pt;color:#6E6A63;margin-bottom:.06in}}.lgx i{{display:inline-block;width:9px;height:9px;margin:0 4px 0 8px;border-radius:2px}}.vb{{grid-template-columns:1.3in 1fr .35in}}
.evc{{background:#fff;border-radius:12px;border:1px solid #E7E3DA;border-left:4px solid {AC};padding:.12in .14in;font-size:8pt}}.evc p{{margin:.03in 0;line-height:1.35}}.evh{{font-size:7.3pt;color:#6E6A63}}.q{{color:#5E5A52;font-style:italic}}a{{color:{AC};font-weight:700;text-decoration:none}}
.mgrid{{display:grid;gap:.12in}}.mc{{background:#fff;border-radius:12px;border:1px solid #E7E3DA;padding:.12in;text-align:center}}.mc .av{{width:.7in;height:.7in}}.gauge{{position:relative;width:120px;margin:.04in auto 0}}.gauge b{{position:absolute;left:0;right:0;bottom:0;font-size:15pt}}.ml{{font-size:6.9pt;color:#6E6A63}}.ms{{font-size:7.3pt;margin:.04in 0}}.mq{{font-size:6.9pt;color:#5E5A52;text-align:left;border-top:1px solid #EEEAE2;padding-top:.04in}}
.tlist{{display:flex;flex-direction:column;gap:4px}}.ti{{font-size:8pt;background:#fff;border-radius:8px;padding:5px 10px;border:1px solid #EEEAE2}}.ti span{{color:#6E6A63;margin-right:8px}}
.g3a{{display:grid;grid-template-columns:1.25fr .9fr 1.1fr;gap:.14in}}.tag{{display:inline-block;font-size:7pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;border-radius:99px;padding:2px 9px;margin-bottom:.06in}}.t1{{background:#FFE9D2;color:#9A4A00}}.t2{{background:#E9E5FF;color:{AC}}}
.cl p,.cl li{{font-size:8.2pt;line-height:1.4}}.cl ul{{padding-left:1em;margin:0}}.cr{{display:grid;grid-template-columns:.95in 1fr;gap:2px 8px;font-size:8pt;padding:.06in 0;border-bottom:1px solid #EEEAE2}}.cr em{{grid-column:2;font-size:7.2pt;color:#6E6A63;font-style:normal}}
.est,.stamp{{font-size:6.8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#9A4A00;background:#FFE9D2;border-radius:99px;padding:2px 8px}}.fx{{font-size:9pt;margin:.08in 0}}
.g2p{{display:grid;grid-template-columns:1fr 1fr;gap:.18in}}.fut{{position:relative}}.stamp{{position:absolute;right:.16in;top:.16in;border:1.5px dashed #9A4A00;background:#FFF7EE}}.plac{{font-size:54pt;font-weight:700;line-height:1;margin-top:.12in}}.plac span{{font-size:28pt;color:#9A958C;margin:0 .1in}}.pl{{font-size:8pt;color:#6E6A63}}
.fxb{{margin:.18in 0 .1in}}.fxl{{position:relative;height:14px;background:#F0EDE6;border-radius:7px}}.fxl i{{position:absolute;top:0;bottom:0;background:{AC};opacity:.35;border-radius:7px}}.fxl b{{position:absolute;top:-4px;width:4px;height:22px;background:{AC};border-radius:2px}}.fxt{{font-size:9pt;margin-top:.08in}}.muda{{font-size:8pt;line-height:1.45;padding-left:1em;color:#3A3833}}
.vtl{{display:flex;flex-direction:column;gap:5px;border-left:3px solid #E7E3DA;margin-left:.9in;padding-left:.2in}}.vt{{position:relative;font-size:8.1pt;background:#fff;border:1px solid #EEEAE2;border-radius:8px;padding:5px 10px}}.vd{{position:absolute;left:-1.12in;top:6px;width:.8in;text-align:right;font-size:7.5pt;color:#6E6A63}}.vt>i{{position:absolute;left:-.29in;top:8px;width:11px;height:11px;border-radius:50%;border:2px solid #fff}}.vk{{font-size:6.8pt;font-weight:700;text-transform:uppercase}}
.fim{{padding:0;display:grid;grid-template-columns:1fr 1fr;background:#0B0B0B;color:#fff}}.ffoto{{background-size:cover}}.fc{{padding:.5in .5in;display:flex;flex-direction:column;gap:.12in}}.fim h2{{font-size:20pt;margin-top:.2in}}.fimc{{font-size:8pt;line-height:1.5;color:#CFCAC0}}
.tl2{{display:flex;flex-direction:column;gap:5px}}.ev2{{display:grid;grid-template-columns:14px .85in 1.1in 1fr;align-items:center;gap:6px;font-size:8pt;border-bottom:1px solid #EEEAE2;padding:3px 0}}.ev2 i{{width:11px;height:11px;border-radius:50%}}.ev2 i.r{{background:{AC}}}.ev2 i.m{{background:{AC2}}}.ev2 em{{color:#6E6A63;font-style:normal}}
.pp .card{{min-height:5.6in}}.pp .br{{font-size:10pt;margin:.14in 0;grid-template-columns:1.6in 1fr .5in .55in}}.pp .bt{{height:14px}}.pp h3{{font-size:12pt;margin:.06in 0 .16in}}.pp .nt{{font-size:8pt;margin-top:.2in}}.pp .plac{{font-size:80pt;margin-top:.3in}}.pp .muda{{font-size:9.5pt;margin-top:.3in}}.pp .fxt{{font-size:11pt}}
.ft{{width:100%;border-collapse:separate;border-spacing:6px 0;font-size:7.6pt;table-layout:fixed}}.ft th{{background:#fff;border-radius:10px 10px 0 0;padding:.08in .04in;border:1px solid #E7E3DA;border-bottom:0}}.ft th:first-child{{background:none;border:0;width:1.25in}}.ft .av{{width:.6in;height:.6in}}
.ft td{{background:#fff;border-left:1px solid #E7E3DA;border-right:1px solid #E7E3DA;padding:5px 7px;vertical-align:top;line-height:1.32}}.ft td.fl{{background:none;border:0;font-weight:650;color:#3A3833;font-size:7.8pt}}.ft tr:last-child td:not(.fl){{border-bottom:1px solid #E7E3DA;border-radius:0 0 10px 10px}}.fq{{font-style:italic;color:#4A4741}}
.pag{{position:absolute;right:.45in;bottom:.15in;font-size:7.5pt;font-weight:700;color:{GOLD}}}"""
base = f"{P}/relatorio_painel"
open(base + ".html", "w").write(leve_html(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(nome_curto)} · {NOME}</title><style>{CSS}</style></head><body>{"".join(S)}</body></html>'))
js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(base)}.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(base)}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
if r.returncode == 0: leve_pdf(base + ".pdf")
print(base + ".pdf" if r.returncode == 0 else r.stderr[-400:], TOT, "páginas", (os.path.getsize(base + ".pdf") // 1024 if r.returncode == 0 else 0), "KB")
