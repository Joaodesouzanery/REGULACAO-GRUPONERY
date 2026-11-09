"""Relatório «Circle» (v2): apresentação 16:9, uma ideia por página.
Uso: python3 pipeline/relatorio_v2.py <pasta> --titulo "..." [--subtitulo "..."] [--agencia antt] [--sem-marca]
Entrada (mesma da v1): <pasta>/perguntas.md («- pergunta [agencia: x] [diretor: Y] [tema: z] [setor: s]») e <pasta>/respostas/NN.md
(«**1. Resposta curta:** …» + o resto da ficha/consulta). Saída: <pasta>/relatorio_v2.html e .pdf.
Por pergunta: (1) resposta + 3 números grandes; (2) um gráfico; (3) três evidências em cartões com link no minuto.
Identidade: docs/marca/circle/ (logo branco/preto); fotos de setor em docs/marca/setores/<setor>.jpg (créditos em CREDITOS.md)."""
import sys, os, re, glob, html, json, base64, sqlite3, datetime, subprocess, collections
P = sys.argv[1].rstrip("/")
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
TIT = arg("--titulo", "Inteligência regulatória"); SUB = arg("--subtitulo", "Como a diretoria decide, com evidência de cada voto")
AG = arg("--agencia", "antt"); SEM = "--sem-marca" in sys.argv
E = html.escape
def b64(p):
    if not p or not os.path.exists(p): return None
    ext = p.rsplit(".", 1)[-1].lower().replace("jpg", "jpeg")
    return f"data:image/{ext};base64," + base64.b64encode(open(p, "rb").read()).decode()
LOGO_B = None if SEM else b64("docs/marca/circle/logo_circle_branco.png")
LOGO_P = None if SEM else b64("docs/marca/circle/logo_circle_preto.png")
def foto(setor):
    for e in ("jpg", "jpeg", "png", "webp"):
        if setor and os.path.exists(f"docs/marca/setores/{setor}.{e}"): return b64(f"docs/marca/setores/{setor}.{e}")
    return None
CRED = {}
if os.path.exists("docs/marca/setores/CREDITOS.md"):
    for l in open("docs/marca/setores/CREDITOS.md"):
        c_ = [x.strip() for x in l.split("|")]
        if len(c_) > 5 and "." in c_[1]: CRED[c_[1].split(".")[0]] = f"Foto: {c_[3]} ({c_[4]}), Wikimedia Commons"
_C = {}
def conn(ag):
    if ag not in _C:
        db = "data/regulacao.db" if ag == "antt" else f"data/{ag}/regulacao.db"
        _C[ag] = sqlite3.connect(db) if os.path.exists(db) else None
        if _C[ag]: _C[ag].row_factory = sqlite3.Row
    return _C[ag]
def seg(ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]
def yt(vid, t):
    if str(vid).startswith("ata_"):
        f = f"data/{'' if AG == 'antt' else AG + '/'}analise/{vid}.analise.json"
        return json.load(open(f))["meta"].get("url", "") if os.path.exists(f) else ""
    return f"https://www.youtube.com/watch?v={vid}&t={max(int(t or 0) - 3, 0)}s"
fmt = lambda n: f"{n:,}".replace(",", ".")
# ---------- dados por pergunta ----------
perg = []
for l in open(f"{P}/perguntas.md"):
    if l.startswith("- "):
        tags = dict(re.findall(r"\[(\w+):\s*([^\]]+)\]", l)); perg.append((re.sub(r"\[\w+:[^\]]+\]", "", l[2:]).strip(), tags))
resp = sorted(glob.glob(f"{P}/respostas/*.md"))
def curta(md):
    m = re.search(r"\*\*1\. Resposta curta:\*\*\s*(.+)", md); s = re.sub(r"\s*\[Completar[^\]]*\]", "", m.group(1)) if m else ""
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
def do_diretor(ag, d, tema):
    c = conn(ag)
    q = ("select v.*, i.item, i.assunto, i.resultado, i.unanime, i.ts its, r.numero, r.data, r.video_id from votos v join itens i on i.id=v.item_id "
         "join reunioes r on r.id=i.reuniao_id where v.diretor=?") + (" and v.item_id in (select item_id from item_temas where tema=?)" if tema else "")
    R = c.execute(q + " order by r.data", [d] + ([tema] if tema else [])).fetchall()
    if not R: return None
    cat = collections.Counter(r["categoria"] for r in R); rel = sum(r["eh_relator"] for r in R)
    ac = cat["acompanha"] + cat["revisor_acompanha"]; fora = cat["vista"] + cat["vencido"] + cat["revisor_diverge"]
    kpis = [(fmt(len(R)), "votos analisados"), (fmt(rel), "relatorias"), (f"{round(100*ac/max(len(R)-rel,1))}%", "acompanha o relator")]
    barras = [("Relator", rel), ("Acompanha", ac), ("Vista", cat["vista"]), ("Voto-vista divergente", cat["revisor_diverge"]), ("Vencido", cat["vencido"])]
    ev = [r for r in R if r["eh_relator"] and r["justificativa"]] or [r for r in R if r["justificativa"]] or list(R)
    fora_l = [r for r in R if r["categoria"] in ("vista", "vencido", "revisor_diverge")]
    pick = ev[len(ev) // 2: len(ev) // 2 + 1] + ev[-1:] + (fora_l[-1:] if fora_l else ev[:1])
    cards = [{"rd": f"Reunião {r['numero']}", "data": r["data"], "item": r["item"], "assunto": r["assunto"], "voto": r["voto"], "just": r["justificativa"] or "",
              "trecho": r["trecho"] or "", "link": yt(r["video_id"], r["trecho_t"] or seg(r["ts"] or r["its"])), "tag": "fora do padrão" if r in fora_l else "padrão"} for r in pick]
    return {"kpis": kpis, "barras": barras, "titulo_graf": f"Como vota ({R[0]['data'][:7]} a {R[-1]['data'][:7]})", "cards": cards, "fonte": f"n = {len(R)} votos" + (f" no tema {tema}" if tema else "")}
def do_md(md):
    """Pergunta sem diretor: números do texto, gráfico da 1ª tabela, evidências das linhas «- **RD …**»."""
    linhas = md.splitlines(); tab = [l for l in linhas if l.strip().startswith("|")]
    barras, kpis = [], []
    if len(tab) > 2:
        cab = [x.strip() for x in tab[0].strip("|").split("|")]
        rows = [[x.strip() for x in l.strip("|").split("|")] for l in tab[2:] if not re.match(r"^\|?\s*-", l)]
        col = next((i for i, h in enumerate(cab) if h.lower().startswith("relator")), 1)
        barras = [(r[0], int(re.sub(r"\D", "", r[col]) or 0)) for r in rows[:8] if len(r) > col]
        tv = sum(int(re.sub(r"\D", "", r[1]) or 0) for r in rows if len(r) > 1)
        dvi = next((i for i, h in enumerate(cab) if "diverg" in h.lower()), None)
        kpis = [(fmt(tv), "votos no recorte"), (str(len(rows)), "diretores"), (str(sum(int(re.sub(r'\D', '', r[dvi]) or 0) for r in rows if dvi and len(r) > dvi)) if dvi else "—", "divergências / vencidos")]
        tg = f"{cab[col]} por diretor"
    else:
        m = re.search(r"(\d+) itens", md); f = re.search(r"favorável (\d+)", md); d = re.search(r"desfavorável (\d+)", md)
        kpis = [(m.group(1) if m else "—", "itens deliberados"), (f.group(1) if f else "—", "desfecho favorável*"), (d.group(1) if d else "—", "desfecho desfavorável*")]
        rl = re.search(r"\*\*Relatores?[^*]*:\*\*\s*(.+)", md)
        barras = [(re.sub(r"\s*\d+$", "", x.strip()), int(re.search(r"(\d+)\s*$", x.strip()).group(1))) for x in (rl.group(1).split(";") if rl else []) if re.search(r"\d+\s*$", x.strip())]
        ef = re.search(r"\*\*Efeito com sustentação:\*\*\s*(.+)", md)
        if ef: barras = [(re.sub(r"\s*\d+ \(.*", "", x.strip()), int(re.search(r"\((\d+)%\)", x).group(1))) for x in ef.group(1).split(",") if "%" in x]
        tg = "Efeito (% dos itens)" if ef else "Quem relata"
    cards = []
    for l in linhas:
        m = re.match(r"\s*- \*\*RD ([^*]+?) \(([\d-]+)\)\*\*,? item ([^·]+?) · (.+)", l)
        if m:
            lk = re.search(r"\((https?://[^)]+)\)", l); resto = re.sub(r"\[[^\]]+\]\([^)]+\)", "", m.group(4))
            partes = [x.strip() for x in resto.split("·") if x.strip()]
            ass, _, res = (partes[0] if partes else "").partition("→")
            votos = next((x for x in partes[1:] if x.startswith("votos:") or x.startswith("relator")), "")
            cards.append({"rd": f"Reunião {m.group(1)}", "data": m.group(2), "item": m.group(3).strip(), "assunto": ass.strip(), "voto": res.strip() or votos, "rotulo": "Resultado" if res.strip() else "Votos", "just": "", "trecho": "", "link": lk.group(1) if lk else "", "tag": "precedente"})
    return {"kpis": kpis, "barras": [b for b in barras if b[1] > 0][:8], "titulo_graf": tg, "cards": cards[:3], "fonte": "classificação automática; ver anexo"}
Q = []
for i, (q, t) in enumerate(perg):
    md = open(resp[i]).read() if i < len(resp) else ""
    ag = t.get("agencia", AG).strip().lower()
    d = do_diretor(ag, t["diretor"].strip(), t.get("tema", "").strip() or None) if t.get("diretor") and conn(ag) else None
    Q.append({"q": q, "t": t, "ag": ag, "curta": curta(md), "dados": d or do_md(md), "setor": t.get("setor") or {"antt": "rodovias", "anm": "mineracao", "antaq": "portos"}.get(ag, "rodovias")})
# ---------- HTML ----------
SET_NOME = {"onibus": "Ônibus", "rodovias": "Rodovias", "ferrovias": "Ferrovias", "mineracao": "Mineração", "portos": "Portos", "barragens": "Barragens", "navegacao": "Navegação"}
def setor_de(x):
    t = x["t"]; s = (t.get("tema", "") + " " + x["q"]).lower()
    for k, rx in (("onibus", "ônibus|onibus|cassa"), ("ferrovias", "ferrov|rumo"), ("barragens", "barrage"), ("rodovias", "concess|rodov|free flow|reequil|concer"), ("mineracao", "mine|cfem|outorga|vale|garimp|área")):
        if re.search(rx, s) and foto(k): return k
    return x["setor"] if foto(x["setor"]) else next((k for k in SET_NOME if foto(k)), None)
def img(s): f = foto(s); return f"background-image:url({f})" if f else ""
def barras_svg(B):
    if not B: return '<p class="vazio">Sem dados para o gráfico neste recorte.</p>'
    W, rh = 760, 46; mx = max(v for _, v in B) or 1; lab = 230
    g = "".join(f'<g transform="translate(0,{i*rh})"><text x="{lab-14}" y="27" text-anchor="end" class="bl">{E(k[:28])}</text>'
                f'<rect x="{lab}" y="10" width="{max(3,int((W-lab-90)*v/mx))}" height="24" rx="3" class="{"bar hi" if i==0 else "bar"}"/>'
                f'<text x="{lab+max(3,int((W-lab-90)*v/mx))+10}" y="28" class="bv">{fmt(v)}</text></g>' for i, (k, v) in enumerate(B))
    return f'<svg viewBox="0 0 {W} {len(B)*rh+10}" class="graf" role="img">{g}</svg>'
def frase(s, n=420):
    s = re.sub(r"\s+", " ", s or "").strip()
    if len(s) <= n: return s
    corte = s[:n]; p = max(corte.rfind(". "), corte.rfind("; "))
    return (corte[:p + 1] if p > 160 else corte.rsplit(" ", 1)[0] + "…")
hoje = datetime.date.today().strftime("%d/%m/%Y")
ags = " · ".join(dict.fromkeys(x["ag"].upper() for x in Q))
S = []
capa_set = setor_de(Q[0]) if Q else "rodovias"
S.append(f'''<section class="pg capa" style="{img(capa_set)}"><div class="veu"></div>
<div class="cartao">{f'<img class="logo" src="{LOGO_B}" alt="Circle">' if LOGO_B else ''}<div class="eyebrow">Inteligência regulatória · {E(ags)}</div>
<h1>{E(TIT)}</h1><div class="onda"></div><p>{E(SUB)}</p><div class="meta">{hoje} · {len(Q)} perguntas</div></div>
<div class="cred">{E(CRED.get(capa_set, ""))}</div></section>''')
# sumário em cartões (5 por página)
for k in range(0, len(Q), 5):
    cards = "".join(f'''<div class="sc" style="{img(setor_de(x))}"><div class="sc-veu"></div><div class="sc-tag">• {E(SET_NOME.get(setor_de(x) or "", x["ag"].upper()))}</div>
<div class="sc-n">{k+j+1:02d}</div><div class="sc-t">{E(x["q"])}</div></div>''' for j, x in enumerate(Q[k:k+5]))
    menu = "".join(f'<li class="{"on" if k <= i < k+5 else ""}"><span>{i+1:02d}</span>{E(x["q"][:52])}{"…" if len(x["q"]) > 52 else ""}</li>' for i, x in enumerate(Q))
    S.append(f'''<section class="pg sum"><div class="sum-esq">{f'<img class="logo-s" src="{LOGO_B}" alt="">' if LOGO_B else ''}<h2>O que<br>respondemos</h2><ul>{menu}</ul></div><div class="sum-cards">{cards}</div></section>''')
for i, x in enumerate(Q):
    d = x["dados"]; n = f"{i+1:02d}"; st = setor_de(x)
    topo = f'<header class="top"><span class="num">{n}</span><span class="ag">{E(x["ag"].upper())}</span>{f"<img src={LOGO_P} class=logo-p alt=>" if LOGO_P else ""}</header>'
    kp = "".join(f'<div class="kpi"><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in d["kpis"])
    S.append(f'''<section class="pg resp"><div class="resp-foto" style="{img(st)}"><div class="resp-veu"></div><div class="resp-n">{n}</div></div>
<div class="resp-txt">{topo}<h2>{E(x["q"])}</h2><p class="lead">{E(frase(x["curta"]))}</p><div class="kpis">{kp}</div></div></section>''')
    S.append(f'''<section class="pg graf-pg">{topo}<div class="graf-head"><span class="eyebrow-d">{n} · em números</span><h3>{E(d["titulo_graf"])}</h3></div>
{barras_svg(d["barras"])}<div class="rod">Fonte: reuniões públicas de diretoria ({E(x["ag"].upper())}), vídeos oficiais no YouTube · {E(d["fonte"])}</div></section>''')
    cs = "".join(f'''<article class="ev"><div class="ev-top"><span class="pill {"warn" if c["tag"]=="fora do padrão" else ""}">{E(c["tag"])}</span><span>{E(c["data"] or "")}</span></div>
<h4>{E(c["rd"])} · item {E(str(c["item"]))}</h4><p class="ev-a">{E(frase(c["assunto"], 150))}</p>
{f'<p class="ev-v"><b>{c.get("rotulo", "Voto")}:</b> {E(frase(c["voto"], 110))}</p>' if c["voto"] else ""}{f'<p class="ev-j">«{E(frase(c["just"], 150))}»</p>' if c["just"] else ""}
{f'<p class="ev-t">Trecho: “{E(frase(c["trecho"], 170))}”</p>' if c["trecho"] else ""}
{f'<a class="btn" href="{E(c["link"])}">▶ assistir no minuto</a>' if c["link"].startswith("https://www.youtube") else (f'<a class="btn" href="{E(c["link"])}">ata oficial</a>' if c["link"] else "")}</article>''' for c in d["cards"][:3])
    S.append(f'''<section class="pg evs">{topo}<div class="graf-head"><span class="eyebrow-d">{n} · evidências</span><h3>Os votos que sustentam a resposta</h3></div><div class="ev-grid">{cs or '<p class="vazio">Sem evidências individuais neste recorte.</p>'}</div>
<div class="rod">Trechos da legenda automática do YouTube; podem conter erros de transcrição.</div></section>''')
S.append(f'''<section class="pg fim">{f'<img class="logo" src="{LOGO_B}" alt="">' if LOGO_B else ''}<h2>Como ler este relatório</h2><div class="fim-grid">
<div><b>Fonte</b><p>Vídeos oficiais das reuniões públicas de diretoria e dos eventos da agência, transcritos e estruturados item a item.</p></div>
<div><b>Confiança</b><p>Releitura cega por amostra: ≈ 94–96% de concordância no voto de cada diretor (ANTT 2019–2026; ANM 2021–2026). ANM conferida com as atas oficiais.</p></div>
<div><b>Limites</b><p>Legenda automática erra nomes e números; quem só acompanha o relator raramente fala; voto escrito completo e itens sigilosos não estão nos vídeos.</p></div></div></section>''')
CSS = """@page{size:13.333in 7.5in;margin:0}
:root{--ink:#0B0B0B;--paper:#FFFFFF;--gold:#C99A06;--gold-2:#E2B93B;--mist:#F3F1EC;--grey:#6E6A63;--line:#E3DFD6;--night:#151412}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:'Inter',system-ui,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:13.333in;height:7.5in;position:relative;overflow:hidden;page-break-after:always;break-after:page}
h1,h2,h3,h4{font-family:'Rubik','Inter',sans-serif;margin:0;letter-spacing:-.01em;text-wrap:balance}
.capa{background:var(--night) center/cover no-repeat}.veu{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,11,.55),rgba(11,11,11,.05) 70%)}
.cartao{position:absolute;left:.75in;top:1.05in;width:5.6in;padding:.5in .55in;border-radius:18px;background:rgba(17,17,15,.62);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.14);color:#fff}
.cartao .logo{height:.42in;margin-bottom:.32in}.eyebrow{font-size:11pt;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-2)}
.cartao h1{font-size:34pt;line-height:1.08;margin:.16in 0 .2in;font-weight:600}.onda{height:6px;width:100%;background:repeating-linear-gradient(90deg,rgba(255,255,255,.35) 0 10px,transparent 10px 16px);border-radius:3px;margin-bottom:.22in}
.cartao p{font-size:13pt;line-height:1.5;color:#E8E5DE;margin:0}.meta{margin-top:.3in;font-size:10pt;color:#BDB8AE}.cred{position:absolute;right:.3in;bottom:.18in;font-size:7pt;color:rgba(255,255,255,.7)}
.sum{background:var(--ink);color:#fff;display:flex;gap:.35in;padding:.55in .45in .55in .6in}
.sum-esq{width:3.3in;flex:none}.logo-s{height:.3in;margin-bottom:.45in}.sum-esq h2{font-size:30pt;font-weight:500;line-height:1.08;margin-bottom:.35in}
.sum-esq ul{list-style:none;padding:0;margin:0;font-size:9.5pt;line-height:1.45;color:#8E8A82}.sum-esq li{display:flex;gap:.12in;padding:2px 0}.sum-esq li span{color:#5A574F;width:.28in}.sum-esq li.on{color:#fff}.sum-esq li.on span{color:var(--gold)}
.sum-cards{flex:1;display:flex;gap:2px;border-radius:6px;overflow:hidden}
.sc{flex:1;position:relative;background:#2A2824 center/cover no-repeat;color:#fff;min-width:0}.sc-veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.05) 35%,rgba(0,0,0,.72))}
.sc-tag{position:absolute;top:.2in;left:.18in;font-size:9pt;font-weight:600;letter-spacing:.02em}.sc-n{position:absolute;top:.5in;left:.18in;font-family:Rubik;font-size:30pt;color:var(--gold-2);font-weight:500}
.sc-t{position:absolute;left:.18in;right:.18in;bottom:.28in;font-family:Rubik;font-size:13pt;line-height:1.25;font-weight:500}
.resp{display:flex}.resp-foto{width:4.6in;flex:none;position:relative;background:#2A2824 center/cover no-repeat}.resp-veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,11,.1),rgba(11,11,11,.55))}
.resp-n{position:absolute;left:.45in;bottom:.4in;font-family:Rubik;font-size:96pt;line-height:1;color:#fff;font-weight:500}
.resp-txt{flex:1;padding:.5in .65in .5in .6in;display:flex;flex-direction:column}
.top{display:flex;align-items:center;gap:.14in;font-size:9.5pt;color:var(--grey);letter-spacing:.08em;text-transform:uppercase}.top .num{color:var(--gold);font-weight:700}.logo-p{height:.24in;margin-left:auto}
.resp h2{font-size:24pt;line-height:1.15;font-weight:600;margin:.28in 0 .22in;max-width:7.2in}.lead{font-size:14.5pt;line-height:1.55;color:#2B2925;margin:0;max-width:7.4in}
.kpis{display:flex;gap:.25in;margin-top:auto}.kpi{flex:1;border-top:3px solid var(--gold);padding-top:.14in}.kpi b{display:block;font-family:Rubik;font-size:34pt;font-weight:500;line-height:1}.kpi span{display:block;font-size:10pt;color:var(--grey);margin-top:.08in}
.graf-pg,.evs{padding:.5in .65in;background:var(--mist)}.graf-head{margin:.25in 0 .25in}.eyebrow-d{font-size:10pt;letter-spacing:.1em;text-transform:uppercase;color:var(--gold)}.graf-head h3{font-size:24pt;font-weight:600;margin-top:.06in}
.graf{width:100%;max-height:4.6in}.bl{font-size:15px;fill:#3A3833;font-family:Inter}.bv{font-size:15px;fill:var(--ink);font-weight:700;font-family:Inter}.bar{fill:#BDB6A6}.bar.hi{fill:var(--gold)}
.rod{position:absolute;left:.65in;right:.65in;bottom:.28in;font-size:8.5pt;color:var(--grey)}
.ev-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.22in}.ev{background:#fff;border-radius:12px;padding:.26in .26in .3in;display:flex;flex-direction:column;gap:.08in;border:1px solid var(--line);min-width:0}
.ev-top{display:flex;justify-content:space-between;font-size:9pt;color:var(--grey)}.pill{background:var(--mist);border-radius:99px;padding:1px 9px;font-weight:600;color:#3A3833}.pill.warn{background:#FFF3D2;color:#8A6400}
.ev h4{font-size:13pt;font-weight:600}.ev p{margin:0;font-size:10pt;line-height:1.45}.ev-a{color:#2B2925}.ev-v{color:#3A3833}.ev-j{color:#5E5A52;font-style:italic}.ev-t{color:#5E5A52;font-size:9pt!important;border-left:3px solid var(--gold);padding-left:.1in}
.btn{margin-top:auto;align-self:flex-start;background:var(--ink);color:#fff;text-decoration:none;font-size:9.5pt;font-weight:600;padding:7px 14px;border-radius:99px}
.vazio{color:var(--grey);font-size:12pt}
.fim{background:var(--ink);color:#fff;padding:.7in .8in}.fim .logo{height:.36in}.fim h2{font-size:28pt;font-weight:500;margin:.45in 0 .45in}.fim-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.4in}
.fim-grid b{display:block;color:var(--gold-2);font-family:Rubik;font-size:14pt;margin-bottom:.1in;font-weight:500}.fim-grid p{margin:0;font-size:11pt;line-height:1.55;color:#CFCAC0}"""
H = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(TIT)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Rubik:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{"".join(S)}</body></html>'''
open(f"{P}/relatorio_v2.html", "w").write(H)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(P)}/relatorio_v2.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(P)}/relatorio_v2.pdf',width:'13.333in',height:'7.5in',printBackground:true,margin:{{top:'0',bottom:'0',left:'0',right:'0'}}}});await b.close();}})();"""
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
print(f"{P}/relatorio_v2.pdf" if r.returncode == 0 else "PDF não gerado: " + r.stderr[-300:], len(Q), "perguntas,", len(S), "páginas")
