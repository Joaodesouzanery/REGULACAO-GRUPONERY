"""Cruza as análises (vídeos) com as atas oficiais. Uso: bash pipeline/ag.sh anm python3 pipeline/cruzar_atas.py
Entrada: data/atas/indice_atas.json (tipo ROP/REP, numero, data, itens[id, relator, resultado]).
Saída: agencias/<ag>/qualidade/cruzamento_atas.md (+ .csv) e data/atas/datas_oficiais.json (video_id -> data da ata).
Compara: data da sessão, itens com o mesmo número, relator e resultado (unânime/maioria/vista/retirado)."""
import json, glob, re, os, csv, collections, unicodedata
AG = os.environ.get("AGENCIA", "antt")
A = {(a["tipo"], int(a["numero"])): a for a in json.load(open("data/atas/indice_atas.json")) if a.get("numero")}
V = {json.loads(l)["id"]: json.loads(l) for l in open("data/videos.jsonl")}
norm = lambda s: unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
def chave(vid, r):
    t = norm(V.get(vid, {}).get("titulo", "")) + " " + norm(str(r.get("numero")))
    tipo = "REP" if "extraord" in t else "ROP"
    m = re.search(r"(\d+)\s*[aoªº]?\s*(reuniao|rop|rep|ordin|extraord)", t) or re.search(r"(\d+)", norm(str(r.get("numero"))))
    return (tipo, int(m.group(1))) if m else None
def res(s):
    s = norm(s)
    return "retirado" if "retir" in s else "vista" if "vista" in s and "voto-vista" not in s and "voto vista" not in s else "maioria" if "maioria" in s or "vencid" in s else "unanime" if "unanim" in s else "outro"
def sobren(s): return (norm(re.sub(r"\(.*", "", s or "")).split() or [""])[-1][:5]
n = collections.Counter(); rows = []; datas = {}; casadas = set()
for f in sorted(glob.glob("data/analise/*.analise.json")):
    vid = os.path.basename(f).split(".")[0]; d = json.load(open(f)); r = d["reuniao"]; k = chave(vid, r)
    if not k or k not in A: n["sem_ata"] += 1; rows.append([vid, r.get("numero"), r.get("data"), "", "", "sem ata correspondente", "", "", ""]); continue
    a = A[k]; casadas.add(k); n["reunioes"] += 1
    dv, da = str(r.get("data") or ""), str(a.get("data") or "")
    n["data_ok"] += dv == da; datas[vid] = da
    ia = {re.sub(r"\s", "", x["id"]): x for x in a.get("itens", []) if x.get("id")}
    for it in d["itens"]:
        x = ia.get(re.sub(r"\s", "", str(it.get("id"))))
        if not x: continue
        n["itens"] += 1
        ok_r = res(it.get("resultado")) == x.get("resultado") or (x.get("resultado") == "unanime" and res(it.get("resultado")) == "unanime")
        n["res_ok"] += ok_r
        if x.get("relator"): n["rel_tot"] += 1; ok_rel = bool({w for w in norm(re.sub(r"\(.*", "", it.get("relator") or "")).split() if len(w) > 3} & set(norm(x["relator"]).split())); n["rel_ok"] += ok_rel
        else: ok_rel = None
        if not ok_r or ok_rel is False: rows.append([vid, r.get("numero"), dv, f"{k[0]} {k[1]}", da, it.get("id"), f"{res(it.get('resultado'))} / {x.get('resultado')}", f"{it.get('relator')} / {x.get('relator')}", ""])
faltam = sorted(k for k in A if k not in casadas)
os.makedirs(f"agencias/{AG}/qualidade", exist_ok=True)
with open(f"agencias/{AG}/qualidade/cruzamento_atas.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["video_id", "numero_analise", "data_analise", "ata", "data_ata", "item", "resultado analise/ata", "relator analise/ata", "obs"]); w.writerows(rows)
json.dump(datas, open("data/atas/datas_oficiais.json", "w"), indent=1)
pc = lambda a, b: f"{100*n[a]/n[b]:.1f}% ({n[a]}/{n[b]})" if n[b] else "n/d"
md = [f"# Cruzamento com as atas oficiais — {AG.upper()}", "",
      f"Atas no índice: {len(A)} · reuniões analisadas casadas com ata: {n['reunioes']} · análises sem ata correspondente: {n['sem_ata']} · atas sem vídeo analisado: {len(faltam)} ({', '.join(f'{t} {k}' for t, k in faltam[:30])}{'…' if len(faltam) > 30 else ''})", "",
      f"- Data da sessão igual à da ata: **{pc('data_ok','reunioes')}** (as diferentes são corrigidas pela ata: `data/atas/datas_oficiais.json`)",
      f"- Itens casados pelo número: {n['itens']}",
      f"- Resultado igual (unânime/maioria/vista/retirado): **{pc('res_ok','itens')}**",
      f"- Relator igual: **{pc('rel_ok','rel_tot')}**", "",
      "A ata é oficial, mas não traz placar nominal: «aprovado por unanimidade dos diretores presentes»; nas maiorias costuma nomear quem divergiu. Divergências item a item em `cruzamento_atas.csv`. Atas de 2019–2020 têm formato irregular e algumas foram lidas por OCR."]
open(f"agencias/{AG}/qualidade/cruzamento_atas.md", "w").write("\n".join(md) + "\n"); print("\n".join(md))
