"""Mapeamento de um assunto por diretor (usado em todo relatório de consultoria): como cada diretor em exercício
votou em itens que casam com uma regex (assunto + resumo), quem relatou, desfecho, justificativa típica e trecho com link.
Uso: python3 pipeline/mapa_tema.py <ag> "<regex>" [--desde AAAA-MM-DD]   (ou importe mapear())"""
import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao
from desfecho import desfecho_item

ACOMP, DIV = previsao.ACOMP, previsao.DIV


def seg(ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]


def link(vid, ts, t=None):
    return f"https://www.youtube.com/watch?v={vid}&t={max(int(t) if t else seg(ts) - 3, 0)}s"


def mapear(ag, rx, desde=None):
    c = previsao.conn(ag)
    R = re.compile(rx, re.I)
    its = [r for r in c.execute("select i.id, i.item, i.assunto, i.interessado, i.resultado, i.resumo, i.relator, i.ts, r.numero, r.data, r.video_id "
                                "from itens i join reunioes r on r.id=i.reuniao_id order by r.data")
           if R.search(f"{r['assunto'] or ''} {r['resumo'] or ''}") and (not desde or r["data"] >= desde)]
    ids = [i["id"] for i in its]
    board, ult = previsao.colegiado_atual(c)
    por = {}
    for d in board:
        V = [v for v in c.execute("select v.*, r.numero, r.data, r.video_id, i.assunto from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id "
                                  "where v.diretor=? and v.item_id in (%s) order by r.data" % ",".join("?" * len(ids) or "0"), [d] + ids)] if ids else []
        cat = collections.Counter(v["categoria"] for v in V)
        rel = [v for v in V if v["eh_relator"]]
        des = collections.Counter(desfecho_item(c, v["item_id"]) for v in rel)
        ac, dv = sum(cat[k] for k in ACOMP), sum(cat[k] for k in DIV)
        p = (ac + 10 * 0.97) / (ac + dv + 10)  # mesma regra de previsao.taxa_acompanha (prior 0,97, peso 10)
        ev = next((v for v in reversed(V) if v["categoria"] in DIV + ("vista",)), None) or next((v for v in reversed(V) if v["trecho"]), None)
        por[d] = {"n": len(V), "rel": len(rel), "ac": ac, "dv": dv, "vista": cat["vista"], "des": des, "p_acomp": p, "ev": ev,
                  "just": [v["justificativa"] for v in V if v["justificativa"]][-3:]}
    unan = sum(1 for i in its if not c.execute("select 1 from votos where item_id=? and categoria in ('vencido','revisor_diverge')", (i["id"],)).fetchone())
    des_all = collections.Counter(desfecho_item(c, i["id"]) for i in its)
    return {"agencia": ag, "regex": rx, "itens": its, "colegiado": board, "por_diretor": por, "unanimes": unan, "desfechos": des_all, "base_ate": ult}


if __name__ == "__main__":
    ag, rx = sys.argv[1], sys.argv[2]
    m = mapear(ag, rx, sys.argv[sys.argv.index("--desde") + 1] if "--desde" in sys.argv else None)
    print(f"{ag.upper()} · «{rx}» · {len(m['itens'])} itens · {m['unanimes']} sem divergência · desfechos {dict(m['desfechos'])}")
    for d, s in m["por_diretor"].items():
        print(f"  {d}: {s['n']} votos, relatou {s['rel']}, acompanhou {s['ac']}, divergiu {s['dv']}, vista {s['vista']} · P(acompanhar) {s['p_acomp']:.0%}")
    for i in m["itens"][-12:]:
        print(f"   {i['data']} {i['numero']}ª item {i['item']}: {(i['assunto'] or '')[:100]} → {(i['resultado'] or '')[:50]} {link(i['video_id'], i['ts'])}")
