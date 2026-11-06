#!/bin/bash
# TRANSCRIÇÃO POR ÁUDIO (Whisper) das reuniões SEM legenda utilizável — rodar NO MAC (o YouTube bloqueia download na nuvem).
# Só rode com aprovação do responsável. Baixa apenas o áudio, transcreve localmente (faster-whisper, pt) e envia ao GitHub.
# Uso: cd ~/REGULACAO-GRUPONERY && git pull && caffeinate -i bash pipeline/whisper_mac.sh [ids...]
# Sem ids: as 4 reuniões de diretoria sem texto (RD 904, RD 931, 81ª Extraordinária, RD 1042).
# Modelo: WHISPER_MODELO=small (padrão; ~1x tempo real num Mac M1) ou medium (melhor, mais lento).
cd "$(dirname "$0")/.." || exit 1
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"
[ -z "$UV" ] && { echo "uv não encontrado. Rode: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
IDS=("$@"); [ ${#IDS[@]} -eq 0 ] && IDS=(tE0KRoC9JhA 5Ekrdu6K-4Y U3h5SQcZJYE 6A8-zT0Sipw)
command -v ffmpeg >/dev/null || { echo "ffmpeg não encontrado. Rode: brew install ffmpeg"; exit 1; }
MOD="${WHISPER_MODELO:-small}"; TMP="$(mktemp -d)"; BR="$(git branch --show-current)"
for id in "${IDS[@]}"; do
  echo "=== $id: baixando áudio ==="
  "$UV" run --python 3.12 --with "yt-dlp>=2026.1.1" yt-dlp -f bestaudio -x --audio-format m4a -o "$TMP/$id.%(ext)s" "https://www.youtube.com/watch?v=$id" || { echo "falhou o download de $id"; continue; }
  echo "=== $id: transcrevendo (modelo $MOD) ==="
  "$UV" run --python 3.12 --with faster-whisper python - "$TMP/$id.m4a" "data/transcricoes/$id.json" "$MOD" <<'PY'
import sys, json, datetime
from faster_whisper import WhisperModel
audio, out, mod = sys.argv[1:4]
segs, info = WhisperModel(mod, device="auto", compute_type="int8").transcribe(audio, language="pt", vad_filter=True)
res = [{"t": round(s.start, 2), "d": round(s.end - s.start, 2), "x": s.text.strip()} for s in segs]
json.dump(res, open(out, "w"), ensure_ascii=False)
open("data/transcricoes_whisper.jsonl", "a").write(json.dumps({"video_id": out.split("/")[-1][:-5], "modelo": mod, "segmentos": len(res), "data": datetime.date.today().isoformat(), "fonte": "Whisper (áudio), não legenda do YouTube"}) + "\n")
print(len(res), "segmentos ->", out)
PY
  git add data/transcricoes/$id.json data/transcricoes_whisper.jsonl && git commit -q -m "Whisper: transcricao de $id" && { git pull -q --rebase --autostash origin "$BR"; git push -q origin "$BR"; echo "  -> enviado"; }
done
rm -rf "$TMP"; echo "Pronto. No chat: «analise as reuniões transcritas por Whisper»."
