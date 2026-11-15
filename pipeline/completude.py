"""Painel de COMPLETUDE de todas as agências (2018+): vídeos, diretoria, mandatos, agenda, prazos, comparativa,
processos de clientes e qualidade. Gera COMPLETUDE.md e imprime a tabela. Uso: python3 pipeline/completude.py"""
import os, json, glob, sqlite3, datetime, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
H = datetime.date.today().isoformat(); DESDE = "2018-01-01"
AGS = [("antt", "data"), ("anm", "data/anm"), ("antaq", "data/antaq"), ("aneel", "data/aneel"), ("anp", "data/anp")]
ld = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
L = [f"# Completude da base — {datetime.date.today():%d/%m/%Y}", "", "Recorte 2018 em diante. Gerado por `python3 pipeline/completude.py` (skill completude).", ""]
lin = []
for ag, d in AGS:
    if not os.path.exists(f"{d}/videos.jsonl"):
        lin.append((ag, None)); continue
    V = [json.loads(l) for l in open(f"{d}/videos.jsonl")]
    V = [v for v in V if not v.get("duplicata_de") and v["tipo"] != "outro" and (not v.get("data") or v["data"] >= DESDE)]
    tx = lambda v: os.path.exists(f"{d}/transcricoes/{v['id']}.json")
    an = lambda v: os.path.exists(f"{d}/analise/{v['id']}.analise.json") or os.path.exists(f"{d}/analise_eventos/{v['id']}.evento.json")
    dire = [v for v in V if v["tipo"] == "diretoria"]; ev = [v for v in V if v["tipo"] != "diretoria"]
    r = {"dir": (len(dire), sum(map(tx, dire)), sum(map(an, dire))), "ev": (len(ev), sum(map(tx, ev)), sum(map(an, ev)))}
    db = f"{d}/regulacao.db"
    if os.path.exists(db):
        c = sqlite3.connect(db)
        r["itens"] = c.execute("select count(*) from itens i join reunioes r on r.id=i.reuniao_id where r.data>=?", (DESDE,)).fetchone()[0]
        r["votos"] = c.execute("select count(*) from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where r.data>=?", (DESDE,)).fetchone()[0]
        r["periodo"] = c.execute("select min(data), max(data) from reunioes where data>=?", (DESDE,)).fetchone()
    # diretoria e perfis
    perf = [json.load(open(f)) for f in glob.glob(f"{d}/dirigentes/*.json")]
    import previsao
    try: atuais = set(previsao.colegiado_atual(previsao.conn(ag))[0])
    except Exception: atuais = set()
    dirs = [p for p in perf if p.get("tipo") == "diretor" and (p.get("nome_chave") in atuais or not atuais)]; sups = [p for p in perf if p.get("tipo") == "superintendente"]
    def foto_ok(p):
        f = p.get("foto")
        if not f or not os.path.exists(f): return False
        try:
            from PIL import Image; return min(Image.open(f).size) >= 600
        except Exception: return False
    r["dirig"] = (len(dirs), sum(map(foto_ok, dirs)), sum(1 for p in dirs if p.get("formacao")), sum(1 for p in dirs if p.get("minibio")))
    r["sups"] = (len(sups), sum(map(foto_ok, sups)))
    M = ld(f"{d}/mandatos.json", []); atu = [m for m in M if not m.get("fim") or m.get("fim", "") >= H]
    r["mand"] = (len(atu), sum(1 for m in atu if m.get("nomeacao_dou") or m.get("confirmado") == "sim" or m.get("confianca") == "alta"))
    r["vagas"] = sum(1 for v in ld(f"{d}/vacancias.json", []) if not v.get("fim"))
    cal = ld(f"{d}/calendario.json", []); fut = [x for x in cal if x["data"] >= H]
    r["agenda"] = (len(fut), max([x["data"] for x in cal], default="—"), sum(1 for f in glob.glob(f"{d}/pautas/*.json") if ld(f, {}).get("itens")))
    try:
        import prazos
        du = prazos.duracoes(ag) if os.path.exists(db) else {}
        mult = sum(1 for v in du.values() if v[2] > 1)
        tipos = len({v[1] for v in du.values()} & {t for t in {v[1] for v in du.values()} if prazos.estatistica(du, t)})
        r["prazo"] = (len(du), mult, tipos)
    except Exception: r["prazo"] = ("—", "—", "—")
    q = [f for f in glob.glob(f"{d}/qualidade/*") + glob.glob(f"agencias/{ag}/qualidade/*") if "conferencia" in f or os.path.isdir(f)]
    r["qual"] = len(q)
    lin.append((ag, r))
L += ["| Agência | Reuniões de diretoria (canal / texto / analisadas) | Eventos (canal / texto / analisados) | Itens · votos | Período | Diretoria em exercício (n / foto ≥600 / formação / minibio) | Superintendentes (n / foto) | Mandatos atuais (n / confirmados) · vagas | Agenda (próx. reuniões / calendário até / pautas baixadas) | Prazos (processos c/ nº / >1 sessão / tipos com base) | Rodadas de conferência cega |",
      "|---|---|---|---|---|---|---|---|---|---|---|"]
for ag, r in lin:
    if not r: L.append(f"| {ag.upper()} | não iniciada | | | | | | | | | |"); continue
    p = r.get("periodo") or ("—", "—")
    L.append(f"| {ag.upper()} | {'/'.join(map(str, r['dir']))} | {'/'.join(map(str, r['ev']))} | {r.get('itens', '—')} · {r.get('votos', '—')} | {p[0]} a {p[1]} | {'/'.join(map(str, r['dirig']))} | {'/'.join(map(str, r['sups']))} | {'/'.join(map(str, r['mand']))} · {r['vagas']} | {r['agenda'][0]} / {r['agenda'][1]} / {r['agenda'][2]} | {'/'.join(map(str, r['prazo']))} | {r['qual']} |")
# clientes (blocos 1 e 2): só contagem, sem dados do cliente
L += ["", "## Processos de clientes (blocos 1 e 2 — dependem do cliente informar o SEI)", ""]
for e in sorted(glob.glob("clientes/*/*/empresa.json")):
    pasta = os.path.dirname(e); pj = ld(f"{pasta}/processos.json", [])
    if "_prospeccao" in pasta: continue
    L.append(f"- {pasta.split('/')[1]}: processos com dados do SEI informados = {len(pj)}" + (" (a pedir ao cliente)" if not pj else ""))
L += ["", "## Como ler", "- Reuniões sem texto: privadas, sem legenda ou aguardando Whisper (Mac). Reuniões virtuais da ANTAQ não têm vídeo (só ata).",
      "- Prazos medem o tempo na diretoria (1ª sessão → decisão) só de processos com mais de uma sessão; o tempo na área técnica depende do SEI informado pelo cliente.",
      "- Agenda: calendário oficial cadastrado à mão a partir do PDF da agência; pautas baixadas quando publicadas."]
open("COMPLETUDE.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
