"""Baixa as atas e pautas das reuniões públicas da diretoria da ANEEL (www2.aneel.gov.br não abre da nuvem: rodar NO MAC).
As atas trazem o voto de cada diretor e corrigem a atribuição de quem só disse «acompanho» no vídeo (meta: votos ≥ 94% na conferência cega).
Uso (Mac):  cd ~/REGULACAO-GRUPONERY && git pull && python3 pipeline/baixar_atas_aneel.py && git add data/aneel/atas && git commit -m "atas ANEEL" && git push
Saída: data/aneel/atas/listagem*.html (páginas da lista), data/aneel/atas/pdf/*.pdf e data/aneel/atas/indice_bruto.json (url, título, arquivo, status)."""
"""NOTA 17/11/2026: www2.aneel.gov.br responde com desafio anti-robô (Cloudflare «Just a moment...»). Não contornamos esse tipo de proteção.
Alternativas: baixar à mão pelo navegador uma amostra de atas (para a conferência) e salvar em data/aneel/atas/pdf/; ou usar as regras de proclamação do prompt da ANEEL."""
import os, re, json, time, html, subprocess, urllib.parse, datetime
BASE = "https://www2.aneel.gov.br/aplicacoes_liferay/ata_diretoria/ata.cfm"
OUT = "data/aneel/atas"; os.makedirs(f"{OUT}/pdf", exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
IDX = f"{OUT}/indice_bruto.json"; idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
get = lambda u: subprocess.run(["curl", "-sL", "--max-time", "60", "--retry", "3", "-A", UA, u], capture_output=True).stdout
ANOS = range(2018, datetime.date.today().year + 1)
paginas = [BASE] + [f"{BASE}?ano={a}" for a in ANOS] + [f"{BASE}?Ano={a}" for a in ANOS]
links = {}
for k, u in enumerate(paginas):
    h = get(u).decode("latin-1", "ignore")
    if len(h) < 500: continue
    if "Just a moment" in h[:3000] or "challenges.cloudflare.com" in h:
        print("Página protegida por desafio anti-robô (Cloudflare). Não contornamos: baixe as atas à mão pelo navegador e salve em data/aneel/atas/pdf/."); break
    open(f"{OUT}/listagem_{k:02d}.html", "w").write(h)
    for href, txt in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', h, re.S | re.I):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", txt))).strip()
        full = urllib.parse.urljoin(u, href)
        if re.search(r"\.pdf|ata|pauta|download|arquivo", href + " " + t, re.I) and not re.search(r"facebook|twitter|whatsapp|linkedin|mailto", full):
            links[full] = t[:200]
    time.sleep(2)
print(len(links), "links candidatos")
for k, (u, t) in enumerate(links.items(), 1):
    if u in idx and idx[u].get("status") == "ok": continue
    b = get(u)
    ext = ".pdf" if b[:4] == b"%PDF" else ".html"
    nome = re.sub(r"[^\w.-]", "_", (t or u.split("/")[-1]))[:90] + f"_{k:04d}{ext}"
    if ext == ".pdf" or len(b) > 2000:
        open(f"{OUT}/pdf/{nome}" if ext == ".pdf" else f"{OUT}/{nome}", "wb").write(b)
    idx[u] = {"titulo": t, "arquivo": nome, "status": "ok" if ext == ".pdf" else f"html {len(b)} bytes", "consulta": datetime.date.today().isoformat()}
    print(f"[{k}/{len(links)}] {'PDF' if ext == '.pdf' else 'html'} {t[:70]}")
    json.dump(idx, open(IDX, "w"), ensure_ascii=False, indent=1)
    time.sleep(2)
print("pronto:", sum(1 for v in idx.values() if v["status"] == "ok"), "PDFs; envie com git add/commit/push")
