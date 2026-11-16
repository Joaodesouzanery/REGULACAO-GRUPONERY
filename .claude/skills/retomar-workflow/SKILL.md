---
name: retomar-workflow
description: Registra e retoma lotes longos de análise (workflows de analistas, ex.: ANEEL) sem refazer o que já terminou — runId, lista de reuniões e script ficam em docs/lotes.md. Use quando o usuário pedir pausa, quando o limite estiver perto, ou para continuar um lote parado.
---
# Retomar workflow
1. Ao lançar um lote: anote em `docs/lotes.md` data, agência, nº de reuniões, `runId`, caminho do script e arquivo com a lista (`scratchpad` não serve: copie a lista para `docs/lotes/<runId>.json`).
2. Pausa: pare o workflow (TaskStop) e faça commit dos `.analise.json` já gravados.
3. Retomar: `Workflow({scriptPath, resumeFromRunId, args: <mesma lista>})` — o que terminou volta do cache. Se a sessão mudou (cache perdido), recalcule a fila (skill analise-lote): só entram `.md` sem `.analise.json`.
4. Lotes de 50 em dias de limite curto; 150 normais. Indexe e faça commit entre lotes.
