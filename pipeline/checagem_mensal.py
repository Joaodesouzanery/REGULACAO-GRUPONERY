"""Checagem do dia 1 (rodar em outro chat todo mês): o que mudou ou precisa conferir na diretoria de cada agência.
Uso: python3 pipeline/checagem_mensal.py [antt anm antaq]
Mostra: quem votou nas últimas reuniões e não está em mandatos/bios (substituto novo?), mandatos que vencem em 90 dias,
vagas abertas, diretores sem minibio/formação/foto, superintendentes ausentes e idade da última verificação."""
import sys, os, json, datetime, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao
H = datetime.date.today()
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")
for ag in (sys.argv[1:] or ["antt", "anm", "antaq"]):
    D = "data" if ag == "antt" else f"data/{ag}"
    c = previsao.conn(ag); board, ult = previsao.colegiado_atual(c, reunioes=3)
    mand = ld(f"{D}/mandatos.json", []); bios = {b["diretor"]: b for b in ld(f"{D}/bios.json", [])}
    nomes_m = {m.get("diretor") for m in mand}
    print(f"\n## {ag.upper()} — base até {ult}; em exercício: {', '.join(board)}")
    for d in board:
        if d not in nomes_m: print(f"- ⚠️ {d} vota mas não está em mandatos.json (substituto novo?)")
        b = bios.get(d, {})
        falta = [k for k in ("minibio", "formacao") if not b.get(k)] + ([] if b.get("foto") or os.path.exists(f"docs/marca/diretores/{ag}/{slug(d)}.jpg") else ["foto"])
        if falta: print(f"- {d}: falta {', '.join(falta)}")
        v = b.get("verificado_em")
        if v and (H - datetime.date.fromisoformat(v)).days > 35: print(f"- {d}: minibio verificada em {v} (> 35 dias)")
    for m in mand:
        f = m.get("fim") or m.get("fim_legal") or m.get("fim_mandato")
        try: dd = datetime.date.fromisoformat(str(f)[:10])
        except Exception: continue
        if H <= dd <= H + datetime.timedelta(days=90): print(f"- ⏳ mandato de {m['diretor']} termina em {dd:%d/%m/%Y}")
    for v in ld(f"{D}/vacancias.json", []):
        if not v.get("fim"): print(f"- 🔴 vaga aberta desde {v['inicio']}: {v['cadeira']} (interinos: {v.get('interinos')})")
    sups = ld(f"{D}/superintendentes.json", [])
    print(f"- superintendentes registrados: {len(sups)}" + ("" if sups else " — ⚠️ levantar (agente pesquisador-superintendentes)"))
print("\nDepois: pesquisar Senado/DOU/Agência iNFRA do mês (skill checagem-mensal), atualizar os JSON, rodar vacancias.py e relatorio_diretoria.py.")
