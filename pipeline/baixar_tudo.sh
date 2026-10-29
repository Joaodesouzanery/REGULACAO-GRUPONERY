#!/bin/bash
# Baixa TODAS as transcrições pendentes, sozinho: roda em lotes, envia ao GitHub a cada lote
# e dorme quando o YouTube limita (429). Uso: caffeinate -i bash pipeline/baixar_tudo.sh
cd "$(dirname "$0")/.." || exit 1
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"
[ -z "$UV" ] && { echo "uv não encontrado. Rode: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
ESPERA=${ESPERA:-10800}   # 3h após um 429
for ciclo in $(seq 1 40); do
  echo "=== ciclo $ciclo $(date '+%d/%m %H:%M') ==="
  "$UV" run --python 3.12 --with "yt-dlp>=2026.1.1" --with youtube-transcript-api \
    python pipeline/02_transcrever.py --tipos todos --max 12 --pausa 45
  rc=$?
  git add data >/dev/null 2>&1
  git commit -q -m "transcricoes ANTT (ciclo $ciclo)" >/dev/null 2>&1 && \
    { git pull -q --rebase --autostash origin "$(git branch --show-current)" >/dev/null 2>&1; git push -q 2>&1 | tail -1; echo "enviado ao GitHub"; }
  [ $rc -eq 0 ] && { echo "TUDO BAIXADO (ou nada a fazer). Fim."; exit 0; }
  if [ $rc -eq 3 ]; then echo "YouTube limitou (429). Dormindo $((ESPERA/3600))h..."; sleep "$ESPERA"; else sleep 600; fi
done
echo "Limite de ciclos atingido; rode de novo para continuar."
