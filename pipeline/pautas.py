"""Pautas futuras e calendário (Proposta 2, bloco 4 · Agenda). Só fontes públicas; nada de contornar bloqueio.
Uso: python3 pipeline/pautas.py <ag> [--proximas 3]
- Calendário oficial: data/<ag>/calendario.json  [{"reuniao": "625", "data": "2026-12-10", "formato": "telepresencial", "fonte": url}]
  (preenchido à mão a partir do PDF oficial — ex.: ANTAQ, Acórdão 351/2026).
- Pautas: tenta os padrões de URL de data/<ag>/config_agencia.json → "pautas_url" (lista com {n}) para as próximas reuniões;
  baixa o PDF em data/<ag>/pautas/<n>.pdf, extrai itens (nº, processo, interessado, assunto, relator) → <n>.json.
  Sem pauta publicada → registra «a confirmar» (o alerta usa então o calendário e os itens retirados/vista da última reunião)."""
import sys, os, re, json, subprocess, datetime, sqlite3

AG = sys.argv[1].lower()
D = "data" if AG == "antt" else f"data/{AG}"
N = int(sys.argv[sys.argv.index("--proximas") + 1]) if "--proximas" in sys.argv else 3
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
os.makedirs(f"{D}/pautas", exist_ok=True)
cfg = ld(f"{D}/config_agencia.json", {})
cal = ld(f"{D}/calendario.json", [])
db = sqlite3.connect(f"{D}/regulacao.db")
nums = [int(m) for (x,) in db.execute("select numero from reunioes") for m in re.findall(r"^(\d{3,4})", str(x))]
ult = max(nums) if nums else 0
hoje = datetime.date.today().isoformat()
futuras = [c for c in cal if c["data"] >= hoje][:N] or [{"reuniao": str(ult + k), "data": None, "formato": None, "fonte": None} for k in range(1, N + 1)]


def extrair(txt):
    """Formato ANTAQ: «RELATOR: DIRETOR X:» seguido de «N. 50300.xxxxxx/aaaa-dd», «Tipo:», «Interessados:», «Contextualização:»."""
    its, cur, rel, campo = [], None, None, None
    for l in txt.splitlines():
        s_ = l.strip().replace("\u200b", "")
        if not s_ or "Pauta de Reunião de Diretoria" in s_: continue
        m = re.match(r"RELATOR[A]?\s*:\s*(?:DIRETOR[A]?\s*(?:SUBSTITUT[OA]\s*)?(?:-?GERAL\s*)?)?(.+?):?$", s_, re.I)
        if m: rel = m.group(1).strip(" :").title(); continue
        m = re.match(r"(\d{1,3})\.\s+(\d{5}\.\d{6}/\d{4}-\d{2})", s_)
        if m:
            cur = {"item": m.group(1), "processo": m.group(2), "relator": rel, "tipo": "", "interessado": "", "assunto": ""}; its.append(cur); campo = None; continue
        if not cur: continue
        for k, chave in (("Tipo:", "tipo"), ("Interessad", "interessado"), ("Contextualiza", "assunto")):
            if s_.startswith(k): campo = chave; s_ = s_.split(":", 1)[1].strip() if ":" in s_ else ""; break
        if re.match(r"^[A-ZÁÉÍÓÚÂÊÔÃÕÇ ]{6,}:?$", s_): campo = None; continue
        if campo: cur[campo] = (cur[campo] + " " + s_).strip()
    return its


out = []
for f in futuras:
    n = re.sub(r"\D", "", str(f["reuniao"]))
    reg = {"reuniao": f["reuniao"], "data": f.get("data"), "formato": f.get("formato"), "calendario_fonte": f.get("fonte"), "pauta": "a confirmar", "itens": []}
    for pad in cfg.get("pautas_url", []):
        url = pad.format(n=n)
        pdf = f"{D}/pautas/{n}.pdf"
        r = subprocess.run(["curl", "-sSL", "-o", pdf, "-w", "%{http_code}", url], capture_output=True, text=True)
        if r.stdout.strip() == "200" and open(pdf, "rb").read(4) == b"%PDF":
            txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
            reg.update({"pauta": url, "itens": extrair(txt), "baixada_em": hoje}); break
        if os.path.exists(pdf) and open(pdf, "rb").read(4) != b"%PDF": os.remove(pdf)
    json.dump(reg, open(f"{D}/pautas/{n}.json", "w"), ensure_ascii=False, indent=1)
    out.append(reg)
    print(f"{AG.upper()} {f['reuniao']}ª · {f.get('data') or 'data a confirmar'} · {f.get('formato') or ''} · pauta: {'publicada, ' + str(len(reg['itens'])) + ' itens' if reg['itens'] else reg['pauta']}")
