"""Casos semelhantes (Proposta 2, bloco 7): os N itens da base mais parecidos com um texto (assunto de pauta,
resumo de processo), por busca textual ponderada (FTS5/bm25) + bônus por tema e empresa. Mostra desfecho,
relator, justificativa e link no minuto.
Uso: python3 pipeline/similares.py <ag> "<texto>" [--n 20] [--empresa "regex"]   (ou importe similares())"""
import sys, os, re, sqlite3, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao
from desfecho import desfecho_item
from mapa_tema import link

PARE = set("para pelo pela pelos pelas sobre entre contra desde quanto como mais menos ainda apos após junto todos todas outro outra outros dessa desse deste desta sendo pedido processo agencia agência nacional".split())


def termos(txt):
    t = unicodedata.normalize("NFKD", txt.lower()).encode("ascii", "ignore").decode()
    ws = [w for w in re.findall(r"[a-z0-9]{4,}", t) if w not in PARE]
    vist, out = set(), []
    for w in ws:
        if w not in vist: vist.add(w); out.append(w)
    return out[:25]


def similares(ag, texto, n=20, empresa=None, excluir=()):
    c = previsao.conn(ag)
    ts = termos(texto)
    if not ts: return []
    q = " OR ".join(f'"{w}"*' for w in ts)
    try:
        cand = c.execute("select item_id, bm25(busca) s from busca where busca match ? order by s limit 200", (q,)).fetchall()
    except sqlite3.OperationalError:
        cand = []
    R = re.compile(empresa, re.I) if empresa else None
    out = []
    for iid, s in cand:
        if iid in excluir: continue
        i = c.execute("select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where i.id=?", (iid,)).fetchone()
        if not i: continue
        score = -s + (3 if R and R.search(f"{i['interessado'] or ''} {i['assunto'] or ''}") else 0)
        rel = c.execute("select diretor, voto, justificativa from votos where item_id=? and eh_relator=1", (iid,)).fetchone()
        div = [d for (d,) in c.execute("select diretor from votos where item_id=? and categoria in ('vencido','revisor_diverge')", (iid,))]
        out.append({"score": score, "id": iid, "numero": i["numero"], "data": i["data"], "item": i["item"], "assunto": i["assunto"], "interessado": i["interessado"],
                    "resultado": i["resultado"], "desfecho": desfecho_item(c, iid), "relator": rel["diretor"] if rel else i["relator"],
                    "justificativa": (rel["justificativa"] if rel else None), "divergiram": div, "link": link(i["video_id"], i["ts"])})
    out.sort(key=lambda x: -x["score"])
    return out[:n]


if __name__ == "__main__":
    ag, txt = sys.argv[1], sys.argv[2]
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 20
    emp = sys.argv[sys.argv.index("--empresa") + 1] if "--empresa" in sys.argv else None
    for k, x in enumerate(similares(ag, txt, n, emp), 1):
        print(f"{k:2d}. {x['data']} {x['numero']}ª item {x['item']} · {x['desfecho']} · relator {x['relator']}{' · divergiram: ' + ', '.join(x['divergiram']) if x['divergiram'] else ''}\n    {(x['assunto'] or '')[:120]}\n    {x['link']}")
