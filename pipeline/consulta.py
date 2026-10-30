"""Consulta a base: perfil por diretor/tema, busca de texto e lista de itens com citação (link do YouTube no minuto).
Uso:
  consulta.py perfil "Alex Azevedo" [--tema onibus]
  consulta.py busca "empresa de ônibus cassação"
  consulta.py temas | diretores | mandatos | trecho <texto> [--tipo audiencia|participativa|diretoria|workshop]"""
import sqlite3, sys, re, collections
c = sqlite3.connect("data/regulacao.db"); c.row_factory = sqlite3.Row
def segs(ts):
    if not ts: return None
    p = [int(x) for x in re.findall(r"\d+", ts)][:3]
    return sum(v * m for v, m in zip(reversed(p), (1, 60, 3600)))
def link(vid, ts):
    s = segs(ts); return f"https://www.youtube.com/watch?v={vid}" + (f"&t={s}s" if s is not None else "")
MARC = {"segurança jurídica": r"segurança jur", "usuário": r"usu[áa]rio", "evidência/dados": r"evid[êe]ncia|dados", "transparência": r"transpar",
        "participação social": r"participa[çc]ão|audi[êe]ncia", "interesse público": r"interesse público", "governança/rito": r"governan|rito|procedimento|devido processo|contradit",
        "eficiência/celeridade": r"efici[êe]ncia|celeridade|agilidade", "TCU/controle externo": r"TCU|Tribunal de Contas", "proporcionalidade": r"proporcion",
        "segurança viária": r"seguran[çc]a vi[áa]ria|vidas|acidente", "sustentabilidade": r"sustentab|ESG|descarbon", "concorrência": r"concorr[êe]ncia|competi[çc]ão|competitiv"}
def perfil(d, tema=None):
    out = [f"# Perfil analítico — {d}" + (f" · tema: {tema}" if tema else "")]
    pres = c.execute("select sum(presente), count(*) from presenca where diretor=?", (d,)).fetchone()
    q = "select v.*, i.item, i.assunto, i.resultado, i.unanime, i.relator, r.numero, r.data, r.video_id from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.diretor=?"
    a = [d]
    if tema: q += " and v.item_id in (select item_id from item_temas where tema=?)"; a.append(tema)
    rows = c.execute(q + " order by r.data, i.ts", a).fetchall()
    n = len(rows); cats = collections.Counter(r["categoria"] for r in rows)
    rel = [r for r in rows if r["eh_relator"]]
    out.append(f"\n**Amostra:** presente em {pres[0] or 0} das {pres[1]} reuniões analisadas em que há registro de presença/ausência; {n} votos"
               + (" neste tema" if tema else "") + f"; {len(rel)} relatorias. " + ("⚠️ n < 5: tratar como indício, não como perfil." if n < 5 else "Amostra ainda pequena (poucas reuniões): leia como tendência observada, não como regra."))
    acomp = cats["acompanha"] + cats["revisor_acompanha"]
    nrel = max(n - len(rel), 1)
    out.append(f"\n**Votos:** acompanha o relator {acomp} ({acomp*100//nrel}% dos votos em que não era relator) · relator {cats['relator']} · vista pedida {cats['vista']} · voto-vista divergente {cats['revisor_diverge']} · vencido {cats['vencido']} · outros/não captado {cats['outro']+cats['nao_captado']}")
    if rel:
        un = sum(1 for r in rel if r["unanime"]); out.append(f"**Como relator:** {un}/{len(rel)} relatorias aprovadas por unanimidade.")
    # temas
    tq = c.execute("select t.tema, count(*) n, sum(v.eh_relator) rel from votos v join item_temas t on t.item_id=v.item_id where v.diretor=? group by 1 order by 2 desc", (d,)).fetchall()
    out.append("\n**Temas (nº de itens em que votou / relatorias):** " + "; ".join(f"{t['tema']} {t['n']}/{t['rel'] or 0}" for t in tq))
    # marcadores
    cnt = collections.Counter()
    for r in rows:
        txt = " ".join(filter(None, [r["justificativa"], r["tom"]]))
        for k, rx in MARC.items():
            if re.search(rx, txt, re.I): cnt[k] += 1
    if cnt: out.append("**Argumentos recorrentes nas justificativas registradas:** " + "; ".join(f"{k} ({v})" for k, v in cnt.most_common(6)))
    tons = [r["tom"] for r in rows if r["tom"]]
    if tons: out.append("**Tom (inferência da leitura, não métrica):** " + " | ".join(dict.fromkeys(tons)))
    out.append("\n## Evidências (reunião · item · voto · justificativa)\n")
    for r in rows:
        if tema is None and not (r["eh_relator"] or r["categoria"] in ("vista", "vencido", "revisor_diverge", "revisor_acompanha") or r["justificativa"]): continue
        out.append(f"- **RD {r['numero']} ({r['data']})**, item {r['item']} — {r['assunto'][:140]} · voto: *{r['voto']}* ({r['categoria']}, conf. {r['confianca']})"
                   + (f" · «{r['justificativa']}»" if r["justificativa"] else "") + f" · [vídeo]({link(r['video_id'], r['ts'])}) · resultado: {r['resultado'][:70]}")
    return "\n".join(out)
def tema(t):
    out = [f"# Itens do tema «{t}» (todos os diretores)\n"]
    for i in c.execute("select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where i.id in (select item_id from item_temas where tema=?) order by r.data, i.ts", (t,)):
        vs = c.execute("select diretor, categoria, justificativa from votos where item_id=?", (i["id"],)).fetchall()
        resumo = "; ".join(f"{v['diretor'].split()[0]}: {v['categoria']}" for v in vs)
        out.append(f"- **RD {i['numero']} ({i['data']})**, {i['item']} · relator **{i['relator']}** · {i['assunto'][:150]} → {i['resultado'][:90]}\n  - votos: {resumo} · [vídeo]({link(i['video_id'], i['ts'])})")
    return "\n".join(out)
def trecho(txt, n=8, tipo=None):
    q = " OR ".join(w for w in re.findall(r"\w+", txt) if len(w) > 3)
    out = []
    for r in c.execute("select t.video_id, t.t, t.texto from trechos_fts f join trechos t on t.id=f.rowid join videos v on v.id=t.video_id where trechos_fts match ? and (? is null or v.tipo=?) order by rank limit ?", (q, tipo, tipo, n)):
        m = c.execute("select numero, data from reunioes where video_id=?", (r["video_id"],)).fetchone()
        vd = c.execute("select titulo, tipo from videos where id=?", (r["video_id"],)).fetchone()
        rot = f"RD {m['numero']} ({m['data']})" if m else f"{vd['tipo']}: {vd['titulo'][:60]}"
        out.append(f"- **{rot}** · [{r['t']//3600}:{r['t']%3600//60:02d}:{r['t']%60:02d}](https://www.youtube.com/watch?v={r['video_id']}&t={r['t']}s) — «{r['texto'][:330]}…»")
    return "\n".join(out) or "nada encontrado"
def busca(txt):
    ids = [r[0] for r in c.execute("select item_id from busca where busca match ? order by rank limit 20", (" OR ".join(re.findall(r"\w+", txt)),))]
    out = []
    for i in ids:
        r = c.execute("select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where i.id=?", (i,)).fetchone()
        out.append(f"- **RD {r['numero']} ({r['data']})**, {r['item']} · relator {r['relator']} · {r['assunto'][:150]} → {r['resultado'][:80]} · [vídeo]({link(r['video_id'], r['ts'])})")
    return "\n".join(out) or "nada encontrado"
if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    if a[0] == "perfil": print(perfil(a[1], a[a.index("--tema") + 1] if "--tema" in a else None))
    elif a[0] == "tema": print(tema(a[1]))
    elif a[0] == "trecho":
        tp = a[a.index("--tipo") + 1] if "--tipo" in a else None
        print(trecho(" ".join(w for i, w in enumerate(a[1:], 1) if w != "--tipo" and a[i - 1] != "--tipo"), tipo=tp))
    elif a[0] == "mandatos":
        for m in c.execute("select * from mandatos"): print(f"- {m['diretor']} · {m['cargo']} · {m['inicio'] or '?'} → {m['fim'] or 'atual'} · {m['situacao']} · confiança {m['confianca']} · fonte: {m['fonte']}")
    elif a[0] == "busca": print(busca(" ".join(a[1:])))
    elif a[0] == "temas": print([tuple(r) for r in c.execute("select tema, count(*) from item_temas group by 1 order by 2 desc")])
    elif a[0] == "diretores": print([r[0] for r in c.execute("select distinct diretor from votos")])
