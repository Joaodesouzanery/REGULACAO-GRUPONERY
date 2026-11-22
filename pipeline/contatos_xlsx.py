"""Junta documentos/comercial/contatos_*.csv numa planilha com uma aba por bloco: documentos/comercial/prospects_contatos.xlsx."""
import csv, glob
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
wb = Workbook(); wb.remove(wb.active)
NOMES = {"rodovias_aviacao": "Rodovias e aviação", "portos_energia_mineracao": "Portos, energia, mineração", "escritorios_associacoes": "Escritórios e associações"}
for arq in sorted(glob.glob("documentos/comercial/contatos_*.csv")):
    chave = arq.split("contatos_")[1][:-4]; rows = list(csv.reader(open(arq, encoding="utf-8"), delimiter=";"))
    ws = wb.create_sheet(NOMES.get(chave, chave)[:31])
    for r in rows: ws.append(r)
    for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="003B4C")
    for col in ws.columns: ws.column_dimensions[col[0].column_letter].width = min(45, max(12, max(len(str(c.value or "")) for c in col[:50])))
    ws.freeze_panes = "B2"
ws = wb.create_sheet("Como usar", 0)
for l in ["Só contatos institucionais públicos (LGPD): nada de e-mail ou celular pessoal.", "Coluna conferido: 'site aberto <data>' = tirado do site oficial; 'conferir' = falta abrir.",
          "canal_circle = sim: empresa conhecida do parceiro; combinar com ele antes do contato direto.", "Cadência sugerida: documentos/comercial/emails.md (3 e-mails) + página da empresa no LinkedIn."]:
    ws.append([l])
ws.column_dimensions["A"].width = 110
wb.save("documentos/comercial/prospects_contatos.xlsx"); print("documentos/comercial/prospects_contatos.xlsx")
