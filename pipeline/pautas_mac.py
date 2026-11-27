"""(rodar NO MAC) Baixa as páginas públicas de calendário, pautas e consultas públicas das agências (a nuvem não abre gov.br)
e salva o bruto em data/<ag>/brutos/<data>/ para a nuvem extrair (calendario.json, pautas/<n>.json, consultas.json).
Uso: python3 pipeline/pautas_mac.py   (o agendamento do Mac roda isto 2x por semana e dá push)"""
import os, re, subprocess, datetime, urllib.parse, html
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
FONTES = {
    "antt": ["https://www.gov.br/antt/pt-br/assuntos/reunioes-de-diretoria", "https://www.gov.br/antt/pt-br/acesso-a-informacao/participacao-social",
             "https://participantt.antt.gov.br/"],
    "antaq": ["https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/calendario-atas-e-pautas-das-reunioes",
              "https://www.gov.br/antaq/pt-br/acesso-a-informacao/participacao-social/audiencias-e-consultas-publicas"],
    "aneel": ["https://www.gov.br/aneel/pt-br/acesso-a-informacao/participacao-social/consultas-publicas"],
}
get = lambda u: subprocess.run(["curl", "-sL", "--max-time", "60", "-A", UA, u], capture_output=True).stdout
HOJE = datetime.date.today().isoformat()
for ag, urls in FONTES.items():
    D = ("data" if ag == "antt" else f"data/{ag}") + f"/brutos/{HOJE}"; os.makedirs(D, exist_ok=True); n = 0
    for k, u in enumerate(urls):
        h = get(u); open(f"{D}/pagina_{k}.html", "wb").write(h); n += 1
        t = h.decode("utf-8", "ignore")
        for href in re.findall(r'href="([^"]+)"', t):
            full = urllib.parse.urljoin(u, html.unescape(href))
            if re.search(r"pauta|calend|consulta|audi[eê]ncia", full, re.I) and re.search(r"\.pdf|/view|@@download", full, re.I) and n < 40:
                b = get(full); ext = ".pdf" if b[:4] == b"%PDF" else ".html"
                open(f"{D}/{re.sub(r'[^\\w.-]', '_', full.split('/')[-1] or 'doc')[:80]}_{n:02d}{ext}", "wb").write(b); n += 1
    print(ag, n, "arquivos em", D)
print("pronto: git add data && git commit -m 'pautas e consultas (bruto)' && git push")
