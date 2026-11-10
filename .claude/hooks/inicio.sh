#!/bin/bash
# SessionStart: lembra o ponto de partida e reconstrói a base da ANTT se faltar.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -f data/regulacao.db ] || python3 pipeline/05_indexar.py >/dev/null 2>&1
echo "Projeto regulação: leia docs/CONTINUAR.md e COBERTURA.md. Perguntas sobre diretor → skill resposta-com-evidencia; lote do Mac → skill lote-mac; relatório → relatorio-cliente + relatorio-visual; antes de commit → cuidados-pipeline; TODA resposta → cobertura-em-toda-resposta."
