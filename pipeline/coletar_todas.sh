#!/bin/bash
# COMANDO ÚNICO DO MAC: coleta ANTT, ANM e ANTAQ em sequência (só baixa o que falta) e mede o tempo de cada uma.
# Uso: cd ~/REGULACAO-GRUPONERY && git pull && caffeinate -i bash pipeline/coletar_todas.sh [--total] [--simular]
#   modo rápido (padrão): lista só os vídeos recentes de cada canal; --total (ou dia 1): relista o canal inteiro.
#   Tempos ficam em data/tempos_coleta.jsonl (o chat usa para estimar o fluxo).
cd "$(dirname "$0")/.." || exit 1
EXTRA=""; SIM=0; for x in "$@"; do [ "$x" = "--total" ] && EXTRA="--total"; [ "$x" = "--simular" ] && SIM=1; done
canal() { python3 -c "import json;d=json.load(open('data/$1/config_agencia.json'));print(d.get('canal') or (d.get('playlists') or [''])[0])"; }
FILA=("antt @canalANTT" "anm $(canal anm)" "antaq $(canal antaq)")
INI=$(date +%s); RES=""
for item in "${FILA[@]}"; do
  set -- $item; t=$(date +%s)
  echo; echo "########## $1 ($2) ##########"
  if [ $SIM = 1 ]; then echo "(simulação) bash pipeline/coletar_tudo_e_enviar.sh $1 $2 $EXTRA"; else bash pipeline/coletar_tudo_e_enviar.sh "$1" "$2" $EXTRA; fi
  RES="$RES $(echo $1 | tr a-z A-Z) $((($(date +%s)-t)/60)) min ·"
done
echo; echo "TEMPOS:$RES total $((($(date +%s)-INI)/60)) min"
echo "Avise o Claude: «rodei a coleta das 3 agências»."
