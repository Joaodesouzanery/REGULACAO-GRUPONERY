"""Baixa do DOU (Seção 2, oficial, via INLABS da Imprensa Nacional) os atos que citam cada diretor — rodar NO MAC.
INLABS = serviço oficial e gratuito de download do DOU em XML (https://inlabs.in.gov.br). Faça o cadastro uma vez no site.
Uso:
  export INLABS_EMAIL='seu@email' INLABS_SENHA='sua_senha'      # nunca grave a senha no repositório
  python3 pipeline/baixar_dou_mac.py                 # ANTT: todas as pessoas/períodos de pipeline/dou_buscas.json
  python3 pipeline/baixar_dou_mac.py --agencia anm   # ANM
  python3 pipeline/baixar_dou_mac.py --pessoa "Lucas Asfor Rocha Lima"   # só uma pessoa
Saída: data/fontes_dou/<agencia>/<data>_<sobrenome>_<id>.txt (texto do ato) + .xml, e indice.jsonl. Depois: git add data/fontes_dou && git commit -m "DOU" && git push.
Só dias úteis; cache dos ZIPs em ~/.cache/dou_inlabs (cada dia é baixado uma vez)."""
import os, sys, json, re, zipfile, io, datetime, html, unicodedata, urllib.request, urllib.parse, http.cookiejar, time
AG = sys.argv[sys.argv.index("--agencia") + 1] if "--agencia" in sys.argv else "antt"
SO = sys.argv[sys.argv.index("--pessoa") + 1] if "--pessoa" in sys.argv else None
EMAIL, SENHA = os.environ.get("INLABS_EMAIL"), os.environ.get("INLABS_SENHA")
if not (EMAIL and SENHA): sys.exit("Defina INLABS_EMAIL e INLABS_SENHA (cadastro gratuito em https://inlabs.in.gov.br).")
BUSCAS = json.load(open("pipeline/dou_buscas.json"))[AG]
CACHE = os.path.expanduser("~/.cache/dou_inlabs"); os.makedirs(CACHE, exist_ok=True)
OUT = f"data/fontes_dou/{AG}"; os.makedirs(OUT, exist_ok=True)
cj = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.open("https://inlabs.in.gov.br/logar.php", urllib.parse.urlencode({"email": EMAIL, "password": SENHA}).encode(), timeout=60)
if not any(c.name == "inlabs_session_cookie" for c in cj): sys.exit("Login no INLABS falhou: confira e-mail/senha.")
norm = lambda s: re.sub(r"\s+", " ", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())
def zip_do_dia(d):
    f = f"{CACHE}/{d}-DO2.zip"
    if not os.path.exists(f):
        try:
            r = op.open(f"https://inlabs.in.gov.br/index.php?p={d}&dl={d}-DO2.zip", timeout=180); b = r.read()
            if not b.startswith(b"PK"): return None  # sem edição nesse dia
            open(f, "wb").write(b); time.sleep(1)
        except Exception as e: print("  falha", d, e); return None
    return zipfile.ZipFile(f)
idx = open(f"{OUT}/indice.jsonl", "a"); n = 0
for b in BUSCAS:
    if SO and norm(SO) not in norm(b["nome"]): continue
    alvo = norm(b["nome"]); d0, d1 = (datetime.date.fromisoformat(x) for x in b["periodo"])
    print(f"== {b['nome']} ({d0} a {d1})")
    d = d0
    while d <= d1:
        if d.weekday() < 5 and (z := zip_do_dia(d.isoformat())):
            for nm in z.namelist():
                if not nm.endswith(".xml"): continue
                x = z.read(nm).decode("utf-8", "ignore"); txt = html.unescape(re.sub(r"<[^>]+>", " ", x))
                if alvo in norm(txt) and re.search(r"ag[eê]ncia nacional de (transportes terrestres|minera)", norm(txt)):
                    base = f"{OUT}/{d}_{alvo.split()[-1]}_{os.path.basename(nm)[:-4]}"
                    open(base + ".xml", "w").write(x); open(base + ".txt", "w").write(re.sub(r"\s+", " ", txt).strip())
                    tipo = next((t for t in ("nomear", "nomeia", "exonerar", "exonera", "posse", "renuncia", "designar", "convoca", "dispensar", "reconduzir") if t in norm(txt)), "outro")
                    idx.write(json.dumps({"pessoa": b["nome"], "data": str(d), "arquivo": base + ".txt", "tipo_provavel": tipo}, ensure_ascii=False) + "\n"); n += 1
                    print("   achado:", d, tipo, base + ".txt")
        d += datetime.timedelta(days=1)
print(n, "atos salvos em", OUT, "— agora: git add data/fontes_dou && git commit -m 'DOU' && git push")
