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

P, MES = sys.argv[1].rstrip("/"), sys.argv[2]
EMP = json.load(open(f"{P}/empresa.json")); AG = EMP.get("agencias", ["antaq"])[0]
NOME = {"antt": "ANTT", "anm": "ANM", "antaq": "ANTAQ"}[AG]; E = html.escape
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
capa = f'''<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:13.333in 7.5in;margin:0}}body{{margin:0;font-family:Inter,system-ui,sans-serif}}
.pg{{width:13.333in;height:7.5in;display:grid;grid-template-columns:4.8in 1fr;background:#0B0B0B;color:#fff}}.f{{background:url({FOTO}) {EMP.get("foco", "50% 55%")}/cover}}.c{{padding:.45in;display:flex;flex-direction:column}}
.lc{{height:.36in;align-self:flex-start}}.eb{{margin-top:.3in;font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:#E2B93B}}.cli{{background:#fff;border-radius:10px;padding:8px 12px;align-self:flex-start;margin-top:.14in}}.cli img{{height:.42in;display:block}}
h1{{font-size:28pt;margin:.14in 0 .04in}}.s{{color:#CFCAC0;font-size:11pt}}ol{{margin:auto 0 0;padding-left:1.1em;font-size:10pt;line-height:1.7}}ol span{{color:#9A958C;font-size:8.5pt}}.m{{font-size:7.5pt;color:#7A766F;margin-top:.15in}}{MARCA_CSS}</style></head>
<body><section class="pg"><div class="c">{f'<img class="lc" src="{LOGO}">' if LOGO else ''}{parceria_html()}<div class="eb">Boletim mensal · {NOME}</div>{f'<div class="cli"><img src="{CLI}"></div>' if CLI else ''}
<h1>{E(EMP["nome"].split("(")[0].strip())} · {MESES[mm - 1]} de {ano}</h1><div class="s">O que vem na diretoria, o que ela decidiu e as respostas às suas perguntas.</div>
<ol>{"".join(f"<li>{E(a)} <span>— {E(b)}</span></li>" for a, b in sumario)}</ol><div class="m">Emitido em {datetime.date.today():%d/%m/%Y} · fontes públicas · previsões são estimativas</div></div><div class="f"></div></section></body></html>'''
cp = f"{P}/.capa_boletim.html"; open(cp, "w").write(leve_html(capa))
js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(cp)}',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(cp)}.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"
subprocess.run(["node", "-e", js], cwd="/tmp", check=True)
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
dst = f"{P}/boletim_cliente_{MES}.pdf"; out.save(dst); leve_pdf(dst)
for f in (cp, cp + ".pdf"): os.remove(f)
print(dst, len(out.pages), "páginas", os.path.getsize(dst) // 1024, "KB")
