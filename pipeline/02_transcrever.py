"""Baixa legenda pt de cada vídeo de data/videos.jsonl -> data/transcricoes/{id}.json (retomável)."""
import json, os
from youtube_transcript_api import YouTubeTranscriptApi
os.makedirs("data/transcricoes", exist_ok=True)
api = YouTubeTranscriptApi()
for l in open("data/videos.jsonl"):
    v = json.loads(l); p = f"data/transcricoes/{v['id']}.json"
    if os.path.exists(p): continue
    try:
        segs = [{"t": s.start, "d": s.duration, "x": s.text} for s in api.fetch(v["id"], languages=["pt"])]
    except Exception as e:
        print("sem legenda", v["id"], type(e).__name__); continue
    json.dump(segs, open(p, "w"), ensure_ascii=False)
