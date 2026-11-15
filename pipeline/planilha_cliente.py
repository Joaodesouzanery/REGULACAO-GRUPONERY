"""Planilha do cliente (xlsx): todas as decisões que citam a empresa (2018+) com voto de cada diretor, relator, desfecho e link.
Uso: python3 pipeline/planilha_cliente.py clientes/<x>/<pasta> [saida.xlsx]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, mapa_tema
from desfecho import desfecho_item
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
P = sys.argv[1].rstrip("/"); EMP = json.load(open(f"{P}/empresa.json")); AG = EMP.get("agencias", ["antaq"])[0]
OUT = sys.argv[2] if len(sys.argv) > 2 else f"{P}/votos_{AG}.xlsx"
MAN = json.load(open(f"{P}/desfechos_manuais.json")) if os.path.exists(f"{P}/desfechos_manuais.json") else {}
c = previsao.conn(AG); pr = previsao.calcular(AG, EMP["aliases"])
its = [i for i in pr["itens"] if i["data"] >= "2018-01-01"]
dirs = sorted({d for i in its for (d,) in c.execute("select diretor from votos where item_id=?", (i["id"],))})
wb = Workbook(); ws = wb.active; ws.title = "Decisões"
cab = ["Data", "Reunião", "Item", "Processo (legenda)", "Interessado", "Assunto", "Resultado", "Relator", "Desfecho p/ empresa", "Link (minuto)"] + dirs
ws.append(cab)
for i in its:
    v = {d: cat for d, cat in c.execute("select diretor, categoria from votos where item_id=?", (i["id"],))}
    dsf = MAN.get(str(i["id"]), {}).get("desfecho") or desfecho_item(c, i["id"])
    ws.append([i["data"], f"{i['numero']}ª", i["item"], i["processo"], i["interessado"], i["assunto"], i["resultado"], i["relator"], dsf, mapa_tema.link(i["video_id"], i["ts"])] + [v.get(d, "") for d in dirs])
for cl in ws[1]: cl.font = Font(bold=True, color="FFFFFF"); cl.fill = PatternFill("solid", fgColor="0B0B0B"); cl.alignment = Alignment(wrap_text=True)
for col, w in zip("ABCDEFGHIJ", (11, 9, 8, 22, 30, 60, 40, 18, 14, 40)): ws.column_dimensions[col].width = w
ws.freeze_panes = "A2"
ws2 = wb.create_sheet("Por diretor"); ws2.append(["Diretor", "Acompanha o relator (temas da empresa, 3 anos)", "n votos"])
for d, (p, n) in pr["por_diretor"].items(): ws2.append([d, round(p, 3), n])
ws3 = wb.create_sheet("Leia-me")
for l in ["Fonte: vídeos oficiais das reuniões de diretoria (legenda automática; nomes e números podem conter erro).", "Categorias de voto: relator, acompanha, vencido, revisor_diverge, vista, outro, nao_captado.",
          "Desfecho: classificação automática pela decisão; casos ambíguos conferidos à mão.", "Previsões são estimativas e não substituem a publicação oficial."]: ws3.append([l])
wb.save(OUT); print(OUT, len(its), "decisões")
