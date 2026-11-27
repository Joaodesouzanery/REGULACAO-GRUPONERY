#!/bin/bash
# Monitor (Mac, seg e qui 09:00 pelo agendamento): coleta rápida de TODAS as agências da fila + pautas/calendários/consultas (bruto) e envia ao GitHub.
# Uso manual:  bash pipeline/monitorar.sh      Agendar:  bash pipeline/instalar_agendamento_mac.sh
cd "$(dirname "$0")/.." || exit 1
git pull -q --rebase --autostash origin "$(git branch --show-current)" 2>&1 | tail -1
python3 pipeline/pautas_mac.py 2>&1 | tail -4
git add data >/dev/null 2>&1; git commit -q -m "monitor: pautas e consultas (bruto) $(date '+%d/%m/%Y')" >/dev/null 2>&1 && git push -q 2>&1 | tail -1
bash pipeline/coletar_todas.sh 2>&1 | tail -20
echo "monitor concluído $(date)"
