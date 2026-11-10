"""Lista os vídeos de um canal (abas /videos e /streams) -> data/videos.jsonl, com `tipo` e `prioridade`.
Uso: 01_coletar.py @canalANTT [anos]  (anos=0: sem corte; lê videos, streams, shorts e playlists; recupera data real dos sem data). Data vem do título (listagem 'flat' não traz upload_date).
Itens sem data no título são mantidos (data=null). Tudo o que não casa nenhum tipo vai como 'outro'."""
import json, re, sys, os, subprocess, datetime, unicodedata
canal = sys.argv[1]; anos = int(sys.argv[2]) if len(sys.argv) > 2 else 0
corte = datetime.date.today() - datetime.timedelta(days=365 * anos) if anos else datetime.date(1990, 1, 1)
TIPOS = [  # (tipo, prioridade, regex) — primeira que casar vence
    ("diretoria", 1, r"reuni[ãa]o.*diretoria|reuni[ãa]o p[úu]blica|sess[ãa]o deliberativa|\bRDP\b|board meeting|board of directors meeting|extraordinary board|diretoria colegiada"),
    ("audiencia", 2, r"audi[êe]ncias? p[úu]blicas?|public hearing|consulta p[úu]blica"),
    ("participativa", 3, r"reuni[ãa]o participativa|participatory meeting"),
    ("romeiros", 3, r"romeiros|caminho dos romeiros"),
    ("workshop", 4, r"workshop|chamamento|sandbox"),
]
DATA = re.compile(r"(\d{1,2})/(\d{1,2})/(\d{2,4})")
def tipo(t):
    for nome, pr, rx in TIPOS:
        if re.search(rx, t, re.I): return nome, pr
    return "outro", 9
def data(t):
    m = DATA.search(t)
    if not m: return None
    a, b, y = int(m[1]), int(m[2]), int(m[3]); y += 2000 if y < 100 else 0
    if re.search(r"board|participatory|hearing|extraordinary board", t, re.I): a, b = b, a  # inglês: mm/dd/aaaa
    try: return datetime.date(y, b, a)
    except ValueError: return None
def numero(t):  # chave p/ dedupe PT/EN de reunião de diretoria
    m = re.search(r"(?:n[ºo°]\.?|no\.?)\s*(\d{3,4})\b|\b(\d{3,4})ª", t, re.I)
    return m and (m[1] or m[2])
vistos, descartados = {}, []
def yt(url, fmt):
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "--print", fmt, url], capture_output=True, text=True)
    return [l for l in r.stdout.splitlines() if l.strip()]
def add(id_, titulo, dur, fonte):
    titulo = unicodedata.normalize("NFC", titulo)
    if id_ in vistos:
        vistos[id_].setdefault("fontes", []).append(fonte); return
    tp, pr = tipo(titulo); d = data(titulo)
    if d and d < corte: descartados.append((titulo, "antigo")); return
    vistos[id_] = {"id": id_, "titulo": titulo, "tipo": tp, "prioridade": pr, "data": str(d) if d else None,
                   "duracao": None if dur in ("NA", "") else int(float(dur)), "agencia": canal, "duplicata_de": None, "fontes": [fonte]}
# Aceita playlist no lugar do canal (ex.: ANM): descobre o canal dono da playlist e varre o canal INTEIRO + a playlist.
extra_pl = []
if os.path.exists("data/config_agencia.json"): extra_pl += json.load(open("data/config_agencia.json")).get("playlists", [])
if canal.startswith("PL") or "list=" in canal:
    pid0 = re.search(r"(PL[\w-]+)", canal).group(1); extra_pl.append(pid0)
    dono = yt(f"https://www.youtube.com/playlist?list={pid0}", "%(playlist_channel_id)s\t%(channel_url)s\t%(uploader_id)s")
    cid = next((x.split("\t")[0] for x in dono if x.split("\t")[0] not in ("", "NA")), None)
    canal = f"channel/{cid}" if cid else canal
    print("canal da playlist:", canal)
for aba in ("videos", "streams", "shorts"):
    for l in yt(f"https://www.youtube.com/{canal}/{aba}", "%(id)s\t%(title)s\t%(duration)s"):
        id_, titulo, dur = (l.split("\t") + ["", ""])[:3]; add(id_, titulo, dur, aba)
# playlists do canal (séries como Caminho dos Romeiros, audiências, cópias de reuniões)
for l in yt(f"https://www.youtube.com/{canal}/playlists", "%(id)s\t%(title)s"):
    pid, ptitulo = (l.split("\t") + [""])[:2]
    if not pid.startswith("PL"): continue
    for m in yt(f"https://www.youtube.com/playlist?list={pid}", "%(id)s\t%(title)s\t%(duration)s"):
        id_, titulo, dur = (m.split("\t") + ["", ""])[:3]
        add(id_, titulo, dur, "playlist:" + ptitulo)
        if id_ in vistos and vistos[id_]["tipo"] == "outro" and re.search(r"romeiros|reuni|audi[êe]ncia|workshop", ptitulo, re.I):
            vistos[id_]["tipo"], vistos[id_]["prioridade"] = tipo(ptitulo)  # classifica pelo nome da playlist
for pid in dict.fromkeys(extra_pl):
    for m in yt(f"https://www.youtube.com/playlist?list={pid}", "%(id)s\t%(title)s\t%(duration)s"):
        id_, titulo, dur = (m.split("\t") + ["", ""])[:3]; add(id_, titulo, dur, "playlist_informada:" + pid)
naplaylist = {v["id"] for v in vistos.values() if any(str(f).startswith("playlist_informada") for f in v.get("fontes", []))}
if naplaylist:
    fora = [v for v in vistos.values() if v["tipo"] == "diretoria" and v["id"] not in naplaylist]
    print(f"playlist informada: {len(naplaylist)} vídeos; reuniões de diretoria FORA dela no canal: {len(fora)}")
# data real (upload_date) só para os sem data no título e que não são «outro»
for v in vistos.values():
    if v["data"] or v["tipo"] == "outro": continue
    out = yt(f"https://www.youtube.com/watch?v={v['id']}", "%(upload_date)s")
    if out and re.fullmatch(r"\d{8}", out[0]):
        v["data"] = f"{out[0][:4]}-{out[0][4:6]}-{out[0][6:]}"; v["data_fonte"] = "upload_date"
# preserva vídeos já inventariados que não apareceram agora (nunca perder registro)
if os.path.exists("data/videos.jsonl"):
    for l in open("data/videos.jsonl"):
        o = json.loads(l)
        if o["id"] not in vistos: vistos[o["id"]] = o
# dedupe PT/EN: mesma reunião de diretoria (mesmo número) -> mantém a versão em português
por_num = {}
for v in vistos.values():
    if v["tipo"] == "diretoria" and (n := numero(v["titulo"])):
        extra = bool(re.search(r"extra", v["titulo"], re.I))
        parte = (re.search(r"parte\s*(\d+)|part\s*(\d+)", v["titulo"], re.I) or [None])[0]  # «Parte 1» e «Parte 2» não são duplicatas
        por_num.setdefault((n, extra, (parte or "").lower().replace("part ", "parte ")), []).append(v)
for grupo in por_num.values():
    grupo.sort(key=lambda v: bool(re.search(r"board|extraordinary", v["titulo"], re.I)))  # PT primeiro
    for v in grupo[1:]: v["duplicata_de"] = grupo[0]["id"]
if os.path.exists("data/duplicatas_manuais.json"):  # duplicatas confirmadas à mão (mesma reunião em dois vídeos)
    for k, alvo in json.load(open("data/duplicatas_manuais.json")).items():
        if k in vistos: vistos[k]["duplicata_de"] = alvo
if os.path.exists("data/datas_manuais.json"):  # datas corrigidas à mão (título errado)
    for k, dt in json.load(open("data/datas_manuais.json")).items():
        if k in vistos: vistos[k]["data"] = dt
with open("data/videos.jsonl", "w") as f:
    for v in vistos.values(): f.write(json.dumps(v, ensure_ascii=False) + "\n")
from collections import Counter
c = Counter((v["tipo"], v["duplicata_de"] is not None) for v in vistos.values())
for (tp, dup), n in sorted(c.items()): print(f"{tp:14} {'duplicata' if dup else 'único':10} {n}")
print("descartados por data:", len(descartados))
