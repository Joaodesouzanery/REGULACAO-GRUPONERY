"""Carrega data/analise/*.analise.json em data/regulacao.db (tabelas de schema2.sql) e normaliza diretores, temas e categorias de voto."""
import json, glob, re, sqlite3, os
DIRETORES = ["Guilherme Sampaio", "Felipe Queiroz", "Lucas Asfor", "Alex Azevedo", "Marcelo Fonseca", "Alessandro Baumgarten", "Amaral Filho", "Severino Medeiros"]
ALIAS = {"Amaral Filho": r"amaral", "Guilherme Sampaio": r"guilherme", "Felipe Queiroz": r"felipe", "Lucas Asfor": r"lucas",
         "Alex Azevedo": r"alex", "Marcelo Fonseca": r"marcelo", "Alessandro Baumgarten": r"alessandro", "Severino Medeiros": r"severino"}
def canon(s):
    s = (s or "").lower()
    for n, rx in ALIAS.items():
        if re.search(rx, s): return n
    return None
TEMAS = [  # (tema normalizado, regex sobre as tags livres do item)
    ("onibus", r"ônibus|passageiros|fretamento|autorizaç(ão|ões) de mercado|TAR\b"),
    ("cargas", r"cargas|frete|RNTRC|CIOT"),
    ("concessoes_rodoviarias", r"concess(ão|ões) rodovi|ato de outorga|transfer[êe]ncia de controle"),
    ("pedagio_freeflow", r"pedágio|free flow|tarifa"),
    ("reequilibrio_contratual", r"reequil|fator D|revis(ão|ões) (extra)?ordin|termo aditivo|idoneidade"),
    ("ferrovias", r"ferrov|ISF|saturaç|autorização ferroviária|interoperab"),
    ("fiscalizacao_sancoes", r"fiscaliza|sanç|cautelar|cassa|reincid|infraç"),
    ("sandbox_inovacao", r"sandbox|inovaç"),
    ("participacao_social", r"participa[çc]ão social|audi[êe]ncia"),
    ("leilao_otimizacao", r"leil[ãa]o|otimiza|solução consensual|processo competitivo|relicita"),
    ("sustentabilidade", r"sustentab|ESG|ambient|PSI"),
    ("institucional", r"institucional|governan|procedimento|inova[çc]ão\b.*interna|regimento"),
    ("regulacao_normativa", r"regula[çc]ão normativa|resolu"),
    ("judicializacao", r"judicial|STF|TRF"),
]
def temas_de(it):
    tags = it.get("tema") or []
    if isinstance(tags, str): tags = [tags]
    txt = " | ".join(tags)
    out = {n for n, rx in TEMAS if re.search(rx, txt, re.I)}
    return sorted(out) or ["outros"]
def categoria(v, relator):
    s = (v.get("voto") or "").lower()
    if "não captado" in s: return "nao_captado"
    if "pede vista" in s or s.strip() == "pede vista": return "vista"
    if "vencido" in s: return "vencido"
    if "voto-vista" in s or "revisor" in s:
        return "revisor_diverge" if "diverg" in s else "revisor_acompanha"
    if "relator" in s and canon(v["diretor"]) == relator and not s.startswith("acompanha"): return "relator"
    if re.search(r"mant[ée]m o voto", s): return "relator"
    if re.search(r"acompanh|de acordo|adere|ades[ãa]o|sigo|voto com|vota pelo|apoia|proclama", s): return "acompanha"
    return "outro"
db = "data/regulacao.db"
if os.path.exists(db): os.remove(db)
c = sqlite3.connect(db); c.executescript(open("pipeline/schema2.sql").read())
n_it = n_v = 0
for f in sorted(glob.glob("data/analise/*.analise.json")):
    d = json.load(open(f)); r = d["reuniao"]
    cur = c.execute("INSERT INTO reunioes(video_id,numero,data,presidente,formato,observacoes) VALUES(?,?,?,?,?,?)",
        (d["meta"]["video_id"], r["numero"], r["data"], canon(r.get("presidente_da_sessao")), r.get("formato"), " | ".join(r.get("observacoes", []))))
    rid = cur.lastrowid
    pres = {canon(x) for x in r.get("diretores_presentes", [])}
    aus = {canon(x) for x in r.get("ausentes", [])}
    for dn in DIRETORES:
        if dn in pres: c.execute("INSERT INTO presenca VALUES(?,?,1)", (rid, dn))
        elif dn in aus: c.execute("INSERT INTO presenca VALUES(?,?,0)", (rid, dn))
    for it in d["itens"]:
        rel_txt = it.get("relator", "")
        rel = canon(rel_txt.split(";")[0].split("(")[0]) if rel_txt else None
        rev = canon(rel_txt.split("revisor:")[1]) if "revisor:" in rel_txt else None
        res = it.get("resultado", "")
        unan = 1 if "unanim" in res.lower() else 0
        cur = c.execute("INSERT INTO itens(reuniao_id,item,ts,processo,interessado,assunto,relator,relator_texto,revisor,resultado,unanime,resumo) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (rid, it["id"], it.get("ts"), it.get("processo"), it.get("interessado"), it["assunto"], rel, rel_txt, rev, res, unan, it.get("resumo_voto")))
        iid = cur.lastrowid; n_it += 1
        for t in temas_de(it): c.execute("INSERT INTO item_temas VALUES(?,?)", (iid, t))
        just = []
        for v in it.get("votos", []):
            dn = canon(v["diretor"])
            if not dn: continue
            cat = categoria(v, rel)
            c.execute("INSERT INTO votos(item_id,diretor,voto,categoria,ts,justificativa,tom,confianca,eh_relator) VALUES(?,?,?,?,?,?,?,?,?)",
                (iid, dn, v["voto"], cat, v.get("ts"), v.get("justificativa"), v.get("tom"), v.get("confianca"), 1 if dn == rel and cat == "relator" else 0))
            n_v += 1; just.append(f"{dn}: {v.get('justificativa') or ''}")
        c.execute("INSERT INTO busca VALUES(?,?)", (iid, " ".join(filter(None, [it["assunto"], it.get("interessado"), it.get("resumo_voto"), " ".join(just)]))))
# trechos literais (janelas de ~30 s) de todas as reuniões de diretoria com transcrição, para citar a frase exata com link no minuto
vids = {}
for l in open("data/videos.jsonl"):
    v = json.loads(l)
    if v["tipo"] != "outro" and not v.get("duplicata_de"): vids[v["id"]] = v
n_tr = 0
c.execute("DROP TABLE IF EXISTS videos"); c.execute("CREATE TABLE videos(id TEXT PRIMARY KEY, titulo TEXT, tipo TEXT, data TEXT)")
for v in vids.values(): c.execute("INSERT INTO videos VALUES(?,?,?,?)", (v["id"], v["titulo"], v["tipo"], v.get("data")))
c.execute("DROP TABLE IF EXISTS mandatos"); c.execute("CREATE TABLE mandatos(diretor TEXT, cargo TEXT, inicio TEXT, fim TEXT, situacao TEXT, fonte TEXT, confianca TEXT, verificar TEXT)")
if os.path.exists("data/mandatos.json"):
    for m in json.load(open("data/mandatos.json")): c.execute("INSERT INTO mandatos VALUES(?,?,?,?,?,?,?,?)", tuple(m.get(k) for k in ("diretor","cargo","inicio","fim","situacao","fonte","confianca","verificar")))
for vid in vids:
    f = f"data/transcricoes/{vid}.json"
    if not os.path.exists(f): continue
    buf, t0 = [], None
    for sg in json.load(open(f)):
        x = re.sub(r"\[[^\]]*\]|>>", " ", sg["x"]).strip()
        if not x: continue
        if t0 is None: t0 = int(sg["t"])
        buf.append(x)
        if sg["t"] - t0 >= 30:
            c.execute("INSERT INTO trechos(video_id,t,texto) VALUES(?,?,?)", (vid, t0, " ".join(buf))); n_tr += 1; buf, t0 = [], None
    if buf: c.execute("INSERT INTO trechos(video_id,t,texto) VALUES(?,?,?)", (vid, t0, " ".join(buf))); n_tr += 1
c.execute("INSERT INTO trechos_fts(rowid, texto) SELECT id, texto FROM trechos")
c.commit(); print(n_tr, "trechos;", c.execute("select count(*) from reunioes").fetchone()[0], "reuniões,", n_it, "itens,", n_v, "votos")
