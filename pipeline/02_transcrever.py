"""Baixa a legenda pt de cada vídeo de data/videos.jsonl -> data/transcricoes/{id}.json  [{t, d, x}] (retomável).
Ordem: youtube-transcript-api; fallback yt-dlp (json3). Opções: --cookies cookies.txt  --tipos diretoria,audiencia"""
import json, os, sys, glob, subprocess, tempfile, argparse
from youtube_transcript_api import YouTubeTranscriptApi
ap = argparse.ArgumentParser(); ap.add_argument("--cookies"); ap.add_argument("--tipos", default="diretoria")
a = ap.parse_args(); tipos = set(a.tipos.split(","))
os.makedirs("data/transcricoes", exist_ok=True)
api = YouTubeTranscriptApi()
def via_yt_dlp(vid):
    with tempfile.TemporaryDirectory() as d:
        cmd = [sys.executable, "-m", "yt_dlp", "--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "pt.*",
               "--sub-format", "json3", "-o", f"{d}/%(id)s", f"https://www.youtube.com/watch?v={vid}"]
        if a.cookies: cmd += ["--cookies", a.cookies]
        subprocess.run(cmd, capture_output=True)
        fs = glob.glob(f"{d}/*.json3")
        if not fs: return None
        ev = json.load(open(fs[0])).get("events", [])
        return [{"t": e["tStartMs"] / 1000, "d": e.get("dDurationMs", 0) / 1000,
                 "x": "".join(s.get("utf8", "") for s in e["segs"]).strip()} for e in ev if e.get("segs")]
ok = falha = 0
for l in open("data/videos.jsonl"):
    v = json.loads(l)
    if v["tipo"] not in tipos or v.get("duplicata_de"): continue
    p = f"data/transcricoes/{v['id']}.json"
    if os.path.exists(p): continue
    try: segs = [{"t": s.start, "d": s.duration, "x": s.text} for s in api.fetch(v["id"], languages=["pt"])]
    except Exception: segs = via_yt_dlp(v["id"])
    if not segs: print("sem legenda", v["id"], v["titulo"]); falha += 1; continue
    json.dump(segs, open(p, "w"), ensure_ascii=False); ok += 1
print(f"ok={ok} falha={falha}")
