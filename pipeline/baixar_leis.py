"""Baixa do Planalto o texto compilado das leis e converte em docs/leis/<id>.md.
O Planalto bloqueia IPs de nuvem (redireciona para gov.br/planalto): RODE NO MAC.
Uso: python3 pipeline/baixar_leis.py [id ...]   (sem argumentos = todas)
Depois: python3 pipeline/indexar_leis.py"""
import datetime, html, os, re, sys, urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = "https://www.planalto.gov.br/ccivil_03/"
LEIS = {
    "lei-13848-2019": ("Lei Geral das Agências Reguladoras", "Lei nº 13.848, de 25 de junho de 2019", P + "_ato2019-2022/2019/lei/l13848.htm"),
    "lei-9784-1999": ("Lei do Processo Administrativo Federal", "Lei nº 9.784, de 29 de janeiro de 1999", P + "leis/l9784.htm"),
    "dl-4657-1942-lindb": ("Lei de Introdução às Normas do Direito Brasileiro (LINDB)", "Decreto-Lei nº 4.657, de 4 de setembro de 1942", P + "decreto-lei/del4657compilado.htm"),
    "lei-9427-1996": ("Lei da ANEEL", "Lei nº 9.427, de 26 de dezembro de 1996", P + "leis/l9427compilada.htm"),
    "lei-9478-1997": ("Lei do Petróleo (ANP)", "Lei nº 9.478, de 6 de agosto de 1997", P + "leis/l9478.htm"),
    "lei-10233-2001": ("Lei da ANTT e ANTAQ", "Lei nº 10.233, de 5 de junho de 2001", P + "leis/leis_2001/l10233.htm"),
    "lei-12815-2013": ("Lei dos Portos", "Lei nº 12.815, de 5 de junho de 2013", P + "_ato2011-2014/2013/lei/l12815.htm"),
    "lei-13575-2017": ("Lei da ANM", "Lei nº 13.575, de 26 de dezembro de 2017", P + "_ato2015-2018/2017/lei/l13575.htm"),
    "lei-13709-2018-lgpd": ("Lei Geral de Proteção de Dados (LGPD)", "Lei nº 13.709, de 14 de agosto de 2018", P + "_ato2015-2018/2018/lei/l13709compilado.htm"),
    "lei-12527-2011-lai": ("Lei de Acesso à Informação (LAI)", "Lei nº 12.527, de 18 de novembro de 2011", P + "_ato2011-2014/2011/lei/l12527.htm"),
    "lei-12846-2013": ("Lei Anticorrupção", "Lei nº 12.846, de 1º de agosto de 2013", P + "_ato2011-2014/2013/lei/l12846.htm"),
    "lei-12813-2013": ("Lei de Conflito de Interesses", "Lei nº 12.813, de 16 de maio de 2013", P + "_ato2011-2014/2013/lei/l12813.htm"),
    "lei-9986-2000": ("Lei de Gestão de Recursos Humanos das Agências Reguladoras", "Lei nº 9.986, de 18 de julho de 2000", P + "leis/l9986.htm"),
}


def baixar(url):
    # o Planalto derruba conexões de clientes «robô» (Connection reset): usar curl com cabeçalhos de navegador e tentar 3x
    import subprocess, time
    UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    b = b""
    for tent in range(3):
        for u in (url, url.replace("https://www.planalto.gov.br", "http://www.planalto.gov.br")):
            r = subprocess.run(["curl", "-sSL", "--compressed", "--http1.1", "-A", UA, "-H", "Accept: text/html,application/xhtml+xml", "-H", "Accept-Language: pt-BR,pt;q=0.9", "--max-time", "90", u], capture_output=True)
            if r.returncode == 0 and b"Art. 1" in r.stdout.replace(b"\xba", b"").replace(b"Art.&nbsp;1", b"Art. 1") or len(r.stdout) > 20000:
                b = r.stdout; break
        if b: break
        time.sleep(5 * (tent + 1))
    if not b: raise RuntimeError("Planalto não respondeu (curl); tente outra rede ou baixe pelo navegador e salve o HTML em docs/leis/_html/")
    m = re.search(rb'charset=["\']?([\w-]+)', b[:3000])
    enc = (m.group(1).decode() if m else "latin-1").lower()
    try: return b.decode("utf-8" if "utf" in enc else "cp1252")
    except UnicodeDecodeError: return b.decode("cp1252", errors="replace")


def para_md(h):
    h = re.sub(r"(?is)<(script|style|head)\b.*?</\1>", "", h)
    # texto revogado vem tachado (<strike>/<s>/<del>): troca por marcador
    def _rev(m):  # mantém o número do artigo/inciso para a referência não sumir
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(0))).strip()
        r = re.match(r"(Art\.\s*\d+[º°o]?(-[A-Z])?\.?|[IVXLC]+\s*-|§\s*\d+[º°o]?|[a-z]\))", t)
        return f" {r.group(0)} (revogado) " if r else " (revogado) "
    h = re.sub(r"(?is)<(strike|s|del)\b[^>]*>.*?</\1>", _rev, h)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</?(p|div|tr|h\d|li|table)\b[^>]*>", "\n\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).replace("\xa0", " ")
    linhas = [re.sub(r"[ \t]+", " ", l).strip() for l in t.splitlines()]
    out = []
    for l in linhas:
        if not l or re.fullmatch(r"(\(revogado\)\s*)+", l):
            if out and out[-1] != "": out.append("")
            continue
        l = re.sub(r"(\(revogado\)\s*){2,}", "(revogado) ", l)
        if re.match(r"Art\.\s*\d", l): l = "**" + re.match(r"Art\.\s*\d+[º°o]?(-[A-Z])?\.?", l).group(0) + "**" + l[len(re.match(r"Art\.\s*\d+[º°o]?(-[A-Z])?\.?", l).group(0)):]
        if re.match(r"(CAPÍTULO|TÍTULO|Seção|SEÇÃO|LIVRO)\b", l): l = "## " + l
        out.append(l)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def main(ids):
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    for k in ids or LEIS:
        nome, num, url = LEIS[k]
        try: md = para_md(baixar(url))
        except Exception as e: print(f"ERRO {k}: {e}"); continue
        if "Art. 1" not in md and "Art.1" not in md: print(f"AVISO {k}: sem «Art. 1» (página de bloqueio?)"); continue
        cab = f"# {num} — {nome}\n\nURL: {url}\n\nData da coleta: {hoje}\n\n> Texto de referência; confira a versão oficial. Dispositivos tachados no original foram marcados «(revogado)».\n\n---\n\n"
        f = os.path.join(RAIZ, "docs/leis", k + ".md")
        open(f, "w", encoding="utf-8").write(cab + md + "\n")
        print(f"{k}: {os.path.getsize(f)//1024} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
