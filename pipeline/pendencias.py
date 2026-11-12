"""O que está pendente hoje na operação (usado pelos lembretes). Uso: python3 pipeline/pendencias.py"""
import os, json, subprocess, datetime, glob
H = datetime.date.today()
def ultimo_commit(pat):
    r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", pat], capture_output=True, text=True).stdout.strip()
    return datetime.date.fromisoformat(r) if r else None
print(f"# Pendências — {H:%d/%m/%Y}")
for ag, d in (("antt", "data"), ("anm", "data/anm"), ("antaq", "data/antaq")):
    u = ultimo_commit(f"{d}/transcricoes")
    if u and (H - u).days > 7: print(f"- {ag.upper()}: última coleta do Mac em {u:%d/%m} ({(H-u).days} dias) → rodar coletar_tudo_e_enviar.sh")
    V = [json.loads(l) for l in open(f"{d}/videos.jsonl")] if os.path.exists(f"{d}/videos.jsonl") else []
    sem = [v for v in V if v["tipo"] == "diretoria" and not v.get("duplicata_de") and not os.path.exists(f"{d}/transcricoes/{v['id']}.json")]
    nao = [v for v in V if v["tipo"] == "diretoria" and not v.get("duplicata_de") and os.path.exists(f"{d}/transcricoes/{v['id']}.json") and not os.path.exists(f"{d}/analise/{v['id']}.analise.json")]
    if sem: print(f"- {ag.upper()}: {len(sem)} reuniões sem texto (legenda/Whisper no Mac)")
    if nao: print(f"- {ag.upper()}: {len(nao)} reuniões com texto ainda não analisadas → skill lote-mac")
m = ultimo_commit("data/mandatos.json")
if H.day <= 7 and (not m or m.month != H.month): print("- Checagem mensal do dia 1 ainda não feita → skill checagem-mensal")
print("- (ok)" if False else "")
