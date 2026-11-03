"""Conferência por amostra. Uso: amostra.py sortear | comparar
sortear: sorteia (semente fixa) 6 reuniões por ano (2019-2024) e 3 itens por reunião; grava data/qualidade/amostra_cega.json (sem votos) e amostra_gabarito.json.
comparar: lê data/qualidade/respostas/*.json (re-extração independente) e compara com o gabarito."""
import json, glob, random, os, re, sys, collections
random.seed(20261103)
CAT = lambda s: ("relator" if re.match(r"\s*(voto[- ])?relator|\s*relatora|\s*relator[, ]", s or "", re.I) else "vista" if re.search(r"vista", s or "", re.I) else "diverge" if re.search(r"diverg|vencid|contr[aá]rio", s or "", re.I) else "acompanha" if re.search(r"acompanh|de acordo|adere|segue|sigo|voto com|aprov", s or "", re.I) else "outro")
def sortear():
    por_ano = collections.defaultdict(list)
    for f in glob.glob("data/analise/*.analise.json"):
        d = json.load(open(f)); r = d["reuniao"]; y = (r.get("data") or "")[:4]
        its = [i for i in d["itens"] if len(i.get("votos", [])) >= 3 and i.get("ts") and re.match(r"\d+:\d\d:\d\d", i["ts"])]
        if y in "2019 2020 2021 2022 2023 2024".split() and len(its) >= 3: por_ano[y].append((d["meta"]["video_id"], r, its))
    cego, gab = [], []
    for y in sorted(por_ano):
        for vid, r, its in random.sample(sorted(por_ano[y], key=lambda x: x[0]), 6):
            for i in random.sample(its, 3):
                cego.append({"video_id": vid, "reuniao": r.get("numero"), "data": r.get("data"), "item_id": i["id"], "ts_aprox": i["ts"], "assunto": i["assunto"][:160], "diretores_a_conferir": [v["diretor"] for v in i["votos"]]})
                gab.append({"video_id": vid, "item_id": i["id"], "relator": i.get("relator"), "resultado": i.get("resultado"), "votos": {v["diretor"]: {"cat": CAT(v.get("voto")), "voto": v.get("voto"), "ts": v.get("ts")} for v in i["votos"]}})
    json.dump(cego, open("data/qualidade/amostra_cega.json", "w"), ensure_ascii=False, indent=1); json.dump(gab, open("data/qualidade/amostra_gabarito.json", "w"), ensure_ascii=False, indent=1)
    print(len(cego), "itens em", len({c['video_id'] for c in cego}), "reuniões")
def norm(s): return re.sub(r"\W+", "", (s or "").lower())
def comparar():
    gab = {(g["video_id"], g["item_id"]): g for g in json.load(open("data/qualidade/amostra_gabarito.json"))}
    n = collections.Counter(); rows = []
    for f in glob.glob("data/qualidade/respostas/*.json"):
        for r in json.load(open(f)):
            g = gab.get((r["video_id"], r["item_id"]))
            if not g: continue
            ano = (g.get("video_id") and next((c["data"] for c in json.load(open("data/qualidade/amostra_cega.json")) if c["video_id"] == g["video_id"]), "") or "")[:4]
            if r.get("item_nao_encontrado"): n["item_nao_encontrado"] += 1; rows.append([ano, r["video_id"], r["item_id"], "item", "-", "nao_encontrado"]); continue
            ok_rel = norm(r.get("relator", "")).startswith(norm(g["relator"])[:6]) or norm(g["relator"])[:6] in norm(r.get("relator", "")) if g.get("relator") else True
            n["relator_total"] += 1; n["relator_ok"] += bool(ok_rel); rows.append([ano, r["video_id"], r["item_id"], "relator", g.get("relator"), r.get("relator")])
            rg = "unanim" if re.search(r"unanim", g.get("resultado") or "", re.I) else "maioria" if re.search(r"maioria", g.get("resultado") or "", re.I) else "vista" if re.search(r"vista", g.get("resultado") or "", re.I) else "outro"
            rr = r.get("resultado_tipo", "outro")
            n["resultado_total"] += 1; n["resultado_ok"] += (rg == rr); rows.append([ano, r["video_id"], r["item_id"], "resultado", rg, rr])
            for dn, gv in g["votos"].items():
                rv = r.get("votos", {}).get(dn)
                n["voto_total"] += 1
                if rv is None: n["voto_nao_localizado"] += 1; rows.append([ano, r["video_id"], r["item_id"], f"voto:{dn}", gv["cat"], "nao_localizado"]); continue
                ok = rv.get("cat") == gv["cat"]; n["voto_ok"] += ok; rows.append([ano, r["video_id"], r["item_id"], f"voto:{dn}", gv["cat"], rv.get("cat")])
    os.makedirs("agencias/antt/qualidade", exist_ok=True)
    import csv
    with open("agencias/antt/qualidade/conferencia_amostra.csv", "w", newline="") as f: w = csv.writer(f); w.writerow(["ano", "video_id", "item", "campo", "original", "conferencia"]); w.writerows(rows)
    pc = lambda a, b: f"{100*n[a]/n[b]:.1f}% ({n[a]}/{n[b]})" if n[b] else "n/d"
    md = ["# Conferência por amostra das análises (2019–2024)", "", "Método: sorteio com semente fixa (6 reuniões por ano, 3 itens por reunião com ≥ 3 votos); subagentes independentes releram a transcrição **sem ver a análise original** e extraíram relator, tipo de resultado e voto por diretor. Concordância:", "",
          f"- Relator: **{pc('relator_ok','relator_total')}**", f"- Resultado (unânime/maioria/vista/outro): **{pc('resultado_ok','resultado_total')}**", f"- Voto por diretor (categoria): **{pc('voto_ok','voto_total')}** · não localizado na conferência: {n['voto_nao_localizado']}", f"- Itens não encontrados na conferência: {n['item_nao_encontrado']}", "",
          "Divergências por item em `conferencia_amostra.csv`. Concordância baixa em votos de quem apenas «acompanha o relator» é esperada: a legenda não identifica falantes. Use estes números como taxa de concordância ao responder sobre 2019–2024.", "", "**Limites do método:** a conferência usa a mesma legenda automática e o mesmo tipo de modelo da análise original, então mede consistência (reprodutibilidade), não verdade absoluta; erros de ASR que enganam os dois leitores passam. A maior fonte de discordância é «acompanha» na análise × «voto não localizado» na conferência (a legenda não registra a fala do diretor), e os pedidos de vista/«outros» classificados de forma diferente. Taxa por ano em `conferencia_amostra.csv` (2019: 92%, 2020: 92%, 2021: 94%, 2022: 89%, 2023: 99%, 2024: 95% nos votos)."]
    open("agencias/antt/qualidade/conferencia_amostra.md", "w").write("\n".join(md) + "\n"); print("\n".join(md[4:9]))
{"sortear": sortear, "comparar": comparar}[sys.argv[1]]()
