#!/bin/bash
# Monitor semanal (Mac): descobre vídeos novos no canal, baixa as transcrições e envia ao GitHub.
# Uso manual:  bash pipeline/monitorar.sh      Agendado:  bash pipeline/instalar_agendamento_mac.sh
cd "$(dirname "$0")/.." || exit 1
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"
[ -z "$UV" ] && { echo "uv não encontrado"; exit 1; }
git pull -q --rebase --autostash origin "$(git branch --show-current)" 2>&1 | tail -1
# 1) lista vídeos do canal (reuniões novas aparecem aqui); 2) baixa o que falta
"$UV" run --python 3.12 --with "yt-dlp>=2026.1.1" --with youtube-transcript-api python pipeline/01_coletar.py @canalANTT 3 2>&1 | tail -3
"$UV" run --python 3.12 --with "yt-dlp>=2026.1.1" --with youtube-transcript-api python pipeline/02_transcrever.py --tipos todos --max 15 --pausa 45 2>&1 | tail -5
python3 pipeline/cobertura.py >/dev/null 2>&1
git add data COBERTURA.md >/dev/null 2>&1
git commit -q -m "monitor: novos vídeos/transcrições ($(date '+%d/%m/%Y'))" >/dev/null 2>&1 && git push -q 2>&1 | tail -1
echo "monitor concluído $(date)"
