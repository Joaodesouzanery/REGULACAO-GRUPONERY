#!/bin/bash
# TRANSCRIÇÃO POR ÁUDIO (Whisper) das reuniões SEM legenda utilizável — rodar NO MAC (o YouTube bloqueia download na nuvem).
# Só rode com aprovação do responsável. Baixa apenas o áudio, transcreve localmente (faster-whisper, pt) e envia ao GitHub.
# Uso: cd ~/REGULACAO-GRUPONERY && git pull && caffeinate -i bash pipeline/whisper_mac.sh [ids...]
# Sem ids: as 4 reuniões de diretoria sem texto (RD 904, RD 931, 81ª Extraordinária, RD 1042).
# Modelo: WHISPER_MODELO=small (padrão; ~1x tempo real num Mac M1) ou medium (melhor, mais lento).
cd "$(dirname "$0")/.." || exit 1
if [ -n "$(git -C "$(cd "$(dirname "$0")/.." && pwd)" diff --name-only --diff-filter=U)" ] || [ -d "$(cd "$(dirname "$0")/.." && pwd)/.git/rebase-merge" ] || [ -f "$(cd "$(dirname "$0")/.." && pwd)/.git/MERGE_HEAD" ]; then
  echo "PARE: o git está com merge/rebase pela metade. Rode:"; echo "  git rebase --abort; git merge --abort; git fetch origin; git merge -X theirs origin/claude/antt-directors-speeches-analysis-93r9hi -m sincroniza; git push"; exit 1; fi

REPO="$(pwd)"; SIG=antt; ALVO=data
if [ "$1" = "--agencia" ]; then SIG="$2"; shift 2; fi
if [ "$SIG" != "antt" ]; then bash pipeline/ag.sh "$SIG" true; cd "data/$SIG/.raiz" || exit 1; ALVO="data/$SIG"; fi
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"
[ -z "$UV" ] && { echo "uv não encontrado. Rode: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
IDS=("$@"); [ ${#IDS[@]} -eq 0 ] && [ "$SIG" != "antt" ] && IDS=($(python3 -c "import json,os;print(' '.join(json.loads(l)['id'] for l in open('data/sem_legenda.jsonl')))" 2>/dev/null)); [ ${#IDS[@]} -eq 0 ] && IDS=(tE0KRoC9JhA 5Ekrdu6K-4Y U3h5SQcZJYE 6A8-zT0Sipw)
command -v ffmpeg >/dev/null || { echo "ffmpeg não encontrado. Rode: brew install ffmpeg"; exit 1; }
MOD="${WHISPER_MODELO:-small}"; TMP="$(mktemp -d)"; BR="$(git -C "$REPO" branch --show-current)"
echo "Branch: $BR (deve ser claude/antt-directors-speeches-analysis-93r9hi)"
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
  git -C "$REPO" add "$ALVO/transcricoes/$id.json" "$ALVO/transcricoes_whisper.jsonl" && git -C "$REPO" commit -q -m "[$SIG] Whisper: transcricao de $id" && { git -C "$REPO" pull -q --no-rebase -X theirs --no-edit origin "$BR"; git -C "$REPO" push origin "$BR" && echo "  -> enviado ao GitHub" || echo "  !! PUSH FALHOU: rode git push depois"; }
done
rm -rf "$TMP"; echo "Pronto. No chat: «analise as reuniões transcritas por Whisper»."
