"""Relatório «Circle» (v2): apresentação 16:9, uma ideia por página.
Uso: python3 pipeline/relatorio_v2.py <pasta> --titulo "..." [--subtitulo "..."] [--agencia antt] [--sem-marca] [--anexo]
v3: capa + sumário (1 pág.) + 1 página por pergunta + «como ler» ≈ 13 páginas; fotos fixas por setor (pipeline/preparar_fotos.py).
Entrada (mesma da v1): <pasta>/perguntas.md («- pergunta [agencia: x] [diretor: Y] [tema: z] [setor: s]») e <pasta>/respostas/NN.md
(«**1. Resposta curta:** …» + o resto da ficha/consulta). Saída: <pasta>/relatorio_v2.html e .pdf.
Por pergunta: (1) resposta + 3 números grandes; (2) um gráfico; (3) três evidências em cartões com link no minuto.
Identidade: docs/marca/circle/ (logo branco/preto); fotos de setor em docs/marca/setores/<setor>.jpg (créditos em CREDITOS.md)."""
import sys, os, re, glob, html, json, base64, sqlite3, datetime, subprocess, collections
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pdf_leve import leve_html, leve_pdf
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
REC = "docs/marca/setores/recortes"  # gerados por pipeline/preparar_fotos.py (recorte e duotom fixos por setor)
FOCO = json.load(open("docs/marca/setores/foco.json")) if os.path.exists("docs/marca/setores/foco.json") else {}
def foto(setor): return bool(setor) and os.path.exists(f"{REC}/{setor}_capa.jpg") and os.path.exists(f"{REC}/{setor}_painel.jpg")
CRED = {}
if os.path.exists("docs/marca/setores/CREDITOS.md"):
    for l in open("docs/marca/setores/CREDITOS.md"):
        c_ = [x.strip() for x in l.split("|")]
        if len(c_) > 5 and "." in c_[1]: CRED[c_[1].split(".")[0]] = f"Foto: {c_[3]} ({c_[4]})"
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
              "trecho": r["trecho"] or "", "ttipo": r["trecho_tipo"] or "", "link": yt(r["video_id"], r["trecho_t"] or seg(r["ts"] or r["its"])), "tag": "fora do padrão" if r in fora_l else "padrão"} for r in pick]
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
        m = re.search(r"(\d+) itens", md); f = re.search(r"(?<!des)favorável (\d+)", md); d = re.search(r"desfavorável (\d+)", md)
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
            pa = next((x for x in partes if "→" in x), next((x for x in partes if not x.startswith(("relator", "votos:"))), ""))
            ass, _, res = pa.partition("→")
            rel = next((x for x in partes if x.startswith("relator")), "")
            votos = next((x for x in partes if x.startswith("votos:")), "") or rel
            if rel and res: res = f"{res.strip()} ({rel})"
            nr = re.sub(r"\s*Reuni[ãa]o\s*", " ", m.group(1)).strip()
            cards.append({"rd": f"Reunião {nr}", "data": m.group(2), "item": m.group(3).strip(), "assunto": ass.strip(), "voto": res.strip() or votos, "rotulo": "Resultado" if res.strip() else "Votos", "just": "", "trecho": "", "link": lk.group(1) if lk else "", "tag": "precedente"})
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
def img(s): return ""  # (v3) imagens via classes CSS .fc-<setor>/.fp-<setor>, embutidas uma única vez
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
# ---------- HTML (v3: ~13 páginas para 10 perguntas; cada imagem embutida uma única vez) ----------
ANEXO = "--anexo" in sys.argv
hoje = datetime.date.today().strftime("%d/%m/%Y")
ags = " · ".join(dict.fromkeys(x["ag"].upper() for x in Q))
for x in Q: x["st"] = setor_de(x) or "rodovias"
usados = sorted({x["st"] for x in Q} | {{"antt": "rodovias", "anm": "mineracao", "antaq": "portos"}.get((Q[0]["ag"] if Q else AG), "rodovias")})
IMG_CSS = "".join(f'.fc-{s}{{background-image:url({b64(f"{REC}/{s}_capa.jpg")})}}.fp-{s}{{background-image:url({b64(f"{REC}/{s}_painel.jpg")})}}.fk-{s}{{background-image:url({b64(f"{REC}/{s}_cartao.jpg") or b64(f"{REC}/{s}_capa.jpg")})}}' for s in usados if foto(s))
COR_CSS = "".join(f'.s-{s}{{--ac:{v.get("cor", "#C99A06")}}}' for s, v in FOCO.items())
S = []
capa = {"antt": "rodovias", "anm": "mineracao", "antaq": "portos"}.get((Q[0]["ag"] if Q else AG), "rodovias")
if not foto(capa): capa = Q[0]["st"] if Q else "rodovias"
S.append(f'''<section class="pg capa fc-{capa}"><div class="veu"></div>
<div class="cartao">{f'<img class="logo" src="{LOGO_B}" alt="Circle">' if LOGO_B else ''}<div class="eyebrow">Inteligência regulatória · {E(ags)}</div>
<h1>{E(TIT)}</h1><div class="onda"></div><p>{E(SUB)}</p><div class="meta">{hoje} · {len(Q)} perguntas</div></div>
<div class="cred">{E(CRED.get(capa, ""))}</div></section>''')
# sumário: uma página, grade de cartões (foto 16:9 sem corte + número + pergunta)
cards = "".join(f'''<div class="sc s-{x["st"]} fk-{x["st"]}"><div class="sc-veu"></div><div class="sc-tag">• {E(SET_NOME.get(x["st"], ""))}<span>{E(x["ag"].upper())}</span></div>
<div class="sc-n">{i+1:02d}</div><div class="sc-t">{E(frase(x["q"], 110))}</div></div>''' for i, x in enumerate(Q[:10]))
S.append(f'''<section class="pg sum"><div class="sum-top"><h2>O que respondemos</h2>{f'<img class="logo-s" src="{LOGO_B}" alt="">' if LOGO_B else ''}</div><div class="sum-grid">{cards}</div></section>''')
def card(c):
    lk = c["link"]
    bt = f'<a class="btn" href="{E(lk)}">▶ assistir no minuto</a>' if lk.startswith("https://www.youtube") else (f'<a class="btn" href="{E(lk)}">ata oficial</a>' if lk else "")
    corpo = (f'<p class="ev-j"><b>Por quê:</b> {E(frase(c["just"], 200))}</p>' if c["just"] else "") + (f'<p class="ev-t">“{E(frase(c["trecho"], 260))}”</p>' if c["trecho"] and (c.get("ttipo") == "fala_no_minuto" or not c["just"]) else "")
    return f'''<article class="ev"><div class="ev-top"><span class="pill {"warn" if c["tag"]=="fora do padrão" else ""}">{E(c["tag"])}</span><span>{E(c["data"] or "")}</span></div>
<h4>{E(c["rd"])} · item {E(str(c["item"]))}</h4><p class="ev-a">{E(frase(c["assunto"], 150 if (c["trecho"] or c["just"]) else 320))}</p>
{f'<p class="ev-v"><b>{c.get("rotulo", "Voto")}:</b> {E(frase(c["voto"], 90))}</p>' if c["voto"] else ""}{corpo}{bt}</article>'''
def mini(B):
    B = sorted([b for b in B if b[1] > 0], key=lambda b: -b[1]) if not any(k in ("Relator", "Acompanha") for k, _ in B) else [b for b in B if b[1] > 0]
    B = B[:5]
    if not B: return '<p class="vazio">Sem dados para o gráfico neste recorte.</p>'
    mx = max(v for _, v in B)
    return "".join(f'<div class="mb"><span class="mb-l">{E(k[:26])}</span><span class="mb-t"><i style="width:{max(2, round(100*v/mx))}%" class="{"hi" if j==0 else ""}"></i></span><b>{fmt(v)}</b></div>' for j, (k, v) in enumerate(B))
for i, x in enumerate(Q):
    d = x["dados"]; n = f"{i+1:02d}"; st = x["st"]
    kp = "".join(f'<div class="kpi"><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in d["kpis"])
    cs = d["cards"]; esc = (cs[:1] + [c for c in cs[1:] if c["tag"] == "fora do padrão"][:1]) or cs[:2]
    if len(esc) < 2: esc += [c for c in cs if c not in esc][:2 - len(esc)]
    S.append(f'''<section class="pg q s-{st}"><div class="q-f fp-{st}"><div class="q-veu"></div><div class="q-tag">{E(SET_NOME.get(st, ""))}</div><div class="q-n">{n}</div></div>
<div class="q-c"><header class="top"><span class="num">{n}</span><span>{E(x["ag"].upper())}</span><span class="dot">•</span><span>{E(d["fonte"])}</span>{f"<img src={LOGO_P} class=logo-p alt=>" if LOGO_P else ""}</header>
<h2>{E(x["q"])}</h2><p class="lead">{E(frase(x["curta"], 400))}</p>
<div class="meio"><div class="kpis">{kp}</div><div class="mini"><div class="mini-h">{E(d["titulo_graf"])}</div>{mini(d["barras"])}</div></div>
<div class="evs{"" if any(c["trecho"] or c["just"] for c in esc) else " curto"}">{"".join(card(c) for c in (esc if any(c["trecho"] or c["just"] for c in esc) else cs[:3])) or '<p class="vazio">Sem evidências individuais neste recorte.</p>'}</div>
<div class="pag">{{PAGN}}</div><div class="rod">Fonte: reuniões públicas de diretoria ({E(x["ag"].upper())}), vídeos oficiais · trechos da legenda automática do YouTube (podem conter erros) · evidência completa no anexo e na base.</div></div></section>''')
if ANEXO:
    linhas = [(f'{k+1:02d}', c) for k, x in enumerate(Q) for c in x["dados"]["cards"][:3]]
    for a in range(0, len(linhas), 12):
        tr = "".join(f'<tr><td>{q}</td><td>{E(c["rd"])}<br><span>{E(c["data"] or "")} · item {E(str(c["item"]))}</span></td><td>{E(frase(c["assunto"], 120))}</td><td>{E(frase(c["voto"], 80))}</td><td>{f"<a href={E(c[chr(108)+chr(105)+chr(110)+chr(107)])}>abrir</a>" if c["link"] else ""}</td></tr>' for q, c in linhas[a:a+12])
        S.append(f'<section class="pg anexo"><h3>Anexo · evidências por pergunta</h3><table><thead><tr><th>#</th><th>Reunião</th><th>Assunto</th><th>Voto / resultado</th><th>Vídeo</th></tr></thead><tbody>{tr}</tbody></table></section>')
S.append(f'''<section class="pg fim">{f'<img class="logo" src="{LOGO_B}" alt="">' if LOGO_B else ''}<h2>Como ler este relatório</h2><div class="fim-grid">
<div><b>Fonte</b><p>Vídeos oficiais das reuniões públicas de diretoria e dos eventos da agência, transcritos e estruturados item a item. Cada evidência abre o vídeo no minuto citado.</p></div>
<div><b>Confiança</b><p>Releitura cega por amostra: ≈ 94–96% de concordância no voto de cada diretor (ANTT 2019–2026; ANM 2021–2026). ANM conferida com as atas oficiais (resultado 97,9%). Mede consistência, não verdade absoluta.</p></div>
<div><b>Limites</b><p>Legenda automática erra nomes e números; quem só acompanha o relator raramente fala; voto escrito completo e itens sigilosos não estão nos vídeos. Tom e perfil são inferência.</p></div></div>
<div class="cred2">{E(" · ".join(dict.fromkeys(CRED[s] for s in usados if s in CRED)))}</div></section>''')
CSS = """@page{size:13.333in 7.5in;margin:0}
:root{--ink:#0B0B0B;--paper:#FFFFFF;--gold:#C99A06;--gold-2:#E2B93B;--mist:#F5F3EE;--grey:#6E6A63;--line:#E3DFD6;--night:#151412;--ac:#C99A06}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:'Inter',system-ui,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:13.333in;height:7.5in;position:relative;overflow:hidden;page-break-after:always;break-after:page}
h1,h2,h3,h4{font-family:'Rubik','Inter',sans-serif;margin:0;letter-spacing:-.01em;text-wrap:balance}
[class^=fc-],[class*=" fc-"],[class^=fp-],[class*=" fp-"]{background-size:cover;background-position:center;background-repeat:no-repeat}
.capa{background-color:var(--night)}.veu{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,11,.6),rgba(11,11,11,.05) 70%)}
.cartao{position:absolute;left:.75in;top:1.05in;width:5.6in;padding:.5in .55in;border-radius:18px;background:rgba(17,17,15,.62);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.14);color:#fff}
.cartao .logo{height:.42in;margin-bottom:.32in}.eyebrow{font-size:11pt;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-2)}
.cartao h1{font-size:34pt;line-height:1.08;margin:.16in 0 .2in;font-weight:600}.onda{height:6px;width:100%;background:repeating-linear-gradient(90deg,rgba(255,255,255,.35) 0 10px,transparent 10px 16px);border-radius:3px;margin-bottom:.22in}
.cartao p{font-size:13pt;line-height:1.5;color:#E8E5DE;margin:0}.meta{margin-top:.3in;font-size:10pt;color:#BDB8AE}.cred{position:absolute;right:.3in;bottom:.18in;font-size:7pt;color:rgba(255,255,255,.7)}
.sum{background:var(--ink);color:#fff;padding:.45in .55in}.sum-top{display:flex;align-items:center;margin-bottom:.3in}.sum-top h2{font-size:26pt;font-weight:500}.logo-s{height:.3in;margin-left:auto}
.sum-grid{display:grid;grid-template-columns:repeat(5,1fr);grid-template-rows:repeat(2,1fr);gap:.16in;height:5.95in}
.sc{position:relative;border-radius:12px;overflow:hidden;color:#fff;background-color:#2A2824;box-shadow:inset 0 0 0 1px rgba(255,255,255,.06)}
.sc-veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,0) 32%,rgba(0,0,0,.25) 50%,rgba(0,0,0,.85))}
.sc-tag{position:absolute;top:.14in;left:.16in;right:.16in;font-size:8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;display:flex;justify-content:space-between}.sc-tag span{opacity:.75;font-weight:600}
.sc-n{position:absolute;left:.16in;bottom:1.02in;font-family:Rubik;font-size:22pt;font-weight:500;color:var(--gold-2)}
.sc-t{position:absolute;left:.16in;right:.16in;bottom:.16in;font-family:Rubik;font-size:10.5pt;line-height:1.25;font-weight:500;border-top:2px solid var(--ac);padding-top:.08in}
.q{display:flex}.q-f{width:2.9in;flex:none;position:relative;background-color:#2A2824}.q-veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,11,.25),rgba(11,11,11,0) 30%,rgba(11,11,11,.7))}
.q-tag{position:absolute;top:.35in;left:.32in;font-size:9pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#fff;border-left:3px solid var(--ac);padding-left:.1in}
.q-n{position:absolute;left:.3in;bottom:.3in;font-family:Rubik;font-size:72pt;line-height:1;color:#fff;font-weight:500}
.q-c{flex:1;padding:.36in .5in .5in .5in;display:flex;flex-direction:column;min-width:0}
.top{display:flex;align-items:center;gap:.1in;font-size:8.5pt;color:var(--grey);letter-spacing:.08em;text-transform:uppercase}.top .num{color:var(--ac);font-weight:700}.top .dot{color:var(--ac)}.logo-p{height:.22in;margin-left:auto}
.q h2{font-size:19pt;line-height:1.18;font-weight:600;margin:.16in 0 .1in}.lead{font-size:11.5pt;line-height:1.5;color:#2B2925;margin:0}
.meio{display:flex;gap:.35in;margin:.2in 0 .18in;align-items:stretch}.kpis{display:flex;gap:.2in;flex:1.1}.kpi{flex:1;border-top:3px solid var(--ac);padding-top:.1in}.kpi b{display:block;font-family:Rubik;font-size:30pt;font-weight:500;line-height:1}.kpi span{display:block;font-size:8.5pt;color:var(--grey);margin-top:.06in;line-height:1.3}
.mini{flex:1;background:var(--mist);border-radius:10px;padding:.12in .16in}.mini-h{font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:var(--grey);margin-bottom:.05in}
.mb{display:flex;align-items:center;gap:.08in;font-size:8.5pt;margin:2px 0}.mb-l{width:1.5in;color:#3A3833;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.mb-t{flex:1;height:9px;background:#E7E3DA;border-radius:5px;overflow:hidden}.mb-t i{display:block;height:100%;background:#B9B2A3;border-radius:5px}.mb-t i.hi{background:var(--ac)}.mb b{width:.45in;text-align:right;font-size:8.5pt}
.evs{display:grid;grid-template-columns:1fr 1fr;gap:.18in;flex:1;min-height:0}.evs.curto{grid-template-columns:repeat(3,1fr);flex:none;margin-top:.1in}.evs.curto .ev{min-height:1.9in}
.ev{background:#fff;border-radius:10px;padding:.14in .18in;display:flex;flex-direction:column;gap:.05in;border:1px solid var(--line);border-left:3px solid var(--ac);min-width:0;overflow:hidden}
.ev-top{display:flex;justify-content:space-between;font-size:8pt;color:var(--grey)}.pill{background:var(--mist);border-radius:99px;padding:1px 8px;font-weight:600;color:#3A3833}.pill.warn{background:#FFF3D2;color:#8A6400}
.ev h4{font-size:11pt;font-weight:600}.ev p{margin:0;font-size:8.8pt;line-height:1.4}.ev-a{color:#2B2925}.ev-v{color:#3A3833}.ev-j{color:#3A3833}.ev-t{color:#5E5A52;font-style:italic;border-left:2px solid var(--line);padding-left:.08in}
.btn{margin-top:auto;align-self:flex-start;background:var(--ink);color:#fff;text-decoration:none;font-size:8.5pt;font-weight:600;padding:5px 12px;border-radius:99px}
.vazio{color:var(--grey);font-size:10pt;margin:0}.rod{position:absolute;left:3.4in;right:1.3in;bottom:.18in;font-size:7.5pt;color:var(--grey)}.pag{position:absolute;right:.5in;bottom:.16in;font-size:8pt;font-weight:700;color:var(--ac);letter-spacing:.06em}
.anexo{padding:.45in .55in}.anexo h3{font-size:18pt;font-weight:600;margin-bottom:.2in}.anexo table{width:100%;border-collapse:collapse;font-size:8.5pt}.anexo th{text-align:left;color:var(--grey);font-weight:600;border-bottom:2px solid var(--ink);padding:4px 6px}.anexo td{border-bottom:1px solid var(--line);padding:4px 6px;vertical-align:top}.anexo td span{color:var(--grey)}.anexo a{color:var(--gold);font-weight:600}
.fim{background:var(--ink);color:#fff;padding:.7in .8in}.fim .logo{height:.36in}.fim h2{font-size:28pt;font-weight:500;margin:.45in 0 .45in}.fim-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.4in}
.fim-grid b{display:block;color:var(--gold-2);font-family:Rubik;font-size:14pt;margin-bottom:.1in;font-weight:500}.fim-grid p{margin:0;font-size:11pt;line-height:1.55;color:#CFCAC0}.cred2{position:absolute;left:.8in;right:.8in;bottom:.3in;font-size:7pt;color:#8E8A82}"""
TOT = len(S)
DIRET = "--sem-diretoria" not in sys.argv  # produto A: a diretoria vai DENTRO do relatório de 10 perguntas
S = [sec.replace("{PAGN}", "" if DIRET else f"{k+1:02d} / {TOT:02d}") for k, sec in enumerate(S)]
H = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(TIT)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Rubik:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}{COR_CSS}{IMG_CSS}</style></head><body>{"".join(S)}</body></html>'''
open(f"{P}/relatorio_v2.html", "w").write(leve_html(H))
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(P)}/relatorio_v2.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(P)}/relatorio_v2.pdf',width:'13.333in',height:'7.5in',printBackground:true,margin:{{top:'0',bottom:'0',left:'0',right:'0'}}}});await b.close();}})();"""
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
if r.returncode == 0 and DIRET:
    import pikepdf
    tmp = f"{P}/.diretoria_tmp"
    rd = subprocess.run(["python3", "pipeline/relatorio_diretoria.py", AG, tmp, "--miolo"], capture_output=True, text=True)
    if rd.returncode == 0 and os.path.exists(f"{tmp}/diretoria_{AG}.pdf"):
        pr, pd = pikepdf.open(f"{P}/relatorio_v2.pdf", allow_overwriting_input=True), pikepdf.open(f"{tmp}/diretoria_{AG}.pdf")
        n = len(pr.pages)
        pr.pages.insert(2, pd.pages[0])  # quadro da diretoria logo após capa + sumário
        for k, pg in enumerate(list(pd.pages)[1:]): pr.pages.insert(n + k, pg)  # comparador + superintendentes antes da última página
        pr.save(f"{P}/relatorio_v2.pdf"); S += [""] * len(pd.pages)
    else: print("aviso: diretoria não incluída:", rd.stderr[-200:])
if r.returncode == 0: leve_pdf(f"{P}/relatorio_v2.pdf")
tam = os.path.getsize(f"{P}/relatorio_v2.pdf") // 1024 if r.returncode == 0 else 0
print(f"{P}/relatorio_v2.pdf" if r.returncode == 0 else "PDF não gerado: " + r.stderr[-300:], len(Q), "perguntas,", len(S), "páginas,", tam, "KB")
