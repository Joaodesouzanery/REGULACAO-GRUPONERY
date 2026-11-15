"""Sistema de design único dos documentos (padrão Grupo Nery, nov/2026).
Cores fixas: azul petróleo #003B4C + lilás #BCCFFF + cinzas. No máximo 2 cores por página; status em tons de azul/cinza com rótulo.
Páginas: capa (foto do setor/cliente) · sumário · divisor de seção (foto + número) · página técnica branca (fio no topo, «↳», «→») · fim.
Kit por setor: docs/marca/setores/kit.json (fotos e ícone por setor; agência → setor). Use: import design as d; d.documento(paginas, titulo, saida)."""
import os, json, base64, html, math, datetime, subprocess
from pdf_leve import leve_html, leve_pdf

E = html.escape
AZUL, AZUL2, LILAS, TINTA, CINZA, FIO, NEVOA = "#003B4C", "#0F5468", "#BCCFFF", "#0B1A20", "#6B7780", "#D5DCE0", "#F2F5F7"
TONS = ["#003B4C", "#2E6475", "#5E8C9A", "#93B3BE", "#C7D6DC", "#E6EDF0"]  # escala monocromática para gráficos
SETOR_AG = {"antaq": "portos", "antt": "rodovias", "anm": "mineracao", "aneel": "energia", "ana": "agua", "anp": "petroleo_gas"}
NOME_AG = {"antaq": "ANTAQ", "antt": "ANTT", "anm": "ANM", "aneel": "ANEEL", "ana": "ANA", "anp": "ANP"}


def b64(p):
    if not p or not os.path.exists(p): return ""
    ext = p.rsplit(".", 1)[-1].lower().replace("jpg", "jpeg").replace("svg", "svg+xml")
    return f"data:image/{ext};base64," + base64.b64encode(open(p, "rb").read()).decode()


def kit(setor):
    k = json.load(open("docs/marca/setores/kit.json")) if os.path.exists("docs/marca/setores/kit.json") else {}
    s = k.get(setor, {})
    capa = s.get("capa") or f"docs/marca/setores/recortes/{setor}_capa.jpg"
    divs = s.get("divisores") or [f"docs/marca/setores/recortes/{setor}_painel.jpg", capa]
    return {"capa": capa, "divisores": divs, "icone": s.get("icone"), "foco": s.get("foco", {})}


MARCAS = {"circle_b": "docs/marca/circle/logo_circle_branco.png", "circle_p": "docs/marca/circle/logo_circle_preto.png",
          "nery_b": "docs/marca/grupo_nery/logo_branco.png", "nery_a": "docs/marca/grupo_nery/logo_azul.png", "simbolo": "docs/marca/grupo_nery/simbolo_lilas.png"}
_cache = {}
def img(k):
    if k not in _cache: _cache[k] = b64(MARCAS.get(k, k))
    return _cache[k]


# ---------------- páginas ----------------
def capa(foto, foco, eyebrow, titulo, subtitulo, linha_fina, numeros, logo_cliente=None):
    nums = "".join(f'<div class="cn"><b>{E(str(a))}</b><span>{E(t)}</span></div>' for a, t in numeros)
    return f'''<section class="pg capa"><div class="cf" style="background-image:url({b64(foto)});background-position:{foco}"></div><div class="cv"></div>
<div class="ctop"><img src="{img("circle_b")}" class="lgc"><span class="sep"></span><span class="parc">em parceria com</span><img src="{img("nery_b")}" class="lgn"></div>
<div class="cbody"><div class="eb">{E(eyebrow)}</div>{f'<div class="lcli"><img src="{b64(logo_cliente)}"></div>' if logo_cliente else ''}<h1>{E(titulo)}</h1><div class="cs">{E(subtitulo)}</div><div class="cl">{E(linha_fina)}</div></div>
<div class="cbar">{nums}</div></section>'''


def sumario(itens, foto, foco="50% 50%"):
    li = "".join(f'<div class="si"><span class="sn">{k + 1:02d}</span><div><b>{E(t)}</b><span>{E(d)}</span></div></div>' for k, (t, d) in enumerate(itens))
    return f'''<section class="pg sum"><div class="sf" style="background-image:url({b64(foto)});background-position:{foco}"></div>
<div class="sc"><div class="eb az">Conteúdo</div><h2 class="sh">O que está neste documento</h2><div class="sl">{li}</div></div></section>'''


def divisor(n, titulo, texto, foto, foco="50% 50%"):
    return f'''<section class="pg div"><div class="df" style="background-image:url({b64(foto)});background-position:{foco}"></div><div class="dv"></div>
<div class="dc"><div class="dn">{n:02d}</div><h2>{E(titulo)}</h2><p>{E(texto)}</p></div><img src="{img("simbolo")}" class="dsim"></section>'''


def tecnica(secao, titulo, corpo, ag, rodape="", logo_cliente=None):
    return f'''<section class="pg tec"><header><span class="hs">{E(NOME_AG.get(ag, ag.upper()))} · {E(secao)}</span><span class="hsp"></span>{f'<img src="{b64(logo_cliente)}" class="hcli">' if logo_cliente else ''}<img src="{img("nery_a")}" class="hn"></header>
<h2 class="th">{E(titulo)}</h2><div class="tb">{corpo}</div>{f'<div class="trod">{rodape}</div>' if rodape else ''}</section>'''


def fim(texto, contato=""):
    return f'''<section class="pg fim"><img src="{img("simbolo")}" class="fsim"><div class="fc"><div class="ftop"><img src="{img("circle_b")}" class="lgc"><span class="sep"></span><span class="parc">em parceria com</span><img src="{img("nery_b")}" class="lgn"></div>
<p>{texto}</p>{f'<p class="fct">{E(contato)}</p>' if contato else ''}</div></section>'''


# ---------------- blocos ----------------
def conceito(n, titulo, sub, itens=None, texto=None):
    """bloco no estilo «Conceito 1 ↳ Título» com fio no topo, subtítulo sublinhado e lista com →."""
    li = "".join(f'<li>{x}</li>' for x in (itens or []))
    return f'''<div class="cc"><div class="ccn">{E(n)}</div><div class="cct">↳ {E(titulo)}</div>{f'<div class="ccs">{E(sub)}</div>' if sub else ''}
{f'<div class="cctx">{texto}</div>' if texto else ''}{f'<ul class="arr">{li}</ul>' if li else ''}</div>'''


def grade(*blocos, cols=2):
    return f'<div class="gd" style="grid-template-columns:repeat({cols},1fr)">{"".join(blocos)}</div>'


def numeros(pares):
    return '<div class="nums">' + "".join(f'<div><b>{E(str(a))}</b><span>{E(t)}</span></div>' for a, t in pares) + "</div>"


def tabela(cab, linhas, larg=None):
    th = "".join(f'<th{f" style=width:{larg[k]}" if larg else ""}>{E(c)}</th>' for k, c in enumerate(cab))
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas)
    return f'<table class="tt"><tr>{th}</tr>{tr}</table>'


def barras(linhas, fmt=lambda v: f"{v}"):
    mx = max([v for _, v, _ in linhas] + [1e-9])
    return '<div class="bb">' + "".join(f'<div class="br"><span>{E(l)}</span><i><em style="width:{100 * v / mx:.0f}%"></em></i><b>{fmt(v)}</b><small>{E(x)}</small></div>' for l, v, x in linhas) + "</div>"


def rosca(cont, rot=""):
    tot = sum(cont.values()) or 1; r, cx = 54, 70; a0 = -math.pi / 2; arcs = ""; leg = ""
    for k, (lab, v) in enumerate(cont.items()):
        if not v: continue
        cor = TONS[min(k, len(TONS) - 1)]; a1 = a0 + 2 * math.pi * v / tot
        arcs += f'<path d="M{cx + r * math.cos(a0):.1f},{cx + r * math.sin(a0):.1f} A{r},{r} 0 {1 if a1 - a0 > math.pi else 0} 1 {cx + r * math.cos(a1 - 1e-4):.1f},{cx + r * math.sin(a1 - 1e-4):.1f}" stroke="{cor}" stroke-width="18" fill="none"/>'
        leg += f'<div><i style="background:{cor}"></i>{E(str(lab))}<b>{v}</b></div>'; a0 = a1
    return f'<div class="ro"><svg width="140" height="140">{arcs}<text x="{cx}" y="{cx + 2}" text-anchor="middle" class="rt">{tot}</text><text x="{cx}" y="{cx + 18}" text-anchor="middle" class="rs">{E(rot)}</text></svg><div class="rl">{leg}</div></div>'


def citacao(texto, quem, onde, link):
    return f'<blockquote class="q">«{E(texto)}»<cite>{E(quem)} · {E(onde)}{f" · <a href={chr(34)}{link}{chr(34)}>vídeo no minuto →</a>" if link else ""}</cite></blockquote>'


def pessoa(foto_html, nome, cargo, linhas):
    return f'<div class="ps">{foto_html}<div><b>{E(nome)}</b><span>{E(cargo)}</span>{"".join(f"<p>{x}</p>" for x in linhas)}</div></div>'


def selo(t):
    return f'<span class="selo">{E(t)}</span>'


CSS = f"""@page{{size:13.333in 7.5in;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:'Inter Display',Inter,system-ui,sans-serif;color:{TINTA};-webkit-print-color-adjust:exact;print-color-adjust:exact;font-weight:400}}
.pg{{width:13.333in;height:7.5in;position:relative;overflow:hidden;page-break-after:always;background:#fff}}h1,h2,h3{{margin:0;font-weight:500;letter-spacing:-.01em}}a{{color:{AZUL};text-decoration:underline;text-underline-offset:2px}}
.eb{{font-size:8.5pt;letter-spacing:.18em;text-transform:uppercase;color:{LILAS}}}.eb.az{{color:{AZUL2}}}
.capa{{background:{AZUL};color:#fff}}.cf{{position:absolute;inset:0 0 1.35in 4.9in;background-size:cover}}.cv{{position:absolute;left:4.9in;top:0;width:1.2in;bottom:1.35in;background:linear-gradient(90deg,{AZUL},rgba(0,59,76,0))}}
.ctop{{position:absolute;left:.6in;top:.5in;display:flex;align-items:center;gap:12px}}.lgc{{height:.32in}}.lgn{{height:.24in}}.sep{{width:1px;height:.3in;background:rgba(255,255,255,.35)}}.parc{{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.65)}}
.cbody{{position:absolute;left:.6in;top:1.75in;width:4.1in}}.lcli{{background:#fff;display:inline-block;padding:8px 12px;margin:.18in 0 .08in}}.lcli img{{height:.4in;display:block}}.capa h1{{font-size:34pt;font-weight:400;line-height:1.05;margin-top:.1in}}.cs{{font-size:11.5pt;color:{LILAS};margin-top:.1in;font-weight:300}}.cl{{font-size:7.6pt;color:rgba(255,255,255,.6);margin-top:.18in;line-height:1.45}}
.cbar{{position:absolute;left:0;right:0;bottom:0;height:1.35in;background:#fff;display:grid;grid-template-columns:repeat(4,1fr);padding:.28in .6in;gap:.4in;color:{TINTA}}}.cn{{border-top:1px solid {AZUL};padding-top:.1in}}.cn b{{font-size:26pt;font-weight:300;color:{AZUL};display:block;line-height:1}}.cn span{{font-size:8pt;color:{CINZA};display:block;margin-top:.06in}}
.sum{{display:grid;grid-template-columns:4.6in 1fr}}.sf{{background-size:cover}}.sc{{padding:.7in .7in}}.sh{{font-size:24pt;font-weight:300;color:{AZUL};margin:.12in 0 .35in}}.sl{{display:grid;grid-template-columns:1fr 1fr;gap:.28in .5in}}.si{{display:flex;gap:.18in;border-top:1px solid {FIO};padding-top:.12in}}.sn{{font-size:22pt;font-weight:300;color:{AZUL2};line-height:1}}.si b{{display:block;font-weight:500;font-size:11pt}}.si span{{font-size:8.6pt;color:{CINZA};line-height:1.4}}
.div{{background:{AZUL};color:#fff}}.df{{position:absolute;inset:0 0 0 5.4in;background-size:cover}}.dv{{position:absolute;left:5.4in;top:0;bottom:0;width:1.4in;background:linear-gradient(90deg,{AZUL},rgba(0,59,76,0))}}
.dc{{position:absolute;left:.7in;top:1.6in;width:4.5in}}.dn{{font-size:84pt;font-weight:200;color:{LILAS};line-height:1}}.div h2{{font-size:28pt;font-weight:400;margin:.18in 0 .14in}}.div p{{font-size:10.5pt;line-height:1.55;color:rgba(255,255,255,.8);font-weight:300}}.dsim{{position:absolute;left:.7in;bottom:.55in;height:.32in;opacity:.9}}
.tec{{padding:.45in .6in .4in}}.tec header{{display:flex;align-items:center;gap:12px;border-top:1px solid {TINTA};padding-top:.1in}}.hs{{font-size:7.6pt;letter-spacing:.14em;text-transform:uppercase;color:{CINZA}}}.hsp{{flex:1}}.hn{{height:.2in}}.hcli{{height:.22in}}
.th{{font-size:20pt;font-weight:400;color:{AZUL};margin:.2in 0 .2in;max-width:10.5in}}.tb{{font-size:9.2pt;line-height:1.5}}.trod{{position:absolute;left:.6in;right:.6in;bottom:.22in;font-size:6.8pt;color:{CINZA};border-top:1px solid {FIO};padding-top:.05in}}
.gd{{display:grid;gap:.25in .45in}}.cc{{border-top:1px solid {FIO};padding-top:.1in}}.ccn{{font-size:13pt;color:{AZUL2};font-weight:400}}.cct{{font-size:13pt;color:{AZUL2};font-weight:400;margin-bottom:.1in}}.ccs{{text-decoration:underline;text-underline-offset:3px;margin-bottom:.1in;font-size:9.4pt}}
.cctx p{{margin:0 0 .08in;text-align:justify;hyphens:auto}}ul.arr{{list-style:none;padding:0;margin:0}}ul.arr li{{padding-left:.3in;position:relative;margin:.04in 0}}ul.arr li:before{{content:"→";position:absolute;left:0;color:{AZUL2}}}
.nums{{display:grid;grid-template-columns:repeat(4,1fr);gap:.3in;margin:.05in 0 .2in}}.nums div{{border-top:1px solid {AZUL};padding-top:.07in}}.nums b{{font-size:22pt;font-weight:300;color:{AZUL};display:block;line-height:1.05}}.nums span{{font-size:7.8pt;color:{CINZA}}}
table.tt{{width:100%;border-collapse:collapse;font-size:8pt}}.tt th{{text-align:left;font-weight:500;color:{CINZA};font-size:7.2pt;letter-spacing:.06em;text-transform:uppercase;border-bottom:1px solid {TINTA};padding:4px 6px}}.tt td{{border-bottom:1px solid {FIO};padding:5px 6px;vertical-align:top;line-height:1.35}}
.bb .br{{display:grid;grid-template-columns:1.5in 1fr .45in .55in;gap:8px;align-items:center;font-size:8.4pt;margin:5px 0}}.br i{{height:6px;background:{NEVOA};display:block}}.br em{{display:block;height:100%;background:{AZUL}}}.br b{{font-weight:500}}.br small{{color:{CINZA};font-size:7.2pt}}
.ro{{display:flex;align-items:center;gap:.16in}}.rt{{font-size:20pt;font-weight:300;fill:{AZUL}}}.rs{{font-size:7pt;fill:{CINZA}}}.rl div{{font-size:8pt;display:flex;align-items:center;gap:6px;margin:3px 0}}.rl i{{width:9px;height:9px;display:inline-block}}.rl b{{margin-left:auto;padding-left:10px;font-weight:500}}
blockquote.q{{margin:.08in 0;padding:.04in 0 .04in .16in;border-left:2px solid {LILAS};font-size:8.8pt;font-style:italic;color:{TINTA}}}blockquote.q cite{{display:block;font-style:normal;font-size:7.2pt;color:{CINZA};margin-top:.03in}}
.ps{{display:flex;gap:.14in;border-top:1px solid {FIO};padding-top:.1in}}.ps .av{{width:.72in;height:.72in;border-radius:50%;background-size:cover;background-position:center 20%;flex:none;background-color:{NEVOA};filter:saturate(.85)}}.ps .av.ini{{display:flex;align-items:center;justify-content:center;color:{AZUL2};font-size:14pt}}.ps b{{display:block;font-weight:500;font-size:10pt}}.ps span{{font-size:7.6pt;color:{CINZA}}}.ps p{{margin:.04in 0 0;font-size:8pt;line-height:1.4}}
.selo{{display:inline-block;font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;background:{LILAS};color:{AZUL};padding:2px 8px;font-weight:600}}
.fim{{background:{AZUL};color:#fff}}.fsim{{position:absolute;right:.9in;top:1.6in;height:3.6in;opacity:.12}}.fc{{position:absolute;left:.7in;top:.6in;right:5in}}.ftop{{display:flex;align-items:center;gap:12px;margin-bottom:.9in}}.fc p{{font-size:8.6pt;line-height:1.6;color:rgba(255,255,255,.78);font-weight:300}}.fct{{font-size:11pt!important;color:{LILAS}!important}}"""


def documento(paginas, titulo, saida):
    H = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(titulo)}</title><style>{CSS}</style></head><body>{"".join(paginas)}</body></html>'
    open(saida + ".html", "w").write(leve_html(H))
    js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(saida)}.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(saida)}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
    if r.returncode: raise SystemExit(r.stderr[-400:])
    leve_pdf(saida + ".pdf")
    return saida + ".pdf"
