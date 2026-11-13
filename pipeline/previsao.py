"""Previsão de votação por diretor (passado × futuro) — usada no relatório por empresa.
Ideia simples e auditável: para cada diretor do colegiado atual, a taxa histórica de acompanhar o relator
nos temas da empresa (últimos 3 anos, suavização de Laplace) → placar esperado e chance de unanimidade.
Backtest: treina com itens até 2024 e testa em 2025–2026 (unânime sim/não), para dizer quanto a regra acerta.
Uso: python3 pipeline/previsao.py <agencia> "<alias1|alias2>"   (ou importe calcular())"""
import sqlite3, sys, re, datetime, collections

DB = {"antt": "data/regulacao.db", "anm": "data/anm/regulacao.db", "antaq": "data/antaq/regulacao.db"}
ACOMP = ("acompanha", "revisor_acompanha")
DIV = ("vencido", "revisor_diverge")


def conn(ag):
    c = sqlite3.connect(DB[ag]); c.row_factory = sqlite3.Row
    return c


def itens_empresa(c, aliases):
    rx = "|".join(re.escape(a) for a in aliases)
    out = []
    for r in c.execute("select i.id, i.item, i.processo, i.interessado, i.assunto, i.resultado, i.unanime, i.relator, r.numero, r.data, r.video_id, i.ts "
                       "from itens i join reunioes r on r.id=i.reuniao_id order by r.data"):
        if re.search(rx, f"{r['interessado'] or ''} {r['assunto'] or ''}", re.I):
            out.append(r)
    return out


def colegiado_atual(c, reunioes=3):
    """Quem votou nas últimas N reuniões (titulares e substitutos em exercício)."""
    ult = c.execute("select max(data) from reunioes").fetchone()[0]
    rs = [r[0] for r in c.execute("select id from reunioes order by data desc limit ?", (reunioes,))]
    return [r[0] for r in c.execute("select v.diretor, count(*) n from votos v join itens i on i.id=v.item_id where i.reuniao_id in (%s) group by 1 having n>=3 order by n desc" % ",".join("?" * len(rs)), rs)][:5], ult


def taxa_acompanha(c, diretor, temas, ate=None, desde=None):
    q = ("select v.categoria from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id "
         "where v.diretor=? and v.eh_relator=0")
    a = [diretor]
    if temas:
        q += " and v.item_id in (select item_id from item_temas where tema in (%s))" % ",".join("?" * len(temas)); a += temas
    if ate: q += " and r.data<=?"; a.append(ate)
    if desde: q += " and r.data>=?"; a.append(desde)
    cats = [r[0] for r in c.execute(q, a)]
    ac = sum(x in ACOMP for x in cats); dv = sum(x in DIV for x in cats)
    base, k = 0.97, 10  # prior: taxa geral de acompanhar o relator nas três agências (~97%); pesa como 10 votos
    return (ac + k * base) / (ac + dv + k), ac + dv


def calcular(ag, aliases, temas=None):
    c = conn(ag)
    its = itens_empresa(c, aliases)
    if temas is None:
        tm = collections.Counter(t for i in its for (t,) in c.execute("select tema from item_temas where item_id=?", (i["id"],)))
        temas = [t for t, _ in tm.most_common(3)]
    board, ult = colegiado_atual(c)
    desde = (datetime.date.fromisoformat(ult) - datetime.timedelta(days=3 * 365)).isoformat()
    P = {d: taxa_acompanha(c, d, temas, desde=desde) for d in board}
    exp_sim = sum(p for p, _ in P.values())
    p_unan = 1.0
    for p, _ in P.values(): p_unan *= p
    # backtest: regra «unânime se P(unanimidade) > 0,5», treino ≤ 2024, teste 2025+
    Ptr = {}
    acertos = tot = 0
    for r in c.execute("select i.id, not exists(select 1 from votos v where v.item_id=i.id and v.categoria in ('vencido','revisor_diverge')) from itens i join reunioes r on r.id=i.reuniao_id where r.data>='2025-01-01' and exists(select 1 from votos v where v.item_id=i.id and v.eh_relator=1)"
                       + (" and i.id in (select item_id from item_temas where tema in (%s))" % ",".join("?" * len(temas)) if temas else ""), temas or []):
        ds = [v[0] for v in c.execute("select diretor from votos where item_id=? and eh_relator=0", (r[0],))]
        if not ds: continue
        pu = 1.0
        for d in ds:
            if d not in Ptr: Ptr[d] = taxa_acompanha(c, d, temas, ate="2024-12-31")[0]
            pu *= Ptr[d]
        acertos += (pu > 0.5) == bool(r[1]); tot += 1
    return {"agencia": ag, "temas": temas, "colegiado": board, "base_ate": ult, "por_diretor": P,
            "placar_esperado": (round(exp_sim), len(board) - round(exp_sim)) if board else (0, 0),
            "p_unanimidade": p_unan, "backtest": (acertos, tot), "itens": its}


if __name__ == "__main__":
    ag, al = sys.argv[1], sys.argv[2].split("|")
    r = calcular(ag, al)
    print(f"{ag.upper()} · temas {r['temas']} · {len(r['itens'])} itens da empresa · colegiado atual: {', '.join(r['colegiado'])}")
    for d, (p, n) in r["por_diretor"].items(): print(f"  {d}: acompanha o relator {p:.0%} (n={n})")
    a, t = r["backtest"]
    print(f"Placar esperado {r['placar_esperado'][0]}×{r['placar_esperado'][1]} · P(unanimidade) {r['p_unanimidade']:.0%} · backtest 2025–26: {a}/{t} = {a / max(t, 1):.0%}")
