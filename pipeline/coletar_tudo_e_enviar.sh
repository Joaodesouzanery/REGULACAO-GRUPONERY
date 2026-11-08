#!/bin/bash
# COLETA TOTAL (rodar no Mac): inventaria TODO o canal (sem corte de ano; videos, streams, shorts e playlists),
# baixa todas as transcrições que faltam e envia tudo ao GitHub a cada lote. Pode ser interrompido e rodado de novo.
# Uso: cd ~/REGULACAO-GRUPONERY && git pull && caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh [sigla] [canal|playlist]
#   ANTT (padrão): bash pipeline/coletar_tudo_e_enviar.sh
#   ANM:           bash pipeline/coletar_tudo_e_enviar.sh anm PLoP8nQ7f1EABonZ_nYkKU9xsGx6L6PjY8
cd "$(dirname "$0")/.." || exit 1
if [ -n "$(git -C "$(cd "$(dirname "$0")/.." && pwd)" diff --name-only --diff-filter=U)" ] || [ -d "$(cd "$(dirname "$0")/.." && pwd)/.git/rebase-merge" ] || [ -f "$(cd "$(dirname "$0")/.." && pwd)/.git/MERGE_HEAD" ]; then
  echo "PARE: o git está com merge/rebase pela metade. Rode:"; echo "  git rebase --abort; git merge --abort; git fetch origin; git merge -X theirs origin/claude/antt-directors-speeches-analysis-93r9hi -m sincroniza; git push"; exit 1; fi

REPO="$(pwd)"; SIG="${1:-antt}"; CANAL="${2:-@canalANTT}"
if [ "$SIG" != "antt" ]; then bash pipeline/ag.sh "$SIG" true; cd "data/$SIG/.raiz" || exit 1; ALVO="data/$SIG"; else ALVO="data"; fi
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"
[ -z "$UV" ] && { echo "uv não encontrado. Rode: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
RUN() { "$UV" run --python 3.12 --with "yt-dlp>=2026.1.1" --with youtube-transcript-api python "$@"; }
BR="$(git branch --show-current)"; [ -z "$BR" ] && { echo "PARE: branch indefinido (merge pendente?)."; exit 1; }
enviar() { git -C "$REPO" add "$ALVO" COBERTURA.md sem_transcricao.md >/dev/null 2>&1
  git -C "$REPO" commit -q -m "[$SIG] $1" >/dev/null 2>&1 && { git -C "$REPO" pull -q --no-rebase -X theirs --no-edit origin "$BR" >/dev/null 2>&1; git -C "$REPO" push -q origin "$BR" && echo "  -> enviado ao GitHub" || echo "  !! PUSH FALHOU (rode git status)"; }; }
ESPERA=${ESPERA:-10800}
echo "=== 1/3 Inventário total do canal (pode levar alguns minutos) ==="
RUN pipeline/01_coletar.py "$CANAL" 0 | tail -12
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
