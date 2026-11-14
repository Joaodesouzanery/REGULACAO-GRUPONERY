"""O que está pendente hoje na operação (usado pelos lembretes). Uso: python3 pipeline/pendencias.py"""
import os, json, subprocess, datetime, glob
H = datetime.date.today()
def ultimo_commit(pat):
    r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", pat], capture_output=True, text=True).stdout.strip()
    return datetime.date.fromisoformat(r) if r else None
print(f"# Pendências — {H:%d/%m/%Y}")
for ag, d in (("antt", "data"), ("anm", "data/anm"), ("antaq", "data/antaq")):
    u = ultimo_commit(f"{d}/transcricoes")
    if u and (H - u).days > 7: print(f"- {ag.upper()}: última coleta do Mac em {u:%d/%m} ({(H-u).days} dias) → rodar no Mac: caffeinate -i bash pipeline/coletar_todas.sh")
    V = [json.loads(l) for l in open(f"{d}/videos.jsonl")] if os.path.exists(f"{d}/videos.jsonl") else []
    sem = [v for v in V if v["tipo"] == "diretoria" and not v.get("duplicata_de") and not os.path.exists(f"{d}/transcricoes/{v['id']}.json")]
    nao = [v for v in V if v["tipo"] == "diretoria" and not v.get("duplicata_de") and os.path.exists(f"{d}/transcricoes/{v['id']}.json") and not os.path.exists(f"{d}/analise/{v['id']}.analise.json")]
    if sem: print(f"- {ag.upper()}: {len(sem)} reuniões sem texto (legenda/Whisper no Mac)")
    if nao: print(f"- {ag.upper()}: {len(nao)} reuniões com texto ainda não analisadas → skill lote-mac")
m = ultimo_commit("data/mandatos.json")
if H.day <= 7 and (not m or m.month != H.month): print("- Checagem mensal do dia 1 ainda não feita → skill checagem-mensal")
# Proposta 2: pautas, alertas, boletins, contratos
for ag, d in (("antt", "data"), ("anm", "data/anm"), ("antaq", "data/antaq")):
    cal = json.load(open(f"{d}/calendario.json")) if os.path.exists(f"{d}/calendario.json") else []
    prox = [c for c in cal if 0 <= (datetime.date.fromisoformat(c["data"]) - H).days <= 10]
    for c in prox:
        pj = f"{d}/pautas/{c['reuniao']}.json"
        pa = json.load(open(pj)) if os.path.exists(pj) else {}
        if not pa.get("itens"): print(f"- {ag.upper()} {c['reuniao']}ª em {c['data']}: pauta ainda não baixada/publicada → python3 pipeline/pautas.py {ag}")
        for e in glob.glob("clientes/*/*/empresa.json"):
            emp = json.load(open(e)); pasta = os.path.dirname(e)
            if ag in emp.get("agencias", []) and not os.path.exists(f"{pasta}/alerta_{ag}_{c['reuniao']}.pdf"):
                print(f"- Alerta pré-pauta não gerado: {emp['nome'][:40]} · {ag.upper()} {c['reuniao']}ª → python3 pipeline/alerta_pauta.py {pasta} --agencia {ag}")
    if not cal and ag != "antt": print(f"- {ag.upper()}: sem calendário oficial em {d}/calendario.json")
mes_ant = (H.replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m")
for ag in ("antt", "anm", "antaq"):
    if H.day >= 3 and not os.path.exists(f"agencias/{ag}/boletins/boletim_{ag}_{mes_ant}.pdf"):
        print(f"- Boletim {ag.upper()} de {mes_ant} não gerado → python3 pipeline/boletim.py {ag} {mes_ant}")
for f in glob.glob("clientes/*/contrato.json"):
    ct = json.load(open(f))
    for k, rot in (("fim_vigencia", "renovação"), ("data_reajuste", "reajuste")):
        if ct.get(k) and 0 <= (datetime.date.fromisoformat(ct[k]) - H).days <= 60:
            print(f"- Contrato {os.path.dirname(f)}: {rot} em {ct[k]} → skill contratos")
