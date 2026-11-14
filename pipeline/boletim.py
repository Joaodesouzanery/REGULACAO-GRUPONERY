"""Boletim mensal da agência (produto à parte): o que a diretoria decidiu no mês, quem divergiu, quem relatou,
empresas citadas, diretoria (vagas, mandatos), eventos e «o que esperar». PDF 16:9 leve (identidade Circle).
Uso: python3 pipeline/boletim.py <antt|anm|antaq> AAAA-MM [saida_dir]
Saída padrão: agencias/<ag>/boletins/boletim_<ag>_<AAAA-MM>.pdf (gerado, fora do git se pesado)."""
import sys, os, re, json, html, base64, sqlite3, datetime, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_leve import leve_html, leve_pdf
from marca import parceria_html, MARCA_CSS
import previsao
from desfecho import desfecho_item

AG, MES = sys.argv[1].lower(), sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else f"agencias/{AG}/boletins"
os.makedirs(OUT, exist_ok=True)
D = "data" if AG == "antt" else f"data/{AG}"
NOME = {"antt": "ANTT", "anm": "ANM", "antaq": "ANTAQ"}[AG]
SET = {"antt": "rodovias", "anm": "mineracao", "antaq": "portos"}[AG]
MESES = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()
ano, mm = map(int, MES.split("-")); MESN = f"{MESES[mm-1]} de {ano}"
ini = datetime.date(ano, mm, 1); fim = (ini + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
E = html.escape
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if s else "—"
c = previsao.conn(AG)


def b64(p, t="jpeg"):
    return f"data:image/{t};base64," + base64.b64encode(open(p, "rb").read()).decode() if p and os.path.exists(p) else ""


def seg(ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]


yt = lambda vid, ts: f"https://www.youtube.com/watch?v={vid}&t={max(seg(ts) - 3, 0)}s"
R = c.execute("select * from reunioes where data between ? and ? order by data", (ini.isoformat(), fim.isoformat())).fetchall()
rid = [r["id"] for r in R]
Q = ",".join("?" * len(rid)) or "null"
IT = c.execute(f"select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where i.reuniao_id in ({Q}) order by r.data, i.id", rid).fetchall()
VT = c.execute(f"select v.*, i.assunto, i.item, i.resultado, r.numero, r.data, r.video_id from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where i.reuniao_id in ({Q})", rid).fetchall()
res = lambda i: (i["resultado"] or "").lower()
n_vista = sum("vista" in res(i) for i in IT); n_ret = sum("retirad" in res(i) for i in IT); n_sig = sum("sigilo" in res(i) for i in IT)
div_items = {v["item_id"] for v in VT if v["categoria"] in ("vencido", "revisor_diverge")}
delib = [i for i in IT if not any(k in res(i) for k in ("vista", "retirad", "sigilo", "conhecimento"))]
n_div = len(div_items)
temas = collections.Counter(t for i in IT for (t,) in c.execute("select tema from item_temas where item_id=?", (i["id"],)))
rel = collections.Counter(v["diretor"] for v in VT if v["eh_relator"])
# empresas citadas: entidades indexadas (ANTT/ANM) ou interessado
ent = collections.Counter()
for i in IT:
    es = [e for (e,) in c.execute("select coalesce(n.sigla, n.nome, ie.entidade) from item_entidade ie left join entidades n on n.id=ie.entidade where ie.item_id=?", (i["id"],))]
    for e in (es or ([i["interessado"]] if i["interessado"] else [])): ent[e[:40]] += 1
# eventos do mês
EV = c.execute("select * from eventos where data between ? and ? order by data", (ini.isoformat(), fim.isoformat())).fetchall()
# diretoria
mand = ld(f"{D}/mandatos.json", []); vac = [v for v in ld(f"{D}/vacancias.json", []) if not v.get("fim")]
board, _ = previsao.colegiado_atual(c)
lim = fim + datetime.timedelta(days=120)
venc = [m for m in mand if (m.get("fim_legal") or m.get("fim") or "") and fim.isoformat() < (m.get("fim_legal") or m.get("fim")) <= lim.isoformat()]
entr = [m for m in mand if (m.get("inicio") or "")[:7] == MES]; sai = [m for m in mand if (m.get("fim") or "")[:7] == MES]
# canal × texto (cobertura do mês)
vids = c.execute("select id, titulo, tipo from videos where data between ? and ?", (ini.isoformat(), fim.isoformat())).fetchall()
sem = [v for v in vids if v["tipo"] == "diretoria" and v["id"] not in {r["video_id"] for r in R}]

LOGO = b64("docs/marca/circle/logo_circle_branco.png", "png"); LOGO_P = b64("docs/marca/circle/logo_circle_preto.png", "png")
REC = "docs/marca/setores/recortes"
top = lambda n, t: f'<header class="top"><span class="num">{n:02d}</span><span>{E(t)} · {NOME} · {MESN}</span>{f"<img src={LOGO_P} class=logo-p>" if LOGO_P else ""}</header>'
S = []
S.append(f'''<section class="pg capa" style="background-image:url({b64(f"{REC}/{SET}_capa.jpg")})"><div class="cartao">{f'<img class="logo" src="{LOGO}">' if LOGO else ''}
{parceria_html()}<div class="eyebrow">Boletim mensal · inteligência regulatória</div><h1>{NOME} em {MESN}</h1><div class="onda"></div>
<p>O que a diretoria colegiada decidiu, quem relatou e quem divergiu, empresas em pauta, diretoria e eventos públicos — com o link do vídeo no minuto de cada decisão.</p>
<div class="meta">{len(R)} reuniões de diretoria · {len(IT)} itens · {len(EV)} eventos públicos · emitido em {datetime.date.today().strftime("%d/%m/%Y")}</div></div></section>''')
# 1 números
kp = [(len(R), "reuniões de diretoria", ", ".join(f"{r['numero']}ª ({fmtd(r['data'])[:5]})" for r in R)), (len(IT), "itens em pauta", f"{len(delib)} deliberados"),
      (len(delib) - n_div, "decididos sem divergência", f"{n_div} com voto vencido/divergente"), (n_vista, "pedidos de vista", "devem voltar à pauta"),
      (n_ret, "retirados de pauta", ""), (n_sig, "itens sigilosos", "sem transmissão")]
tb = "".join(f'<div class="kp"><div class="big">{a}</div><div class="lab">{E(b)}</div><div class="ex">{E(x)}</div></div>' for a, b, x in kp)
tt = "".join(f'<div class="bar"><span>{E(t.replace("_", " "))}</span><i style="width:{100*n/max(temas.values())}%"></i><b>{n}</b></div>' for t, n in temas.most_common(8))
S.append(f'<section class="pg">{top(1, "O mês em números")}<h2>O mês em números</h2><div class="kgrid">{tb}</div><h3>Temas mais frequentes (itens)</h3><div class="bars">{tt}</div>'
         f'<div class="rod">Contagens a partir das transcrições analisadas. Um item pode ter mais de um tema.</div></section>')
# 2 decisões por tema
cards = ""
usados = set()
for t, _ in temas.most_common(5):
    its = [i for i in delib if i["id"] not in usados and c.execute("select 1 from item_temas where item_id=? and tema=?", (i["id"], t)).fetchone()][:1]
    for i in its:
        usados.add(i["id"])
        cards += f'''<div class="cd"><div class="tg">{E(t.replace("_", " "))}</div><div class="cd-t">RD {E(i["numero"])} · {fmtd(i["data"])} · item {E(str(i["item"] or ""))}</div>
<p><b>{E((i["assunto"] or "")[:150])}</b></p><p>{E((i["resultado"] or "")[:110])}{" · relator " + E(i["relator"]) if i["relator"] else ""}</p><p class="rs">{E((i["resumo"] or "")[:230])}</p><a href="{yt(i["video_id"], i["ts"])}">▶ ver no vídeo</a></div>'''
S.append(f'<section class="pg cinza">{top(2, "Decisões por tema")}<h2>Principais decisões, por tema</h2><div class="cgrid3">{cards}</div><div class="rod">Um destaque por tema entre os 5 temas mais frequentes do mês. ▶ abre o vídeo no minuto (legenda automática: confira nomes e valores).</div></section>')
# 3 divergências
dv = [v for v in VT if v["categoria"] in ("vencido", "revisor_diverge", "vista")]
lin = "".join(f'<tr><td>RD {E(v["numero"])}<br>{fmtd(v["data"])[:5]}</td><td>{E(v["diretor"])}</td><td>{E({"vencido": "vencido", "revisor_diverge": "divergiu (revisor)", "vista": "pediu vista"}[v["categoria"]])}</td>'
              f'<td>{E((v["assunto"] or "")[:80])}</td><td>{E((v["justificativa"] or v["voto"] or "")[:150])}</td><td><a href="{yt(v["video_id"], v["ts"])}">▶</a></td></tr>' for v in dv[:9])
S.append(f'<section class="pg">{top(3, "Divergências e vistas")}<h2>Quem divergiu ou pediu vista — e por quê</h2>'
         + (f'<table><tr><th>Reunião</th><th>Diretor</th><th>O quê</th><th>Assunto</th><th>Justificativa registrada</th><th></th></tr>{lin}</table>' if lin else '<p class="vazio">Nenhuma divergência ou vista registrada no mês: todos os itens deliberados seguiram o relator.</p>')
         + f'<div class="rod">{len(dv)} registro(s) no mês{" (mostrando 9)" if len(dv) > 9 else ""}. Justificativa resumida a partir da fala; tom não é inferido aqui.</div></section>')
# 4 relatorias + empresas
rb = "".join(f'<div class="bar"><span>{E(d)}</span><i style="width:{100*n/max(rel.values())}%"></i><b>{n}</b></div>' for d, n in rel.most_common()) or '<p class="vazio">—</p>'
eb = "".join(f'<div class="bar"><span>{E(e)}</span><i style="width:{100*n/max(ent.values())}%"></i><b>{n}</b></div>' for e, n in ent.most_common(8)) or '<p class="vazio">Nenhuma empresa identificada.</p>'
S.append(f'<section class="pg">{top(4, "Quem relatou · empresas")}<div class="dois"><div><h2>Quem relatou</h2><div class="bars">{rb}</div></div><div><h2>Empresas e entes em pauta</h2><div class="bars">{eb}</div></div></div>'
         f'<div class="rod">Relatorias = itens em que o diretor foi relator no mês. Empresas pelo índice de entidades e pelo campo «interessado» (nomes vêm da legenda).</div></section>')
# 5 diretoria
bl = "".join(f"<li>{E(d)}</li>" for d in board)
vl = "".join(f"<li><b>{E(v['cadeira'])}</b> — vaga desde {fmtd(v['inicio'])}; interinos: {E(v.get('interinos') or '—')}</li>" for v in vac) or "<li>Nenhuma vaga aberta.</li>"
ml = "".join(f"<li>{E(m['diretor'])} — mandato até {fmtd(m.get('fim_legal') or m.get('fim'))}</li>" for m in venc) or "<li>Nenhum mandato vence nos próximos 120 dias.</li>"
mv = "".join(f"<li>Entrou: {E(m['diretor'])} ({fmtd(m['inicio'])})</li>" for m in entr) + "".join(f"<li>Saiu: {E(m['diretor'])} ({fmtd(m['fim'])})</li>" for m in sai) or "<li>Sem mudanças registradas no mês.</li>"
S.append(f'<section class="pg cinza">{top(5, "Diretoria")}<h2>Diretoria: quem votou, vagas e mandatos</h2><div class="dois"><div class="bx"><h3>Votaram nas últimas reuniões</h3><ul>{bl}</ul><h3>Mudanças no mês</h3><ul>{mv}</ul></div>'
         f'<div class="bx"><h3>Vagas abertas</h3><ul>{vl}</ul><h3>Mandatos que vencem em até 120 dias</h3><ul>{ml}</ul></div></div>'
         f'<div class="rod">Fontes: mandatos.json e vacancias.json (Senado, DOU, portarias), conferidos na checagem do dia 1. Posse não confirmada no DOU é indicada como tal na base.</div></section>')
# 6 eventos
evh = "".join(f'<div class="cd"><div class="tg">{E(e["tipo"])}</div><div class="cd-t">{fmtd(e["data"])}</div><p><b>{E((e["titulo"] or "")[:110])}</b></p><p class="rs">{E((e["resumo"] or e["objeto"] or "")[:260])}</p><a href="https://www.youtube.com/watch?v={e["video_id"]}">▶ vídeo</a></div>' for e in EV[:6]) or '<p class="vazio">Sem eventos no mês.</p>'
S.append(f'<section class="pg">{top(6, "Eventos públicos")}<h2>Audiências, participativas e workshops</h2><div class="cgrid3">{evh}</div>'
         f'<div class="rod">A maioria das audiências não tem fala de diretor; o resumo cobre janelas da sessão, não a íntegra.</div></section>')
# 7 o que esperar
volta = [i for i in IT if "vista" in res(i) or "retirad" in res(i)]
vh = "".join(f"<li>RD {E(i['numero'])} · {E((i['assunto'] or '')[:110])} — <i>{E((i['resultado'] or '')[:70])}</i></li>" for i in volta[:8]) or "<li>Nenhum item com vista ou retirado.</li>"
S.append(f'<section class="pg cinza">{top(7, "O que esperar")}<h2>O que esperar no próximo mês</h2><div class="dois"><div class="bx"><h3>Itens que devem voltar à pauta</h3><ul>{vh}</ul></div>'
         f'<div class="bx"><h3>Leitura (inferência)</h3><ul><li>Itens com vista costumam voltar em 1 a 2 reuniões; vistas coletivas, na reunião seguinte.</li>'
         f'<li>{"Com vaga aberta, as decisões seguem com interinos — " + E(vac[0].get("interinos") or "") if vac else "Colegiado completo."}</li>'
         f'<li>{"Mandatos vencendo: " + ", ".join(E(m["diretor"]) for m in venc) + " — atenção a sabatinas e reconduções." if venc else "Sem fim de mandato no horizonte de 120 dias."}</li></ul></div></div>'
         f'<div class="rod">Inferência a partir do histórico; pautas futuras ainda não são coletadas automaticamente (ver Proposta 2, bloco Agenda).</div></section>')
cob = E(subprocess.run(["python3", "pipeline/cobertura_resposta.py", AG, "-", "-", str(ano)], capture_output=True, text=True).stdout.strip().replace("**", "")).replace("\n", "<br>")
calj = json.load(open(f"{D}/calendario.json")) if os.path.exists(f"{D}/calendario.json") else []
vv = [x["reuniao"] + "ª (" + fmtd(x["data"])[:5] + ")" for x in calj if x["data"][:7] == MES and x.get("formato") == "virtual"]
virt = ("<b>Reuniões virtuais do mês (sem transmissão; só ata, ainda não incluídas):</b> " + E(", ".join(vv)) + "<br><br>") if vv else ""
semh = ("<b>Reuniões do mês no canal sem transcrição:</b> " + E(", ".join(v["titulo"] for v in sem)) + "<br><br>") if sem else ""
S.append(f'<section class="pg fim">{f"<img class=logo src={LOGO}>" if LOGO else ""}{parceria_html()}<h2>Cobertura e como ler</h2><div class="fimc">{semh}{virt}{cob}</div></section>')
TOT = len(S)
S = [s.replace("</section>", f'<div class="pag">{i+1:02d} / {TOT:02d}</div></section>', 1) if i else s for i, s in enumerate(S)]
CSS = """@page{size:13.333in 7.5in;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,sans-serif;color:#0B0B0B;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:13.333in;height:7.5in;position:relative;overflow:hidden;page-break-after:always;padding:.38in .5in}h1,h2,h3{font-family:Rubik,Inter,sans-serif;margin:0}.cinza{background:#F5F3EE}
.capa{padding:0;background-size:cover;background-position:center;background-color:#151412}.cartao{position:absolute;left:.75in;top:1in;width:6.2in;padding:.5in .55in;border-radius:18px;background:#161513;color:#fff}
.logo{height:.4in;margin-bottom:.3in}.eyebrow{font-size:11pt;letter-spacing:.12em;text-transform:uppercase;color:#E2B93B}.cartao h1{font-size:32pt;margin:.14in 0}.onda{height:6px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.35) 0 10px,transparent 10px 16px);margin:.2in 0}
.cartao p{font-size:12pt;line-height:1.5;color:#E8E5DE;margin:0}.meta{margin-top:.25in;font-size:9pt;color:#BDB8AE}
.top{display:flex;align-items:center;gap:.12in;font-size:9pt;color:#6E6A63;letter-spacing:.08em;text-transform:uppercase}.num{color:#C99A06;font-weight:700}.logo-p{height:.22in;margin-left:auto}
h2{font-size:21pt;margin:.12in 0 .18in}h3{font-size:12pt;margin:.14in 0 .08in}.kgrid{display:grid;grid-template-columns:repeat(6,1fr);gap:.12in}.kp{background:#fff;border:1px solid #E3DFD6;border-top:4px solid #C99A06;border-radius:10px;padding:.12in}
.big{font-family:Rubik;font-size:30pt;font-weight:500;line-height:1.1}.lab{font-size:9pt;font-weight:600}.ex{font-size:7.8pt;color:#6E6A63;margin-top:.04in}
.bars{display:flex;flex-direction:column;gap:6px}.bar{display:grid;grid-template-columns:2.6in 1fr .4in;align-items:center;gap:.1in;font-size:9pt}.bar i{height:12px;background:#C99A06;border-radius:3px;display:block}.bar b{font-family:Rubik}
.cgrid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.14in}.cd{background:#fff;border:1px solid #E3DFD6;border-radius:10px;padding:.14in;font-size:8.6pt;line-height:1.38;max-height:2.55in;overflow:hidden}
.cd p{margin:.04in 0}.rs{color:#4A4741}.tg{font-size:7.5pt;text-transform:uppercase;letter-spacing:.08em;color:#C99A06;font-weight:700}.cd-t{font-size:8pt;color:#6E6A63}a{color:#B08600;font-weight:700;text-decoration:none}
table{width:100%;border-collapse:collapse;font-size:8.4pt}th{text-align:left;font-size:7.8pt;color:#6E6A63;border-bottom:2px solid #C99A06;padding:4px}td{border-bottom:1px solid #E3DFD6;padding:5px 4px;vertical-align:top}
.dois{display:grid;grid-template-columns:1fr 1fr;gap:.3in}.dois .bar{grid-template-columns:2.2in 1fr .35in}.bx{background:#fff;border:1px solid #E3DFD6;border-radius:10px;padding:.08in .2in .16in}.bx ul{margin:0;padding-left:1.1em;font-size:9.4pt;line-height:1.5}
.vazio{color:#6E6A63;font-size:11pt}.rod{position:absolute;left:.5in;right:1.3in;bottom:.16in;font-size:7.5pt;color:#6E6A63}.pag{position:absolute;right:.5in;bottom:.16in;font-size:8pt;font-weight:700;color:#C99A06}
.fim{background:#0B0B0B;color:#fff;padding:.6in .8in}.fim h2{font-size:26pt;margin:.3in 0 .25in}.fimc{font-size:9pt;line-height:1.5;color:#CFCAC0}"""
base = f"{OUT}/boletim_{AG}_{MES}"
open(base + ".html", "w").write(leve_html(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Boletim {NOME} {MES}</title><style>{CSS}{MARCA_CSS}</style></head><body>{"".join(S)}</body></html>'))
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(base)}.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(base)}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"""
r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd="/tmp")
if r.returncode == 0: leve_pdf(base + ".pdf")
print(base + ".pdf" if r.returncode == 0 else r.stderr[-400:], TOT, "páginas")
