"""Planilha Excel de votos por diretor (ANTT), a partir de data/regulacao.db (rode 05_indexar.py antes).
Uso: python3 pipeline/planilha_votos.py [saida.xlsx]   (padrão: agencias/antt/exportacoes/votos_diretores.xlsx)
Abas: Leia-me · Resumo por diretor · Diretor x Tema · Votos · Divergências e vistas · Falas em eventos · Mandatos · Vacâncias"""
import sqlite3, json, sys, re, collections, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
AGS = os.environ.get("AGENCIA", "antt")
OUT = sys.argv[1] if len(sys.argv) > 1 else f"agencias/{AGS}/exportacoes/votos_diretores.xlsx"
c = sqlite3.connect("data/regulacao.db")
def segs(ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]
def link(vid, ts=None, t=None):
    s = t if t is not None else segs(ts) if ts else 0
    return f"https://www.youtube.com/watch?v={vid}&t={max(int(s) - 5, 0)}s"
DIV = ("vencido", "vista", "revisor_diverge", "outro")
wb = Workbook(); H = Font(bold=True, color="FFFFFF"); F = PatternFill("solid", fgColor="1F4E79")
def aba(nome, cab, linhas, larg=None, links=()):
    ws = wb.create_sheet(nome[:31]); ws.append(cab)
    for cel in ws[1]: cel.font = H; cel.fill = F; cel.alignment = Alignment(wrap_text=True, vertical="top")
    for l in linhas: ws.append(list(l))
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
    for i, h in enumerate(cab, 1): ws.column_dimensions[get_column_letter(i)].width = (larg or {}).get(h, min(max(len(h) + 2, 12), 40))
    for h in links:
        col = cab.index(h) + 1
        for r in range(2, ws.max_row + 1):
            cel = ws.cell(r, col)
            if cel.value: cel.hyperlink = cel.value; cel.font = Font(color="0563C1", underline="single")
    return ws
temas_item = collections.defaultdict(list)
for iid, t in c.execute("select item_id, tema from item_temas"): temas_item[iid].append(t)
V = c.execute("""select v.diretor, r.data, r.numero, r.video_id, i.id, i.item, i.processo, i.interessado, i.assunto, i.relator, i.resultado, i.unanime,
  v.voto, v.categoria, v.justificativa, v.tom, v.ts, i.ts, v.confianca, v.trecho, v.trecho_tipo from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id order by r.data, r.numero, i.id""").fetchall()
mand = {m["diretor"]: m for m in json.load(open("data/mandatos.json"))}
# Leia-me
ws = wb.active; ws.title = "Leia-me"
for l in [f"Votos dos diretores da {AGS.upper()} em reuniões públicas de diretoria (YouTube oficial da agência)", "",
          f"Base: {len({v[3] for v in V})} reuniões, {len({v[4] for v in V})} itens, {len(V)} votos, de {min(v[1] for v in V if v[1])} a {max(v[1] for v in V if v[1])}.",
          "Fonte: legenda AUTOMÁTICA do YouTube, lida e estruturada por IA. Nomes, números e valores podem conter erros de transcrição.",
          "Categorias de voto: relator (relatou o item); acompanha (votou com o relator); revisor_acompanha / revisor_diverge; vista (pediu vista); vencido (voto vencido); outro (abstenção, impedimento, ressalva etc.); nao_captado.",
          "Quem só «acompanha» raramente fala: o minuto do link é o do item, aproximado.", "Trecho literal: frase da legenda a partir do minuto do voto (até 30 s). Tipo «fala_no_minuto» = relator/vista/voto-vista/vencido (o diretor fala ali); «janela_do_item» = quem só acompanha (o trecho é do momento do item, não necessariamente a fala dele).",
          f"Qualidade (conferência cega): ver agencias/{AGS}/qualidade/ para 2025–2026 e eventos. Mede consistência, não verdade absoluta.",
          "Itens sigilosos e reuniões sem legenda não estão aqui (ver sem_transcricao.md). Mandatos: datas estimadas quando não confirmadas (coluna confiança).",
          "Gerado por pipeline/planilha_votos.py; regenere após cada atualização da base."]:
    ws.append([l])
ws.column_dimensions["A"].width = 140; ws["A1"].font = Font(bold=True, size=14)
# Resumo
agg = collections.defaultdict(collections.Counter); per = {}
for v in V:
    a = agg[v[0]]; a["votos"] += 1; a[v[13]] += 1
    if v[11] == 0: a["itens_nao_unanimes"] += 1
    p = per.setdefault(v[0], [v[1], v[1]]); p[0] = min(p[0] or v[1], v[1] or p[0]); p[1] = max(p[1] or v[1], v[1] or p[1])
pct = lambda a, b: round(100 * a / b, 1) if b else 0
res = []
for d, a in sorted(agg.items(), key=lambda x: -x[1]["votos"]):
    m = mand.get(d, {}); div = a["vencido"] + a["vista"] + a["revisor_diverge"]
    res.append([d, m.get("cargo"), m.get("inicio"), m.get("fim"), m.get("confianca"), per[d][0], per[d][1], a["votos"], a["relator"], a["acompanha"] + a["revisor_acompanha"],
                pct(a["acompanha"] + a["revisor_acompanha"], a["votos"] - a["relator"]), a["vista"], a["vencido"], a["revisor_diverge"], a["outro"], pct(div, a["votos"]), a["itens_nao_unanimes"]])
aba("Resumo por diretor", ["Diretor", "Cargo", "Mandato início", "Mandato fim", "Confiança mandato", "1º voto", "Último voto", "Votos", "Relatorias", "Acompanha", "% acompanha (exc. relatorias)", "Vistas", "Vencido", "Revisor diverge", "Outro", "% vista+vencido+diverge", "Votos em itens não unânimes"], res, {"Diretor": 26, "Cargo": 30})
# Diretor x Tema
dt = collections.defaultdict(collections.Counter)
for v in V:
    for t in temas_item[v[4]] or ["sem_tema"]:
        k = dt[(v[0], t)]; k["votos"] += 1; k[v[13]] += 1
rows = [[d, t, k["votos"], k["relator"], k["acompanha"] + k["revisor_acompanha"], k["vista"], k["vencido"] + k["revisor_diverge"], k["outro"], pct(k["vista"] + k["vencido"] + k["revisor_diverge"], k["votos"])] for (d, t), k in sorted(dt.items())]
aba("Diretor x Tema", ["Diretor", "Tema", "Votos", "Relatorias", "Acompanha", "Vistas", "Vencido/diverge", "Outro", "% vista+vencido+diverge"], rows, {"Diretor": 26, "Tema": 26})
# Votos
cab = ["Data", "Reunião", "Item", "Diretor", "Categoria", "Voto (texto)", "Justificativa", "Tom (inferido)", "Relator", "Resultado", "Unânime", "Temas", "Processo", "Interessado", "Assunto", "Confiança", "Trecho literal (transcrição)", "Tipo do trecho", "Link (minuto)"]
lin = [[v[1], v[2], v[5], v[0], v[13], v[12], v[14], v[15], v[9], v[10], {1: "sim", 0: "não"}.get(v[11]), ", ".join(temas_item[v[4]]), v[6], v[7], v[8], v[18], v[19], v[20], link(v[3], v[16] or v[17])] for v in V]
aba("Votos", cab, lin, {"Voto (texto)": 40, "Justificativa": 50, "Assunto": 60, "Resultado": 40, "Interessado": 30, "Link (minuto)": 45, "Diretor": 22, "Trecho literal (transcrição)": 70}, links=["Link (minuto)"])
aba("Divergências e vistas", cab, [l for l, v in zip(lin, V) if v[13] in DIV or v[11] == 0], {"Voto (texto)": 40, "Justificativa": 50, "Assunto": 60, "Resultado": 40, "Link (minuto)": 45, "Diretor": 22}, links=["Link (minuto)"])
# Falas em eventos
F2 = c.execute("select e.data, f.tipo_video, e.titulo, f.diretor, f.resumo, f.texto, f.confianca, f.video_id, f.t from falas_diretores f left join eventos e on e.video_id=f.video_id order by e.data").fetchall()
aba("Falas em eventos", ["Data", "Tipo", "Evento", "Diretor", "Resumo", "Trecho literal", "Confiança", "Link (minuto)"], [list(f[:7]) + [link(f[7], t=f[8])] for f in F2], {"Evento": 50, "Resumo": 60, "Trecho literal": 60, "Link (minuto)": 45}, links=["Link (minuto)"])
# Mandatos e vacâncias
mk = ["diretor", "cargo", "situacao", "senado", "nomeacao_dou", "posse", "inicio", "fim", "inicio_tipo", "fim_tipo", "confianca", "confirmado", "fonte", "fonte_url", "verificar"]
aba("Mandatos", mk, [[m.get(k) for k in mk] for m in json.load(open("data/mandatos.json"))], {"inicio_tipo": 50, "fim_tipo": 50, "fonte": 50, "fonte_url": 50})
from datetime import date
vac = json.load(open("data/vacancias.json")); vk = ["id", "cadeira", "inicio", "fim", "dias", "preenchida_por", "interinos", "confianca", "fonte"]
for x in vac:
    try: x["dias"] = (date.fromisoformat(x["fim"]) - date.fromisoformat(x["inicio"])).days
    except Exception: x["dias"] = None
aba("Vacâncias", vk, [[x.get(k) for k in vk] for x in vac], {"cadeira": 45, "preenchida_por": 40, "interinos": 40, "fonte": 40})
os.makedirs(os.path.dirname(OUT), exist_ok=True); wb.save(OUT); print(OUT, len(V), "votos")
