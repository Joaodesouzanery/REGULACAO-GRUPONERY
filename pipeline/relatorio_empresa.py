"""Relatório por EMPRESA (até 3 agências) — formato do rascunho de 11/2026 (identidade Circle, 16:9).
Uso: python3 pipeline/relatorio_empresa.py clientes/<cliente>/<pasta>   (lê empresa.json; gera relatorio_empresa.html/.pdf)
empresa.json: {"nome": "...", "cnpj": "...", "aliases": ["...", "..."], "agencias": ["antaq","antt"], "processos": [opcional]}
Páginas: capa (empresa) · processos + calendário · por agência: diretoria (minibio, mandato) e decisões setoriais · previsão · como ler/cobertura.
Nada é inventado: campo sem fonte aparece como «não disponível»."""
import sys, os, re, json, html, base64, sqlite3, datetime, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao
from desfecho import desfecho_item

P = sys.argv[1].rstrip("/")
EMP = json.load(open(f"{P}/empresa.json"))
AGS = [a.lower() for a in EMP.get("agencias", ["antt", "anm", "antaq"])][:3]
E = html.escape
NOME_AG = {"antt": "ANTT", "anm": "ANM", "antaq": "ANTAQ"}
SETOR_AG = {"antt": "rodovias", "anm": "mineracao", "antaq": "portos"}
TEMA_AG = {"antt": "Rodoviário e ferroviário", "anm": "Mineração", "antaq": "Aquaviário"}
D = lambda ag: "data" if ag == "antt" else f"data/{ag}"
HOJE = datetime.date.today()


def b64(p):
    if not p or not os.path.exists(p): return ""
    ext = p.rsplit(".", 1)[-1].lower().replace("jpg", "jpeg")
    return f"data:image/{ext};base64," + base64.b64encode(open(p, "rb").read()).decode()


def ld(p, d):
    try: return json.load(open(p))
    except Exception: return d


def yt(vid, ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return f"https://www.youtube.com/watch?v={vid}&t={max(p[0]*3600+p[1]*60+p[2]-3,0)}s" if not str(vid).startswith("ata_") else ""


def fmtd(s):
    try: return datetime.date.fromisoformat(s[:10]).strftime("%d/%m/%Y")
    except Exception: return s or "—"


# ---------- dados por agência ----------
AG = {}
for ag in AGS:
    pr = previsao.calcular(ag, EMP["aliases"])
    c = previsao.conn(ag)
    its = pr["itens"]
    des = collections.Counter(desfecho_item(c, i["id"]) for i in its)
    mand = ld(f"{D(ag)}/mandatos.json", [])
    bios = {b["diretor"]: b for b in ld(f"{D(ag)}/bios.json", [])}
    vac = ld(f"{D(ag)}/vacancias.json", [])
    dirs = []
    for d in pr["colegiado"]:
        ms = [m for m in mand if m.get("diretor") == d]
        m = ms[-1] if ms else {}
        fim = m.get("fim") or m.get("fim_legal") or m.get("fim_mandato")
        ids = [i["id"] for i in its]
        vs = [v for v in c.execute("select v.categoria, v.eh_relator from votos v where v.diretor=? and v.item_id in (%s)" % ",".join("?" * len(ids)), [d] + ids)] if ids else []
        cat = collections.Counter(v[0] for v in vs)
        dirs.append({"nome": d, "cargo": (bios.get(d) or {}).get("cargo") or m.get("cargo") or "Diretor(a)",
                     "bio": (bios.get(d) or {}).get("minibio") or "Minibio não disponível (pesquisa pendente).",
                     "fim": fim, "n": len(vs), "rel": sum(v[1] for v in vs),
                     "ac": cat["acompanha"] + cat["revisor_acompanha"], "dv": cat["vencido"] + cat["revisor_diverge"], "vista": cat["vista"],
                     "p": pr["por_diretor"].get(d, (None, 0))})
    pend = [i for i in its if desfecho_item(c, i["id"]) == "pendente" and i["data"] >= (HOJE - datetime.timedelta(days=540)).isoformat()]
    procs = collections.OrderedDict()
    for i in reversed(its):
        k = (i["processo"] or "").strip() or f"{i['assunto'][:40]}…"
        if k not in procs: procs[k] = i
    # evidências: as 2 decisões mais recentes com relator
    ev = []
    for i in reversed(its):
        r = c.execute("select diretor, voto, justificativa from votos where item_id=? and eh_relator=1", (i["id"],)).fetchone()
        if r: ev.append((i, r))
        if len(ev) == 2: break
    AG[ag] = {"pr": pr, "its": its, "des": des, "dirs": dirs, "vac": [v for v in vac if not v.get("fim")], "pend": pend, "procs": list(procs.items())[:8], "ev": ev}

AG = {k: v for k, v in AG.items() if v["its"]} or AG
# ---------- calendário (fatos datados: fins de mandato, vagas abertas, pendências) ----------
CAL = []
for ag, a in AG.items():
    for d in a["dirs"]:
        if d["fim"] and str(d["fim"])[:4] >= str(HOJE.year) and str(d["fim"])[:4] <= str(HOJE.year + 1):
            CAL.append((str(d["fim"])[:10], NOME_AG[ag], f"Fim do mandato de {d['nome']}", "mandato"))
    for v in a["vac"]:
        CAL.append((v["inicio"], NOME_AG[ag], f"Vaga aberta: {v['cadeira']} (interinos: {v.get('interinos') or '—'})", "vaga"))
    for i in a["pend"][-4:]:
        CAL.append((i["data"], NOME_AG[ag], f"Em aberto desde a RD {i['numero']}: {i['assunto'][:90]} — {i['resultado'] or 'vista/retirado'}", "pendente"))
CAL.sort()

# ---------- HTML ----------
SET = SETOR_AG[next(iter(AG))]
REC = "docs/marca/setores/recortes"
FOCO = ld("docs/marca/setores/foco.json", {})
LOGO = b64("docs/marca/circle/logo_circle_branco.png"); LOGO_P = b64("docs/marca/circle/logo_circle_preto.png")
usados = sorted({SETOR_AG[a] for a in AG})
IMG = "".join(f".fc-{s}{{background-image:url({b64(f'{REC}/{s}_capa.jpg')})}}.fp-{s}{{background-image:url({b64(f'{REC}/{s}_painel.jpg')})}}" for s in usados)
COR = "".join(f".s-{s}{{--ac:{v.get('cor','#C99A06')}}}" for s, v in FOCO.items())
S = []
tot_it = sum(len(a["its"]) for a in AG.values())
chips = "".join(f'<span class="chip s-{SETOR_AG[a]}">{NOME_AG[a]} · {len(AG[a]["its"])} itens</span>' for a in AG)
S.append(f'''<section class="pg capa fc-{SET}"><div class="veu"></div><div class="cartao">{f'<img class="logo" src="{LOGO}">' if LOGO else ''}
<div class="eyebrow">Inteligência regulatória · empresa</div><h1>{E(EMP["nome"])}</h1>
<div class="cnpj">CNPJ {E(EMP.get("cnpj") or "não informado")}</div><div class="onda"></div><div class="chips">{chips}</div>
<p>{tot_it} decisões de diretoria envolvendo a empresa nas agências acima, com o voto de cada diretor, o colegiado atual, mandatos e previsão de placar.</p>
<div class="meta">{HOJE.strftime("%d/%m/%Y")} · base até {", ".join(f"{NOME_AG[a]} {fmtd(AG[a]['pr']['base_ate'])}" for a in AG)}</div></div></section>''')
# processos + calendário
linhas = "".join(f'<tr><td><b>{NOME_AG[ag]}</b></td><td>{E(k[:34])}</td><td>{E(i["assunto"][:70])}</td><td>{fmtd(i["data"])}</td><td>{E(desfecho_item(previsao.conn(ag), i["id"]))}</td></tr>'
                 for ag, a in AG.items() for k, i in a["procs"][:max(3, 11 // len(AG))])
cal = "".join(f'<li class="k-{t}"><span>{fmtd(d)}</span><b>{E(ag)}</b>{E(txt)}</li>' for d, ag, txt, t in CAL[-9:]) or "<li>Sem fatos datados futuros na base.</li>"
S.append(f'''<section class="pg proc"><header class="top"><span class="num">01</span><span>Processos e calendário</span>{f"<img src='{LOGO_P}' class='logo-p'>" if LOGO_P else ""}</header>
<div class="duas"><div><h3>Processos mais recentes na diretoria</h3><table class="tab"><thead><tr><th>Agência</th><th>Processo (citado em sessão)</th><th>Assunto</th><th>Última decisão</th><th>Desfecho p/ empresa*</th></tr></thead><tbody>{linhas}</tbody></table>
<p class="nota">*Pelo voto do relator; aproximado. Nº de processo vem da legenda automática — conferir no SEI.</p></div>
<div><h3>Calendário e próximos passos</h3><ul class="cal">{cal}</ul><p class="nota">Pautas futuras ainda não publicadas não estão na base; itens «em aberto» = vista ou retirados de pauta.</p></div></div></section>''')
n = 1
for ag, a in AG.items():
    s = SETOR_AG[ag]; n += 1
    cards = "".join(f'''<div class="dc s-{s}"><div class="dc-n">{E(d["nome"])}</div><div class="dc-c">{E(d["cargo"][:70])}</div><p>{E(d["bio"][:240])}</p>
<div class="dc-m">Mandato até <b>{fmtd(str(d["fim"])) if d["fim"] else "não informado"}</b></div><div class="dc-m">Na empresa: {d["n"]} votos · {d["rel"]} relatorias</div></div>''' for d in a["dirs"])
    S.append(f'''<section class="pg dirp s-{s}"><div class="q-f fp-{s}"><div class="q-veu"></div><div class="q-tag">{NOME_AG[ag]}</div><div class="q-n">{n:02d}</div></div>
<div class="q-c"><header class="top"><span class="num">{n:02d}</span><span>Diretoria · {NOME_AG[ag]}</span>{f"<img src='{LOGO_P}' class='logo-p'>" if LOGO_P else ""}</header><h2>Quem decide hoje</h2>
<div class="dgrid">{cards}</div><div class="sup"><b>Superintendentes:</b> a incluir (pesquisa programada). <b>Vagas abertas:</b> {E("; ".join(v["cadeira"] for v in a["vac"]) or "nenhuma registrada")}.</div>
<div class="rod">Mandatos: Senado/DOU (mandatos.json, conferência mensal). Minibios com fontes em bios.json.</div></div></section>''')
    n += 1
    mx = max([d["n"] for d in a["dirs"]] + [1])
    bars = "".join(f'<div class="mb"><span class="mb-l">{E(d["nome"])}</span><span class="mb-t"><i class="r" style="width:{100*d["rel"]/mx:.0f}%"></i><i class="a" style="width:{100*d["ac"]/mx:.0f}%"></i><i class="d" style="width:{100*(d["dv"]+d["vista"])/mx:.0f}%"></i></span><b>{d["n"]}</b></div>' for d in a["dirs"])
    des = " · ".join(f"{k} {v}" for k, v in a["des"].most_common())
    evs = "".join(f'''<article class="ev"><h4>RD {E(str(i["numero"]))} · {fmtd(i["data"])} · item {E(str(i["item"]))}</h4><p>{E(i["assunto"][:150])}</p><p><b>Relator {E(r["diretor"])}:</b> {E((r["voto"] or "")[:110])}</p>
{f'<p class="ev-t">«{E((r["justificativa"] or "")[:160])}»</p>' if r["justificativa"] else ""}{f'<a class="btn" href="{yt(i["video_id"], i["ts"])}">▶ assistir no minuto</a>' if yt(i["video_id"], i["ts"]) else ""}</article>''' for i, r in a["ev"])
    S.append(f'''<section class="pg setp s-{s}"><div class="q-c full"><header class="top"><span class="num">{n:02d}</span><span>Decisões setoriais · {NOME_AG[ag]} · {TEMA_AG[ag]}</span>{f"<img src='{LOGO_P}' class='logo-p'>" if LOGO_P else ""}</header>
<h2>Como o colegiado atual vota nos temas da empresa</h2><p class="lead">{len(a["its"])} decisões envolvendo a empresa ({fmtd(a["its"][0]["data"]) if a["its"] else "—"} a {fmtd(a["its"][-1]["data"]) if a["its"] else "—"}). Desfecho para a empresa: {E(des)}. Temas: {E(", ".join(a["pr"]["temas"]))}.</p>
<div class="meio"><div class="mini"><div class="mini-h">Votos de cada diretor nos itens da empresa · <i class="lg r"></i>relatou <i class="lg a"></i>acompanhou <i class="lg d"></i>divergiu/vista</div>{bars}</div>
<div class="evs">{evs}</div></div><div class="rod">Fonte: reuniões públicas de diretoria (vídeos oficiais); legenda automática pode errar nomes e valores.</div></div></section>''')
# previsão
n += 1
blocos = ""
for ag, a in AG.items():
    pr = a["pr"]; ac, tt = pr["backtest"]
    pd = "".join(f'<tr><td>{E(d)}</td><td>{p:.0%}</td><td>{k}</td></tr>' for d, (p, k) in pr["por_diretor"].items())
    blocos += f'''<div class="prev s-{SETOR_AG[ag]}"><h3>{NOME_AG[ag]}</h3><div class="placar">{pr["placar_esperado"][0]}<span>×</span>{pr["placar_esperado"][1]}</div>
<div class="pu">Chance de decisão unânime com o relator: <b>{pr["p_unanimidade"]:.0%}</b></div><table class="tab sm"><thead><tr><th>Diretor</th><th>Acompanha o relator</th><th>n</th></tr></thead><tbody>{pd}</tbody></table>
<div class="nota">Regra testada em 2025–26 (treino até 2024): acertou {ac}/{tt} = {ac/max(tt,1):.0%} (unânime ou não).</div></div>'''
leitura = []
for ag, a in AG.items():
    low = [(d, p) for d, (p, k) in a["pr"]["por_diretor"].items() if p < 0.95 and k >= 10]
    rel = sorted(a["dirs"], key=lambda d: -d["rel"])[:1]
    leitura.append(f"{NOME_AG[ag]}: o mais provável é decisão unânime nos termos do relator ({a['pr']['p_unanimidade']:.0%}). " +
                   (f"Maior chance de divergência: {', '.join(f'{d} ({1-p:.0%})' for d, p in low)}. " if low else "Nenhum diretor com histórico relevante de divergência nesses temas. ") +
                   (f"Quem mais relatou processos da empresa: {rel[0]['nome']} ({rel[0]['rel']}). " if rel and rel[0]["rel"] else "") +
                   ("Desfecho histórico para a empresa: " + ", ".join(f"{k} {v}" for k, v in a["des"].most_common(3)) + "."))
S.append(f'''<section class="pg prevp"><div class="q-c full"><header class="top"><span class="num">{n:02d}</span><span>Previsão · passado × futuro</span>{f"<img src='{LOGO_P}' class='logo-p'>" if LOGO_P else ""}</header>
<h2>Placar provável para os próximos processos da empresa</h2><div class="pgrid">{blocos}</div>
<div class="leit"><b>Leitura (inferência, gerada a partir dos números acima):</b> {E(" ".join(leitura))}</div>
<div class="rod">Modelo simples e auditável: taxa de cada diretor de acompanhar o relator nos temas da empresa (últimos 3 anos, com prior de 97%). Não prevê o mérito de um caso específico; o relatório do relator define o resultado na grande maioria dos casos.</div></div></section>''')
cob = "<br>".join(E(subprocess.run(["python3", "pipeline/cobertura_resposta.py", ag], capture_output=True, text=True).stdout.strip()).replace("\n", "<br>") for ag in AG)
S.append(f'''<section class="pg fim">{f'<img class="logo" src="{LOGO}">' if LOGO else ''}<h2>Como ler e cobertura</h2><div class="fimc">{cob}</div></section>''')
TOT = len(S)
CSS = """@page{size:13.333in 7.5in;margin:0}:root{--ink:#0B0B0B;--gold:#C99A06;--gold-2:#E2B93B;--mist:#F5F3EE;--grey:#6E6A63;--line:#E3DFD6;--ac:#C99A06}
*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:13.333in;height:7.5in;position:relative;overflow:hidden;page-break-after:always;display:flex}h1,h2,h3,h4{font-family:Rubik,Inter,sans-serif;margin:0}
[class^=fc-],[class*=" fc-"],[class^=fp-],[class*=" fp-"]{background-size:cover;background-position:center}
.capa{background-color:#151412}.veu{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,11,.65),rgba(11,11,11,.05) 75%)}
.cartao{position:absolute;left:.75in;top:.9in;width:6.2in;padding:.5in .55in;border-radius:18px;background:rgba(17,17,15,.66);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.14);color:#fff}
.logo{height:.4in;margin-bottom:.3in}.eyebrow{font-size:11pt;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-2)}.cartao h1{font-size:34pt;line-height:1.08;margin:.14in 0 .08in}
.cnpj{font-size:12pt;color:#D8D3C8}.onda{height:6px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.35) 0 10px,transparent 10px 16px);margin:.2in 0}
.chips{display:flex;gap:.1in;flex-wrap:wrap;margin-bottom:.2in}.chip{border:1px solid var(--ac);border-left:5px solid var(--ac);border-radius:99px;padding:3px 12px;font-size:10pt}
.cartao p{font-size:12pt;line-height:1.5;color:#E8E5DE;margin:0}.meta{margin-top:.25in;font-size:9pt;color:#BDB8AE}
.top{display:flex;align-items:center;gap:.12in;font-size:9pt;color:var(--grey);letter-spacing:.08em;text-transform:uppercase}.top .num{color:var(--ac);font-weight:700}.logo-p{height:.22in;margin-left:auto}
.proc{flex-direction:column;padding:.4in .55in;background:var(--mist)}.duas{display:grid;grid-template-columns:1.5fr 1fr;gap:.35in;margin-top:.2in}.duas h3{font-size:15pt;margin-bottom:.12in}
.tab{width:100%;border-collapse:collapse;font-size:8.6pt;background:#fff}.tab th{text-align:left;color:var(--grey);border-bottom:2px solid var(--ink);padding:4px 6px}.tab td{border-bottom:1px solid var(--line);padding:4px 6px;vertical-align:top}.tab.sm{font-size:8pt;margin-top:.08in}
.nota{font-size:7.5pt;color:var(--grey);margin:.06in 0 0}.cal{list-style:none;margin:0;padding:0}.cal li{background:#fff;border-left:4px solid var(--gold);padding:6px 10px;margin-bottom:6px;font-size:9pt;line-height:1.35}.cal li span{display:block;font-weight:700;color:var(--grey);font-size:8pt}.cal li b{margin-right:6px}
.cal li.k-vaga{border-color:#9B2C2C}.cal li.k-pendente{border-color:#1E3A5F}
.q-f{width:2.6in;flex:none;position:relative;background-color:#2A2824}.q-veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,11,.25),rgba(11,11,11,0) 30%,rgba(11,11,11,.7))}
.q-tag{position:absolute;top:.35in;left:.3in;font-size:10pt;font-weight:700;letter-spacing:.14em;color:#fff;border-left:3px solid var(--ac);padding-left:.1in}.q-n{position:absolute;left:.28in;bottom:.3in;font-family:Rubik;font-size:64pt;color:#fff}
.q-c{flex:1;padding:.36in .5in .5in;display:flex;flex-direction:column;min-width:0}.q-c.full{padding:.36in .55in .5in}.q-c h2{font-size:20pt;margin:.14in 0 .12in}
.dgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:.14in}.dc{background:#fff;border:1px solid var(--line);border-top:4px solid var(--ac);border-radius:10px;padding:.12in .14in}
.dc-n{font-family:Rubik;font-size:12pt;font-weight:600}.dc-c{font-size:8pt;color:var(--grey);margin:.02in 0 .05in}.dc p{font-size:8.4pt;line-height:1.38;margin:0 0 .06in}.dc-m{font-size:8pt;color:#3A3833}
.sup{margin-top:.14in;font-size:9pt;background:var(--mist);border-radius:8px;padding:8px 12px}.rod{position:absolute;left:3.1in;right:.5in;bottom:.16in;font-size:7.5pt;color:var(--grey)}.full .rod,.setp .rod,.prevp .rod{left:.55in;right:1.3in}
.lead{font-size:11pt;line-height:1.5;margin:0 0 .14in;color:#2B2925}.meio{display:grid;grid-template-columns:1fr 1.15fr;gap:.3in}.mini{background:var(--mist);border-radius:10px;padding:.14in .18in}
.mini-h{font-size:8pt;color:var(--grey);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.08in}.mb{display:flex;align-items:center;gap:.1in;font-size:9pt;margin:6px 0}.mb-l{width:1.6in}
.mb-t{flex:1;height:12px;background:#E7E3DA;border-radius:6px;display:flex;overflow:hidden}.mb-t i{display:block;height:100%}.mb-t .r,.lg.r{background:var(--ac)}.mb-t .a,.lg.a{background:#B9B2A3}.mb-t .d,.lg.d{background:#9B2C2C}
.lg{display:inline-block;width:9px;height:9px;border-radius:2px;margin:0 3px 0 8px}.mb b{width:.4in;text-align:right}
.evs{display:flex;flex-direction:column;gap:.12in}.ev{background:#fff;border:1px solid var(--line);border-left:3px solid var(--ac);border-radius:10px;padding:.12in .16in}.ev h4{font-size:10.5pt}.ev p{font-size:8.6pt;margin:.04in 0;line-height:1.4}.ev-t{font-style:italic;color:#5E5A52}
.btn{display:inline-block;margin-top:.04in;background:var(--ink);color:#fff;text-decoration:none;font-size:8pt;font-weight:600;padding:4px 11px;border-radius:99px}
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:.22in}.prev{background:#fff;border:1px solid var(--line);border-top:4px solid var(--ac);border-radius:10px;padding:.14in .18in}.prev h3{font-size:13pt}
.placar{font-family:Rubik;font-size:44pt;font-weight:500;line-height:1.1}.placar span{color:var(--grey);font-size:28pt;margin:0 6px}.pu{font-size:9.5pt}.leit{margin-top:.2in;font-size:10pt;line-height:1.5;background:var(--mist);border-radius:10px;padding:.14in .18in}
.fim{background:var(--ink);color:#fff;padding:.6in .8in;flex-direction:column}.fim h2{font-size:26pt;margin:.3in 0 .25in}.fimc{font-size:9.5pt;line-height:1.55;color:#CFCAC0}
.pag{position:absolute;right:.5in;bottom:.16in;font-size:8pt;font-weight:700;color:var(--ac)}"""
S = [s.replace("</section>", f'<div class="pag">{k+1:02d} / {TOT:02d}</div></section>', 1) if k else s for k, s in enumerate(S)]
H = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(EMP["nome"])}</title><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Rubik:wght@500;600&display=swap" rel="stylesheet"><style>{CSS}{COR}{IMG}</style></head><body>{"".join(S)}</body></html>'
open(f"{P}/relatorio_empresa.html", "w").write(H)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(P)}/relatorio_empresa.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(P)}/relatorio_empresa.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"""
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
print(f"{P}/relatorio_empresa.pdf" if r.returncode == 0 else r.stderr[-300:], TOT, "páginas,", os.path.getsize(f"{P}/relatorio_empresa.pdf") // 1024 if r.returncode == 0 else 0, "KB")
