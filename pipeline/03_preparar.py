"""Prepara cada transcrição para leitura/análise: turnos de fala (separados por '>>'), marcadores de pauta
e menções normalizadas a diretores. Saída: data/analise/{id}.turnos.json  e  data/analise/{id}.md (leitura).
Uso: 03_preparar.py [id ...]   (sem args = todas as reuniões de diretoria com transcrição)"""
import json, re, os, sys, glob
ALIAS = {  # nome canônico -> regex de variações de ASR (legenda automática erra muito os nomes)
    "Guilherme Sampaio": r"guilherme|sampaio",
    "Felipe Queiroz": r"f[ie]lipe|queir[oó]z|quer[oó]z|queir[oó]",
    "Alex Azevedo": r"\balex(?:o)?\b|azevedo",
    "Marcelo Fonseca": r"marcelo|fonseca",
    "Lucas Asfor": r"lucas\s+a[a-zç]+|\blucas\b",
    "Alessandro Baumgarten": r"alessandro|balgart\w*|baumgart\w*",
}
PAUTA = re.compile(r"\bitem\s+\d+(?:\.\d+)*|autos?\s+n[úu]mero|processo\s+n[úu]mero|pedido\s+de\s+vista|retir\w+\s+de\s+pauta|"
                   r"aprovad[oa]|por\s+unanimidade|voto\s+vencid\w*|acompanho\s+o\s+relator|diverg\w+|ressalva|"
                   r"declaro\s+aberta|encerrad[oa]\s+a\s+sess", re.I)
def turnos(segs):
    out, cur, t0 = [], [], 0.0
    for s in segs:
        x = re.sub(r"\[[^\]]*\]", " ", s["x"]).replace("\n", " ").strip()
        if not x: continue
        partes = re.split(r">>", x)
        for i, p in enumerate(partes):
            p = p.strip()
            if i > 0 and cur: out.append({"t": t0, "x": " ".join(cur)}); cur = []
            if p:
                if not cur: t0 = s["t"]
                cur.append(p)
    if cur: out.append({"t": t0, "x": " ".join(cur)})
    return [u for u in out if len(u["x"]) > 25]
def tag(u):
    men = [n for n, rx in ALIAS.items() if re.search(rx, u["x"], re.I)]
    return {"t": round(u["t"]), "x": u["x"], "dir": men, "pauta": sorted({m.group(0).lower() for m in PAUTA.finditer(u["x"])})[:6]}
def mmss(t): return f"{t//3600:d}:{t%3600//60:02d}:{t%60:02d}"
ids = sys.argv[1:] or [json.loads(l)["id"] for l in open("data/videos.jsonl") if json.loads(l)["tipo"] == "diretoria"]
meta = {json.loads(l)["id"]: json.loads(l) for l in open("data/videos.jsonl")}
for i in ids:
    p = f"data/transcricoes/{i}.json"
    if not os.path.exists(p): continue
    tu = [tag(u) for u in turnos(json.load(open(p)))]
    json.dump(tu, open(f"data/analise/{i}.turnos.json", "w"), ensure_ascii=False)
    with open(f"data/analise/{i}.md", "w") as f:
        f.write(f"# {meta[i]['titulo']} ({meta[i].get('data')}) — {i}\n\n")
        for u in tu:
            f.write(f"[{mmss(u['t'])}] {'{'+', '.join(u['dir'])+'} ' if u['dir'] else ''}{u['x']}\n\n")
    print(i, meta[i]["titulo"][:45], len(tu), "turnos")
