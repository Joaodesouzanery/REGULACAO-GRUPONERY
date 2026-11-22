"""Completa contatos INSTITUCIONAIS dos prospects abrindo o site oficial de cada empresa (rodar NO MAC: a nuvem é bloqueada).
LGPD: guarda só e-mail genérico do domínio da empresa (contato@, ri@, imprensa@, ouvidoria@...), telefone publicado e link da página no LinkedIn.
Uso: cd ~/REGULACAO-GRUPONERY && git pull && python3 pipeline/contatos_mac.py && python3 pipeline/contatos_xlsx.py && git add documentos/comercial && git commit -m "contatos" && git push"""
import csv, re, glob, subprocess, urllib.parse, datetime, time
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
CAMINHOS = ["", "contato", "fale-conosco", "faleconosco", "contatos", "ri", "investidores", "imprensa", "sala-de-imprensa", "ouvidoria"]
GENERICO = re.compile(r"^(contato|contatos|faleconosco|fale|atendimento|sac|ri|investidores|relacoes|imprensa|comunicacao|ouvidoria|institucional|juridico|regulatorio|info|comercial|secretaria|recepcao|contact|ir|press)", re.I)
get = lambda u: subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, u], capture_output=True).stdout.decode("utf-8", "ignore")
for arq in sorted(glob.glob("documentos/comercial/contatos_*.csv")):
    rows = list(csv.DictReader(open(arq, encoding="utf-8"), delimiter=";")); campos = list(rows[0].keys()) if rows else []
    for r in rows:
        site = (r.get("site") or "").strip()
        if not site or (r.get("email_institucional") and r.get("telefone_institucional")): continue
        dom = urllib.parse.urlparse(site if "//" in site else "https://" + site).netloc.replace("www.", "")
        emails, tels, lk = set(), set(), ""
        for c in CAMINHOS:
            h = get(urllib.parse.urljoin(site.rstrip("/") + "/", c))
            if len(h) < 500: continue
            for e in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", h):
                if dom.split(".")[0] in e.split("@")[1] and GENERICO.match(e.split("@")[0]): emails.add(e.lower())
            tels |= set(re.findall(r"(?:\+55\s?)?\(?\d{2}\)?\s?\d{4,5}[-\s]\d{4}|0800[\s-]?\d{3}[\s-]?\d{4}", h))
            lk = lk or next(iter(re.findall(r"https?://(?:www\.)?linkedin\.com/company/[\w-]+", h)), "")
            time.sleep(1)
        if emails and not r.get("email_institucional"): r["email_institucional"] = ", ".join(sorted(emails)[:3])
        if tels and not r.get("telefone_institucional"): r["telefone_institucional"] = ", ".join(sorted(tels)[:2])
        if lk and not r.get("linkedin_pagina"): r["linkedin_pagina"] = lk
        if emails or tels or lk:
            r["conferido"] = f"site aberto {datetime.date.today()}"; r["fonte"] = (r.get("fonte") or "") + f" | {site}"
        print(f"{r.get('empresa') or r.get('nome')}: {len(emails)} e-mail, {len(tels)} tel, {'LinkedIn' if lk else '-'}")
    with open(arq, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";"); w.writeheader(); w.writerows(rows)
print("pronto; agora rode python3 pipeline/contatos_xlsx.py")
