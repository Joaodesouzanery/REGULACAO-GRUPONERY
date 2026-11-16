"""DEMO de prospecção (4 páginas, só dado público): mostra o suficiente para a empresa querer o resto.
Uso: python3 pipeline/demo_empresa.py <ag> "<Nome da empresa>" "<alias1|alias2>" [--foto caminho.jpg] [--contato "texto"]
Saída: clientes/_prospeccao/<slug>/demo_<ag>.pdf  (fora do git). Marca d'água DEMO, validade 30 dias.
Páginas: capa → painel parcial (decisões sobre a empresa, desfecho, próxima reunião) → 1 diretor aberto + demais desfocados →
«o que você recebe» (4 documentos) com previsão oculta e CTA."""
import sys, os, re, json, html, base64, datetime, subprocess, collections, math, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, mapa_tema, design as dz
from desfecho import desfecho_item
from pdf_leve import leve_html, leve_pdf

AG, NOMEEMP, ALI = sys.argv[1].lower(), sys.argv[2], sys.argv[3].split("|")
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
D = "data" if AG == "antt" else f"data/{AG}"; NOME = {"antt": "ANTT", "anm": "ANM", "antaq": "ANTAQ", "aneel": "ANEEL", "anp": "ANP"}.get(AG, AG.upper())
SET = dz.SETOR_AG.get(AG, "portos"); KIT = dz.kit(SET)
E = html.escape; HOJE = datetime.date.today(); TRES = (HOJE - datetime.timedelta(days=3 * 365)).isoformat()
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")
OUT = f"clientes/_prospeccao/{slug(NOMEEMP)}"; os.makedirs(OUT, exist_ok=True)
b64 = lambda p: ("data:image/" + p.rsplit(".", 1)[-1].replace("jpg", "jpeg") + ";base64," + base64.b64encode(open(p, "rb").read()).decode()) if p and os.path.exists(p) else ""
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if s else "—"
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
c = previsao.conn(AG)
pr = previsao.calcular(AG, ALI)
its = [i for i in pr["itens"] if i["data"] >= "2018-01-01"]
its3 = [i for i in its if i["data"] >= TRES]
DES = collections.Counter(desfecho_item(c, i["id"]) for i in its3)
board = pr["colegiado"]; bios = {b["diretor"]: b for b in ld(f"{D}/bios.json", [])}
cal = [x for x in ld(f"{D}/calendario.json", []) if x["data"] >= HOJE.isoformat()][:2]
rel = collections.Counter(c.execute("select diretor from votos where item_id=? and eh_relator=1", (i["id"],)).fetchone()[0] for i in its3 if c.execute("select 1 from votos where item_id=? and eh_relator=1", (i["id"],)).fetchone())
aberto = (rel.most_common(1)[0][0] if rel else (board[0] if board else None))
FOTOP = arg("--foto") or KIT["capa"]; FOTO = b64(FOTOP); LOGO_B, LOGO_P = b64("docs/marca/circle/logo_circle_branco.png"), b64("docs/marca/circle/logo_circle_preto.png")
NERY_B = b64("docs/marca/grupo_nery/logo_branco.png")
CONTATO = arg("--contato", "Fale com a Circle Consultoria para receber o relatório completo.")
CORES = {"favorável": dz.TONS[0], "parcial": dz.TONS[2], "neutro": dz.TONS[4], "desfavorável": dz.TINTA, "pendente": dz.LILAS}


def foto_dir(nome):
    for p in [(bios.get(nome) or {}).get("foto"), f"{D}/dirigentes/{slug(nome)}.jpg", f"docs/marca/diretores/{AG}/{slug(nome)}.jpg"]:
        if p and os.path.exists(p): return f'<div class="av" style="background-image:url({b64(p)})"></div>'
    return '<div class="av ini">' + E("".join(w[0] for w in nome.split()[:2]).upper()) + "</div>"


def rosca(cont):
    tot = sum(cont.values()) or 1; r, cx = 58, 80; a0 = -math.pi / 2; arcs = ""
    for k, v in cont.items():
        if not v: continue
        a1 = a0 + 2 * math.pi * v / tot; big = 1 if a1 - a0 > math.pi else 0
        arcs += f'<path d="M{cx + r * math.cos(a0):.1f},{cx + r * math.sin(a0):.1f} A{r},{r} 0 {big} 1 {cx + r * math.cos(a1 - 1e-4):.1f},{cx + r * math.sin(a1 - 1e-4):.1f}" stroke="{CORES.get(k, "#BBB")}" stroke-width="24" fill="none"/>'; a0 = a1
    leg = "".join(f'<div><i style="background:{CORES.get(k)}"></i>{E(k)} <b>{v}</b></div>' for k, v in cont.items() if v)
    return f'<div class="rosca"><svg width="160" height="160">{arcs}<text x="80" y="86" text-anchor="middle" class="rt">{tot}</text></svg><div class="leg">{leg}</div></div>'


def falas(lista, n=4, diretor=None):
    rows, vistos = [], set()
    for i in lista:
        q = "select * from votos where item_id=? and trecho is not null and trecho!=''" + (" and diretor=?" if diretor else "") + " order by eh_relator desc, id limit 3"
        for v in c.execute(q, (i["id"], diretor) if diretor else (i["id"],)):
            if v["trecho"][:60] in vistos: continue
            vistos.add(v["trecho"][:60])
            rows.append(f'<tr><td class="pn">{fmtd(i["data"])}<br>{i["numero"]}ª, item {E(str(i["item"]))}</td><td><b>{E(v["diretor"])}</b>{" (relator)" if v["eh_relator"] else ""}</td><td><i>«{E(v["trecho"][:230])}»</i> <a href="{mapa_tema.link(i["video_id"], v["ts"] or i["ts"], v["trecho_t"])}">▶ minuto</a></td></tr>')
            if len(rows) >= n: break
        if len(rows) >= n: break
    return ('<table class="tt"><tr><th style="width:13%">Sessão</th><th style="width:17%">Quem</th><th>O que foi dito (trecho literal da legenda)</th></tr>' + "".join(rows) + "</table>") if rows else ""


S = []
S.append(dz.capa(FOTOP, "50% 55%", f"Prévia de inteligência regulatória · {NOME}", NOMEEMP, f"Como a diretoria da {NOME} decide os temas da sua empresa",
                  f"DEMO · válida até {(HOJE + datetime.timedelta(days=30)):%d/%m/%Y} · só fontes públicas · voto de cada diretor com link do vídeo no minuto exato",
                  [(len(its3), "decisões da diretoria sobre a empresa (3 anos)"), (len(board), "diretores mapeados voto a voto"), (len(cal) or "—", "próximas reuniões no calendário"), ("4", "documentos por mês no pacote completo")]).replace("</section>", '<div class="wm">DEMO</div></section>'))
ult = list(reversed(its3))[:3]
evs = "".join(f'<li><b>{fmtd(i["data"])} · {i["numero"]}ª reunião</b> {E((i["assunto"] or "")[:110])}: <i>{E((i["resultado"] or "")[:60])}</i> <a href="{mapa_tema.link(i["video_id"], i["ts"])}">▶ vídeo no minuto</a></li>' for i in ult)
S.append(f'''<section class="pg">{f'<img src="{LOGO_P}" class="lp">' if LOGO_P else ''}<div class="tg">Prévia · {NOME}</div><h2>O que a diretoria decidiu sobre {E(NOMEEMP)}</h2><div class="g2">
<div class="card"><h3>Desfecho para a empresa (3 anos)</h3>{rosca(DES)}<p class="nt">Classificação automática pela decisão; conferida à mão no relatório completo.</p></div>
<div class="card"><h3>Decisões mais recentes</h3><ul>{evs or "<li>Sem decisões no recorte.</li>"}</ul><h3 style="margin-top:.16in">Próximas reuniões</h3><p>{" · ".join(f"{x['reuniao']}ª em {fmtd(x['data'])} ({x.get('formato', '')})" for x in cal) or "calendário oficial no relatório completo"}</p></div></div>
{f'<div class="card mt"><h3>O que foi dito nessas decisões</h3>{fl}</div>' if (fl := falas(list(reversed(its3)), 4)) else ""}<div class="wm">DEMO</div></section>''')
if aberto not in board and board: aberto = max(board, key=lambda n: rel.get(n, 0))
cards = ""
for d in sorted(board, key=lambda x: x != aberto):
    if d == aberto:
        b = bios.get(d, {}); st = mapa_tema.mapear(AG, "|".join(map(re.escape, ALI)), TRES)["por_diretor"].get(d, {})
        cards += f'''<div class="dcd open">{foto_dir(d)}<div class="dnm">{E(d)}</div><div class="dg">{E((b.get("cargo") or "Diretor(a)")[:60])}</div><p>{E((b.get("minibio") or "")[:170])}</p>
<div class="kv"><b>{st.get("n", 0)}</b> votos nos processos da empresa · <b>{st.get("rel", 0)}</b> relatorias · <b>{st.get("dv", 0)}</b> divergências</div>
{f'<p class="q">«{E((st["ev"]["justificativa"] or st["ev"]["voto"] or "")[:120])}» <a href="{mapa_tema.link(st["ev"]["video_id"], st["ev"]["ts"], st["ev"]["trecho_t"])}">▶</a></p>' if st.get("ev") else ""}</div>'''
    else:
        cards += f'<div class="dcd blur">{foto_dir(d)}<div class="dnm">{E(d)}</div><div class="lock">disponível no relatório completo</div><div class="fake"><span></span><span></span><span></span></div></div>'
S.append(f'''<section class="pg">{f'<img src="{LOGO_P}" class="lp">' if LOGO_P else ''}<div class="tg">Prévia · diretoria</div><h2>Quem decide os processos de {E(NOMEEMP)}</h2><p class="lead">Abrimos o diretor que mais relatou processos da empresa. Os demais (voto, argumentos e chance de divergir) estão no relatório completo.</p>
<div class="dgrid" style="grid-template-columns:1.6fr {" ".join(["1fr"] * max(len(board) - 1, 1))}">{cards}</div>
{f'<div class="card mt"><h3>O que {E(aberto)} disse nos processos da empresa</h3>{fl}</div>' if (fl := falas(list(reversed(its)), 2, aberto)) else ""}<div class="wm">DEMO</div></section>''')
BASE = c.execute("select count(*), count(distinct i.reuniao_id), min(r.data) from itens i join reunioes r on r.id=i.reuniao_id where r.data>='2018-01-01'").fetchone()
docs = [("1", "Relatório da empresa", "processos, calendário, diretoria e mandatos, como cada diretor vota nos seus temas, previsão"), ("2", "Boletim mensal", "alerta antes de cada reunião, respostas às suas perguntas, o mês na agência"),
        ("3", "Raio-X dos processos", "etapa, linha do tempo e prazo estimado de cada processo"), ("4", "Agenda e comparativa", "pautas, casos semelhantes e possíveis contradições")]
S.append(f'''<section class="pg">{f'<img src="{LOGO_P}" class="lp">' if LOGO_P else ''}<div class="tg">O que você recebe</div><h2>4 documentos por mês, cada afirmação com prova</h2><div class="g4">{"".join(f'<div class="card dk"><b class="nb">{a}</b><h3>{E(t)}</h3><p>{E(x)}</p></div>' for a, t, x in docs)}</div>
<div class="g2 mt"><div class="card"><h3>Previsão para o próximo processo <span class="est">estimativa</span></h3><div class="plac">●<span>×</span>●</div><p>Placar provável e chance de unanimidade, com o histórico de cada diretor e o teste no passado, no relatório completo.</p></div>
<div class="card cta"><h3>Quer ver o resto?</h3><p>{E(CONTATO)}</p><p class="nt">Fontes públicas (vídeos oficiais das reuniões, pautas, DOU). Previsões são estimativas e não substituem a publicação oficial nem orientação jurídica.</p></div></div>
<div class="card mt"><h3>A base por trás da prévia</h3>{dz.numeros([(f"{BASE[0]:,}".replace(",", "."), f"decisões da diretoria da {NOME} na base"), (BASE[1], "reuniões de diretoria analisadas"), (fmtd(BASE[2]), "primeira reunião da base"), (len(board), "diretores em exercício mapeados")])}<p class="nt">Cada decisão tem relator, voto de cada diretor, resultado, justificativa e o link do vídeo oficial no minuto. A legenda é automática: nomes e valores são conferidos no relatório.</p></div><div class="wm">DEMO</div></section>''')
S.append(dz.fim("Prévia feita só com fontes públicas (vídeos oficiais das reuniões, pautas, DOU). Previsões são estimativas e não substituem a publicação oficial nem orientação jurídica.", CONTATO, KIT["divisores"][0]))
CSS = dz.CSS + """@page{size:13.333in 7.5in;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Inter Display',Inter,system-ui,sans-serif;color:#0B1A20;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg:not(.capa):not(.fim){background:#fff;padding:.45in .6in}h1,h2,h3{margin:0;font-weight:500}a{color:#0F5468;font-weight:500;text-decoration:none}
.wm{position:absolute;right:.4in;bottom:.25in;font-size:46pt;font-weight:300;color:rgba(0,59,76,.08);letter-spacing:.1em;pointer-events:none}
.lp{position:absolute;right:.5in;top:.4in;height:.24in}.tg{font-size:8.5pt;letter-spacing:.12em;text-transform:uppercase;color:#0F5468;font-weight:500}h2{font-weight:400;color:#003B4C;font-size:21pt;margin:.06in 0 .16in}.lead{font-size:10pt;color:#3A3833;margin:-.06in 0 .16in}
.card{background:#fff;border-radius:0;border:1px solid #D5DCE0;padding:.16in .18in}.g2{display:grid;grid-template-columns:1fr 1.3fr;gap:.18in}.mt{margin-top:.18in}.card ul{margin:0;padding-left:1.1em;font-size:9pt;line-height:1.5}.card p{font-size:9pt;line-height:1.45}
.rosca{display:flex;align-items:center;gap:.14in}.rt{font-size:24pt;font-weight:500}.leg{font-size:8.5pt;display:flex;flex-direction:column;gap:4px}.leg i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px}.nt{font-size:7.4pt;color:#7A766F}
.dgrid{display:grid;gap:.14in}.dcd{background:#fff;border-radius:0;border:1px solid #D5DCE0;padding:.16in;text-align:center;position:relative}.dcd.open{border-top:4px solid #003B4C;text-align:left}.av{width:.9in;height:.9in;border-radius:50%;background-size:cover;background-position:center 20%;margin:0 auto .08in;background-color:#D5DCE0}.av.ini{display:flex;align-items:center;justify-content:center;font-size:20pt;color:#6B7780}
.open .av{margin:0 0 .08in}.dnm{font-weight:500;font-size:11pt}.dg{font-size:7.6pt;color:#6B7780}.kv{font-size:8.6pt;margin:.08in 0}.q{font-style:italic;color:#4A4741}.blur .av,.blur .dnm{filter:blur(5px)}.lock{font-size:8pt;color:#003B4C;background:#BCCFFF;border-radius:99px;padding:3px 8px;display:inline-block;margin-top:.08in}
.fake span{display:block;height:8px;background:#E6EDF0;border-radius:4px;margin:8px 0}.fake span:nth-child(2){width:70%}.fake span:nth-child(3){width:85%}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:.14in}.dk{background:#0B1A20;color:#fff;border:0}.dk p{color:#CFCAC0;font-size:8.6pt}.nb{font-size:22pt;color:#BCCFFF}.est{font-size:6.8pt;font-weight:500;text-transform:uppercase;color:#003B4C;background:#BCCFFF;border-radius:99px;padding:2px 8px}
.plac{font-size:48pt;font-weight:500;color:#C9C4BA}.plac span{font-size:24pt;margin:0 .1in}.cta{border:2px solid #003B4C}"""
base = f"{OUT}/demo_{AG}"
open(base + ".html", "w").write(leve_html(dz.sem_travessao(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Prévia {E(NOMEEMP)}</title><style>{CSS}</style></head><body>{"".join(S)}</body></html>')))
js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(base)}.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(base)}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
if r.returncode == 0: leve_pdf(base + ".pdf"); dz.densidade(base + ".html")
print(base + ".pdf" if r.returncode == 0 else r.stderr[-300:], len(its3), "decisões (3 anos)")
