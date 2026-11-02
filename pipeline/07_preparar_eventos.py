"""Prepara resumos de leitura (data/analise_eventos/<id>.md) de audiências/participativas/workshops/romeiros:
abertura (15 min), janelas ±75 s em torno de falas/menções de diretores e encerramento, com marcadores [h:mm:ss] a cada ~45 s.
Uso: 07_preparar_eventos.py [--ano 2026] [--tipos audiencia,participativa,workshop,romeiros] [id ...]"""
import json, re, os, sys, argparse
ap = argparse.ArgumentParser(); ap.add_argument("--ano"); ap.add_argument("--tipos", default="audiencia,participativa,workshop,romeiros"); ap.add_argument("ids", nargs="*"); a = ap.parse_args()
RX = re.compile(r"\bdiretor(?:a|es)?\b|diretoria colegiada|diretor[- ]geral|\b(?:guilherme|felipe|lucas|alex|alessandro|marcelo|severino|rafael vital\w*|luciano louren\w*|davi barreto|amaral)\b", re.I)
def hms(t): t = int(t); return f"{t//3600}:{t%3600//60:02d}:{t%60:02d}"
tipos = set(a.tipos.split(","))
vids = [json.loads(l) for l in open("data/videos.jsonl")]
for v in vids:
    if v.get("duplicata_de") or v["tipo"] not in tipos: continue
    if a.ids and v["id"] not in a.ids: continue
    if a.ano and (v["data"] or "")[:4] != a.ano: continue
    f = f"data/transcricoes/{v['id']}.json"
    if not os.path.exists(f): continue
    seg = json.load(open(f)); fim = seg[-1]["t"] if seg else 0
    marc = [s["t"] for s in seg if RX.search(s["x"])]
    jan = [(0, 900), (max(0, fim - 300), fim + 1)] + [(max(0, t - 75), t + 75) for t in marc]
    jan.sort(); mer = []
    for i, j in jan:
        if mer and i <= mer[-1][1] + 20: mer[-1][1] = max(mer[-1][1], j)
        else: mer.append([i, j])
    out = [f"# {v['titulo']} — {v['data']} — {v['tipo']} — {v['id']}", f"duração aproximada: {hms(fim)}; janelas: abertura, menções a diretores (n={len(marc)}), encerramento", ""]
    for i, j in mer:
        out.append(f"\n--- trecho {hms(i)} a {hms(min(j, fim))} ---")
        ult = -999; buf = []
        for s in seg:
            if i <= s["t"] <= j:
                if s["t"] - ult >= 45: buf.append(f"\n[{hms(s['t'])}]"); ult = s["t"]
                buf.append(re.sub(r"\[[^\]]*\]|>>", " ", s["x"]).strip())
        out.append(" ".join(buf))
    open(f"data/analise_eventos/{v['id']}.md", "w").write("\n".join(out) + "\n")
    print(v["id"], v["tipo"], v["data"], os.path.getsize(f"data/analise_eventos/{v['id']}.md") // 1000, "KB")
