"""Gera COBERTURA.md: vídeos publicados x transcritos x analisados, por ano e tipo. Uso: python3 pipeline/cobertura.py"""
import json, os, collections, datetime
rows = [json.loads(l) for l in open("data/videos.jsonl")]
tab = collections.defaultdict(lambda: [0, 0, 0])
pend = []
for v in rows:
    if v["tipo"] == "outro" or v.get("duplicata_de"): continue
    y = v["data"][:4] if v["data"] else "sem data"
    k = (y, v["tipo"])
    tr = os.path.exists(f"data/transcricoes/{v['id']}.json"); an = os.path.exists(f"data/analise/{v['id']}.analise.json")
    tab[k][0] += 1; tab[k][1] += tr; tab[k][2] += an
    if v["tipo"] == "diretoria" and tr and not an: pend.append((v["data"] or "", v["titulo"][:70], v["id"]))
out = [f"# Cobertura da base (atualizado em {datetime.date.today()})\n", "Janela de coleta: últimos 2 anos pelo título (reuniões sem data ficam em 's/data').\n",
       "| Ano | Tipo | Publicados | Transcritos | Analisados |", "|---|---|---|---|---|"]
for (y, t), (a, b, c) in sorted(tab.items(), reverse=True): out.append(f"| {y} | {t} | {a} | {b} | {c} |")
out += ["", "## Reuniões de diretoria transcritas e ainda sem análise", ""] + [f"- {d} · {t} · `{i}`" for d, t, i in sorted(pend, reverse=True)]
sd = "data/sem_legenda.jsonl"
if os.path.exists(sd): out += ["", f"Vídeos sem legenda registrados: {sum(1 for _ in open(sd))} (ver `{sd}`)."]
open("COBERTURA.md", "w").write("\n".join(out) + "\n"); print("\n".join(out[:20]))
