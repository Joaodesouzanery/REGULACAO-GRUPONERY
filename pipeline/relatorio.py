"""Relatório da consultoria (.docx) a partir de uma pasta de semana do cliente.
Uso: python3 pipeline/relatorio.py clientes/<cliente>/<AAAA-semNN> [--titulo "..."]
Entrada: perguntas.md (linhas «- pergunta») e respostas/NN.md (ficha em Markdown, gerada com consulta.py ficha e revisada).
Saída: relatorio.docx na mesma pasta (capa, sumário executivo, uma seção por pergunta, anexo de metodologia)."""
import sys, os, re, glob, datetime
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
P = sys.argv[1].rstrip("/"); tit = sys.argv[sys.argv.index("--titulo") + 1] if "--titulo" in sys.argv else None
cliente, semana = P.split("/")[-2], P.split("/")[-1]
perg = [l[2:].strip() for l in open(f"{P}/perguntas.md") if l.startswith("- ")]
resp = sorted(glob.glob(f"{P}/respostas/*.md"))
doc = Document(); st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
def link(par, texto, url):
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), par.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True))
    r = OxmlElement("w:r"); rp = OxmlElement("w:rPr"); c = OxmlElement("w:color"); c.set(qn("w:val"), "0563C1"); u = OxmlElement("w:u"); u.set(qn("w:val"), "single")
    rp.append(c); rp.append(u); r.append(rp); t = OxmlElement("w:t"); t.text = texto; t.set(qn("xml:space"), "preserve"); r.append(t); h.append(r); par._p.append(h)
def md_par(par, s):
    """Markdown simples: **negrito**, *itálico*, [texto](url)."""
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\]\([^)]+\))", s):
        if not tok: continue
        if tok.startswith("**"): par.add_run(tok[2:-2]).bold = True
        elif tok.startswith("[") and "](" in tok: m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok); link(par, m.group(1), m.group(2))
        elif tok.startswith("*") and len(tok) > 2: par.add_run(tok[1:-1]).italic = True
        else: par.add_run(tok)
def bloco(md):
    for l in md.splitlines():
        if not l.strip(): continue
        if l.startswith("# "): continue
        if l.startswith("## "): doc.add_heading(l[3:], level=3); continue
        m = re.match(r"(\s*)- (.*)", l)
        if m: md_par(doc.add_paragraph(style="List Bullet 2" if m.group(1) else "List Bullet"), m.group(2))
        else: md_par(doc.add_paragraph(), l)
doc.add_heading(tit or "Relatório de inteligência regulatória", 0)
doc.add_paragraph(f"Cliente: {cliente} · Período: {semana} · Emitido em {datetime.date.today():%d/%m/%Y}")
doc.add_paragraph("Confidencial. Baseado em reuniões públicas transmitidas (YouTube oficial das agências), legendas automáticas lidas e estruturadas, com evidência literal e link no minuto exato.").runs[0].italic = True
doc.add_heading("Sumário executivo", 1)
for i, (q, f) in enumerate(zip(perg, resp + [None] * len(perg)), 1):
    linha = ""
    if f:
        m = re.search(r"\*\*1\. Resposta curta:\*\*\s*(.+)", open(f).read()); linha = m.group(1) if m else ""
    md_par(doc.add_paragraph(style="List Number"), f"**{q}** — {linha or 'ver seção'}")
for i, q in enumerate(perg, 1):
    doc.add_page_break(); doc.add_heading(f"{i}. {q}", 1)
    f = resp[i - 1] if i <= len(resp) else None
    bloco(open(f).read()) if f else doc.add_paragraph("(resposta pendente)")
doc.add_page_break(); doc.add_heading("Anexo — Metodologia, confiabilidade e cobertura", 1)
for l in ["Fonte primária: vídeos das reuniões públicas de diretoria e de eventos (audiências, participativas) no canal oficial da agência; legenda automática do YouTube.",
          "Cada item de pauta é estruturado (relator, resultado, voto de cada diretor, justificativa) e cada voto traz o trecho literal da transcrição e o link no minuto.",
          "Confiabilidade: conferência cega por amostra — ≈ 94–95% de concordância no voto por diretor (2019–2026), 93–100% em relator e resultado; trechos de eventos 100% localizados.",
          "Limites: erros de legenda em nomes e valores; quem apenas acompanha o relator raramente fala (minuto aproximado); itens sigilosos e reuniões sem legenda não constam; o voto escrito completo fica no processo (SEI).",
          "Mandatos: datas de Senado/DOU de fontes públicas; posses ainda não confirmadas no DOU são marcadas como estimadas."]:
    doc.add_paragraph(l, style="List Bullet")
out = f"{P}/relatorio.docx"; doc.save(out); print(out, len(perg), "perguntas,", len(resp), "respostas")
