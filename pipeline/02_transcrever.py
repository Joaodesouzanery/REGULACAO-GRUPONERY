"""Baixa a legenda pt de cada vídeo de data/videos.jsonl -> data/transcricoes/{id}.json  [{t, d, x}] (retomável).
Ordem: youtube-transcript-api; fallback yt-dlp (json3). Processa por prioridade (diretoria primeiro).
Opções: --tipos diretoria,audiencia | todos   --cookies cookies.txt   --pausa 4"""
import json, os, sys, glob, subprocess, tempfile, argparse, time, random
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import IpBlocked, RequestBlocked
ap = argparse.ArgumentParser(); ap.add_argument("--cookies"); ap.add_argument("--browser", help="chrome|safari|firefox|edge: usa os cookies do navegador (só yt-dlp)"); ap.add_argument("--tipos", default="diretoria")
ap.add_argument("--pausa", type=float, default=25); ap.add_argument("--max", type=int, default=0, help="máx. de vídeos por rodada (0 = sem limite)"); a = ap.parse_args()
os.makedirs("data/transcricoes", exist_ok=True)
api = YouTubeTranscriptApi()
def via_yt_dlp(vid):
    with tempfile.TemporaryDirectory() as d:
        cmd = [sys.executable, "-m", "yt_dlp", "--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "pt.*,en.*",
               "--sub-format", "json3", "--sleep-requests", "2", "--sleep-subtitles", "5", "-o", f"{d}/%(id)s", f"https://www.youtube.com/watch?v={vid}"]
        if a.cookies: cmd += ["--cookies", a.cookies]
        if a.browser: cmd += ["--cookies-from-browser", a.browser]
        r = subprocess.run(cmd, capture_output=True, text=True)
        fs = sorted(glob.glob(f"{d}/*.json3"), key=lambda f: ".pt" not in f)  # pt primeiro
        if not fs:
            err = (r.stderr.strip().splitlines() or [""])[-1][:140]
            motivo = "sem_legenda" if "no subtitles" in r.stderr.lower() and "bot" not in r.stderr else "bloqueio"
            if "429" in r.stderr: motivo = "limite429"
            elif motivo == "bloqueio" and "bot" not in r.stderr and "Sign in" not in r.stderr: motivo = "erro_yt"
            return None, motivo, err
        ev = json.load(open(fs[0])).get("events", [])
        return [{"t": e["tStartMs"] / 1000, "d": e.get("dDurationMs", 0) / 1000,
                 "x": "".join(s.get("utf8", "") for s in e["segs"]).strip()} for e in ev if e.get("segs")], "ok", fs[0].split(".")[-2]
def baixar(vid):
    """-> (segmentos|None, motivo, idioma). motivo: ok | bloqueio | sem_legenda"""
    if a.browser: return via_yt_dlp(vid)
    try:
        lista = api.list(vid)
        try: t = lista.find_transcript(["pt", "pt-BR"])
        except Exception: t = next(iter(lista))  # qualquer idioma (ex.: versão em inglês)
        return [{"t": s.start, "d": s.duration, "x": s.text} for s in t.fetch()], "ok", t.language_code
    except (IpBlocked, RequestBlocked) as e:
        r = via_yt_dlp(vid)
        return r if r[0] else (None, r[1] if r[1] != "erro_yt" else "bloqueio", f"api:{type(e).__name__} | yt-dlp:{r[2]}")
    except Exception as e:
        r = via_yt_dlp(vid)
        if r[0]: return r
        real = type(e).__name__ in ("TranscriptsDisabled", "NoTranscriptFound", "VideoUnavailable")
        return None, "sem_legenda" if real else "bloqueio", f"{type(e).__name__} | {r[2]}"
vids = [json.loads(l) for l in open("data/videos.jsonl")]
vids = [v for v in vids if not v.get("duplicata_de") and v["tipo"] != "outro"
        and (a.tipos == "todos" or v["tipo"] in a.tipos.split(","))]
vids.sort(key=lambda v: (v["prioridade"], -int((v["data"] or "0000-00-00").replace("-", ""))))
fila = [v for v in vids if not os.path.exists(f"data/transcricoes/{v['id']}.json")]
print(f"{len(vids)-len(fila)} já baixadas, {len(fila)} na fila", flush=True)
ok = falha = seguidas = 0
for i, v in enumerate(fila, 1):
    if a.max and ok >= a.max: print(f"Limite da rodada ({a.max}) atingido. Rode de novo mais tarde."); break
    segs, motivo, info = baixar(v["id"])
    if not segs:
        falha += 1; seguidas += (motivo in ("bloqueio", "limite429"))
        if motivo == "limite429": print("HTTP 429: o YouTube limitou seu IP. Pare e tente de novo em 2-4 horas (sem cookies; --pausa 40)."); break
        print(f"[{i}/{len(fila)}] {motivo.upper()} ({info}) {v['tipo']} {v['titulo'][:60]}", flush=True)
        open("data/sem_legenda.jsonl", "a").write(json.dumps({"id": v["id"], "motivo": motivo, "info": info}) + "\n")
        if motivo == "erro_yt": seguidas = 0
        if seguidas >= 5:
            print("5 BLOQUEIOS seguidos: provável bloqueio do YouTube. Espere ~1h ou use --pausa 40 e rode de novo (retoma de onde parou)."); break
        time.sleep(a.pausa * 2); continue
    seguidas = 0; ok += 1
    json.dump(segs, open(f"data/transcricoes/{v['id']}.json", "w"), ensure_ascii=False)
    print(f"[{i}/{len(fila)}] ok[{info}] {v['tipo']} {v['titulo'][:60]}", flush=True)
    time.sleep(a.pausa + random.random() * 2)
print(f"ok={ok} falha={falha}")
