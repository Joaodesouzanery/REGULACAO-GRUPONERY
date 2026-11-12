"""PDF «Diretoria» de uma agência: quadro atual (foto, formação, minibio, mandato) + comparador (cada página = 1 pergunta
com TODOS os diretores lado a lado) + lote de superintendentes + cobertura. Só PDF (16:9, identidade Circle).
Uso: python3 pipeline/relatorio_diretoria.py <antt|anm|antaq> [saida_dir] [--perguntas arquivo.json]
perguntas.json (opcional): [{"titulo": "...", "tema": "concessoes_rodoviarias"|null, "metrica": "relata|diverge|desfecho|tema"}]"""
import sys, os, re, json, html, base64, sqlite3, datetime, subprocess, collections, unicodedata
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pdf_leve import leve_html, leve_pdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao
from desfecho import desfecho_item

AG = sys.argv[1].lower()
OUT = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else f"agencias/{AG}/diretoria"
os.makedirs(OUT, exist_ok=True)
D = "data" if AG == "antt" else f"data/{AG}"
NOME = {"antt": "ANTT", "anm": "ANM", "antaq": "ANTAQ"}[AG]
SET = {"antt": "rodovias", "anm": "mineracao", "antaq": "portos"}[AG]
E = html.escape
HOJE = datetime.date.today()
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")


def b64(p):
    if not p or not os.path.exists(p): return ""
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()


def foto(nome, info):
    for p in [(info or {}).get("foto"), f"docs/marca/diretores/{AG}/{slug(nome)}.jpg"]:
        if p and os.path.exists(p): return f'<div class="ft" style="background-image:url({b64(p)})"></div>'
    ini = "".join(w[0] for w in nome.split()[:2]).upper()
    return f'<div class="ft ini">{E(ini)}</div>'


def fmtd(s):
    try: return datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y")
    except Exception: return str(s) if s else "não informado"


c = previsao.conn(AG)
board, ult = previsao.colegiado_atual(c, reunioes=3)
bios = {b["diretor"]: b for b in ld(f"{D}/bios.json", [])}
mand = ld(f"{D}/mandatos.json", [])
vac = [v for v in ld(f"{D}/vacancias.json", []) if not v.get("fim")]
sups = ld(f"{D}/superintendentes.json", [])
desde = (datetime.date.fromisoformat(ult) - datetime.timedelta(days=3 * 365)).isoformat()


def mandato(d):
    ms = [m for m in mand if m.get("diretor") == d]
    m = ms[-1] if ms else {}
    return m.get("fim") or m.get("fim_legal") or m.get("fim_mandato"), m.get("cargo") or ""


def stats(d, tema=None):
    q = ("select v.categoria, v.eh_relator, v.item_id, v.justificativa, v.voto, v.ts, i.assunto, r.numero, r.data, r.video_id from votos v "
         "join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.diretor=? and r.data>=?")
    a = [d, desde]
    if tema: q += " and v.item_id in (select item_id from item_temas where tema=?)"; a.append(tema)
    R = c.execute(q, a).fetchall()
    cat = collections.Counter(r["categoria"] for r in R)
    rel = [r for r in R if r["eh_relator"]]
    temas = collections.Counter(t for r in rel for (t,) in c.execute("select tema from item_temas where item_id=?", (r["item_id"],)))
    des = collections.Counter(desfecho_item(c, r["item_id"]) for r in rel)
    pres = c.execute("select count(distinct i.reuniao_id) from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.diretor=? and r.data>=?", (d, desde)).fetchone()[0]
    fora = [r for r in R if r["categoria"] in ("vencido", "revisor_diverge", "vista")]
    ev = (fora[-1] if fora else (rel[-1] if rel else (R[-1] if R else None)))
    return {"n": len(R), "rel": len(rel), "ac": cat["acompanha"] + cat["revisor_acompanha"], "dv": cat["vencido"] + cat["revisor_diverge"], "vista": cat["vista"],
            "temas": temas.most_common(3), "des": des, "pres": pres, "ev": ev}


TOT_R = c.execute("select count(*) from reunioes where data>=?", (desde,)).fetchone()[0]
temas_top = [t for (t,) in c.execute("select tema from item_temas it join itens i on i.id=it.item_id join reunioes r on r.id=i.reuniao_id where r.data>=? group by 1 order by count(*) desc limit 2", (desde,))]
PERG = ld(sys.argv[sys.argv.index("--perguntas") + 1], None) if "--perguntas" in sys.argv else None
PERG = PERG or [
    {"titulo": "Quem mais relata — e em quais temas?", "metrica": "relata"},
    {"titulo": "Quem mais diverge do relator ou pede vista?", "metrica": "diverge"},
    {"titulo": "Quando relata, qual costuma ser o desfecho para a empresa?", "metrica": "desfecho"},
] + [{"titulo": f"Em «{t.replace('_', ' ')}», como cada diretor vota?", "tema": t, "metrica": "tema"} for t in temas_top]
ST = {d: stats(d) for d in board}
LOGO = b64("docs/marca/circle/logo_circle_branco.png").replace("jpeg", "png"); LOGO_P = b64("docs/marca/circle/logo_circle_preto.png").replace("jpeg", "png")
REC = "docs/marca/setores/recortes"
S = []
S.append(f'''<section class="pg capa" style="background-image:url({b64(f"{REC}/{SET}_capa.jpg")})"><div class="veu"></div><div class="cartao">{f'<img class="logo" src="{LOGO}">' if LOGO else ''}
<div class="eyebrow">Inteligência regulatória · diretoria</div><h1>{NOME}: quem decide e como</h1><div class="onda"></div>
<p>Quadro atual da diretoria colegiada, comparação lado a lado de todos os diretores em exercício e superintendentes.</p>
<div class="meta">{HOJE.strftime("%d/%m/%Y")} · votos de {fmtd(desde)} a {fmtd(ult)} · {TOT_R} reuniões</div></div></section>''')
cards = ""
for d in board:
    b = bios.get(d, {}); fim, cargo = mandato(d)
    cards += f'''<div class="dc">{foto(d, b)}<div class="dc-b"><div class="dc-n">{E(d)}</div><div class="dc-c">{E((b.get("cargo") or cargo or "Diretor(a)")[:80])}</div>
<div class="dc-f"><b>Formação:</b> {E(b.get("formacao") or "não informada")}</div><p>{E((b.get("minibio") or "Minibio pendente.")[:230])}</p>
<div class="dc-m">Mandato até <b>{fmtd(fim)}</b> · {ST[d]["pres"]} de {TOT_R} reuniões</div></div></div>'''
S.append(f'''<section class="pg quad"><header class="top"><span class="num">01</span><span>Quadro atual da diretoria · {NOME}</span>{f"<img src='{LOGO_P}' class='logo-p'>" if LOGO_P else ""}</header>
<h2>Diretoria em atividade</h2><div class="qgrid">{cards}</div>
<div class="vac"><b>Vagas abertas:</b> {E("; ".join(f"{v['cadeira']} (desde {fmtd(v['inicio'])}; interinos: {v.get('interinos') or '—'})" for v in vac) or "nenhuma registrada")}</div>
<div class="rod">Em exercício = votaram nas 3 últimas reuniões. Minibios e formação com fontes em bios.json; mandatos em mandatos.json (checagem todo dia 1).</div></section>''')


def yt(r):
    p = [int(x) for x in re.findall(r"\d+", r["ts"] or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return f"https://www.youtube.com/watch?v={r['video_id']}&t={max(p[0]*3600+p[1]*60+p[2]-3,0)}s"


for k, q in enumerate(PERG):
    cols = ""
    data = {d: (stats(d, q.get("tema")) if q.get("tema") else ST[d]) for d in board}
    for d in board:
        s = data[d]; m = q["metrica"]
        if m == "relata": big, lab = s["rel"], f"relatorias de {s['n']} votos"; extra = "<br>".join(E(t.replace("_", " ")) + f" ({n})" for t, n in s["temas"]) or "—"
        elif m == "diverge": big, lab = s["dv"] + s["vista"], f"divergências ({s['dv']}) + vistas ({s['vista']})"; extra = f"acompanha o relator em {100*s['ac']/max(s['n']-s['rel'],1):.0f}% dos votos em que não relata"
        elif m == "desfecho": tot = sum(s["des"].values()) or 1; big, lab = f"{100*s['des']['desfavorável']/tot:.0f}%", f"desfavorável à empresa quando relata (n={sum(s['des'].values())})"; extra = " · ".join(f"{a} {b}" for a, b in s["des"].most_common(4)) or "—"
        else: big, lab = s["n"], f"votos no tema · {s['rel']} relatorias"; extra = f"divergiu {s['dv']} · vista {s['vista']} · acompanhou {s['ac']}"
        r = s["ev"]
        evh = f'<div class="ev"><b>RD {E(str(r["numero"]))} · {fmtd(r["data"])}</b> {E((r["assunto"] or "")[:70])} — <i>{E((r["voto"] or "")[:60])}</i> <a href="{yt(r)}">▶</a></div>' if r else '<div class="ev">Sem votos no recorte.</div>'
        cols += f'''<div class="cc">{foto(d, bios.get(d))}<div class="cc-n">{E(d)}</div><div class="big">{big}</div><div class="lab">{E(lab)}</div><div class="ex">{extra}</div>{evh}</div>'''
    S.append(f'''<section class="pg comp"><header class="top"><span class="num">{k+2:02d}</span><span>Comparador · {NOME}{" · tema " + E(q["tema"].replace("_"," ")) if q.get("tema") else ""}</span>{f"<img src='{LOGO_P}' class='logo-p'>" if LOGO_P else ""}</header>
<h2>{E(q["titulo"])}</h2><div class="cgrid" style="grid-template-columns:repeat({len(board)},1fr)">{cols}</div>
<div class="rod">Últimos 3 anos ({fmtd(desde)}–{fmtd(ult)}). Mesmos indicadores para todos os diretores em exercício; ▶ abre o vídeo no minuto. Legenda automática pode errar nomes e valores.</div></section>''')
sc = "".join(f'''<div class="sc">{foto(s["nome"], s)}<div><div class="dc-n">{E(s["nome"])}</div><div class="dc-c">{E(s.get("superintendencia") or s.get("cargo") or "")}</div>
<div class="dc-f"><b>Formação:</b> {E(s.get("formacao") or "não informada")}</div><p>{E((s.get("minibio") or "")[:180])}</p></div></div>''' for s in sups[:12]) or '<p class="vazio">Lote de superintendentes ainda não levantado para esta agência.</p>'
S.append(f'''<section class="pg quad"><header class="top"><span class="num">{len(PERG)+2:02d}</span><span>Superintendentes · {NOME}</span>{f"<img src='{LOGO_P}' class='logo-p'>" if LOGO_P else ""}</header>
<h2>Superintendentes</h2><div class="sgrid">{sc}</div><div class="rod">Fonte: páginas oficiais de composição (gov.br) e DOU; superintendentes não votam na diretoria — aparecem em eventos e na instrução dos processos.</div></section>''')
cob = E(subprocess.run(["python3", "pipeline/cobertura_resposta.py", AG], capture_output=True, text=True).stdout.strip()).replace("\n", "<br>")
S.append(f'''<section class="pg fim">{f'<img class="logo" src="{LOGO}">' if LOGO else ''}<h2>Como ler e cobertura</h2><div class="fimc">{cob}</div></section>''')
TOT = len(S)
S = [s.replace("</section>", f'<div class="pag">{i+1:02d} / {TOT:02d}</div></section>', 1) if i else s for i, s in enumerate(S)]
CSS = """@page{size:13.333in 7.5in;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,sans-serif;color:#0B0B0B;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:13.333in;height:7.5in;position:relative;overflow:hidden;page-break-after:always;padding:.38in .5in}h1,h2{font-family:Rubik,Inter,sans-serif;margin:0}
.capa{padding:0;background-size:cover;background-position:center;background-color:#151412}.veu{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,11,.65),rgba(11,11,11,.05) 75%)}
.cartao{position:absolute;left:.75in;top:1in;width:6in;padding:.5in .55in;border-radius:18px;background:rgba(17,17,15,.66);backdrop-filter:blur(10px);color:#fff;border:1px solid rgba(255,255,255,.14)}
.logo{height:.4in;margin-bottom:.3in}.eyebrow{font-size:11pt;letter-spacing:.12em;text-transform:uppercase;color:#E2B93B}.cartao h1{font-size:32pt;margin:.14in 0}.onda{height:6px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.35) 0 10px,transparent 10px 16px);margin:.2in 0}
.cartao p{font-size:12pt;line-height:1.5;color:#E8E5DE;margin:0}.meta{margin-top:.25in;font-size:9pt;color:#BDB8AE}
.top{display:flex;align-items:center;gap:.12in;font-size:9pt;color:#6E6A63;letter-spacing:.08em;text-transform:uppercase}.num{color:#C99A06;font-weight:700}.logo-p{height:.22in;margin-left:auto}
h2{font-size:21pt;margin:.12in 0 .16in}.qgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:.14in}.dc{display:flex;gap:.12in;background:#fff;border:1px solid #E3DFD6;border-top:4px solid #C99A06;border-radius:10px;padding:.12in}
.ft{width:.95in;height:.95in;flex:none;border-radius:50%;background-size:cover;background-position:center;background-color:#E7E3DA}.ft.ini{display:flex;align-items:center;justify-content:center;font-family:Rubik;font-size:22pt;color:#6E6A63}
.dc-n{font-family:Rubik;font-size:11.5pt;font-weight:600}.dc-c{font-size:7.8pt;color:#6E6A63;margin:.02in 0 .04in}.dc-f{font-size:8pt;margin-bottom:.03in}.dc p{font-size:8pt;line-height:1.35;margin:0 0 .04in}.dc-m{font-size:7.8pt;color:#3A3833}
.vac{margin-top:.14in;font-size:9pt;background:#F5F3EE;border-radius:8px;padding:8px 12px}.rod{position:absolute;left:.5in;right:1.3in;bottom:.16in;font-size:7.5pt;color:#6E6A63}.pag{position:absolute;right:.5in;bottom:.16in;font-size:8pt;font-weight:700;color:#C99A06}
.comp{background:#F5F3EE}.cgrid{display:grid;gap:.12in}.cc{background:#fff;border-radius:12px;border:1px solid #E3DFD6;padding:.16in .12in;display:flex;flex-direction:column;align-items:center;text-align:center;min-width:0}
.cc .ft{width:1.05in;height:1.05in}.cc-n{font-family:Rubik;font-size:11pt;font-weight:600;margin:.08in 0 .02in}.big{font-family:Rubik;font-size:34pt;font-weight:500;color:#0B0B0B;line-height:1.1}.lab{font-size:8pt;color:#6E6A63;min-height:.32in}
.ex{font-size:8.2pt;line-height:1.35;margin:.08in 0;color:#2B2925}.ev{font-size:7.6pt;line-height:1.35;color:#5E5A52;border-top:1px solid #E3DFD6;padding-top:.06in;margin-top:auto;text-align:left}.ev a{color:#C99A06;font-weight:700;text-decoration:none}
.sgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:.14in}.sc{display:flex;gap:.12in;background:#fff;border:1px solid #E3DFD6;border-radius:10px;padding:.1in}.sc .ft{width:.75in;height:.75in}.sc p{font-size:7.8pt;margin:.03in 0;line-height:1.3}.vazio{color:#6E6A63}
.fim{background:#0B0B0B;color:#fff;padding:.6in .8in}.fim h2{font-size:26pt;margin:.3in 0 .25in}.fimc{font-size:9.5pt;line-height:1.55;color:#CFCAC0}"""
H = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{NOME} diretoria</title><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Rubik:wght@500;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>{"".join(S)}</body></html>'
open(f"{OUT}/diretoria_{AG}.html", "w").write(leve_html(H))
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(OUT)}/diretoria_{AG}.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(OUT)}/diretoria_{AG}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"""
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
if r.returncode == 0: leve_pdf(f"{OUT}/diretoria_{AG}.pdf")
print(f"{OUT}/diretoria_{AG}.pdf" if r.returncode == 0 else r.stderr[-300:], TOT, "páginas")
