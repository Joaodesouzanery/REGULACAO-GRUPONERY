"""Inteligência de prazo (bloco 3) — processos que passaram por MAIS DE UMA sessão (vista, retirada, retorno): tempo entre a 1ª aparição de um processo na diretoria e a decisão, por tipo/tema.
Processo = nº 50300.xxxxxx/aaaa (normalizado a partir da legenda; números ilegíveis ficam de fora).
Uso: python3 pipeline/prazos.py <ag> [--tema <tema>]   (ou importe duracoes() / estatistica() / processo())"""
import sys, os, re, statistics, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao
from desfecho import desfecho_item

NUM = re.compile(r"(\d{5})[.\s]?(\d{6})[/\s]?(\d{4})")


def chave(proc):
    m = NUM.search(re.sub(r"[^\d./ ]", " ", proc or ""))
    return f"{m.group(1)}.{m.group(2)}/{m.group(3)}" if m else None


def aparicoes(ag):
    c = previsao.conn(ag); P = collections.defaultdict(list)
    for r in c.execute("select i.id, i.processo, i.assunto, i.resultado, r.data, r.numero from itens i join reunioes r on r.id=i.reuniao_id order by r.data"):
        k = chave(r["processo"])
        if k: P[k].append(r)
    return c, P


def _d(x):
    x = str(x)[:10]
    return datetime.date.fromisoformat(x if len(x) == 10 else (x + "-15")[:10])


def duracoes(ag, desde="2018-01-01"):
    """{processo: (dias, tema, n_aparicoes, decidido)} — dias da 1ª aparição até a decisão (ou até hoje, se pendente)."""
    c, P = aparicoes(ag); out = {}
    hoje = datetime.date.today()
    for k, its in P.items():
        if its[0]["data"] < desde: continue
        decs = [i for i in its if desfecho_item(c, i["id"]) != "pendente"]
        dec = decs[-1] if decs else None  # decisão final (última deliberação)
        fim = _d(dec["data"]) if dec else hoje
        tema = (c.execute("select tema from item_temas where item_id=? limit 1", (its[0]["id"],)).fetchone() or ["outros"])[0]
        out[k] = ((fim - _d(its[0]["data"])).days, tema, len({i["data"] for i in its}), bool(dec))
    return out


def estatistica(dur, tema=None):
    xs = sorted(d for d, t, n, ok in dur.values() if ok and n > 1 and (tema is None or t == tema))
    if len(xs) < 5: return None
    q = statistics.quantiles(xs, n=4)
    return {"n": len(xs), "mediana": statistics.median(xs), "p25": q[0], "p75": q[2], "max": xs[-1]}


def processo(ag, proc):
    c, P = aparicoes(ag); k = chave(proc)
    return k, P.get(k, [])


if __name__ == "__main__":
    ag = sys.argv[1]; tema = sys.argv[sys.argv.index("--tema") + 1] if "--tema" in sys.argv else None
    d = duracoes(ag)
    por = collections.defaultdict(list)
    for v in d.values(): por[v[1]].append(v)
    print(f"{ag.upper()}: {len(d)} processos com nº legível desde 2018")
    for t in sorted(por):
        e = estatistica(d, t)
        if e: print(f"  {t}: n={e['n']} · mediana {e['mediana']:.0f} dias · faixa típica {e['p25']:.0f}–{e['p75']:.0f} dias")
