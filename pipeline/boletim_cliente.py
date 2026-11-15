"""Boletim mensal DO CLIENTE (peça 2 do pacote): capa + alerta pré-pauta + perguntas do mês + o mês na agência + diretoria + cobertura.
Junta PDFs já gerados (sem refazer análise):
  - <pasta>/alerta_<ag>_<reuniao>.pdf          (pipeline/alerta_pauta.py)
  - <pasta>/perguntas/relatorio_v2.pdf          (pipeline/relatorio_v2.py; usa só as páginas das perguntas)
  - agencias/<ag>/boletins/boletim_<ag>_<AAAA-MM>.pdf  (pipeline/boletim.py; números, decisões, divergências, diretoria, cobertura)
Uso: python3 pipeline/boletim_cliente.py clientes/<x>/<pasta> AAAA-MM   → <pasta>/boletim_cliente_<AAAA-MM>.pdf"""
import sys, os, re, json, glob, base64, datetime, subprocess, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pikepdf
from pdf_leve import leve_html, leve_pdf
from marca import parceria_html, MARCA_CSS

if len(sys.argv) < 3 or not re.match(r"^\d{4}-\d{2}$", sys.argv[2]): sys.exit("Uso: python3 pipeline/boletim_cliente.py clientes/<x>/<pasta> 2026-11   (mês no formato AAAA-MM; gere no chat — a pasta clientes/ não vai para o Mac)")
P, MES = sys.argv[1].rstrip("/"), sys.argv[2]
if not os.path.exists(f"{P}/empresa.json"): sys.exit(f"Pasta do cliente não encontrada: {P}. Os relatórios de cliente são gerados no chat (clientes/ fica fora do git); no Mac rode só a coleta: caffeinate -i bash pipeline/coletar_todas.sh")
EMP = json.load(open(f"{P}/empresa.json")); AG = EMP.get("agencias", ["antaq"])[0]
NOME = AG.upper(); E = html.escape
MESES = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()
ano, mm = map(int, MES.split("-"))
b64 = lambda p: ("data:image/" + p.rsplit(".", 1)[-1].replace("jpg", "jpeg") + ";base64," + base64.b64encode(open(p, "rb").read()).decode()) if p and os.path.exists(p) else ""
alerta = sorted(glob.glob(f"{P}/alerta_{AG}_*.pdf"), key=os.path.getmtime)
perg = f"{P}/perguntas/relatorio_v2.pdf"
ag_mes = (datetime.date(ano, mm, 1) - datetime.timedelta(days=1)).strftime("%Y-%m")  # o mês fechado anterior
bol = f"agencias/{AG}/boletins/boletim_{AG}_{ag_mes}.pdf"
if not os.path.exists(bol): subprocess.run(["python3", "pipeline/boletim.py", AG, ag_mes])
FOTO, CLI, LOGO = b64(EMP.get("foto_capa")), b64(EMP.get("logo")), b64("docs/marca/circle/logo_circle_branco.png")
nperg = len([l for l in open(f"{P}/perguntas/perguntas.md") if l.startswith("- ")]) if os.path.exists(f"{P}/perguntas/perguntas.md") else 0
sumario = [("O que acompanhar na próxima reunião", "alerta pré-pauta"), (f"Suas perguntas do mês ({nperg})", "resposta com evidência e link no minuto"),
           (f"O mês na {NOME} ({MESES[int(ag_mes[5:]) - 1]})", "números, decisões por tema, divergências"), ("Diretoria", "mudanças, vagas e mandatos"), ("Cobertura", "o que a base cobre e os limites")]
import design as dz
KIT = dz.kit(EMP.get("setor") or dz.SETOR_AG.get(AG, "portos")); FT = EMP.get("foto_capa") or KIT["capa"]
cp = f"{P}/.capa_boletim"
dz.documento([dz.capa(FT, EMP.get("foco", "50% 55%"), f"Boletim mensal · {NOME}", f'{EMP["nome"].split("(")[0].strip()}', f"{MESES[mm - 1]} de {ano}",
                      "O que vem na diretoria, o que ela decidiu e as respostas às suas perguntas. Fontes públicas; previsões são estimativas.",
                      [(nperg, "perguntas respondidas no mês"), (len(alerta) and "sim" or "—", "alerta pré-pauta"), (MESES[int(ag_mes[5:]) - 1], "mês fechado na agência"), (f"{datetime.date.today():%d/%m}", "emissão")], EMP.get("logo")),
              dz.sumario(sumario, KIT["divisores"][0])], "capa", cp)
fp = f"{P}/.fim_boletim"
dz.documento([dz.fim("Fontes públicas: vídeos oficiais das reuniões, pautas e calendário da agência, Senado e DOU. Legenda automática pode errar nomes e números. Previsões e alertas são estimativas — não substituem a publicação oficial nem orientação jurídica.",
                     EMP.get("contato", "Circle Consultoria em parceria com Grupo Nery"), KIT["divisores"][0])], "fim", fp)
out = pikepdf.new()
def add(path, idx=None):
    if not path or not os.path.exists(path): print("aviso: falta", path); return 0
    src = pikepdf.open(path); pgs = list(src.pages)
    sel = [pgs[i] for i in (idx if idx is not None else range(len(pgs))) if -len(pgs) <= i < len(pgs)]
    out.pages.extend(sel); return len(sel)
add(cp + ".pdf")
add(alerta[-1] if alerta else None)
if os.path.exists(perg):
    # relatorio_v2 com diretoria: capa, sumário, quadro da diretoria, depois 1 página por pergunta
    add(perg, list(range(3, 3 + nperg)))
add(bol, [1, 2, 3, 5, -1])  # números · decisões por tema · divergências · diretoria · cobertura
add(fp + ".pdf")
dst = f"{P}/boletim_cliente_{MES}.pdf"; out.save(dst); leve_pdf(dst)
for f in (cp + ".html", cp + ".pdf", fp + ".html", fp + ".pdf"):
    if os.path.exists(f): os.remove(f)
print(dst, len(out.pages), "páginas", os.path.getsize(dst) // 1024, "KB")
