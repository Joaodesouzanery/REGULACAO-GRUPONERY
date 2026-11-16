"""Quadro comparativo de transparência e facilidade das agências (skill transparencia-agencias).
Lê data/<ag>/transparencia.json (notas do agente auditor-transparencia) + números da base e escreve docs/transparencia_agencias.md.
Uso: python3 pipeline/transparencia.py"""
import os, json, glob, datetime, collections
AGS = [("antt", "data"), ("anm", "data/anm"), ("antaq", "data/antaq"), ("aneel", "data/aneel"), ("anp", "data/anp")]
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d


def base(ag, d):
    if not os.path.exists(f"{d}/videos.jsonl"): return None
    V = [json.loads(l) for l in open(f"{d}/videos.jsonl")]
    V = [v for v in V if v.get("tipo") == "diretoria" and not v.get("duplicata_de") and (v.get("data") or "9") >= "2018"]
    tx = sum(os.path.exists(f"{d}/transcricoes/{v['id']}.json") for v in V)
    cal = ld(f"{d}/calendario.json", [])
    return {"videos": len(V), "legenda_pct": round(100 * tx / max(len(V), 1)), "calendario": bool(cal), "pautas": len(glob.glob(f"{d}/pautas/*.json"))}


L = [f"# Transparência e facilidade de acompanhar as agências — {datetime.date.today():%d/%m/%Y}", "",
     "Notas 0–2 por critério (0 = não existe/não funciona; 1 = parcial; 2 = completo e fácil), com evidência em `data/<ag>/transparencia.json`. Gerado por `python3 pipeline/transparencia.py`.", ""]
crit, linhas = [], []
for ag, d in AGS:
    t = ld(f"{d}/transparencia.json", {}); b = base(ag, d)
    notas = {c["nome"]: c["nota"] for c in t.get("criterios", [])}
    for c in notas:
        if c not in crit: crit.append(c)
    linhas.append((ag, notas, b))
L += ["| Agência | " + " | ".join(crit) + " | Total | Vídeos de diretoria 2018+ | % com legenda | Calendário na base | Pautas baixadas |", "|---" * (len(crit) + 6) + "|"]
rank = []
for ag, notas, b in linhas:
    tot = sum(notas.values()) if notas else None
    rank.append((tot or -1, ag))
    L.append(f"| {ag.upper()} | " + " | ".join(str(notas.get(c, "—")) for c in crit) + f" | {tot if tot is not None else '—'}/{2 * len(crit) if crit else '—'} | "
             + (f"{b['videos']} | {b['legenda_pct']}% | {'sim' if b['calendario'] else 'não'} | {b['pautas']} |" if b else "— | — | — | — |"))
L += ["", "## Ranking", ""] + [f"{k + 1}. {ag.upper()} ({t if t >= 0 else 'sem avaliação'})" for k, (t, ag) in enumerate(sorted(rank, reverse=True))]
L += ["", "## Evidências", ""]
for ag, d in AGS:
    t = ld(f"{d}/transparencia.json", {})
    if not t: continue
    L += [f"### {ag.upper()}"] + [f"- **{c['nome']}** ({c['nota']}): {c['evidencia']} — {c.get('fonte') or 'base interna'}" for c in t.get("criterios", [])] + ([f"- Observações: {t['observacoes']}"] if t.get("observacoes") else []) + [""]
open("docs/transparencia_agencias.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[:12 + len(linhas)]))
