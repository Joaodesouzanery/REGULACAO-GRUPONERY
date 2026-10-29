"""Lista os vídeos de um canal (abas /videos e /streams) -> data/videos.jsonl, com `tipo` e `prioridade`.
Uso: 01_coletar.py @canalANTT [anos]. Data vem do título (listagem 'flat' não traz upload_date).
Itens sem data no título são mantidos (data=null). Tudo o que não casa nenhum tipo vai como 'outro'."""
import json, re, sys, subprocess, datetime, unicodedata
canal = sys.argv[1]; anos = int(sys.argv[2]) if len(sys.argv) > 2 else 2
corte = datetime.date.today() - datetime.timedelta(days=365 * anos)
TIPOS = [  # (tipo, prioridade, regex) — primeira que casar vence
    ("diretoria", 1, r"reuni[ãa]o.*diretoria|board meeting|extraordinary board"),
    ("audiencia", 2, r"audi[êe]ncias? p[úu]blicas?|public hearing|consulta p[úu]blica"),
    ("participativa", 3, r"reuni[ãa]o participativa|participatory meeting"),
    ("romeiros", 3, r"romeiros"),
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
for aba in ("videos", "streams"):
    out = subprocess.run(["yt-dlp", "--flat-playlist", "--print", "%(id)s\t%(title)s\t%(duration)s",
        f"https://www.youtube.com/{canal}/{aba}"], capture_output=True, text=True).stdout
    for l in out.splitlines():
        id_, titulo, dur = l.split("\t"); titulo = unicodedata.normalize("NFC", titulo)
        if id_ in vistos: continue
        tp, pr = tipo(titulo); d = data(titulo)
        if d and d < corte: descartados.append((titulo, "antigo")); continue
        vistos[id_] = {"id": id_, "titulo": titulo, "tipo": tp, "prioridade": pr, "data": str(d) if d else None,
                       "duracao": None if dur == "NA" else int(float(dur)), "agencia": canal,
                       "duplicata_de": None}
# dedupe PT/EN: mesma reunião de diretoria (mesmo número) -> mantém a versão em português
por_num = {}
for v in vistos.values():
    if v["tipo"] == "diretoria" and (n := numero(v["titulo"])):
        extra = bool(re.search(r"extra", v["titulo"], re.I))
        por_num.setdefault((n, extra), []).append(v)
for grupo in por_num.values():
    grupo.sort(key=lambda v: bool(re.search(r"board|extraordinary", v["titulo"], re.I)))  # PT primeiro
    for v in grupo[1:]: v["duplicata_de"] = grupo[0]["id"]
with open("data/videos.jsonl", "w") as f:
    for v in vistos.values(): f.write(json.dumps(v, ensure_ascii=False) + "\n")
from collections import Counter
c = Counter((v["tipo"], v["duplicata_de"] is not None) for v in vistos.values())
for (tp, dup), n in sorted(c.items()): print(f"{tp:14} {'duplicata' if dup else 'único':10} {n}")
print("descartados por data:", len(descartados))
