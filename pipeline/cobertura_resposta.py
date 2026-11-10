"""Bloco «Cobertura desta resposta» — rodar antes de TODA resposta sobre diretor/assunto.
Uso: python3 pipeline/cobertura_resposta.py <agencia> [diretor] [tema] [AAAA-AAAA]
Diz: o que existe no canal × o que tem texto × o que foi analisado (período), presença do diretor,
lacunas (sem legenda, Whisper pendente, anos não analisados, datas de upload) e a taxa da conferência cega."""
import sys, os, json, re, glob, sqlite3, collections
ag = (sys.argv[1] if len(sys.argv) > 1 else "antt").lower()
dire = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None
tema = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None
per = sys.argv[4] if len(sys.argv) > 4 else None
D = "data" if ag == "antt" else f"data/{ag}"
if not os.path.exists(f"{D}/videos.jsonl"):
    print(f"**Cobertura desta resposta:** a agência {ag.upper()} ainda NÃO está na base — não temos dados para responder."); sys.exit()
a0, a1 = (per.split("-") + [per])[:2] if per else ("0000", "9999")
V = [json.loads(l) for l in open(f"{D}/videos.jsonl")]
V = [v for v in V if not v.get("duplicata_de") and v["tipo"] != "outro" and a0 <= (v.get("data") or "")[:4] <= a1]
tx = lambda v: os.path.exists(f"{D}/transcricoes/{v['id']}.json")
an = lambda v: os.path.exists(f"{D}/analise/{v['id']}.analise.json") or os.path.exists(f"{D}/analise_eventos/{v['id']}.evento.json")
c = collections.Counter(); anos_falt = collections.Counter(); sem = []
for v in V:
    t = "reuniões de diretoria" if v["tipo"] == "diretoria" else "eventos (audiências/participativas/workshops)"
    c[(t, "canal")] += 1; c[(t, "texto")] += tx(v); c[(t, "analisado")] += an(v)
    if tx(v) and not an(v): anos_falt[(t, (v.get("data") or "????")[:4])] += 1
    if not tx(v): sem.append(v)
L = ["**Cobertura desta resposta** (" + ag.upper() + (f", {per}" if per else ", todos os anos") + "):"]
for t in ("reuniões de diretoria", "eventos (audiências/participativas/workshops)"):
    if c[(t, "canal")]: L.append(f"- {t}: {c[(t,'canal')]} no canal · {c[(t,'texto')]} com texto · **{c[(t,'analisado')]} analisadas**")
falt = collections.defaultdict(list)
for (t, a), n in sorted(anos_falt.items()): falt[t].append(f"{a}: {n}")
for t, xs in falt.items(): L.append(f"- ⚠️ {t} com texto ainda NÃO analisadas — " + ", ".join(xs) + " (a resposta não inclui esses anos/eventos)")
if sem:
    wh = set()
    for f in glob.glob(f"{D}/sem_legenda.jsonl"):
        wh |= {json.loads(l)["id"] for l in open(f) if l.strip()}
    L.append(f"- Sem texto: {len(sem)} vídeos (privados, sem legenda ou aguardando Whisper no Mac) — ver sem_transcricao.md")
db = "data/regulacao.db" if ag == "antt" else f"{D}/regulacao.db"
if os.path.exists(db) and dire:
    k = sqlite3.connect(db)
    q = "select count(distinct r.id), count(*), min(r.data), max(r.data) from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id where v.diretor=? and substr(r.data,1,4) between ? and ?"
    a = [dire, a0, a1]
    if tema: q += " and v.item_id in (select item_id from item_temas where tema=?)"; a.append(tema)
    nr, nv, d0, d1 = k.execute(q, a).fetchone()
    L.append(f"- {dire}: {nv} votos em {nr} reuniões" + (f" ({d0} a {d1})" if nr else " — **sem votos na base neste recorte**") + (f" no tema «{tema}»" if tema else ""))
    up = sum(1 for (o,) in k.execute("select r.video_id from reunioes r join itens i on i.reuniao_id=r.id join votos v on v.item_id=i.id where v.diretor=? group by r.id", [dire])
             if os.path.exists(f"{D}/analise/{o}.analise.json") and re.search(r"upload", json.dumps(json.load(open(f"{D}/analise/{o}.analise.json")).get("reuniao", {}), ensure_ascii=False), re.I))
    if up: L.append(f"- {up} dessas reuniões têm data tirada do upload do vídeo (pode diferir da sessão em dias/semanas)")
QUAL = {"antt": "voto por diretor ≈ 94–95% (2019 mais fraco), relator/resultado 93–100%",
        "anm": "voto ≈ 96% em 2021–2026 (2019–2020 só como índice); resultado 97,9% contra as atas oficiais",
        "antaq": "voto 92,3%, relator e resultado 100% (2019–2026)"}
L.append(f"- Conferência cega: {QUAL.get(ag, 'ainda não feita')} — mede consistência, não verdade absoluta. Legenda automática: nomes e valores podem errar; itens sigilosos e voto escrito completo (SEI) não estão nos vídeos.")
print("\n".join(L))
