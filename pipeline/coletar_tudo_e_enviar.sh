#!/bin/bash
# COLETA TOTAL (rodar no Mac): inventaria TODO o canal (sem corte de ano; videos, streams, shorts e playlists),
# baixa todas as transcrições que faltam e envia tudo ao GitHub a cada lote. Pode ser interrompido e rodado de novo.
# Uso: cd ~/REGULACAO-GRUPONERY && git pull && caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh
cd "$(dirname "$0")/.." || exit 1
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"
[ -z "$UV" ] && { echo "uv não encontrado. Rode: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
RUN() { "$UV" run --python 3.12 --with "yt-dlp>=2026.1.1" --with youtube-transcript-api python "$@"; }
BR="$(git branch --show-current)"
enviar() { git add data COBERTURA.md sem_transcricao.md >/dev/null 2>&1
  git commit -q -m "$1" >/dev/null 2>&1 && { git pull -q --rebase --autostash origin "$BR" >/dev/null 2>&1; git push -q origin "$BR" 2>&1 | tail -1; echo "  -> enviado ao GitHub"; }; }
ESPERA=${ESPERA:-10800}
echo "=== 1/3 Inventário total do canal (pode levar alguns minutos) ==="
RUN pipeline/01_coletar.py @canalANTT 0 | tail -12
python3 pipeline/cobertura.py >/dev/null 2>&1; enviar "inventario total do canal (todos os anos, abas e playlists)"
echo "=== 2/3 Transcrições (todas as faltantes, em lotes) ==="
for ciclo in $(seq 1 80); do
  echo "--- lote $ciclo $(date '+%d/%m %H:%M') ---"
  RUN pipeline/02_transcrever.py --tipos todos --max 12 --pausa 45 | tail -16; rc=${PIPESTATUS[0]}
  python3 pipeline/cobertura.py >/dev/null 2>&1; enviar "transcricoes (lote $ciclo)"
  [ $rc -eq 0 ] && break
  if [ $rc -eq 3 ]; then echo "YouTube limitou (429). Dormindo $((ESPERA/3600))h (deixe o Mac ligado)..."; sleep "$ESPERA"; elif [ $rc -eq 2 ]; then sleep 60; else sleep 600; fi
done
echo "=== 3/3 Resumo ==="
python3 pipeline/cobertura.py | tail -1; head -6 sem_transcricao.md
echo "FIM. Avise o Claude: ele organiza as pastas, analisa e atualiza o GitHub."
