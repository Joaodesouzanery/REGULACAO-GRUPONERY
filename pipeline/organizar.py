import os
"""Gera a árvore organizada agencias/<agencia>/ a partir de data/ (fonte de trabalho). Idempotente: apaga e recria (exceto agencias/<ag>/qualidade/).
Uso: python3 pipeline/organizar.py [antt]   (rodar depois de 05_indexar.py)
Estrutura: reunioes/<ano>/<tipo>/<data>_<numero>_<id>/ · diretores/<nome>/ · temas/ · exportacoes/ (csv, trechos, banco)"""
import json, os, re, shutil, sqlite3, subprocess, sys, csv, gzip, unicodedata
ag = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("AGENCIA", "antt")
R = f"agencias/{ag}"
PRESERVAR = {"qualidade"}  # pastas mantidas à mão (não geradas aqui)
if os.path.exists(R):
    for x in os.listdir(R):
        if x in PRESERVAR: continue
        y = f"{R}/{x}"
        shutil.rmtree(y) if os.path.isdir(y) else os.remove(y)
for d in ("reunioes", "diretores", "temas", "exportacoes"): os.makedirs(f"{R}/{d}")
def slug(s): return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()).strip("-")[:40] or "sem-numero"
vids = [json.loads(l) for l in open("data/videos.jsonl")]
inv = open(f"{R}/inventario.jsonl", "w"); n = 0
for v in vids:
    inv.write(json.dumps(v, ensure_ascii=False) + "\n")
    tr = f"data/transcricoes/{v['id']}.json"
    if v["tipo"] == "outro" or v.get("duplicata_de") or not os.path.exists(tr): continue
    an = f"data/analise/{v['id']}.analise.json"; d = None; num = None
    ev = f"data/analise_eventos/{v['id']}.evento.json"
    if os.path.exists(an):
        r = json.load(open(an))["reuniao"]; d = r.get("data"); num = r.get("numero")
    elif os.path.exists(ev):
        r = json.load(open(ev))["evento"]; d = r.get("data"); num = r.get("numero")
    d = d or v.get("data") or "sem-data"
    ano = d[:4] if re.match(r"\d{4}", d) else "sem-data"
    m = re.search(r"(?:n[ºo°]\.?|no\.?)\s*(\d{1,4})|(\d{1,4})ª", v["titulo"], re.I)
    num = num or (m and (m[1] or m[2])) or v["titulo"]
    pasta = f"{R}/reunioes/{ano}/{v['tipo']}/{d}_{slug(str(num))}_{v['id']}"; os.makedirs(pasta)
    shutil.copy(tr, f"{pasta}/transcricao.json")
    for src, dst in ((f"data/analise/{v['id']}.md", "leitura.md"), (an, "analise.json"), (ev, "evento.json"), (f"data/analise_eventos/{v['id']}.md", "leitura_evento.md")):
        if os.path.exists(src): shutil.copy(src, f"{pasta}/{dst}")
    json.dump({**v, "data_resolvida": d, "link": f"https://www.youtube.com/watch?v={v['id']}", "analisada": os.path.exists(an) or os.path.exists(ev)}, open(f"{pasta}/meta.json", "w"), ensure_ascii=False, indent=1)
    n += 1
for f in ("COBERTURA.md", "sem_transcricao.md"):
    if os.path.exists(f): shutil.copy(f, f"{R}/{f}")
shutil.copy("data/mandatos.json", f"{R}/mandatos.json")
c = sqlite3.connect("data/regulacao.db"); c.row_factory = sqlite3.Row
def csvdump(nome, sql):
    rows = c.execute(sql).fetchall()
    with open(f"{R}/exportacoes/{nome}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(rows[0].keys()) if rows else None
        for r in rows: w.writerow(list(r))
csvdump("reunioes", "select r.*, ' ' as _ from reunioes r")
csvdump("itens", "select i.*, r.numero as reuniao, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id")
csvdump("votos", "select r.data, r.numero as reuniao, r.video_id, i.item, i.relator, i.assunto, v.diretor, v.categoria, v.voto, v.ts, v.justificativa, v.tom, v.confianca from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id order by r.data, i.item")
csvdump("falas_audiencias", "select f.*, v.titulo from falas_diretores f join videos v on v.id=f.video_id")
with gzip.open(f"{R}/exportacoes/trechos.jsonl.gz", "wt") as f:
    for r in c.execute("select t.video_id, t.t, t.texto, v.tipo from trechos t join videos v on v.id=t.video_id"):
        f.write(json.dumps({"video_id": r[0], "t": r[1], "tipo": r[3], "link": f"https://www.youtube.com/watch?v={r[0]}&t={r[1]}s", "texto": r[2]}, ensure_ascii=False) + "\n")
import gzip
with open("data/regulacao.db","rb") as _a, gzip.open(f"{R}/exportacoes/regulacao.db.gz","wb",compresslevel=9) as _b:
    shutil.copyfileobj(_a,_b)
if os.path.exists(f"{R}/exportacoes/regulacao.db"): os.remove(f"{R}/exportacoes/regulacao.db")
def cons(*a): return subprocess.run([sys.executable, "-I", "pipeline/consulta.py", *a], capture_output=True, text=True).stdout
temas = [r[0] for r in c.execute("select tema from item_temas group by 1 having count(*)>=3 order by count(*) desc")]
for t in temas: open(f"{R}/temas/{t}.md", "w").write(cons("tema", t))
mand = {m["diretor"]: m for m in json.load(open("data/mandatos.json"))}
for (dn,) in c.execute("select diretor from votos group by 1 order by count(*) desc"):
    p = f"{R}/diretores/{slug(dn)}"; os.makedirs(p)
    open(f"{p}/perfil.md", "w").write(cons("perfil", dn))
    for t in temas: open(f"{p}/perfil_{t}.md", "w").write(cons("perfil", dn, "--tema", t))
    with open(f"{p}/votos.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["data", "reuniao", "item", "relator", "assunto", "voto", "categoria", "ts", "justificativa", "confianca", "link"])
        for r in c.execute("select r.data, r.numero, i.item, i.relator, i.assunto, v.voto, v.categoria, v.ts, v.justificativa, v.confianca, r.video_id from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.diretor=? order by r.data", (dn,)):
            h = [int(x) for x in (r[7] or "0:0:0").split(":")][-3:]; s = sum(a * b for a, b in zip(reversed(h), (1, 60, 3600)))
            w.writerow([*list(r)[:10], f"https://www.youtube.com/watch?v={r[10]}&t={s}s"])
    m = next((v for k, v in mand.items() if k.split()[0] in dn or dn.split()[0] in k), None)
    open(f"{p}/mandato.md", "w").write(f"# Mandato — {dn}\n\n" + (json.dumps(m, ensure_ascii=False, indent=1) if m else "sem registro em mandatos.json") + "\n")
    open(f"{p}/falas_audiencias.md", "w").write(cons("falas", dn.split()[0]))
open(f"{R}/README.md", "w").write(f"""# {ag.upper()} — dados organizados

Gerado por `pipeline/organizar.py` a partir de `data/` (fonte de trabalho). Não edite aqui: rode `python3 pipeline/05_indexar.py && python3 pipeline/organizar.py {ag}`.

- `reunioes/<ano>/<tipo>/<data>_<numero>_<video_id>/` — `transcricao.json` (legenda com tempos), `leitura.md`, `analise.json` (itens, votos, justificativas), `meta.json` (link do vídeo). Tipos: diretoria, audiencia, participativa, workshop, romeiros.
- `diretores/<nome>/` — `perfil.md`, `perfil_<tema>.md`, `votos.csv` (com link no minuto), `mandato.md`, `falas_audiencias.md`.
- `temas/<tema>.md` — itens por tema, todos os diretores.
- `exportacoes/` — `votos_diretores.xlsx` (planilha: resumo por diretor, diretor × tema, todos os votos com link no minuto, divergências, falas em eventos, mandatos, vacâncias), CSV (reuniões, itens, votos, falas em audiências), `trechos.jsonl.gz` (fala literal com link e minuto), `regulacao.db.gz` (SQLite compactado; descompacte com gunzip, ou regenere com `python3 pipeline/05_indexar.py`).
- `inventario.jsonl`, `COBERTURA.md`, `sem_transcricao.md` (o que NÃO temos e por quê), `mandatos.json`.
""")
subprocess.run([sys.executable, "-I", "pipeline/vacancias.py", ag])
subprocess.run([sys.executable, "-I", "pipeline/planilha_votos.py", f"{R}/exportacoes/votos_diretores.xlsx"])
print(n, "reuniões com transcrição organizadas;", len(temas), "temas;", len(os.listdir(f"{R}/diretores")), "diretores")
