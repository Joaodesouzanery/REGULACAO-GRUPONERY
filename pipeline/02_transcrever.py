"""Baixa a legenda pt de cada vídeo de data/videos.jsonl -> data/transcricoes/{id}.json  [{t, d, x}] (retomável).
Ordem: youtube-transcript-api; fallback yt-dlp (json3). Processa por prioridade (diretoria primeiro).
Opções: --tipos diretoria,audiencia | todos   --cookies cookies.txt   --pausa 4"""
import json, os, sys, glob, subprocess, tempfile, argparse, time, random
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import IpBlocked, RequestBlocked
ap = argparse.ArgumentParser(); ap.add_argument("--cookies"); ap.add_argument("--tipos", default="diretoria")
ap.add_argument("--pausa", type=float, default=4); a = ap.parse_args()
os.makedirs("data/transcricoes", exist_ok=True)
api = YouTubeTranscriptApi()
def via_yt_dlp(vid):
    with tempfile.TemporaryDirectory() as d:
        cmd = [sys.executable, "-m", "yt_dlp", "--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "pt.*,en.*",
               "--sub-format", "json3", "-o", f"{d}/%(id)s", f"https://www.youtube.com/watch?v={vid}"]
        if a.cookies: cmd += ["--cookies", a.cookies]
        r = subprocess.run(cmd, capture_output=True, text=True)
        fs = sorted(glob.glob(f"{d}/*.json3"), key=lambda f: ".pt" not in f)  # pt primeiro
        if not fs:
            motivo = "bloqueio" if "not a bot" in r.stderr or "Sign in" in r.stderr else "sem_legenda"
            return None, motivo, ""
        ev = json.load(open(fs[0])).get("events", [])
        return [{"t": e["tStartMs"] / 1000, "d": e.get("dDurationMs", 0) / 1000,
                 "x": "".join(s.get("utf8", "") for s in e["segs"]).strip()} for e in ev if e.get("segs")], "ok", fs[0].split(".")[-2]
def baixar(vid):
    """-> (segmentos|None, motivo, idioma). motivo: ok | bloqueio | sem_legenda"""
    try:
        lista = api.list(vid)
        try: t = lista.find_transcript(["pt", "pt-BR"])
        except Exception: t = next(iter(lista))  # qualquer idioma (ex.: versão em inglês)
        return [{"t": s.start, "d": s.duration, "x": s.text} for s in t.fetch()], "ok", t.language_code
    except (IpBlocked, RequestBlocked): return via_yt_dlp(vid)
    except Exception as e:
        r = via_yt_dlp(vid)
        return r if r[0] else (None, "sem_legenda" if r[1] != "bloqueio" else "bloqueio", type(e).__name__)
vids = [json.loads(l) for l in open("data/videos.jsonl")]
vids = [v for v in vids if not v.get("duplicata_de") and v["tipo"] != "outro"
        and (a.tipos == "todos" or v["tipo"] in a.tipos.split(","))]
vids.sort(key=lambda v: v["prioridade"])
fila = [v for v in vids if not os.path.exists(f"data/transcricoes/{v['id']}.json")]
print(f"{len(vids)-len(fila)} já baixadas, {len(fila)} na fila", flush=True)
ok = falha = seguidas = 0
for i, v in enumerate(fila, 1):
    segs, motivo, info = baixar(v["id"])
    if not segs:
        falha += 1; seguidas += (motivo == "bloqueio")
        print(f"[{i}/{len(fila)}] {motivo.upper()} ({info}) {v['tipo']} {v['titulo'][:60]}", flush=True)
        open("data/sem_legenda.jsonl", "a").write(json.dumps({"id": v["id"], "motivo": motivo, "info": info}) + "\n")
        if seguidas >= 5:
            print("5 BLOQUEIOS seguidos: provável bloqueio do YouTube. Espere ~1h ou use --cookies cookies.txt e rode de novo (retoma de onde parou)."); break
        time.sleep(a.pausa * 2); continue
    seguidas = 0; ok += 1
    json.dump(segs, open(f"data/transcricoes/{v['id']}.json", "w"), ensure_ascii=False)
    print(f"[{i}/{len(fila)}] ok[{info}] {v['tipo']} {v['titulo'][:60]}", flush=True)
    time.sleep(a.pausa + random.random() * 2)
print(f"ok={ok} falha={falha}")
