"""Perfis de dirigentes (diretores e superintendentes): fonte canônica em data/<ag>/dirigentes/<slug>.json (+ <slug>.jpg).
Uso: python3 pipeline/dirigentes.py migrar   (cria a pasta a partir de bios.json/superintendentes.json e das fotos atuais)
     python3 pipeline/dirigentes.py gerar    (regera bios.json e superintendentes.json a partir da pasta — rodar após qualquer mudança)
     python3 pipeline/dirigentes.py faltas   (quem vota/é atual e não tem perfil, foto ou formação)
Status: «ativo» | «ex-dirigente» (nunca apagar: arquivar com data_saida)."""
import sys, os, json, re, glob, shutil, unicodedata
AGS = {"antt": "data", "anm": "data/anm", "antaq": "data/antaq"}
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")
ld = lambda p: json.load(open(p)) if os.path.exists(p) else []
cmd = sys.argv[1] if len(sys.argv) > 1 else "faltas"
for ag, D in AGS.items():
    P = f"{D}/dirigentes"
    if cmd == "migrar":
        os.makedirs(P, exist_ok=True)
        for tipo, arq in (("diretor", "bios.json"), ("superintendente", "superintendentes.json")):
            for b in ld(f"{D}/{arq}"):
                nome = b.get("diretor") or b.get("nome"); s = slug(nome); dst = f"{P}/{s}.json"
                atual = json.load(open(dst)) if os.path.exists(dst) else {}
                atual.update({k: v for k, v in b.items() if v not in (None, "", [])}); atual.setdefault("tipo", tipo); atual["nome_chave"] = nome
                atual.setdefault("status", "ativo")
                for f in [b.get("foto"), f"docs/marca/diretores/{ag}/{s}.jpg"]:
                    if f and os.path.exists(f) and not os.path.exists(f"{P}/{s}.jpg"): shutil.copy(f, f"{P}/{s}.jpg")
                if os.path.exists(f"{P}/{s}.jpg"): atual["foto"] = f"{P}/{s}.jpg"
                json.dump(atual, open(dst, "w"), ensure_ascii=False, indent=1)
        print(ag, len(glob.glob(f"{P}/*.json")), "perfis")
    elif cmd == "gerar":
        perf = [json.load(open(f)) for f in sorted(glob.glob(f"{P}/*.json"))]
        bios = [dict(p, diretor=p["nome_chave"]) for p in perf if p.get("tipo") == "diretor"]
        sups = [dict(p, nome=p["nome_chave"]) for p in perf if p.get("tipo") == "superintendente"]
        json.dump(bios, open(f"{D}/bios.json", "w"), ensure_ascii=False, indent=1)
        json.dump(sups, open(f"{D}/superintendentes.json", "w"), ensure_ascii=False, indent=1)
        print(ag, len(bios), "diretores,", len(sups), "superintendentes")
    else:
        sys.path.insert(0, "pipeline"); import previsao
        board, _ = previsao.colegiado_atual(previsao.conn(ag), 3)
        perf = {json.load(open(f))["nome_chave"]: json.load(open(f)) for f in glob.glob(f"{P}/*.json")}
        for d in board:
            p = perf.get(d)
            if not p: print(f"{ag}: ⚠️ {d} sem perfil → pesquisador-dirigentes"); continue
            falta = [k for k in ("formacao", "minibio", "foto") if not p.get(k)]
            if falta: print(f"{ag}: {d} sem {', '.join(falta)}")
            elif p.get("foto") and os.path.exists(p["foto"]):
                from PIL import Image
                w, h = Image.open(p["foto"]).size
                if min(w, h) < 600: print(f"{ag}: {d} foto fraca ({w}×{h} px; mínimo 600) → pesquisador-dirigentes buscar a maior oficial")
