"""Baixa o texto de cada ato do DOU citado numa tabela de mandatos (links extraídos do PDF), para a conferência auditável.
Roda NO MAC (o in.gov.br não abre da nuvem). Uso:
  cd ~/REGULACAO-GRUPONERY && git pull && python3 pipeline/conferir_dou.py && git add data/auditoria_mandatos && git commit -m "atos do DOU para auditoria" && git push
Entrada: data/auditoria_mandatos_links.json (página, posição, url). Saída: data/auditoria_mandatos/dou/<id>.txt + indice.json (url, status, data da consulta)."""
import json, os, re, time, html, subprocess, datetime
L = json.load(open("data/auditoria_mandatos_links.json"))
os.makedirs("data/auditoria_mandatos/dou", exist_ok=True)
IDX = "data/auditoria_mandatos/dou/indice.json"
idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
for k, u in enumerate(dict.fromkeys(x["url"] for x in L), 1):
    aid = re.sub(r"[^\w-]", "_", u.rstrip("/").split("/")[-1])[:120]
    dest = f"data/auditoria_mandatos/dou/{aid}.txt"
    if os.path.exists(dest) and os.path.getsize(dest) > 200: continue
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "--retry", "3", "-A", UA, u], capture_output=True, text=True)
    h = r.stdout
    m = re.search(r'<div class="texto-dou">(.*?)</div>\s*</div>', h, re.S) or re.search(r'class="texto-dou"[^>]*>(.*?)<div class="(?:informacao|rodape)', h, re.S)
    corpo = m.group(1) if m else ""
    meta = " | ".join(html.unescape(x) for x in re.findall(r'class="(?:publicado-dou-data|secao-dou|edicao-dou-data|orgao-dou-data)"[^>]*>(.*?)<', h))
    txt = html.unescape(re.sub(r"<[^>]+>", " ", corpo)); txt = re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", txt)).strip()
    ok = bool(txt)
    open(dest, "w").write(f"URL: {u}\nCONSULTA: {datetime.datetime.now():%Y-%m-%d %H:%M}\nPUBLICACAO: {meta}\n\n{txt}\n")
    idx[u] = {"arquivo": dest, "status": "ok" if ok else f"sem texto (http? {len(h)} bytes)", "consulta": datetime.date.today().isoformat()}
    print(f"[{k}] {'ok ' if ok else 'ERRO'} {aid}")
    json.dump(idx, open(IDX, "w"), ensure_ascii=False, indent=1)
    time.sleep(2)
print("pronto:", sum(1 for v in idx.values() if v["status"] == "ok"), "de", len(idx), "atos com texto")
