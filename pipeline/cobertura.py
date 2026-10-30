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

# ---- sem_transcricao.md: tudo o que NÃO conseguimos obter, por vídeo e com motivo ----
import re
mot = {}
if os.path.exists(sd):
    for l in open(sd):
        try: d = json.loads(l); mot[d["id"]] = d
        except Exception: pass
ROT = {"sem_legenda": "legenda desativada/inexistente no YouTube", "bloqueio": "bloqueio temporário do YouTube (tentar de novo)",
       "limite429": "limite do YouTube (429; tentar de novo)", "erro_yt": "erro do YouTube (tentar de novo)"}
linhas, cont = [], collections.Counter()
for v in sorted(rows, key=lambda v: (v["data"] or "0", v["titulo"]), reverse=True):
    if v["tipo"] == "outro" or v.get("duplicata_de"): continue
    f = f"data/transcricoes/{v['id']}.json"
    if os.path.exists(f):
        t = json.load(open(f)); txt = re.sub(r"\s+", " ", " ".join(re.sub(r"\[[^\]]*\]|>>|Heat\.", " ", s["x"]) for s in t)).strip()
        if len(txt) < 1500 and v["tipo"] == "diretoria" or len(txt) < 400: m = f"transcrição sem fala útil ({len(txt)} caracteres; só música/ruído)"
        else: continue
    elif v["id"] in mot: m = ROT.get(mot[v["id"]].get("motivo"), mot[v["id"]].get("motivo", "motivo desconhecido"))
    else: m = "ainda não baixado (rodar a coleta no Mac)"
    cont[((v["data"] or "sem data")[:4], v["tipo"])] += 1
    linhas.append(f"- {v['data'] or 's/data'} · {v['tipo']} · {v['titulo'][:80]} · https://www.youtube.com/watch?v={v['id']} · **{m}**")
topo = ["# O que NÃO temos (sem transcrição utilizável)", "",
        "Estes vídeos existem no canal, mas não há texto para analisar. Nada aqui entra nos perfis. Opção futura: transcrever o áudio localmente (Whisper), se aprovado.", "",
        f"Total: **{len(linhas)}** · " + "; ".join(f"{a}/{t}: {n}" for (a, t), n in sorted(cont.items(), reverse=True)), ""]
open("sem_transcricao.md", "w").write("\n".join(topo + linhas) + "\n")
print("sem_transcricao.md:", len(linhas))
