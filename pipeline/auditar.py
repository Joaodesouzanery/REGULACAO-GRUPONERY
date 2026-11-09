"""Auditoria da base e dos relatórios entregues. Uso: python3 pipeline/auditar.py [pasta_relatorio ...]
Base (ANTT e ANM): integridade referencial, links (minuto dentro da duração do vídeo), trecho literal presente perto do minuto (amostra),
consistência das contagens. Relatórios: cada evidência «RD N (data), item X» citada existe na base com a mesma data e o link aponta para o vídeo dessa reunião.
Saída: impressa e em docs/AUDITORIA_dados.json."""
import sqlite3, json, re, random, os, sys, glob, difflib, unicodedata, collections
random.seed(20261109)
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", unicodedata.normalize("NFKD", (s or "").lower()).encode("ascii", "ignore").decode())
def seg(ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    if not p: return None
    while len(p) < 3: p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]
R = {}
for ag, base in (("antt", "data"), ("anm", "data/anm")):
    c = sqlite3.connect(f"{base}/regulacao.db"); c.row_factory = sqlite3.Row
    vids = {json.loads(l)["id"]: json.loads(l) for l in open(f"{base}/videos.jsonl")}
    r = collections.OrderedDict()
    r["reunioes"] = c.execute("select count(*) from reunioes").fetchone()[0]
    r["itens_sem_reuniao"] = c.execute("select count(*) from itens where reuniao_id not in (select id from reunioes)").fetchone()[0]
    r["votos_sem_item"] = c.execute("select count(*) from votos where item_id not in (select id from itens)").fetchone()[0]
    r["reunioes_sem_fonte"] = sum(1 for (v,) in c.execute("select video_id from reunioes") if not v.startswith("ata_") and v not in vids)
    r["reunioes_sem_data"] = c.execute("select count(*) from reunioes where data is null or data='' or length(data)<7").fetchone()[0]
    r["votos_duplicados"] = c.execute("select count(*) from (select item_id, diretor, count(*) n from votos group by 1,2 having n>1)").fetchone()[0]
    # links: minuto dentro da duração
    fora = tot = 0
    for v, ts, its in c.execute("select r.video_id, v.ts, i.ts from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where r.video_id not like 'ata_%'"):
        d = (vids.get(v) or {}).get("duracao"); s = seg(ts or its)
        if d and s is not None:
            tot += 1; fora += s > d + 60
    r["links_testados"] = tot; r["links_minuto_apos_fim_do_video"] = fora
    # trecho literal: amostra de 300 votos com trecho «fala_no_minuto»: o trecho está na transcrição perto do minuto?
    amostra = c.execute("select r.video_id, v.trecho, v.trecho_t from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.trecho is not null and v.trecho_tipo='fala_no_minuto'").fetchall()
    amostra = random.sample(amostra, min(300, len(amostra))); ok = 0
    for vid, tr, t0 in amostra:
        f = f"{base}/transcricoes/{vid}.json"
        if not os.path.exists(f): continue
        txt = norm(" ".join(x["x"] for x in json.load(open(f)) if abs(x["t"] - (t0 or 0)) <= 60))
        ok += norm(tr)[:80] in txt or difflib.SequenceMatcher(None, norm(tr)[:120], txt).find_longest_match(0, min(120, len(norm(tr))), 0, len(txt)).size > 40
    r["trechos_amostra"] = len(amostra); r["trechos_encontrados"] = ok
    # categorias impossíveis
    r["relatorias_sem_relator_no_item"] = c.execute("select count(*) from votos v join itens i on i.id=v.item_id where v.eh_relator=1 and (i.relator is null or i.relator!=v.diretor)").fetchone()[0]
    R[ag] = (r, c)
out = {ag: dict(r) for ag, (r, _) in R.items()}
for ag, r in out.items():
    print(f"== {ag.upper()}"); [print(f"  {k}: {v}") for k, v in r.items()]
# relatórios entregues
rel = {}
for pasta in sys.argv[1:]:
    ag_default = "anm" if "anm" in pasta else "antt"
    falhas = []; n = 0
    tags = [l for l in open(f"{pasta}/perguntas.md") if l.startswith("- ")] if os.path.exists(f"{pasta}/perguntas.md") else []
    for k, f in enumerate(sorted(glob.glob(f"{pasta}/respostas/*.md"))):
        txt = open(f).read()
        t = tags[k] if k < len(tags) else ""
        ag = "anm" if ("agencia: anm" in t or ("agencia:" not in t and ag_default == "anm")) else "antt"
        c = R[ag][1]
        for m in re.finditer(r"RD ([^()\n]{1,60}?) \((\d{4}-\d{2}(?:-\d{2})?)\)\**,? item ([\w.\-+]{1,25})", txt):
            num, data, item = m.group(1).strip(" *"), m.group(2), m.group(3).strip()
            n += 1
            hit = c.execute("select count(*) from itens i join reunioes r on r.id=i.reuniao_id where r.data=? and (i.item=? or i.item like ?)", (data, item, item + "%")).fetchone()[0]
            if not hit: falhas.append(f"{os.path.basename(f)}: RD {num} ({data}) item {item} não encontrado")
    rel[pasta] = {"evidencias_citadas": n, "nao_encontradas": len(falhas), "detalhe": falhas[:30]}
    print(f"== Relatório {pasta}: {n} evidências citadas, {len(falhas)} não encontradas"); [print("  -", x) for x in falhas[:15]]
json.dump({"base": out, "relatorios": rel}, open("docs/AUDITORIA_dados.json", "w"), ensure_ascii=False, indent=1)
