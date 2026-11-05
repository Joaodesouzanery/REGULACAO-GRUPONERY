"""Conferência dos eventos (audiências/participativas/workshops).
Uso: conferencia_eventos.py trechos   -> confere AUTOMATICAMENTE se cada trecho literal de fala de diretor existe na transcrição perto do minuto registrado.
     conferencia_eventos.py sortear   -> sorteia 20 eventos (10 com fala de diretor, 10 sem) para conferência cega por subagente (data/qualidade/eventos/amostra_cega.json).
     conferencia_eventos.py comparar  -> compara respostas cegas (data/qualidade/eventos/respostas/*.json) com as análises e grava o relatório.
Relatório: agencias/antt/qualidade/conferencia_eventos.md (+ .csv)."""
import json, glob, os, re, sys, random, difflib, csv, collections, unicodedata
D = "data/qualidade/eventos"; os.makedirs(D + "/respostas", exist_ok=True); OUT = "agencias/antt/qualidade"; os.makedirs(OUT, exist_ok=True)
def norm(s): return re.sub(r"[^a-z0-9 ]+", "", unicodedata.normalize("NFKD", (s or "").lower()).encode("ascii", "ignore").decode())
def sec(ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    while len(p) < 3: p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]
def eventos(): return {f.split("/")[-1].split(".")[0]: json.load(open(f)) for f in sorted(glob.glob("data/analise_eventos/*.evento.json"))}
def trechos():
    rows, n = [], collections.Counter()
    for vid, d in eventos().items():
        tf = f"data/transcricoes/{vid}.json"
        if not os.path.exists(tf): continue
        segs = json.load(open(tf))
        for fa in d.get("falas_diretores", []):
            alvo = norm(fa.get("trecho")); t0 = sec(fa.get("ts"))
            if not alvo: continue
            melhor, tm = 0, None
            for i, s in enumerate(segs):
                if abs(s["t"] - t0) > 600: continue
                janela = norm(" ".join(x["x"] for x in segs[i:i + 12]))
                r = difflib.SequenceMatcher(None, alvo[:200], janela[:len(alvo[:200]) + 40]).ratio()
                if r > melhor: melhor, tm = r, s["t"]
            achou = melhor >= 0.6; perto = achou and abs(tm - t0) <= 120
            n["total"] += 1; n["achou"] += achou; n["perto"] += perto
            rows.append([d["evento"].get("data"), vid, fa["diretor"], fa.get("ts"), f"{melhor:.2f}", int(tm) if tm is not None else "", int(tm - t0) if tm is not None else "", "ok" if perto else "minuto_desviado" if achou else "nao_encontrado"])
    with open(f"{OUT}/conferencia_eventos_trechos.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["data", "video_id", "diretor", "ts_registrado", "similaridade", "t_encontrado_s", "desvio_s", "status"]); w.writerows(rows)
    json.dump(dict(n), open(f"{D}/trechos_resumo.json", "w")); print(dict(n))
def sortear():
    random.seed(20261107); ev = eventos()
    com = sorted(v for v, d in ev.items() if d.get("falas_diretores") and os.path.exists(f"data/analise_eventos/{v}.md"))
    sem = sorted(v for v, d in ev.items() if not d.get("falas_diretores") and os.path.exists(f"data/analise_eventos/{v}.md"))
    am = random.sample(com, min(10, len(com))) + random.sample(sem, 10)
    json.dump([{"video_id": v, "titulo": ev[v]["evento"].get("titulo"), "data": ev[v]["evento"].get("data")} for v in am], open(f"{D}/amostra_cega.json", "w"), ensure_ascii=False, indent=1)
    print(len(am), "eventos")
def comparar():
    ev = eventos(); n = collections.Counter(); rows = []
    for f in glob.glob(f"{D}/respostas/*.json"):
        for r in json.load(open(f)):
            d = ev[r["video_id"]]; orig = {fa["diretor"] for fa in d.get("falas_diretores", [])}
            conf = {x["diretor"] for x in r.get("falas_diretores", [])}
            ka = lambda s: {norm(re.sub(r"\(.*", "", x)).split()[-1][:5] for x in s if x and norm(re.sub(r"\(.*", "", x)).split()}
            o, c = ka(orig), ka(conf)
            n["eventos"] += 1; n["mesmo_conjunto"] += o == c
            n["tem_fala_orig"] += bool(o); n["tem_fala_conf"] += bool(c); n["concorda_tem_fala"] += bool(o) == bool(c)
            for x in o | c: n["dir_total"] += 1; n["dir_ok"] += x in o and x in c
            rows.append([d["evento"].get("data"), r["video_id"], "; ".join(sorted(orig)) or "-", "; ".join(sorted(conf)) or "-", "ok" if o == c else "diverge"])
    with open(f"{OUT}/conferencia_eventos.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["data", "video_id", "diretores_com_fala_analise", "diretores_com_fala_conferencia", "status"]); w.writerows(sorted(rows))
    t = json.load(open(f"{D}/trechos_resumo.json")) if os.path.exists(f"{D}/trechos_resumo.json") else {}
    pc = lambda a, b, m=n: f"{100*m[a]/m[b]:.1f}% ({m[a]}/{m[b]})" if m.get(b) else "n/d"
    md = ["# Conferência dos eventos (audiências, participativas, workshops)", "",
          "## 1. Trechos literais (todas as falas de diretor, automática)", "",
          "Para cada fala registrada, procura-se o trecho literal na transcrição a até 10 min do minuto registrado (similaridade ≥ 0,6).", "",
          f"- Trecho encontrado na transcrição: **{pc('achou','total',t)}**", f"- Encontrado a até 2 min do minuto registrado (link confiável): **{pc('perto','total',t)}**", "", "Detalhe em `conferencia_eventos_trechos.csv`.", "",
          "## 2. Conferência cega (amostra de 20 eventos: 10 com fala de diretor, 10 sem)", "",
          "Subagentes releram o resumo do evento (`data/analise_eventos/<id>.md`) e a transcrição **sem ver a análise** e listaram os diretores que falam.", "",
          f"- Concordância sobre «houve fala de diretor?»: **{pc('concorda_tem_fala','eventos')}**", f"- Mesmo conjunto de diretores falantes: **{pc('mesmo_conjunto','eventos')}**", f"- Diretores (por evento) identificados por ambos: **{pc('dir_ok','dir_total')}**", "",
          "Detalhe em `conferencia_eventos.csv`. **Limites:** mesma legenda automática e mesmo tipo de leitura (janelas do resumo, não a sessão inteira); mede consistência, não verdade absoluta."]
    open(f"{OUT}/conferencia_eventos.md", "w").write("\n".join(md) + "\n"); print("\n".join(md))
{"trechos": trechos, "sortear": sortear, "comparar": comparar}[sys.argv[1]]()
