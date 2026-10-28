"""Lista os vídeos de um canal do YouTube -> data/videos.jsonl. Uso: 01_coletar.py @canalANTT [anos]"""
import json, sys, subprocess, datetime
canal = sys.argv[1]; anos = int(sys.argv[2]) if len(sys.argv) > 2 else 2
desde = (datetime.date.today() - datetime.timedelta(days=365 * anos)).strftime("%Y%m%d")
out = subprocess.run(["yt-dlp", "--dateafter", desde, "--print",
    "%(.{id,title,upload_date,duration})j", f"https://www.youtube.com/{canal}/videos"],
    capture_output=True, text=True, check=True).stdout
with open("data/videos.jsonl", "w") as f:
    for l in out.splitlines():
        v = json.loads(l); v["agencia"] = canal; f.write(json.dumps(v, ensure_ascii=False) + "\n")
