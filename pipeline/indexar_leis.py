"""Indexa docs/leis/**/*.md em data/leis.db (tabela leis + FTS5 leis_fts), quebrando por artigo.
Cabeçalho esperado no .md: linhas «# <nome>» e «URL: <url>». Artigos começam com «Art. N».
Uso: python3 pipeline/indexar_leis.py"""
import glob, os, re, sqlite3

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(RAIZ, "data", "leis.db")
ART = re.compile(r"^\**\s*Art\.?\s*(\d+[º°o]?(?:-[A-Z])?)", re.M)


def ler(caminho):
    t = open(caminho, encoding="utf-8").read()
    nome = (re.search(r"^#\s+(.+)$", t, re.M) or [None, os.path.basename(caminho)[:-3]])[1].strip()
    url = (re.search(r"^\**URL:?\**:?\s*<?(\S+?)>?\s*$", t, re.M) or [None, ""])[1]
    pos = [m for m in ART.finditer(t)]
    if not pos:  # sem artigos: indexa por parágrafos grandes
        return [(nome, "texto", b.strip(), url) for b in re.split(r"\n{2,}", t) if len(b.strip()) > 40]
    out = [(nome, "preâmbulo", t[:pos[0].start()].strip(), url)]
    for i, m in enumerate(pos):
        fim = pos[i + 1].start() if i + 1 < len(pos) else len(t)
        out.append((nome, "Art. " + m.group(1).replace("o", "º"), t[m.start():fim].strip(), url))
    return [r for r in out if r[2]]


def main():
    arqs = sorted(f for f in glob.glob(os.path.join(RAIZ, "docs/leis/**/*.md"), recursive=True)
                  if os.path.basename(f).lower() != "readme.md")
    if os.path.exists(DB): os.remove(DB)
    c = sqlite3.connect(DB)
    c.executescript("""create table leis(lei text, artigo text, texto text, url text, arquivo text);
      create virtual table leis_fts using fts5(lei, artigo, texto, url unindexed, tokenize='unicode61 remove_diacritics 2');""")
    n = 0
    for f in arqs:
        rel = os.path.relpath(f, RAIZ)
        for lei, art, txt, url in ler(f):
            c.execute("insert into leis values (?,?,?,?,?)", (lei, art, txt, url, rel))
            c.execute("insert into leis_fts values (?,?,?,?)", (lei, art, txt, url)); n += 1
    c.commit()
    print(f"{len(arqs)} arquivos, {n} trechos → {os.path.relpath(DB, RAIZ)}")


if __name__ == "__main__":
    main()
