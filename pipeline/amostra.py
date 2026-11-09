"""Conferência por amostra. Uso: amostra.py sortear | comparar
sortear: sorteia (semente fixa) 6 reuniões por ano (2019-2024) e 3 itens por reunião; grava data/qualidade/amostra_cega.json (sem votos) e amostra_gabarito.json.
comparar: lê data/qualidade/respostas/*.json (re-extração independente) e compara com o gabarito."""
import json, glob, random, os, re, sys, collections
# Rodadas: amostra.py sortear|comparar [rodada]. Padrão = 2019_2024 (original, caminhos antigos).
RODADAS = {"2019_2024": dict(anos="2019 2020 2021 2022 2023 2024", reun=6, seed=20261103, dir="data/qualidade", rel="conferencia_amostra"),
           "2025_2026": dict(anos="2025 2026", reun=8, seed=20261105, dir="data/qualidade/2025_2026", rel="conferencia_2025_2026"),
           "2019_2024_b": dict(anos="2019 2020 2021 2022 2023 2024", reun=2, seed=20261106, dir="data/qualidade/2019_2024_b", rel="conferencia_2019_2024_b", excluir="data/qualidade/amostra_cega.json")}
RODADAS["antt_c_2019_2026"] = dict(anos="2019 2020 2021 2022 2023 2024 2025 2026", reun=2, seed=20261110, dir="data/qualidade/antt_c", rel="conferencia_antt_c_2019_2026", excluir="data/qualidade/amostra_cega.json")
RODADAS["anm_2019_2026"] = dict(anos="2019 2020 2021 2022 2023 2024 2025 2026", reun=3, seed=20261108, dir="data/qualidade/anm_2019_2026", rel="conferencia_anm_2019_2026")
RD = sys.argv[2] if len(sys.argv) > 2 else "2019_2024"; CFG = RODADAS[RD]; D = CFG["dir"]; os.makedirs(D + "/respostas", exist_ok=True)
random.seed(CFG["seed"])
CAT = lambda s: ("relator" if re.match(r"\s*(voto[- ])?relator|\s*relatora|\s*relator[, ]", s or "", re.I) else ("diverge" if re.search(r"diverg|vencid|contr[aá]rio", s or "", re.I) else "acompanha") if re.search(r"voto[- ]vista", s or "", re.I) else "vista" if re.search(r"vista", s or "", re.I) else "diverge" if re.search(r"diverg|vencid|contr[aá]rio", s or "", re.I) else "acompanha" if re.search(r"acompanh|de acordo|adere|segue|sigo|voto com|aprov", s or "", re.I) else "outro")
def sortear():
    EXC = {c["video_id"] for c in json.load(open(CFG["excluir"]))} if CFG.get("excluir") else set()
    por_ano = collections.defaultdict(list)
    for f in glob.glob("data/analise/*.analise.json"):
        d = json.load(open(f)); r = d["reuniao"]; y = (r.get("data") or "")[:4]
        its = [i for i in d["itens"] if len(i.get("votos", [])) >= 3 and i.get("ts") and re.match(r"\d+:\d\d:\d\d", i["ts"])]
        if y in CFG["anos"].split() and len(its) >= 3 and d["meta"]["video_id"] not in EXC: por_ano[y].append((d["meta"]["video_id"], r, its))
    cego, gab = [], []
    for y in sorted(por_ano):
        for vid, r, its in random.sample(sorted(por_ano[y], key=lambda x: x[0]), min(CFG["reun"], len(por_ano[y]))):
            for i in random.sample(its, 3):
                cego.append({"video_id": vid, "reuniao": r.get("numero"), "data": r.get("data"), "item_id": i["id"], "ts_aprox": i["ts"], "assunto": i["assunto"][:160], "diretores_a_conferir": sorted(v["diretor"] for v in i["votos"])})
                gab.append({"video_id": vid, "item_id": i["id"], "relator": i.get("relator"), "resultado": i.get("resultado"), "votos": {v["diretor"]: {"cat": CAT(v.get("voto")), "voto": v.get("voto"), "ts": v.get("ts")} for v in i["votos"]}})
    json.dump(cego, open(f"{D}/amostra_cega.json", "w"), ensure_ascii=False, indent=1); json.dump(gab, open(f"{D}/amostra_gabarito.json", "w"), ensure_ascii=False, indent=1)
    print(len(cego), "itens em", len({c['video_id'] for c in cego}), "reuniões")
def norm(s): return re.sub(r"\W+", "", (s or "").lower())
def comparar():
    gab = {(g["video_id"], g["item_id"]): g for g in json.load(open(f"{D}/amostra_gabarito.json"))}
    n = collections.Counter(); rows = []
    for f in glob.glob(f"{D}/respostas/*.json"):
        for r in json.load(open(f)):
            g = gab.get((r["video_id"], r["item_id"]))
            if not g: continue
            ano = (g.get("video_id") and next((c["data"] for c in json.load(open(f"{D}/amostra_cega.json")) if c["video_id"] == g["video_id"]), "") or "")[:4]
            if r.get("item_nao_encontrado"): n["item_nao_encontrado"] += 1; rows.append([ano, r["video_id"], r["item_id"], "item", "-", "nao_encontrado"]); continue
            ok_rel = norm(r.get("relator", "")).startswith(norm(g["relator"])[:6]) or norm(g["relator"])[:6] in norm(r.get("relator", "")) if g.get("relator") else True
            n["relator_total"] += 1; n["relator_ok"] += bool(ok_rel); rows.append([ano, r["video_id"], r["item_id"], "relator", g.get("relator"), r.get("relator")])
            rg = "unanim" if re.search(r"unanim", g.get("resultado") or "", re.I) else "maioria" if re.search(r"maioria", g.get("resultado") or "", re.I) else "vista" if re.search(r"vista", g.get("resultado") or "", re.I) else "outro"
            rr = r.get("resultado_tipo", "outro")
            n["resultado_total"] += 1; n["resultado_ok"] += (rg == rr); rows.append([ano, r["video_id"], r["item_id"], "resultado", rg, rr])
            for dn, gv in g["votos"].items():
                rv = r.get("votos", {}).get(dn)
                n["voto_total"] += 1
                if rv is None: n["voto_nao_localizado"] += 1; rows.append([ano, r["video_id"], r["item_id"], f"voto:{dn}", CAT(gv.get("voto")), "nao_localizado"]); continue
                ok = rv.get("cat") == CAT(gv.get("voto")); n["voto_ok"] += ok; rows.append([ano, r["video_id"], r["item_id"], f"voto:{dn}", CAT(gv.get("voto")), rv.get("cat")])
    QD = f"agencias/{os.environ.get("AGENCIA", "antt")}/qualidade"; os.makedirs(QD, exist_ok=True)
    import csv
    with open(f"{QD}/{CFG['rel']}.csv", "w", newline="") as f: w = csv.writer(f); w.writerow(["ano", "video_id", "item", "campo", "original", "conferencia"]); w.writerows(rows)
    pa = collections.defaultdict(lambda: [0, 0])
    for r_ in rows:
        if r_[3].startswith("voto:"): pa[r_[0]][1] += 1; pa[r_[0]][0] += r_[4] == r_[5]
    tipos = collections.Counter(f"{r_[4]}→{r_[5]}" for r_ in rows if r_[3].startswith("voto:") and r_[4] != r_[5])
    POR_ANO_DIV = "; ".join(f"{k}: {v}" for k, v in tipos.most_common())
    cego = {(x["video_id"], x["item_id"]): x for x in json.load(open(f"{D}/amostra_cega.json"))}
    pdir = collections.defaultdict(list)
    for r_ in rows:
        if r_[3].startswith("voto:") and r_[4] != r_[5]:
            cx = cego.get((r_[1], r_[2]), {}); pdir[r_[3][5:]].append(f"RD {cx.get('reuniao')} ({cx.get('data')}) item {r_[2]}: {r_[4]}→{r_[5]}")
    POR_DIR = ["", "## Discordâncias por diretor", ""] + [f"- **{k}** ({len(v)}): " + "; ".join(v) for k, v in sorted(pdir.items(), key=lambda x: -len(x[1]))]
    POR_ANO = ", ".join(f"{a}: {100*k/t:.0f}% ({k}/{t})" for a, (k, t) in sorted(pa.items()))
    pc = lambda a, b: f"{100*n[a]/n[b]:.1f}% ({n[a]}/{n[b]})" if n[b] else "n/d"
    md = [f"# Conferência por amostra das análises ({RD.replace('_','–',1)})", "", f"Método: sorteio com semente fixa ({CFG['reun']} reuniões por ano, 3 itens por reunião com ≥ 3 votos); subagentes independentes releram a transcrição **sem ver a análise original** e extraíram relator, tipo de resultado e voto por diretor. Concordância:", "",
          f"- Relator: **{pc('relator_ok','relator_total')}**", f"- Resultado (unânime/maioria/vista/outro): **{pc('resultado_ok','resultado_total')}**", f"- Voto por diretor (categoria): **{pc('voto_ok','voto_total')}** · não localizado na conferência: {n['voto_nao_localizado']}", f"- Itens não encontrados na conferência: {n['item_nao_encontrado']}", "",
          "Divergências por item em `conferencia_amostra.csv`. Concordância baixa em votos de quem apenas «acompanha o relator» é esperada: a legenda não identifica falantes. Use estes números como taxa de concordância ao responder sobre os anos desta rodada.", "", "**Limites do método:** a conferência usa a mesma legenda automática e o mesmo tipo de modelo da análise original, então mede consistência (reprodutibilidade), não verdade absoluta; erros de ASR que enganam os dois leitores passam. A maior fonte de discordância é «acompanha» na análise × «voto não localizado» na conferência (a legenda não registra a fala do diretor), e os pedidos de vista/«outros» classificados de forma diferente.", "", "Taxa de voto por ano: " + POR_ANO, "", "Tipos de discordância (análise→conferência): " + POR_ANO_DIV + ". «vista→acompanha» = diretor que pediu vista e depois apresentou voto-vista convergente: a análise registra «vista», a conferência «acompanha». Desde 06/11/2026 o gabarito trata «voto-vista» como acompanha/diverge (convenção única); só quem apenas pediu vista fica «vista»."]
    open(f"{QD}/{CFG['rel']}.md", "w").write("\n".join(md + POR_DIR) + "\n"); print("\n".join(md[4:9]))
{"sortear": sortear, "comparar": comparar}[sys.argv[1]]()
