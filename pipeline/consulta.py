"""Consulta a base: perfil por diretor/tema, busca de texto e lista de itens com citação (link do YouTube no minuto).
Uso:
  consulta.py perfil "Alex Azevedo" [--tema onibus]
  consulta.py ficha "Lucas Asfor" [--tema onibus]   ← FORMATO PADRÃO DE RESPOSTA (ficha fixa com trechos literais)
  consulta.py busca "empresa de ônibus cassação"
  consulta.py temas | diretores | mandatos | trecho <texto> [--tipo audiencia|participativa|diretoria|workshop]"""
import json, sqlite3, sys, re, collections
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
import os
QUAL = ("conferência cega: ≈ 94–95% de concordância nos votos por diretor (2019–2026; 2019 é o ano mais fraco); mede consistência, não verdade absoluta (agencias/antt/qualidade/README.md)" if os.environ.get("AGENCIA", "antt") == "antt" else f"conferência cega: ver agencias/{os.environ.get("AGENCIA", "antt")}/qualidade/README.md (mede consistência, não verdade absoluta)")
def ficha(d, tema=None, n_ev=5):
    """Ficha fixa: 1 resposta curta · 2 números · 3 evidências com trecho literal · 4 contra-exemplos · 5 falas em eventos · 6 confiança e lacunas."""
    q = "select v.*, i.item, i.assunto, i.resultado, i.unanime, i.relator, i.ts its, r.numero, r.data, r.video_id from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.diretor=?"
    a = [d]
    if tema: q += " and v.item_id in (select item_id from item_temas where tema=?)"; a.append(tema)
    rows = c.execute(q + " order by r.data, i.ts", a).fetchall()
    if not rows: return f"Sem votos de «{d}»" + (f" no tema {tema}" if tema else "") + ". Diretores: " + ", ".join(r[0] for r in c.execute("select distinct diretor from votos"))
    n = len(rows); cat = collections.Counter(r["categoria"] for r in rows); rel = [r for r in rows if r["eh_relator"]]
    acomp = cat["acompanha"] + cat["revisor_acompanha"]; nao_rel = max(n - len(rel), 1)
    div = [r for r in rows if r["categoria"] in ("vista", "vencido", "revisor_diverge", "outro")]
    tot = c.execute("select count(*) from votos where diretor=?", (d,)).fetchone()[0]
    per = f"{rows[0]['data']} a {rows[-1]['data']}"
    L = [f"# {d}" + (f" · tema «{tema}»" if tema else ""), "",
         "**1. Resposta curta:** " + (f"envolve-se ativamente como relator ({len(rel)} relatorias, {100*len(rel)//n}% dos votos no tema)" if len(rel) >= 0.15 * n else f"participa sobretudo votando ({len(rel)} relatorias em {n} votos)")
         + f"; acompanha o relator em {100*acomp//nao_rel}% dos votos em que não relata; {len(div)} votos fora do padrão (vista, vencido, divergência, outro). [Completar com o padrão de mérito lido nas evidências.]", "",
         f"**2. Números:** n = {n} votos" + (f" no tema (de {tot} no total)" if tema else "") + f" · período {per} · relator {len(rel)} (unânimes {sum(r['unanime'] for r in rel)}) · acompanha {acomp} · vista {cat['vista']} · voto-vista divergente {cat['revisor_diverge']} · vencido {cat['vencido']} · outro/não captado {cat['outro'] + cat['nao_captado']}", "",
         "**3. Evidências** (relatorias e votos justificados; trecho literal da legenda automática):"]
    ev = [r for r in rows if r["eh_relator"] and r["justificativa"]] or [r for r in rows if r["justificativa"]] or rows
    passo = max(len(ev) // n_ev, 1)
    for r in ev[::passo][:n_ev]:
        L.append(f"- **RD {r['numero']} ({r['data']}), item {r['item']}** — {r['assunto'][:150]} · voto: *{r['voto']}* · justificativa: «{r['justificativa'] or '—'}» · resultado: {r['resultado'][:80]}"
                 + f"\n  - trecho ({r['trecho_tipo']}): «{(r['trecho'] or '—')[:280]}…» · [vídeo no minuto](https://www.youtube.com/watch?v={r['video_id']}&t={max((r['trecho_t'] or 0) - 3, 0)}s)")
    L += ["", "**4. Contra-exemplos / fora do padrão:**"]
    for r in div[-n_ev:] or []:
        L.append(f"- RD {r['numero']} ({r['data']}), item {r['item']} · {r['categoria']}: *{r['voto']}* · «{r['justificativa'] or '—'}» · [vídeo]({link(r['video_id'], r['ts'] or r['its'])})")
    if not div: L.append("- nenhum voto de vista, vencido ou divergente neste recorte.")
    fal = c.execute("select f.*, v.titulo from falas_diretores f join videos v on v.id=f.video_id where f.diretor like ? and f.fonte='estruturada' order by f.video_id, f.t limit 4", (f"%{d.split()[-1]}%",)).fetchall()
    L += ["", "**5. Falas em eventos (audiências/participativas):**"] + ([f"- {f['titulo'][:70]} · [{f['t']//60} min](https://www.youtube.com/watch?v={f['video_id']}&t={f['t']}s): {f['resumo'] or ''} «{(f['texto'] or '')[:200]}»" for f in fal] or ["- nenhuma fala estruturada (a maioria das audiências não tem fala de diretor; a análise cobre janelas do resumo)."])
    L += ["", f"**6. Confiança e lacunas:** {QUAL}. Legenda automática (nomes/valores podem estar errados); trecho «janela_do_item» = minuto do item, não necessariamente a fala do diretor; itens sigilosos e 4 reuniões sem texto fora da base (sem_transcricao.md); voto escrito completo fica no SEI, não no vídeo."]
    return "\n".join(L)
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
    elif a[0] == "ficha":
        print(ficha(a[1], a[a.index("--tema") + 1] if "--tema" in a else None))
    elif a[0] == "falas":  # falas/menções do diretor em audiências, participativas e workshops
        for r in c.execute("select f.*, v.titulo from falas_diretores f join videos v on v.id=f.video_id where f.diretor like ? order by (f.fonte='estruturada') desc, f.video_id, f.t limit 40", (f"%{a[1]}%",)):
            print(f"- {r['tipo_video']}: {r['titulo'][:60]} · [{r['t']//3600}:{r['t']%3600//60:02d}:{r['t']%60:02d}](https://www.youtube.com/watch?v={r['video_id']}&t={r['t']}s) — {('**'+r['resumo']+'** ') if r['resumo'] else ''}«{(r['texto'] or '')[:260]}…» ({r['fonte']})")
    elif a[0] == "mandatos":
        import datetime
        d = lambda x: datetime.date.fromisoformat(x[:10]) if x and len(x) >= 10 else None
        hoje = datetime.date.today()
        for m in c.execute("select * from mandatos"):
            i, f = d(m["inicio"]), d(m["fim"]) or hoje
            dias = f"{(f - i).days} dias (≈ {(f - i).days/365:.1f} anos)" if i else "início anterior a 2023"
            print(f"- {m['diretor']} · {m['cargo']} · {m['inicio'] or '?'} → {m['fim'] or 'atual'} · {m['situacao']} · {dias} · confiança {m['confianca']} · {m['fonte']}")
        print("\nVacâncias de cadeira titular (estimadas):")
        for v in json.load(open("data/vacancias.json")):
            print(f"- {v['inicio']} a {v['fim'] or 'em aberto'} · {v['cadeira']} · preenchida por: {v['preenchida_por']} · interinos: {v['interinos']} · confiança {v['confianca']}")
    elif a[0] == "diretores": print([r[0] for r in c.execute("select distinct diretor from votos")])
