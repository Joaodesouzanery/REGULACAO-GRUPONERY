#!/bin/bash
# Roda qualquer comando do pipeline para uma agência. A ANTT (piloto) usa a raiz (data/); as demais usam data/<sigla>/
# através de uma «raiz virtual» data/<sigla>/.raiz (data -> .., pipeline/agencias/docs -> raiz do repo), então
# todos os scripts (que usam caminhos relativos data/...) funcionam sem mudança.
# Uso: bash pipeline/ag.sh anm python3 pipeline/05_indexar.py
#      bash pipeline/ag.sh anm python3 pipeline/consulta.py ficha "Mauro Sousa"
set -e
SIG="$1"; shift
RAIZ_REPO="$(cd "$(dirname "$0")/.." && pwd)"
export AGENCIA="$SIG" REPO_ROOT="$RAIZ_REPO"
if [ "$SIG" = "antt" ]; then cd "$RAIZ_REPO"; exec "$@"; fi
W="$RAIZ_REPO/data/$SIG/.raiz"
mkdir -p "$RAIZ_REPO/data/$SIG"/{transcricoes,analise,analise_eventos,qualidade} "$W"
for l in "data:.." "pipeline:../../../pipeline" "agencias:../../../agencias" "docs:../../../docs" ".claude:../../../.claude"; do
  n="${l%%:*}"; t="${l#*:}"; [ -L "$W/$n" ] || ln -s "$t" "$W/$n"
done
cd "$W"; exec "$@"
