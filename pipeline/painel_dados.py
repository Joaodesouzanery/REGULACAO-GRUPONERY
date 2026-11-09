"""Gera os JSONs do painel web (Painel ANTT · ANM) a partir dos bancos. Uso: python3 pipeline/painel_dados.py [pasta_saida]
Depois: subir cada JSON como asset do artifact e atualizar datasets/<id>.source.url (ver docs/CONTINUAR.md)."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from desfecho import desfecho_item as _desf
import sqlite3, json, re, collections, sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/painel"; os.makedirs(OUT, exist_ok=True)
FAV = lambda r: "favorável" if re.search(r"provimento|provido|deferi|aprova|autoriz|homolog|acolh", r or "", re.I) and not re.search(r"nega|indefer|desprov|n[ãa]o conhec", r or "", re.I) else "desfavorável" if re.search(r"nega|indefer|desprov|n[ãa]o conhec|cassa|multa|penalidade|caducidade|mant[ée]m", r or "", re.I) else "outro"
def seg(ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]
R = {k: [] for k in ("resumo", "temas", "microtemas", "empresas", "divergencias")}
for ag, db in (("ANTT", "data/regulacao.db"), ("ANM", "data/anm/regulacao.db")):
    c = sqlite3.connect(db)
    for d, n, rel, ac, vi, dv, ve, a, b in c.execute("select v.diretor,count(*),sum(eh_relator),sum(categoria in ('acompanha','revisor_acompanha')),sum(categoria='vista'),sum(categoria='revisor_diverge'),sum(categoria='vencido'),min(r.data),max(r.data) from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id group by 1"):
        R["resumo"].append({"agencia": ag, "diretor": d, "votos": n, "relatorias": rel, "acompanha_pct": round(ac / max(n - rel, 1), 3), "vistas": vi, "divergencias": dv + ve, "desde": a[:7], "ate": b[:7]})
    for d, t, n, rel, dv in c.execute("select v.diretor,t.tema,count(*),sum(eh_relator),sum(categoria in ('vencido','revisor_diverge','vista')) from votos v join item_temas t on t.item_id=v.item_id group by 1,2"):
        R["temas"].append({"agencia": ag, "diretor": d, "tema": t, "votos": n, "relatorias": rel, "fora_do_padrao": dv})
    for d, m, n, rel, dv in c.execute("select v.diretor,m.microtema,count(*),sum(eh_relator),sum(categoria in ('vencido','revisor_diverge','vista')) from votos v join item_microtema m on m.item_id=v.item_id group by 1,2"):
        R["microtemas"].append({"agencia": ag, "diretor": d, "microtema": m, "votos": n, "relatorias": rel, "fora_do_padrao": dv})
    for eid, nome, tp, gr in c.execute("select id,nome,tipo,grupo from entidades where tipo not like 'orgao%'"):
        its = c.execute("select i.id,i.relator,r.data from itens i join reunioes r on r.id=i.reuniao_id join item_entidade ie on ie.item_id=i.id where ie.entidade=?", (eid,)).fetchall()
        if len(its) < 2: continue
        f = collections.Counter(_desf(c, x[0]) for x in its); rl = collections.Counter(x[1] for x in its if x[1]).most_common(1)
        R["empresas"].append({"agencia": ag, "empresa": nome, "tipo": tp, "grupo": gr or "", "itens": len(its), "favoravel": f["favorável"], "desfavoravel": f["desfavorável"], "relator_frequente": rl[0][0] if rl else "", "ultimo": max(x[2] or "" for x in its)})
    for d, cat, just, rn, dt, it, ass, vid, ts, its in c.execute("select v.diretor,v.categoria,v.justificativa,r.numero,r.data,i.item,i.assunto,r.video_id,v.ts,i.ts from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.categoria in ('vista','vencido','revisor_diverge') order by r.data desc"):
        R["divergencias"].append({"id": f"{ag}-{len(R['divergencias'])}", "agencia": ag, "data": dt, "reuniao": str(rn)[:40], "item": str(it)[:20], "diretor": d,
            "tipo": {"vista": "pediu vista", "vencido": "vencido", "revisor_diverge": "voto-vista divergente"}[cat], "assunto": ass[:160], "justificativa": (just or "")[:200],
            "video": f"https://www.youtube.com/watch?v={vid}&t={max(seg(ts or its) - 5, 0)}s" if not vid.startswith("ata_") else ""})
for k, v in R.items():
    json.dump(v, open(f"{OUT}/{k}.json", "w"), ensure_ascii=False); print(k, len(v))
