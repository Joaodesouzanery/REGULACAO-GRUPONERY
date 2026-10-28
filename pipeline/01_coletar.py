"""Lista reuniões de diretoria de um canal (abas /videos e /streams) -> data/videos.jsonl.
Uso: 01_coletar.py @canalANTT [anos]. A data vem do título (a listagem 'flat' não traz upload_date)."""
import json, re, sys, subprocess, datetime
canal = sys.argv[1]; anos = int(sys.argv[2]) if len(sys.argv) > 2 else 2
corte = datetime.date.today() - datetime.timedelta(days=365 * anos)
RD = re.compile(r"reuni[ãa]o.*diretoria|board meeting", re.I)
DATA = re.compile(r"(\d{1,2})/(\d{1,2})/(\d{2,4})")
vistos = {}
for aba in ("videos", "streams"):
    out = subprocess.run(["yt-dlp", "--flat-playlist", "--print", "%(id)s|%(title)s|%(duration)s",
        f"https://www.youtube.com/{canal}/{aba}"], capture_output=True, text=True).stdout
    for l in out.splitlines():
        id_, titulo, dur = l.split("|")[0], "|".join(l.split("|")[1:-1]), l.split("|")[-1]
        if not RD.search(titulo) or id_ in vistos: continue
        m = DATA.search(titulo); data = None
        if m:
            a, b, y = int(m[1]), int(m[2]), int(m[3]); y += 2000 if y < 100 else 0
            if "board meeting" in titulo.lower(): a, b = b, a  # versões em inglês usam mm/dd/aaaa
            try: data = datetime.date(y, b, a)
            except ValueError: pass
        if data and data < corte: continue
        vistos[id_] = {"id": id_, "titulo": titulo, "data": str(data) if data else None,
                       "duracao": None if dur == "NA" else int(float(dur)), "agencia": canal}
with open("data/videos.jsonl", "w") as f:
    for v in vistos.values(): f.write(json.dumps(v, ensure_ascii=False) + "\n")
print(len(vistos), "reuniões")
