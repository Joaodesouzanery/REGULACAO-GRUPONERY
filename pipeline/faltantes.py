"""O que falta coletar/analisar em TODOS os canais: por agência, tipo e ano — no canal / com texto / analisado — e a lista dos vídeos de diretoria sem texto.
Uso: python3 pipeline/faltantes.py   → documentos/agencias/faltantes.md (+ resumo no terminal)"""
import json, os, glob, collections
AGS = ["antt", "anm", "antaq", "aneel", "anp", "ana", "anac", "anatel", "anvisa", "ans", "anpd", "ancine", "artesp"]
TIPOS = ["diretoria", "audiencia", "participativa", "workshop"]
L = ["# O que falta nos canais das agências", "", "Gerado por `pipeline/faltantes.py`. «Texto» = legenda baixada; «analisado» = reunião lida (.analise.json) ou evento (.evento.json).", "",
     "| Agência | Tipo | No canal | Com texto | Analisados | Sem texto | Texto sem análise |", "|---|---|---|---|---|---|---|"]
sem_texto = {}
resumo = []
for ag in AGS:
    D = "data" if ag == "antt" else f"data/{ag}"
    if not os.path.exists(f"{D}/videos.jsonl"):
        L.append(f"| {ag.upper()} | — | canal ainda não inventariado | | | | |"); resumo.append(f"{ag.upper()}: sem inventário"); continue
    V = {}
    for l in open(f"{D}/videos.jsonl"):
        x = json.loads(l)
        if not x.get("duplicata_de"): V[x["id"]] = x
    ev = {os.path.basename(f).split(".")[0] for f in glob.glob(f"{D}/analise_eventos/*.evento.json")}
    for t in TIPOS:
        ids = [i for i, x in V.items() if x.get("tipo") == t]
        if not ids: continue
        tx = [i for i in ids if os.path.exists(f"{D}/transcricoes/{i}.json")]
        an = [i for i in tx if (os.path.exists(f"{D}/analise/{i}.analise.json") if t == "diretoria" else i in ev)]
        st = [i for i in ids if i not in tx]
        L.append(f"| {ag.upper()} | {t} | {len(ids)} | {len(tx)} | {len(an)} | {len(st)} | {len(tx) - len(an)} |")
        if t == "diretoria":
            sem_texto[ag] = sorted(((V[i].get("data") or "????"), i, V[i].get("titulo", "")[:90]) for i in st)
            resumo.append(f"{ag.upper()}: diretoria {len(ids)} no canal · {len(tx)} com texto · {len(an)} analisadas · faltam {len(st)} textos e {len(tx) - len(an)} análises")
L += ["", "## Reuniões de diretoria sem texto (candidatas a Whisper no Mac)", ""]
for ag, xs in sem_texto.items():
    if not xs: continue
    por_ano = collections.Counter(d[:4] for d, _, _ in xs)
    L.append(f"**{ag.upper()}** ({len(xs)}): " + ", ".join(f"{a}: {n}" for a, n in sorted(por_ano.items())))
    L += [f"- {d} · `{i}` · {t}" for d, i, t in xs[:40]] + ([f"- … mais {len(xs) - 40}"] if len(xs) > 40 else []) + [""]
os.makedirs("documentos/agencias", exist_ok=True)
open("documentos/agencias/faltantes.md", "w").write("\n".join(L) + "\n")
print("\n".join(resumo)); print("→ documentos/agencias/faltantes.md")
