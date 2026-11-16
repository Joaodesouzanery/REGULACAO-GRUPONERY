"""Sistema de design único dos documentos (padrão Grupo Nery, nov/2026).
Cores fixas: azul petróleo #003B4C + lilás #BCCFFF + cinzas. No máximo 2 cores por página; status em tons de azul/cinza com rótulo.
Páginas: capa (foto do setor/cliente) · sumário · divisor de seção (foto + número) · página técnica branca (fio no topo, «↳», «→») · fim.
Kit por setor: docs/marca/setores/kit.json (fotos e ícone por setor; agência → setor). Use: import design as d; d.documento(paginas, titulo, saida)."""
import os, re, json, base64, html, math, datetime, subprocess
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


def fim(texto, contato="", foto=None, foco="50% 50%", titulo="Obrigado."):
    """encerramento estilo brochura: página azul, foto do setor ao fundo, «Obrigado.» grande e faixa branca de contato no rodapé."""
    fo = f'<div class="ff" style="background-image:url({b64(foto)});background-position:{foco}"></div><div class="fv"></div>' if foto else ""
    return f'''<section class="pg fim">{fo}<div class="fc"><div class="ftop"><img src="{img("circle_b")}" class="lgc"><span class="sep"></span><span class="parc">em parceria com</span><img src="{img("nery_b")}" class="lgn"></div>
<h2 class="fh">{E(titulo)}</h2><span class="fr"></span><p>{texto}</p></div>
<div class="fbar"><img src="{img("nery_a")}" class="hn"><span class="fsp"></span><span>{E(contato)}</span></div></section>'''


def whitepaper(rotulo, itens, intro="", foto=None, foco="50% 50%", h_foto="2.1in"):
    """bloco no estilo whitepaper: rótulo azul à esquerda, linhas «01 Título →» com parágrafo à direita, fio entre itens, foto arredondada embaixo.
    itens = [(titulo, html_texto)]"""
    li = "".join(f'<div class="wr"><span class="wn">{k + 1:02d}</span><span class="wt">{E(t)}</span><span class="wa">→</span><div class="wx">{x}</div></div>' for k, (t, x) in enumerate(itens))
    return (f'<div class="wp"><div class="wl">{E(rotulo)}</div><div class="wi">{intro}</div></div>{li}'
            + (f'<div class="wf" style="height:{h_foto};background-image:url({b64(foto)});background-position:{foco}"></div>' if foto else ""))


def lista_tripla(cols):
    """3 colunas numeradas com → (estilo «Getting Started»). cols=[(titulo,[itens])]"""
    return '<div class="l3">' + "".join(f'<div><div class="l3h"><span>{k + 1}</span><u>{E(t)}</u></div><ul class="arr sm">{"".join(f"<li>{x}</li>" for x in xs)}</ul></div>' for k, (t, xs) in enumerate(cols)) + "</div>"


def quadro_mandatos(cadeiras, desde="2018-01-01", ate=None, foto_fn=None, ex=False):
    """controle da diretoria por cadeira: ocupante atual + linha do tempo de ocupantes (VAGO hachurado) + substitutos.
    cadeiras=[{"cadeira","ocupantes":[{"nome","tipo","ordem_mandato","inicio","fim_legal","posse","saida","decreto"}],"lista_triplice"}]"""
    hoje = (ate or datetime.date.today().isoformat())
    t0, t1 = datetime.date.fromisoformat(desde), datetime.date.fromisoformat(hoje)
    W = (t1 - t0).days or 1
    pos = lambda x: max(0, min(100, 100 * (datetime.date.fromisoformat(str(x)[:10]) - t0).days / W)) if x else 100
    fd = lambda x: datetime.date.fromisoformat(str(x)[:10]).strftime("%d/%m/%Y") if x and len(str(x)) >= 10 else (str(x) if x else "—")
    anos = "".join(f'<span style="left:{pos(f"{a}-01-01")}%">{a}</span>' for a in range(t0.year, t1.year + 1))
    out = f'<div class="qm"><div class="qmh"><span>Cadeira</span><span>Em exercício</span><span class="qax">{anos}</span></div>'
    for cad in cadeiras:
        oc = [o for o in cad.get("ocupantes", []) if (o.get("saida") or o.get("fim_legal") or hoje) >= desde]
        tit = [o for o in oc if (o.get("tipo") or "titular").lower().startswith("tit")]
        atual = next((o for o in oc if not o.get("saida") and (o.get("posse") or o.get("inicio") or "9") <= hoje and (o.get("fim_legal") or "9") >= hoje), None)
        barras = ""
        for o in oc:
            a, b = o.get("posse") or o.get("inicio"), o.get("saida") or (o.get("fim_legal") if (o.get("fim_legal") or "9") < hoje else hoje)
            if not a: continue
            sub = not (o.get("tipo") or "titular").lower().startswith("tit")
            l, r = pos(a), pos(b)
            ant = o is not atual and not sub
            barras += f'<i class="{"qs" if sub else "qx" if ant else "qt"}" style="left:{l}%;width:{max(r - l, .4)}%" title="{E(o["nome"])}"><em>{E(o["nome"].split()[0] + " " + o["nome"].split()[-1]) if r - l > 9 else ""}</em></i>'
        cr = f'<i class="qn" style="left:0;width:{pos(cad["criada"])}%"></i>' if cad.get("criada") else ""
        barras = f'<div class="qv"></div>' + cr + barras  # fundo hachurado = vago
        if atual:
            ft = foto_fn(atual.get("nome_chave") or atual["nome"]) if foto_fn else ""
            info = (f'{ft}<div><b>{E(atual["nome"])}</b><span>{E((atual.get("tipo") or "Titular").capitalize())}'
                    f'{" · " + str(atual["ordem_mandato"]) + "º mandato da cadeira" if atual.get("ordem_mandato") else ""}</span>'
                    f'<span>mandato {fd(atual.get("inicio"))} → {fd(atual.get("fim_legal"))} · posse {fd(atual.get("posse"))}</span>'
                    f'<span>{E(atual.get("decreto") or "decreto a confirmar")}</span></div>')
        else:
            info = '<div><b class="qvago">VAGO</b><span>sem titular em exercício</span></div>'
        hist = " · ".join(f'{E(o["nome"].split()[0] + " " + o["nome"].split()[-1])} ({fd(o.get("posse") or o.get("inicio"))[-4:]}–{fd(o.get("saida"))[-4:] if o.get("saida") else "…"}{", subst." if not (o.get("tipo") or "titular").lower().startswith("tit") else ""})' for o in oc if o is not atual)
        lt = f'<div class="qlt">Lista tríplice: {E(", ".join(cad["lista_triplice"]))}</div>' if cad.get("lista_triplice") else ""
        out += f'<div class="qr"><div class="qc">{E(cad["cadeira"])}</div><div class="qa">{info}</div><div class="qb"><div class="qtl">{barras}</div><div class="qh">{hist}</div>{lt}</div></div>'
    exh = ""
    if ex:
        vistos, lst = set(), []
        atuais = {o["nome"] for cad in cadeiras for o in cad.get("ocupantes", []) if not o.get("saida")}
        for cad in cadeiras:
            for o in cad.get("ocupantes", []):
                if o.get("saida") and (o.get("saida") >= desde) and o["nome"] not in atuais and o["nome"] not in vistos and (o.get("tipo") or "titular").lower().startswith("tit"):
                    vistos.add(o["nome"]); lst.append((o, cad["cadeira"]))
        def papel(o, cad):
            return "Ex-Diretor(a)-Geral" if "Geral" in cad else "Ex-Diretor(a)"
        exh = '<div class="qex"><div class="qexh">Saíram do colegiado desde ' + desde[:4] + '</div><div class="qexg">' + "".join(
            f'<div class="qe">{foto_fn(o.get("nome_chave") or o["nome"]) if foto_fn else ""}<div><b>{E(o["nome"])}</b><span>{papel(o, cad)} · {fd(o.get("posse") or o.get("inicio"))[-4:]} a {fd(o.get("saida"))[-4:]}</span></div></div>'
            for o, cad in lst) + "</div></div>"
    return out + '<div class="qleg"><i class="qt"></i>em exercício <i class="qx"></i>ex-diretor(a) <i class="qs"></i>substituto/interino <i class="qv0"></i>vago</div>' + exh + "</div>"


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
.bb .br{{display:grid;grid-template-columns:1.4in 1fr .45in .9in;gap:8px;align-items:center;font-size:8.4pt;margin:5px 0}}.br i{{height:6px;background:{NEVOA};display:block}}.br em{{display:block;height:100%;background:{AZUL}}}.br b{{font-weight:500}}.br small{{color:{CINZA};font-size:7.2pt}}
.ro{{display:flex;align-items:center;gap:.16in}}.rt{{font-size:20pt;font-weight:300;fill:{AZUL}}}.rs{{font-size:7pt;fill:{CINZA}}}.rl div{{font-size:8pt;display:flex;align-items:center;gap:6px;margin:3px 0}}.rl i{{width:9px;height:9px;display:inline-block}}.rl b{{margin-left:auto;padding-left:10px;font-weight:500}}
blockquote.q{{margin:.08in 0;padding:.04in 0 .04in .16in;border-left:2px solid {LILAS};font-size:8.8pt;font-style:italic;color:{TINTA}}}blockquote.q cite{{display:block;font-style:normal;font-size:7.2pt;color:{CINZA};margin-top:.03in}}
.ps{{display:flex;gap:.14in;border-top:1px solid {FIO};padding-top:.1in}}.ps .av{{width:.72in;height:.72in;border-radius:50%;background-size:cover;background-position:center 20%;flex:none;background-color:{NEVOA};filter:saturate(.85)}}.ps .av.ini{{display:flex;align-items:center;justify-content:center;color:{AZUL2};font-size:14pt}}.ps b{{display:block;font-weight:500;font-size:10pt}}.ps span{{font-size:7.6pt;color:{CINZA}}}.ps p{{margin:.04in 0 0;font-size:8pt;line-height:1.4}}
.nar p{{margin:0 0 .07in;font-size:8.7pt;line-height:1.45;text-align:justify;hyphens:auto}}ul.arr.sm li{{font-size:8pt}}.tec .gd>div>blockquote.q{{font-size:8.2pt}}
.selo{{display:inline-block;font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;background:{LILAS};color:{AZUL};padding:2px 8px;font-weight:600}}
.fim{{background:{AZUL};color:#fff}}.ff{{position:absolute;inset:0 0 .85in 0;background-size:cover;opacity:.55;filter:saturate(.6)}}.fv{{position:absolute;inset:0 0 .85in 0;background:linear-gradient(90deg,{AZUL} 25%,rgba(0,59,76,.55) 60%,rgba(0,59,76,.25))}}
.fc{{position:absolute;left:.8in;top:.75in;width:6.4in}}.ftop{{display:flex;align-items:center;gap:12px;margin-bottom:1.1in}}.fim .fh{{font-size:92pt!important;font-weight:500;letter-spacing:-.03em;line-height:1;color:#fff!important;margin:0!important}}.fr{{display:block;width:.5in;height:2px;background:{LILAS};margin:.35in 0 .2in}}.fc p{{font-size:9.6pt;line-height:1.6;color:rgba(255,255,255,.85);font-weight:300}}
.fbar{{position:absolute;left:0;right:0;bottom:0;height:.85in;background:#fff;color:{TINTA};display:flex;align-items:center;gap:.3in;padding:0 .8in;font-size:9pt}}.fbar .hn{{height:.26in}}.fsp{{flex:1}}
.wp{{display:grid;grid-template-columns:3.3in 1fr;gap:.4in;border-top:1px solid {TINTA};padding-top:.12in}}.wl{{font-size:15pt;color:{AZUL2};font-weight:400}}.wi p{{margin:0 0 .08in;font-size:10pt;line-height:1.55}}
.wr{{display:grid;grid-template-columns:.4in 2.5in .4in 1fr;gap:0;border-top:1px solid {FIO};padding:.14in 0 .12in;margin-left:0}}.wr:first-of-type{{border-top:none}}.wn{{font-size:8pt;color:{AZUL2};font-weight:600;padding-top:.05in}}.wt{{font-size:13pt;font-weight:400;line-height:1.2;color:{TINTA}}}.wa{{font-size:13pt;color:{TINTA}}}.wx{{font-size:8.8pt;line-height:1.5;padding-left:.4in}}.wx p{{margin:0 0 .06in}}
.wf{{border-radius:8px;background-size:cover;margin-top:.14in;flex:1 1 0;min-height:0}}.tec{{display:flex;flex-direction:column}}.tec .tb{{flex:1 1 auto;display:flex;flex-direction:column;min-height:0;padding-bottom:.3in}}.tec .tb>*{{flex:none}}.tec .tb>.wf{{flex:1 1 0}}
.l3{{display:grid;grid-template-columns:repeat(3,1fr);gap:.3in}}.l3h{{display:flex;gap:.12in;align-items:baseline;margin-bottom:.08in}}.l3h span{{font-size:16pt;color:{AZUL2};font-weight:300}}.l3h u{{text-underline-offset:3px;font-size:9.6pt}}
.qm{{font-size:8pt}}.qmh{{display:grid;grid-template-columns:1.1in 3.6in 1fr;gap:.2in;color:{CINZA};font-size:7pt;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid {TINTA};padding-bottom:4px}}.qax{{position:relative;height:1em}}.qax span{{position:absolute;transform:translateX(-50%);letter-spacing:0}}
.qr{{display:grid;grid-template-columns:1.1in 3.6in 1fr;gap:.2in;border-bottom:1px solid {FIO};padding:.09in 0;align-items:center}}.qc{{font-size:11pt;color:{AZUL};font-weight:500}}.qa{{display:flex;gap:.12in;align-items:center}}.qa .av{{width:.56in;height:.56in;border-radius:50%;background-size:cover;background-position:center 20%;flex:none;background-color:{NEVOA}}}.qa .av.ini{{display:flex;align-items:center;justify-content:center;color:{AZUL2}}}.qa b{{display:block;font-weight:500;font-size:9pt}}.qa span{{display:block;color:{CINZA};font-size:7.4pt;line-height:1.35}}.qvago{{color:{CINZA};letter-spacing:.1em}}
.qtl{{position:relative;height:.24in}}.qv{{position:absolute;inset:0;background:repeating-linear-gradient(45deg,{NEVOA} 0 4px,#fff 4px 8px);border:1px solid {FIO}}}.qtl i{{position:absolute;top:0;bottom:0;display:block;border-right:2px solid #fff;overflow:hidden}}.qt{{background:{AZUL}}}.qs{{background:{LILAS}}}.qx{{background:#8C969C}}.qex{{margin-top:.12in;border-top:1px solid {FIO};padding-top:.08in}}.qexh{{font-size:7pt;letter-spacing:.08em;text-transform:uppercase;color:{CINZA};margin-bottom:.06in}}.qexg{{display:grid;grid-template-columns:repeat(5,1fr);gap:.1in}}.qe{{display:flex;gap:.08in;align-items:center;filter:grayscale(1)}}.qe .av{{width:.42in;height:.42in;border-radius:50%;background-size:cover;background-position:center 20%;flex:none;background-color:{NEVOA}}}.qe .av.ini{{display:flex;align-items:center;justify-content:center;font-size:8pt;color:{CINZA}}}.qe b{{display:block;font-size:7.6pt;font-weight:500}}.qe span{{font-size:6.8pt;color:{CINZA}}}.mins{{font-size:7.8pt;margin-top:.04in!important}}.mins a{{white-space:nowrap}}.nw{{white-space:nowrap;color:{CINZA}}}.qtl i.qn{{background:#fff;border:none}}.qn em{{color:{CINZA}!important}}.qtl em{{font-style:normal;color:#fff;font-size:6.6pt;padding-left:4px;line-height:.24in;white-space:nowrap}}.qs em{{color:{AZUL}}}
.qh{{font-size:6.8pt;color:{CINZA};margin-top:3px;line-height:1.35}}.qlt{{font-size:6.8pt;color:{AZUL2};margin-top:2px}}.qleg{{margin-top:.08in;font-size:7pt;color:{CINZA};display:flex;gap:.08in;align-items:center}}.qleg i{{width:14px;height:8px;display:inline-block;margin-left:.1in}}.qv0{{background:repeating-linear-gradient(45deg,{NEVOA} 0 3px,#fff 3px 6px);border:1px solid {FIO}}}"""


LIMITE_VAZIO = 1.4  # polegadas livres no pé de uma página técnica (skill pagina-cheia)


def densidade(html_path, estrito=False):
    """mede o espaço vazio no pé de cada página técnica (.pg que não é capa, sumário, divisor ou fim) e avisa acima do limite."""
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});"
          f"await p.goto('file://{os.path.abspath(html_path)}');"
          "const r=await p.evaluate(()=>[...document.querySelectorAll('.pg')].map((g,k)=>{if(/capa|sum|div|fim/.test(g.className.replace('pg','')))return null;"
          "const t=g.getBoundingClientRect();let m=t.top;g.querySelectorAll('*').forEach(e=>{if(e.closest('.trod,.pag,.rod,.wm'))return;const q=e.getBoundingClientRect();if(q.height>0&&q.width>0)m=Math.max(m,q.bottom)});"
          "return [k+1,(t.bottom-m)/96]}).filter(Boolean));console.log(JSON.stringify(r));await b.close();})();")
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
    try: res = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: return []
    ruins = [(k, v) for k, v in res if v > LIMITE_VAZIO]
    for k, v in res:
        if v < 0.05: print(f"AVISO estouro: página {k} com conteúdo passando do pé ({v:.2f} pol); reduza ou divida.")
    for k, v in ruins: print(f"AVISO densidade: página {k} com {v:.1f} pol vazias no pé (limite {LIMITE_VAZIO}); preencha com falas, votos ou precedentes (skill pagina-cheia).")
    if estrito and ruins: raise SystemExit("densidade abaixo do padrão")
    return ruins


def sem_travessao(h):
    """troca o travessão de texto corrido por vírgula (skill pagina-cheia); mantém «—» sozinho (célula vazia)."""
    return re.sub(r"(?<=\S) — (?=\S)", ", ", h).replace("→ —", "→ a definir")


def documento(paginas, titulo, saida):
    H = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(titulo)}</title><style>{CSS}</style></head><body>{"".join(paginas)}</body></html>'
    open(saida + ".html", "w").write(leve_html(sem_travessao(H)))
    js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(saida)}.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(saida)}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
    if r.returncode: raise SystemExit(r.stderr[-400:])
    leve_pdf(saida + ".pdf")
    densidade(saida + ".html")
    return saida + ".pdf"
