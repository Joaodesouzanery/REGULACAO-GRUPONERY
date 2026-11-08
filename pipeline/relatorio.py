"""Relatório da consultoria (PDF, identidade Grupo Nery) a partir de uma pasta de semana do cliente.
Uso: python3 pipeline/relatorio.py clientes/<cliente>/<AAAA-semNN> [--titulo "..."] [--agencia antt]
Entrada:
  perguntas.md  — uma pergunta por linha «- texto [diretor: Nome] [tema: onibus] [setor: rodovias]» (tags opcionais).
  respostas/NN.md (opcional) — ficha revisada (consulta.py ficha). Se faltar e houver [diretor:], a ficha é gerada da base.
Saída: relatorio.html e relatorio.pdf (A4 paisagem, visual de apresentação: capa, conteúdo I/II/III, KPIs, gráfico,
tabela de evidências com trecho literal e link no minuto, contra-exemplos, confiança, anexo de metodologia).
Imagens de setor: docs/marca/setores/<setor>.jpg|png (opcional). Logo: docs/marca/logo_grupo_nery.png.
O PDF é gerado com o Chromium do Playwright (node); em máquina sem ele, abra o .html e use «Imprimir → PDF»."""
import sys, os, re, glob, html, json, base64, sqlite3, datetime, subprocess, collections
P = sys.argv[1].rstrip("/")
tit = sys.argv[sys.argv.index("--titulo") + 1] if "--titulo" in sys.argv else "Inteligência Regulatória"
AG = sys.argv[sys.argv.index("--agencia") + 1] if "--agencia" in sys.argv else os.environ.get("AGENCIA", "antt")
cliente, semana = P.split("/")[-2], P.split("/")[-1]
E = html.escape
def b64(path):
    if not path or not os.path.exists(path): return None
    ext = path.rsplit(".", 1)[-1].lower().replace("jpg", "jpeg")
    return f"data:image/{ext};base64," + base64.b64encode(open(path, "rb").read()).decode()
LOGO = b64("docs/marca/logo_grupo_nery.png")
def setor_img(s):
    for e in ("jpg", "jpeg", "png", "webp"):
        if s and os.path.exists(f"docs/marca/setores/{s}.{e}"): return b64(f"docs/marca/setores/{s}.{e}")
_CONN = {}
def conn(ag):
    if ag not in _CONN:
        db = "data/regulacao.db" if ag == "antt" else f"data/{ag}/regulacao.db"
        _CONN[ag] = sqlite3.connect(db) if os.path.exists(db) else None
        if _CONN[ag]: _CONN[ag].row_factory = sqlite3.Row
    return _CONN[ag]
c = conn(AG)
def seg(ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]
def _ata_url(vid):
    import json as _j, os as _o
    f = f"data/analise/{vid}.analise.json"
    return _j.load(open(f))["meta"].get("url") if _o.path.exists(f) else None
def link(vid, ts):
    if str(vid).startswith("ata_"): return _ata_url(vid) or ""
    return f"https://www.youtube.com/watch?v={vid}&t={max(seg(ts) - 5, 0)}s"
def md_inline(s):
    s = E(s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s); s = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", s)
    return s
def md_block(md):
    out, lista = [], False
    for l in md.splitlines():
        if not l.strip() or l.startswith("# "): continue
        m = re.match(r"\s*- (.*)", l)
        if m:
            if not lista: out.append("<ul>"); lista = True
            out.append(f"<li>{md_inline(m.group(1))}</li>"); continue
        if lista: out.append("</ul>"); lista = False
        out.append(f"<p>{md_inline(l)}</p>")
    if lista: out.append("</ul>")
    return "\n".join(out)
def dados(diretor, tema, ag=None):
    c = conn(ag or AG)
    """KPIs, distribuição, evidências e contra-exemplos direto da base."""
    q = ("select v.*, i.item, i.assunto, i.resultado, i.unanime, i.ts its, r.numero, r.data, r.video_id from votos v "
         "join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.diretor=?")
    a = [diretor]
    if tema: q += " and v.item_id in (select item_id from item_temas where tema=?)"; a.append(tema)
    R = c.execute(q + " order by r.data, i.ts", a).fetchall()
    if not R: return None
    cat = collections.Counter(r["categoria"] for r in R); rel = [r for r in R if r["eh_relator"]]
    acomp = cat["acompanha"] + cat["revisor_acompanha"]; nao_rel = max(len(R) - len(rel), 1)
    ev = [r for r in R if r["eh_relator"] and r["justificativa"]] or [r for r in R if r["justificativa"]] or R
    passo = max(len(ev) // 5, 1)
    div = [r for r in R if r["categoria"] in ("vista", "vencido", "revisor_diverge")]
    return {"n": len(R), "periodo": f"{R[0]['data'][:7]} a {R[-1]['data'][:7]}", "rel": len(rel), "rel_un": sum(r["unanime"] for r in rel),
            "pct_acomp": round(100 * acomp / nao_rel), "div": len(div),
            "dist": [("Relator", cat["relator"]), ("Acompanha", acomp), ("Vista", cat["vista"]), ("Voto-vista divergente", cat["revisor_diverge"]), ("Vencido", cat["vencido"]), ("Outro", cat["outro"] + cat["nao_captado"])],
            "ev": ev[::passo][:5], "contra": div[-4:]}
def barras(dist):
    mx = max(v for _, v in dist) or 1; W = 560; linhas = []
    for i, (k, v) in enumerate(dist):
        y = 10 + i * 34; w = int((W - 230) * v / mx)
        linhas.append(f'<text x="0" y="{y+17}" class="lb">{E(k)}</text><rect x="170" y="{y}" width="{max(w,2)}" height="24" rx="3" fill="url(#g)"/><text x="{176+w}" y="{y+17}" class="vl">{v}</text>')
    return (f'<svg viewBox="0 0 {W} {16+34*len(dist)}" class="chart"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#1F6F63"/><stop offset="1" stop-color="#5FCF9F"/></linearGradient></defs>'
            + "".join(linhas) + "</svg>")
perg = []
for l in open(f"{P}/perguntas.md"):
    if not l.startswith("- "): continue
    tags = dict(re.findall(r"\[(\w+):\s*([^\]]+)\]", l)); txt = re.sub(r"\[\w+:[^\]]+\]", "", l[2:]).strip()
    perg.append((txt, tags))
ROM = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"]
hoje = datetime.date.today().strftime("%d/%m/%Y")
pag = []
CAP_SETOR = next((t.get("setor") for _, t in perg if setor_img(t.get("setor"))), None)
CRED = ""
if CAP_SETOR and os.path.exists("docs/marca/setores/CREDITOS.md"):
    for l in open("docs/marca/setores/CREDITOS.md"):
        c_ = [x.strip() for x in l.split("|")]
        if len(c_) > 5 and c_[1].startswith(CAP_SETOR + "."): CRED = f"{c_[2]} — {c_[3]} ({c_[4]}), Wikimedia Commons"
cap_img = next((setor_img(t.get("setor")) for _, t in perg if setor_img(t.get("setor"))), None)
pag.append(f'''<section class="pg capa"><div class="faixa" style="{f"background-image:linear-gradient(160deg,rgba(27,42,74,.92),rgba(31,122,107,.75),rgba(95,207,159,.55)),url({cap_img})" if cap_img else ""}"><span class="c1"></span><span class="c2"></span></div>
<div class="capa-txt">{f'<img class="logo" src="{LOGO}">' if LOGO else ""}<h1>{E(tit)}</h1><div class="sub">{E(" · ".join(dict.fromkeys((t.get("agencia") or AG).upper() for _, t in perg)))} · Perfil decisório de diretores</div>
<div class="meta">Cliente: <b>{E(cliente)}</b><br>Período: {E(semana)} · Emitido em {hoje}</div><div class="conf">Confidencial — uso exclusivo do cliente</div>{f'<div class="cred">Foto da capa: {E(CRED)}</div>' if CRED else ""}</div></section>''')
cols = "".join(f'<div class="item"><div class="rom">{ROM[i]}</div><h3>{E(q[:110])}</h3><p>{E(" · ".join(v for k, v in t.items() if k in ("diretor", "tema")))}</p></div>' for i, (q, t) in enumerate(perg[:10]))
mais = f'<p class="mais">+ {len(perg)-10} perguntas</p>' if len(perg) > 10 else ""
pag.append(f'<section class="pg"><header>{f"<img class=logo-s src={LOGO}>" if LOGO else ""}</header><h2>Conteúdo</h2><div class="kicker">PERGUNTAS DESTE RELATÓRIO</div><div class="conteudo">{cols}</div>{mais}</section>')
for i, (q, t) in enumerate(perg):
    rf = sorted(glob.glob(f"{P}/respostas/{i+1:02d}*.md"))
    d = dados(t["diretor"].strip(), t.get("tema", "").strip() or None, t.get("agencia", "").strip().lower() or None) if (conn(t.get("agencia", "").strip().lower() or AG) and t.get("diretor")) else None
    head = f'<header>{f"<img class=logo-s src={LOGO}>" if LOGO else ""}</header><div class="rom-s">{ROM[i]}</div><h2>{E(q)}</h2>'
    if d:
        kp = "".join(f'<div class="kpi"><b>{v}</b><span>{E(k)}</span></div>' for k, v in [("votos analisados", d["n"]), ("relatorias", d["rel"]), ("acompanha o relator", f'{d["pct_acomp"]}%'), ("vista / divergência / vencido", d["div"])])
        curta = ""
        if rf:
            m = re.search(r"\*\*1\. Resposta curta:\*\*\s*(.+)", open(rf[0]).read()); curta = re.sub(r"\s*\[Completar[^\]]*\]", "", m.group(1)) if m else ""
        pag.append(f'<section class="pg">{head}<div class="lead">{md_inline(curta) if curta else ""}</div><div class="kpis">{kp}</div>'
                   f'<div class="dois"><div><h4>Como vota ({E(d["periodo"])})</h4>{barras(d["dist"])}<div class="fonte">Fonte: reuniões públicas de diretoria ({(t.get("agencia") or AG).upper()}), YouTube oficial; base Grupo Nery. n = {d["n"]}.</div></div>'
                   f'<div><h4>Contra-exemplos (fora do padrão)</h4><ul>' + ("".join(f'<li><b>RD {E(str(r["numero"]))} ({E(r["data"])})</b>, item {E(r["item"])} — {E(r["categoria"])}: {E((r["justificativa"] or r["voto"] or "")[:160])} · <a href="{link(r["video_id"], r["ts"] or r["its"])}">vídeo</a></li>' for r in d["contra"]) or "<li>Nenhum voto de vista, divergência ou vencido neste recorte.</li>") + '</ul></div></div></section>')
        linhas = "".join(f'<tr><td><b>RD {E(str(r["numero"]))}</b><br>{E(r["data"])}<br>item {E(r["item"])}</td><td>{E(r["assunto"][:150])}</td><td>{E((r["voto"] or "")[:90])}<br><i>{E((r["justificativa"] or "")[:140])}</i></td><td class="lit">«{E((r["trecho"] or "—")[:230])}…»</td><td><a href="{link(r["video_id"], None) if str(r["video_id"]).startswith("ata_") else f'https://www.youtube.com/watch?v={r["video_id"]}&t={max((r["trecho_t"] or seg(r["ts"] or r["its"])) - 3, 0)}s'}">{"ata oficial" if str(r["video_id"]).startswith("ata_") else "assistir no minuto"}</a></td></tr>' for r in d["ev"])
        pag.append(f'<section class="pg">{head}<h4>Evidências</h4><table><tr><th>Reunião</th><th>Assunto</th><th>Voto e justificativa</th><th>Trecho literal (legenda)</th><th>Vídeo</th></tr>{linhas}</table>'
                   f'<div class="fonte">Trechos da legenda automática do YouTube (podem conter erros de transcrição). Links abrem o vídeo no minuto do voto.</div></section>')
    if rf:
        corpo = re.sub(r"\*\*3\. Evidências.*?(?=\*\*4\.)", "", open(rf[0]).read(), flags=re.S) if d else open(rf[0]).read()
        corpo = re.sub(r"\s*\[Completar[^\]]*\]", "", corpo)
        pag.append(f'<section class="pg texto">{head}{md_block(corpo)}</section>')
    elif not d:
        pag.append(f'<section class="pg">{head}<p>(resposta pendente)</p></section>')
pag.append(f'''<section class="pg texto"><header>{f"<img class=logo-s src={LOGO}>" if LOGO else ""}</header><h2>Metodologia, confiabilidade e cobertura</h2>
<table><tr><th>Etapa</th><th>O que fazemos</th><th>Entregável</th></tr>
<tr><td>Coleta</td><td>Todas as reuniões públicas de diretoria e eventos (audiências, participativas) do canal oficial da agência</td><td>Inventário e transcrições</td></tr>
<tr><td>Estruturação</td><td>Cada item: relator, resultado, voto de cada diretor, justificativa, trecho literal e minuto</td><td>Base de votos com evidência</td></tr>
<tr><td>Conferência</td><td>Releitura cega por amostra; concordância ≈ 94–95% no voto por diretor (ANTT 2019–2026)</td><td>Relatório de qualidade</td></tr>
<tr><td>Mandatos</td><td>Senado, DOU e imprensa especializada; vacâncias calculadas por cadeira</td><td>Linha do tempo e vacância</td></tr>
<tr><td>Análise</td><td>Padrões por diretor e tema, contra-exemplos, falas públicas — sem rótulos pessoais</td><td>Este relatório</td></tr></table>
<ul><li>Limites: legenda automática (nomes e valores podem ter erros); quem apenas acompanha o relator raramente fala (minuto aproximado); itens sigilosos e voto escrito completo (processo SEI) não constam.</li>
<li>Inferências de comportamento baseiam-se em contagens e falas registradas; não são juízo pessoal.</li></ul></section>''')
CSS = """@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Helvetica Neue',Arial,sans-serif;color:#3D4766;background:#fff}
.pg{width:297mm;height:210mm;padding:14mm 16mm 12mm;position:relative;page-break-after:always;overflow:hidden;background:#F6F7F9}
header{position:absolute;right:14mm;top:9mm}.logo-s{height:9mm}h2{color:#1F7A6B;font-size:27pt;margin:4mm 0 3mm;max-width:235mm;line-height:1.1}
h3{color:#1F7A6B;font-size:13pt;margin:3mm 0}h4{color:#1B2A4A;font-size:13pt;margin:2mm 0}.kicker{font-size:10pt;letter-spacing:.06em;margin-bottom:6mm}
.capa{display:flex;padding:0;background:#fff}.faixa{width:95mm;height:100%;background:linear-gradient(160deg,#1B2A4A 0%,#1F7A6B 55%,#4FB98A 100%);background-size:cover;background-position:center;position:relative}
.c1,.c2{position:absolute;border-radius:50%;border:16mm solid #fff}.c1{width:70mm;height:70mm;left:-38mm;top:-38mm}.c2{width:70mm;height:70mm;right:-35mm;bottom:-35mm}
.capa-txt{flex:1;padding:22mm 18mm;position:relative}.capa .logo{height:13mm;position:absolute;right:14mm;top:10mm}.capa h1{color:#1F7A6B;font-size:36pt;margin:38mm 0 4mm}
.sub{font-size:15pt;color:#1B2A4A;font-weight:600}.meta{margin-top:18mm;font-size:12pt;line-height:1.6}.conf{position:absolute;bottom:14mm;font-size:9pt;color:#8A93A8}.cred{position:absolute;bottom:9mm;font-size:7pt;color:#8A93A8}
.conteudo{display:flex;flex-wrap:wrap;gap:6mm 8mm;justify-content:space-around;text-align:center}.item{flex:0 0 18%}.conteudo h3{font-size:10.5pt;margin:1mm 0}.conteudo p{font-size:8.5pt;margin:1mm 0}.rom{font-size:22pt;font-weight:800;color:#1B2A4A;letter-spacing:.08em}.item p{font-size:10pt}
.rom-s{position:absolute;left:16mm;top:6mm;font-weight:800;color:#1B2A4A;font-size:12pt}.lead{font-size:13pt;line-height:1.45;max-width:250mm;margin-bottom:5mm}
.kpis{display:flex;gap:6mm;margin-bottom:6mm}.kpi{flex:1;background:#fff;border:1px solid #DCE3EA;border-radius:4mm;padding:4mm 5mm;box-shadow:0 1mm 2mm rgba(0,0,0,.04)}
.kpi b{display:block;font-size:24pt;color:#2FB37A}.kpi span{font-size:10pt}.dois{display:flex;gap:10mm}.dois>div{flex:1}.chart{width:100%}.lb{font-size:12px;fill:#3D4766}.vl{font-size:12px;fill:#1B2A4A;font-weight:700}
.fonte{font-size:8pt;color:#8A93A8;margin-top:2mm}ul{font-size:10.5pt;line-height:1.45;padding-left:5mm}a{color:#1F7A6B}
table{width:100%;border-collapse:collapse;font-size:9.5pt;background:#fff}th{background:#207A6A;color:#fff;padding:3mm;text-align:center;font-size:10.5pt}
td{padding:2.5mm 3mm;border:1px solid #fff;vertical-align:top}tr:nth-child(even) td{background:#E3EFDB}tr:nth-child(odd) td{background:#F0F1F2}td.lit{font-style:italic;color:#2F3A55}
.texto p,.texto li{font-size:10.5pt;line-height:1.45}.texto{overflow:hidden}.mais{text-align:center;margin-top:8mm}"""
H = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(tit)} — {E(cliente)}</title><style>{CSS}</style></head><body>{"".join(pag)}</body></html>'
open(f"{P}/relatorio.html", "w").write(H)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(P)}/relatorio.html');await p.pdf({{path:'{os.path.abspath(P)}/relatorio.pdf',landscape:true,format:'A4',printBackground:true,margin:{{top:'0',bottom:'0',left:'0',right:'0'}}}});await b.close();}})();"""
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
print(f"{P}/relatorio.pdf" if r.returncode == 0 else "PDF não gerado (" + (r.stderr[-300:] or "node/playwright ausente") + f"); abra {P}/relatorio.html e imprima em PDF", len(perg), "perguntas")
