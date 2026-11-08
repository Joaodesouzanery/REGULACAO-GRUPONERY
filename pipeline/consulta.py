"""Consulta a base: perfil por diretor/tema, busca de texto e lista de itens com citação (link do YouTube no minuto).
Uso:
  consulta.py perfil "Alex Azevedo" [--tema onibus]
  consulta.py ficha "Lucas Asfor" [--tema onibus]   ← FORMATO PADRÃO DE RESPOSTA (ficha fixa com trechos literais)
  consulta.py empresa CONCER | microtema onibus_cassacao [--diretor "Lucas Asfor"] | precedentes "cassação circuito aberto" | relator CONCER
  consulta.py reincidencia | grupo Rumo | sustentacoes | tramitacao
  consulta.py busca "empresa de ônibus cassação"
  consulta.py temas | diretores | mandatos | trecho <texto> [--tipo audiencia|participativa|diretoria|workshop]"""
import json, sqlite3, sys, re, collections
c = sqlite3.connect("data/regulacao.db"); c.row_factory = sqlite3.Row
def segs(ts):
    if not ts: return None
    p = [int(x) for x in re.findall(r"\d+", ts)][:3]
    return sum(v * m for v, m in zip(reversed(p), (1, 60, 3600)))
def _ata_url(vid):
    import json as _j, os as _o
    f = f"data/analise/{vid}.analise.json"
    return _j.load(open(f))["meta"].get("url") if _o.path.exists(f) else None
def link(vid, ts):
    if str(vid).startswith("ata_"): return _ata_url(vid) or ""
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
                 + f"\n  - trecho ({r['trecho_tipo']}): «{(r['trecho'] or '—')[:280]}…» · " + (f"[ata oficial]({link(r['video_id'], None)})" if str(r['video_id']).startswith('ata_') else f"[vídeo no minuto](https://www.youtube.com/watch?v={r['video_id']}&t={max((r['trecho_t'] or 0) - 3, 0)}s)") + "")
    L += ["", "**4. Contra-exemplos / fora do padrão:**"]
    for r in div[-n_ev:] or []:
        L.append(f"- RD {r['numero']} ({r['data']}), item {r['item']} · {r['categoria']}: *{r['voto']}* · «{r['justificativa'] or '—'}» · [vídeo]({link(r['video_id'], r['ts'] or r['its'])})")
    if not div: L.append("- nenhum voto de vista, vencido ou divergente neste recorte.")
    fal = c.execute("select f.*, v.titulo from falas_diretores f join videos v on v.id=f.video_id where f.diretor like ? and f.fonte='estruturada' order by f.video_id, f.t limit 4", (f"%{d.split()[-1]}%",)).fetchall()
    L += ["", "**5. Falas em eventos (audiências/participativas):**"] + ([f"- {f['titulo'][:70]} · [{f['t']//60} min](https://www.youtube.com/watch?v={f['video_id']}&t={f['t']}s): {f['resumo'] or ''} «{(f['texto'] or '')[:200]}»" for f in fal] or ["- nenhuma fala estruturada (a maioria das audiências não tem fala de diretor; a análise cobre janelas do resumo)."])
    L += ["", f"**6. Confiança e lacunas:** {QUAL}. Legenda automática (nomes/valores podem estar errados); trecho «janela_do_item» = minuto do item, não necessariamente a fala do diretor; itens sigilosos e 4 reuniões sem texto fora da base (sem_transcricao.md); voto escrito completo fica no SEI, não no vídeo."]
    return "\n".join(L)

# ---------- camada de empresas e microtemas ----------
def _ent(nome):
    q = f"%{nome}%"
    return c.execute("select * from entidades where nome like ? or sigla like ? or id like ? order by (select count(*) from item_entidade ie where ie.entidade=entidades.id) desc", (q, q, q)).fetchall()
FAV = lambda res: "favorável" if re.search(r"(dá|dar|deu|dado) provimento|provido|deferi|aprova|autoriz|homolog|acolh", res or "", re.I) and not re.search(r"nega|indefer|desprov|n[ãa]o conhec", res or "", re.I) else "desfavorável" if re.search(r"nega|indefer|desprov|n[ãa]o conhec|cassa|multa|penalidade|caducidade|mant[ée]m", res or "", re.I) else "neutro/outro"
def empresa(nome):
    E_ = _ent(nome)
    if not E_: return f"Nenhuma entidade com «{nome}». Tente parte do nome ou a sigla."
    e = E_[0]
    its = c.execute("select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id join item_entidade ie on ie.item_id=i.id where ie.entidade=? order by r.data", (e["id"],)).fetchall()
    out = [f"# {e['nome']}" + (f" ({e['sigla']})" if e["sigla"] else "") + f" · {e['tipo']} · setor {e['setor']}" + (f" · grupo {e['grupo']}" if e["grupo"] else ""), "",
           f"**{len(its)} itens** deliberados de {its[0]['data'] if its else '-'} a {its[-1]['data'] if its else '-'}. Desfecho (classificação automática pelo texto do resultado): " + ", ".join(f"{k} {v}" for k, v in collections.Counter(FAV(i['resultado']) for i in its).most_common()), ""]
    mts = collections.Counter(m[0] for m in c.execute("select microtema from item_microtema where item_id in (select item_id from item_entidade where entidade=?)", (e["id"],)))
    out.append("**Microtemas:** " + "; ".join(f"{k} {v}" for k, v in mts.most_common(8)))
    rel = collections.Counter(i["relator"] for i in its if i["relator"]); out.append("**Quem relata (relator mais provável no próximo processo):** " + "; ".join(f"{k} {v}" for k, v in rel.most_common(5)))
    out.append("\n**Por diretor (votos nos itens da empresa):**")
    for d, n, ac, dv, vi in c.execute("select v.diretor, count(*), sum(v.categoria in ('acompanha','revisor_acompanha')), sum(v.categoria in ('vencido','revisor_diverge')), sum(v.categoria='vista') from votos v join item_entidade ie on ie.item_id=v.item_id where ie.entidade=? group by 1 order by 2 desc", (e["id"],)):
        out.append(f"- {d}: {n} votos · acompanha {ac} · diverge/vencido {dv} · vista {vi}")
    out.append("\n**Itens (mais recentes):**")
    for i in its[-12:][::-1]:
        out.append(f"- **RD {i['numero']} ({i['data']})**, item {i['item']} · relator {i['relator']} · {i['assunto'][:140]} → {(i['resultado'] or '')[:80]} · [vídeo]({link(i['video_id'], i['ts'])})")
    if len(E_) > 1: out.append("\nOutras entidades parecidas: " + "; ".join(f"{x['nome']}" for x in E_[1:6]))
    return "\n".join(out)
def microtema(mt, diretor=None):
    q = "select v.diretor, count(*) n, sum(v.eh_relator) rel, sum(v.categoria in ('acompanha','revisor_acompanha')) ac, sum(v.categoria in ('vencido','revisor_diverge')) dv, sum(v.categoria='vista') vi from votos v join item_microtema m on m.item_id=v.item_id where m.microtema=?"
    a = [mt] + ([diretor] if diretor else [])
    rows = c.execute(q + (" and v.diretor=?" if diretor else "") + " group by 1 order by n desc", a).fetchall()
    if not rows: return "Microtemas: " + ", ".join(r[0] for r in c.execute("select distinct microtema from item_microtema order by 1"))
    out = [f"# Microtema «{mt}»" + (f" · {diretor}" if diretor else ""), "", "| Diretor | Votos | Relatorias | Acompanha | Diverge/vencido | Vista |", "|---|---|---|---|---|---|"]
    out += [f"| {r['diretor']} | {r['n']} | {r['rel']} | {r['ac']} | {r['dv']} | {r['vi']} |" for r in rows]
    ent = c.execute("select e.nome, count(*) n from item_microtema m join item_entidade ie on ie.item_id=m.item_id join entidades e on e.id=ie.entidade where m.microtema=? and e.tipo!='orgao_interno_antt' group by 1 order by n desc limit 8", (mt,)).fetchall()
    if ent: out.append("\n**Empresas mais frequentes:** " + "; ".join(f"{e['nome']} {e['n']}" for e in ent))
    return "\n".join(out)
def precedentes(texto, n=5):
    q = " OR ".join(w for w in re.findall(r"\w+", texto) if len(w) > 3)
    rows = c.execute("select i.*, r.numero, r.data, r.video_id from busca b join itens i on i.id=b.item_id join reunioes r on r.id=i.reuniao_id where busca match ? order by rank limit ?", (q, n)).fetchall()
    out = [f"# Precedentes para «{texto}»", ""]
    for i in rows:
        vs = "; ".join(f"{v['diretor'].split()[0]}: {v['categoria']}" for v in c.execute("select diretor, categoria from votos where item_id=?", (i["id"],)))
        out.append(f"- **RD {i['numero']} ({i['data']})**, item {i['item']} · relator {i['relator']} · {i['assunto'][:150]} → {(i['resultado'] or '')[:80]}\n  - votos: {vs} · [vídeo]({link(i['video_id'], i['ts'])})")
    return "\n".join(out)
def relator_provavel(texto):
    E_ = _ent(texto); mt = c.execute("select distinct microtema from item_microtema where microtema like ?", (f"%{texto}%",)).fetchall()
    out = [f"# Relator mais provável — «{texto}»", ""]
    if E_:
        for d, n in c.execute("select i.relator, count(*) from itens i join item_entidade ie on ie.item_id=i.id where ie.entidade=? and i.relator is not null group by 1 order by 2 desc limit 5", (E_[0]["id"],)): out.append(f"- empresa {E_[0]['nome']}: {d} ({n})")
    for (m,) in mt:
        for d, n in c.execute("select i.relator, count(*) from itens i join item_microtema m on m.item_id=i.id where m.microtema=? and i.relator is not null and i.reuniao_id in (select id from reunioes where data >= date('now','-2 years')) group by 1 order by 2 desc limit 5", (m,)): out.append(f"- microtema {m} (últimos 2 anos): {d} ({n})")
    return "\n".join(out) + "\n\nObs.: a ANTT distribui relatoria por sorteio/regras internas; isto é a frequência histórica, não previsão garantida."

SANC = r"cassa|multa|caducidade|circuito|seccion|frota|supress|tah|nulidade"
def reincidencia(n=20):
    rows = c.execute(f"""select e.nome, e.tipo, count(distinct i.id) n, min(r.data), max(r.data), group_concat(distinct substr(r.data,1,4)) from item_microtema m join item_entidade ie on ie.item_id=m.item_id join entidades e on e.id=ie.entidade
        join itens i on i.id=m.item_id join reunioes r on r.id=i.reuniao_id where e.tipo not like 'orgao%' group by e.id order by n desc""").fetchall()
    out = ["# Reincidência — empresas com mais processos sancionadores", "", "| Empresa | Tipo | Itens sancionadores | Período | Anos | Desfechos |", "|---|---|---|---|---|---|"]
    L = []
    for nome, tp, _, a, b, anos in rows:
        its = c.execute("select distinct i.id, i.resultado from item_microtema m join item_entidade ie on ie.item_id=m.item_id join entidades e on e.id=ie.entidade join itens i on i.id=m.item_id where e.nome=? and m.microtema regexp ?", (nome, SANC)).fetchall() if False else \
              [x for x in c.execute("select distinct i.id, i.resultado, m.microtema from item_microtema m join item_entidade ie on ie.item_id=m.item_id join entidades e on e.id=ie.entidade join itens i on i.id=m.item_id where e.nome=?", (nome,)) if re.search(SANC, x[2])]
        ids = {x[0] for x in its}
        if len(ids) < 3: continue
        d = collections.Counter(FAV(x[1]) for x in {x[0]: x for x in its}.values())
        L.append((len(ids), f"| {nome} | {tp} | {len(ids)} | {a} a {b} | {','.join(sorted(set(anos.split(','))))} | " + ", ".join(f"{k_} {v}" for k_, v in d.most_common()) + " |"))

    out += [x[1] for x in sorted(L, key=lambda x: -x[0])[:n]]
    return "\n".join(out) + "\n\nItens sancionadores = microtemas de multa, cassação, caducidade, circuito aberto, seccionamento, frota, supressão, TAH, nulidade. Desfecho «desfavorável» = sanção mantida/aplicada (classificação automática aproximada)."
def grupo(nome):
    ents = c.execute("select * from entidades where grupo like ?", (f"%{nome}%",)).fetchall()
    if not ents: return "Grupos conhecidos: " + ", ".join(r[0] for r in c.execute("select distinct grupo from entidades where grupo is not null order by 1"))
    ids = [e["id"] for e in ents]; ph = ",".join("?" * len(ids))
    its = c.execute(f"select i.*, r.numero, r.data, r.video_id, ie.entidade from itens i join reunioes r on r.id=i.reuniao_id join item_entidade ie on ie.item_id=i.id where ie.entidade in ({ph}) order by r.data", ids).fetchall()
    out = [f"# Grupo econômico «{nome}» — {len(ents)} empresas, {len(its)} itens", "", "**Empresas:** " + "; ".join(f"{e['nome']} ({sum(1 for i in its if i['entidade']==e['id'])})" for e in ents),
           "**Desfechos:** " + ", ".join(f"{k} {v}" for k, v in collections.Counter(FAV(i['resultado']) for i in its).most_common()),
           "**Microtemas:** " + "; ".join(f"{k} {v}" for k, v in c.execute(f"select microtema, count(*) from item_microtema where item_id in (select item_id from item_entidade where entidade in ({ph})) group by 1 order by 2 desc limit 8", ids).fetchall()),
           "**Relatores:** " + "; ".join(f"{k} {v}" for k, v in collections.Counter(i['relator'] for i in its if i['relator']).most_common(5)), "", "**Itens recentes:**"]
    out += [f"- **RD {i['numero']} ({i['data']})** item {i['item']} · {i['assunto'][:130]} → {(i['resultado'] or '')[:70]} · [vídeo]({link(i['video_id'], i['ts'])})" for i in its[-10:][::-1]]
    return "\n".join(out)
def sustentacoes():
    its = c.execute("select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id order by r.data").fetchall()
    its = [i for i in its if re.search(r"sustenta[çc][ãa]o oral|sustentou oralmente|sustenta[çc][õo]es orais", f"{i['assunto']} {i['resumo'] or ''} {i['resultado'] or ''}", re.I)]
    base = collections.Counter(FAV(r[0]) for r in c.execute("select resultado from itens"))
    efeito = lambda res: "retirado" if re.search(r"retir", res or "", re.I) else "vista" if re.search(r"vista", res or "", re.I) else FAV(res)
    ef = collections.Counter(efeito(i["resultado"]) for i in its)
    tb = sum(base.values()) or 1; ts_ = len(its) or 1
    out = [f"# Sustentações orais — {len(its)} itens", "", f"**Efeito com sustentação:** " + ", ".join(f"{k} {v} ({100*v//ts_}%)" for k, v in ef.most_common()),
           f"**Base geral (todos os itens):** " + ", ".join(f"{k} {100*v//tb}%" for k, v in base.most_common()), "", "**Por empresa:**"]
    pe = collections.Counter(r[0] for r in c.execute("select e.nome from item_entidade ie join entidades e on e.id=ie.entidade where ie.item_id in (%s)" % ",".join(str(i["id"]) for i in its))) if its else {}
    out += [f"- {k}: {v}" for k, v in pe.most_common(12)]
    out += ["", "**Itens recentes:**"] + [f"- **RD {i['numero']} ({i['data']})** item {i['item']} · {i['assunto'][:120]} → {efeito(i['resultado'])} · [vídeo]({link(i['video_id'], i['ts'])})" for i in its[-8:][::-1]]
    return "\n".join(out)
def tramitacao(n=15):
    rows = c.execute("select i.processo, i.id, i.item, i.assunto, i.resultado, r.numero, r.data, r.video_id, i.ts from itens i join reunioes r on r.id=i.reuniao_id where i.processo is not null and length(i.processo) > 8 order by r.data").fetchall()
    g = collections.defaultdict(list)
    for x in rows:
        k = re.sub(r"\D", "", x[0])[:15]
        if len(k) >= 9: g[k].append(x)
    mult = sorted(((k, v) for k, v in g.items() if len({y[6] for y in v}) > 1), key=lambda kv: -len({y[6] for y in kv[1]}))
    vistas = collections.Counter(r[0] for r in c.execute("select diretor from votos where categoria='vista'"))
    out = [f"# Tramitação — processos que voltam à pauta", "", f"{len(mult)} processos aparecem em mais de uma sessão (mesmo número de processo; número vem da legenda, pode falhar).", "",
           "**Quem mais pede vista:** " + "; ".join(f"{k} {v}" for k, v in vistas.most_common(8)), "", "| Processo | Sessões | Primeira | Última | Dias | Último resultado |", "|---|---|---|---|---|---|"]
    import datetime as _dt
    for k, v in mult[:n]:
        ds = sorted({y[6] for y in v if y[6] and len(y[6]) == 10})
        dias = (_dt.date.fromisoformat(ds[-1]) - _dt.date.fromisoformat(ds[0])).days if len(ds) > 1 else "-"
        out.append(f"| {v[0][0][:30]} | {len({y[6] for y in v})} | {ds[0] if ds else '-'} | {ds[-1] if ds else '-'} | {dias} | {(v[-1][4] or '')[:60]} |")
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
    elif a[0] == "empresa": print(empresa(a[1]))
    elif a[0] == "microtema": print(microtema(a[1], a[a.index("--diretor") + 1] if "--diretor" in a else None))
    elif a[0] == "precedentes": print(precedentes(" ".join(a[1:])))
    elif a[0] == "relator": print(relator_provavel(" ".join(a[1:])))
    elif a[0] == "reincidencia": print(reincidencia())
    elif a[0] == "grupo": print(grupo(" ".join(a[1:])))
    elif a[0] == "sustentacoes": print(sustentacoes())
    elif a[0] == "tramitacao": print(tramitacao())
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
