"""Alerta pré-pauta (produto D): 1–2 páginas antes da próxima reunião, por cliente.
Cruza a pauta publicada (pipeline/pautas.py) com os aliases/temas do cliente; sem pauta publicada, usa o calendário
oficial + os itens retirados/vista da última reunião + os temas do cliente. Para cada item: relator, previsão por
diretor (mapa_tema), precedentes (similares). Depois da reunião: rode de novo com --resultado para a linha de resultado.
Uso: python3 pipeline/alerta_pauta.py clientes/<x>/<pasta> [--agencia antaq]   → <pasta>/alerta_<ag>_<reuniao>.pdf"""
import sys, os, re, json, html, glob, datetime, subprocess, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, mapa_tema, similares
from pdf_leve import leve_html, leve_pdf

P = sys.argv[1].rstrip("/")
EMP = json.load(open(f"{P}/empresa.json"))
AG = sys.argv[sys.argv.index("--agencia") + 1] if "--agencia" in sys.argv else EMP.get("agencias", ["antaq"])[0]
D = "data" if AG == "antt" else f"data/{AG}"
NOME = {"antt": "ANTT", "anm": "ANM", "antaq": "ANTAQ"}[AG]
E = html.escape
hoje = datetime.date.today().isoformat()
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if s else "a confirmar"
b64 = lambda p, t="png": f"data:image/{t};base64," + base64.b64encode(open(p, "rb").read()).decode() if p and os.path.exists(p) else ""
RX = re.compile("|".join(EMP["aliases"]), re.I)
TEMAS = EMP.get("temas_consultoria", [])
c = previsao.conn(AG)

# próxima reunião (calendário + pauta)
pautas = sorted((json.load(open(f)) for f in glob.glob(f"{D}/pautas/*.json")), key=lambda x: x.get("data") or "9999")
prox = [p for p in pautas if (p.get("data") or "9999") >= hoje]
alvo = prox[0] if prox else {"reuniao": "próxima", "data": None, "pauta": "a confirmar", "itens": []}
seg = prox[1] if len(prox) > 1 else None

itens = []  # (origem, texto, relator, regex de tema para previsão)
for it in alvo.get("itens", []):
    txt = f"{it.get('interessado','')} {it.get('assunto','')}"
    tema = next((t for t in TEMAS if re.search(t["regex"], txt, re.I)), None)
    if RX.search(txt) or tema:
        itens.append(("pauta", f"Item {it['item']} · {it.get('processo') or ''} · {it.get('interessado','')[:90]}: {it.get('assunto','')[:260]}", it.get("relator"), (tema or {}).get("regex")))
# última reunião: itens retirados / vista / do cliente
ult = c.execute("select id, numero, data, video_id from reunioes order by data desc limit 1").fetchone()
for i in c.execute("select * from itens where reuniao_id=?", (ult["id"],)):
    res = (i["resultado"] or "").lower(); txt = f"{i['interessado'] or ''} {i['assunto'] or ''}"
    pedido = str(i["item"]) in [str(x) for x in EMP.get("itens_acompanhar", [])]
    cliente = bool(RX.search(txt)) or pedido
    if cliente or "retirad" in res or "vista" in res:
        tema = next((t for t in TEMAS if re.search(t["regex"], txt, re.I)), None)
        itens.append(("cliente (informado pelo cliente)" if pedido and not RX.search(i["assunto"] or "") else "cliente" if cliente else "em aberto", f"{ult['numero']}ª · item {i['item']}: {(i['assunto'] or 'assunto não lido em sessão')[:220]} — {(i['resultado'] or '')[:90]}",
                      i["relator"], (tema or {}).get("regex"), mapa_tema.link(ult["video_id"], i["ts"]), i["id"]))
ia = EMP.get("item_antecipado")

ordem = {"pauta": 0, "cliente": 1, "cliente (informado pelo cliente)": 1, "em aberto": 2}
itens.sort(key=lambda x: (ordem[x[0]], 0 if x[3] else 1))
blocos = ""
for k, x in enumerate(itens[:8]):
    origem, txt, rel, rx = x[:4]
    lk = x[4] if len(x) > 4 else None
    prev = ""
    if rx:
        m = mapa_tema.mapear(AG, rx, "2023-01-01"); pu = 1.0
        for st in m["por_diretor"].values(): pu *= st["p_acomp"]
        prev = f'<div class="pv">Previsão (inferência; base: tema do item desde 2023, n={sum(st["n"] for st in m["por_diretor"].values())} votos): unânime com o relator <b>{pu:.0%}</b> · ' + " · ".join(f'{E(d.split()[0])} {st["p_acomp"]:.0%}' for d, st in m["por_diretor"].items()) + "</div>"
    blocos += (f'<li class="o-{origem.split()[0]}"><span class="tg">{E(origem)}</span> {E(txt)}{" · relator " + E(rel) if rel else ""} '
               + (f'<a href="{lk}">▶</a>' if lk else "") + prev + "</li>")
# precedentes para o tema principal do cliente
base_txt = " ".join(re.sub(r"^\w\)\s*|:.*$", "", t["titulo"]) for t in TEMAS) or EMP["nome"]
sim = [x for x in similares.similares(AG, base_txt, 12, "|".join(EMP["aliases"])) if "não lido" not in (x["assunto"] or "")][:6]
simh = "".join(f'<li><b>{fmtd(s["data"])} · {s["numero"]}ª item {E(str(s["item"]))}</b> {E((s["assunto"] or "")[:120])} — {E(s["desfecho"])} · relator {E(s["relator"] or "—")} <a href="{s["link"]}">▶</a></li>' for s in sim)

LOGO_P = b64("docs/marca/circle/logo_circle_preto.png"); NERY = b64("docs/marca/grupo_nery/logo_preto.png"); CLI = b64(EMP.get("logo"))
pauta_txt = f'<a href="{alvo["pauta"]}">pauta publicada</a>' if alvo.get("itens") else "pauta ainda não publicada — itens abaixo vêm da última reunião e dos temas do cliente"
H = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Alerta {NOME}</title><style>
@page{{size:13.333in 7.5in;margin:0}}body{{margin:0;font-family:Inter,system-ui,sans-serif;color:#0B0B0B}}.pg{{width:13.333in;height:7.5in;padding:.4in .55in;box-sizing:border-box;position:relative;overflow:hidden}}
.top{{display:flex;align-items:center;gap:14px}}.top img{{height:.3in}}.top .cli{{margin-left:auto;height:.4in}}.eb{{font-size:9pt;letter-spacing:.12em;text-transform:uppercase;color:#B08600;margin-top:.2in}}
h1{{font-size:22pt;margin:.06in 0 .04in}}.sub{{font-size:10pt;color:#4A4741}}.duas{{display:grid;grid-template-columns:1.35fr 1fr;gap:.3in;margin-top:.18in}}
ul{{margin:0;padding-left:1.1em;font-size:8.8pt;line-height:1.42}}li{{margin-bottom:.07in}}.tg{{font-size:7pt;text-transform:uppercase;letter-spacing:.06em;background:#F5F3EE;border-radius:99px;padding:1px 7px;font-weight:700;color:#6E6A63}}
.o-cliente .tg{{background:#FFF3D2;color:#8A6400}}.pv{{font-size:8pt;color:#3A3833;margin-top:2px}}a{{color:#B08600;font-weight:700;text-decoration:none}}h3{{font-size:11pt;margin:0 0 .08in}}
.cal{{background:#F5F3EE;border-radius:10px;padding:.12in .16in;font-size:9pt;margin-bottom:.16in}}.rod{{position:absolute;left:.55in;right:.55in;bottom:.18in;font-size:7.3pt;color:#6E6A63}}
</style></head><body><section class="pg"><div class="top">{f'<img src="{LOGO_P}">' if LOGO_P else ""}<span style="font-size:8pt;color:#6E6A63">em parceria com</span>{f'<img src="{NERY}">' if NERY else "Grupo Nery"}{f'<img class="cli" src="{CLI}">' if CLI else ""}</div>
<div class="eb">Alerta pré-pauta · {NOME} · {E(EMP["nome"].split("(")[0].strip())}</div><h1>{E(str(alvo["reuniao"]))}ª reunião · {fmtd(alvo.get("data"))} · {E(alvo.get("formato") or "")}</h1>
<div class="sub">{pauta_txt}. Emitido em {fmtd(hoje)}.</div>
<div class="duas"><div><h3>O que acompanhar</h3><ul>{blocos or "<li>Nenhum item do cliente identificado.</li>"}</ul></div>
<div><div class="cal"><b>Calendário oficial:</b> {E(str(alvo["reuniao"]))}ª em {fmtd(alvo.get("data"))} ({E(alvo.get("formato") or "")}){f" · {E(seg['reuniao'])}ª em {fmtd(seg.get('data'))} ({E(seg.get('formato') or '')})" if seg else ""}.<br>
{"Reunião virtual: sem transmissão; resultado só em ata." if (alvo.get("formato") or "") == "virtual" else "Reunião transmitida: resultado com link no minuto no dia seguinte."}</div>
<h3>Precedentes mais parecidos</h3><ul>{simh}</ul></div></div>
<div class="rod">Fontes públicas (vídeos oficiais, pauta e calendário da agência). Previsões são estimativas a partir do histórico de votos (prior 97%) e não substituem a publicação oficial. Legenda automática pode errar nomes e números.</div></section></body></html>'''
base = f"{P}/alerta_{AG}_{re.sub(r'\\W', '', str(alvo['reuniao']))}"
open(base + ".html", "w").write(leve_html(H))
js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(base)}.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(base)}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
if r.returncode == 0: leve_pdf(base + ".pdf")
print(base + ".pdf" if r.returncode == 0 else r.stderr[-300:], len(itens), "itens")
