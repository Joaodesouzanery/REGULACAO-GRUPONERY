"""Monitor de empresas/temas por cliente (funcionalidade 10). Uso: python3 pipeline/monitor.py [--dias 7] [--cliente X]
Config: data/monitor.json (fica no repositório SEM dados sensíveis; use apelidos de cliente) =
 {"clientes": {"<apelido>": {"agencias": ["antt","anm"], "entidades": ["CONCER","Rumo"], "microtemas": ["onibus_cassacao"], "diretores": ["Lucas Asfor"], "termos": ["free flow"]}}}
Lista, por cliente, os itens deliberados nos últimos N dias (pela data da reunião) que batem com entidade, grupo, microtema, diretor relator ou termo.
A tarefa semanal roda este script e inclui o resultado no resumo."""
import json, sqlite3, sys, os, re, datetime
dias = int(sys.argv[sys.argv.index("--dias") + 1]) if "--dias" in sys.argv else 7
so = sys.argv[sys.argv.index("--cliente") + 1] if "--cliente" in sys.argv else None
cfg = json.load(open("data/monitor.json"))["clientes"]
desde = (datetime.date.today() - datetime.timedelta(days=dias)).isoformat()
DB = {"antt": "data/regulacao.db", "anm": "data/anm/regulacao.db"}
def link(vid, ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return f"https://www.youtube.com/watch?v={vid}&t={max(p[0]*3600+p[1]*60+p[2]-5,0)}s" if not str(vid).startswith("ata_") else f"(ata) {vid}"
for nome, f in cfg.items():
    if so and nome != so: continue
    print(f"## Cliente: {nome} (desde {desde})")
    achou = 0
    for ag in f.get("agencias", ["antt", "anm"]):
        if not os.path.exists(DB[ag]): continue
        c = sqlite3.connect(DB[ag]); c.row_factory = sqlite3.Row
        its = c.execute("select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where r.data >= ? order by r.data", (desde,)).fetchall()
        for i in its:
            motivos = []
            ents = c.execute("select e.nome, e.sigla, e.grupo from item_entidade ie join entidades e on e.id=ie.entidade where ie.item_id=?", (i["id"],)).fetchall()
            for e in f.get("entidades", []):
                if any(re.search(re.escape(e), " ".join(filter(None, x)), re.I) for x in ents) or re.search(re.escape(e), i["interessado"] or "", re.I): motivos.append(f"empresa {e}")
            mts = {r[0] for r in c.execute("select microtema from item_microtema where item_id=?", (i["id"],))}
            motivos += [f"microtema {m}" for m in f.get("microtemas", []) if m in mts]
            motivos += [f"relator {d}" for d in f.get("diretores", []) if (i["relator"] or "") == d]
            motivos += [f"termo «{t}»" for t in f.get("termos", []) if re.search(re.escape(t), f"{i['assunto']} {i['resumo'] or ''}", re.I)]
            if motivos:
                achou += 1
                print(f"- [{ag.upper()}] RD {i['numero']} ({i['data']}) item {i['item']} · {i['assunto'][:140]} → {(i['resultado'] or '')[:70]} · relator {i['relator']} · motivo: {', '.join(motivos)} · {link(i['video_id'], i['ts'])}")
    if not achou: print("- nada novo no período.")
    print()
